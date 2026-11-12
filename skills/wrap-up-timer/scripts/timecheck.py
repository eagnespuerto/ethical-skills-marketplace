#!/usr/bin/env python3
"""Tiny wall-clock tracker for coding-session wrap-up nudges.
State lives in ~/.wrap-up-timer/state.json so it persists across turns."""
import json, sys, os, time
from datetime import datetime

DIR = os.path.expanduser("~/.wrap-up-timer")
PATH = os.path.join(DIR, "state.json")

def today():
    return datetime.now().strftime("%Y-%m-%d")

def load():
    try:
        with open(PATH) as f:
            return json.load(f)
    except Exception:
        return {}

def save(s):
    os.makedirs(DIR, exist_ok=True)
    with open(PATH, "w") as f:
        json.dump(s, f)

def fresh_day(s):
    if s.get("day") != today():
        return {"day": today(), "limit": s.get("limit", 50), "cap": s.get("cap", 90),
                "used_today": 0, "start": None, "acked": []}
    return s

def cmd_start(args):
    s = fresh_day(load())
    for i, a in enumerate(args):
        if a == "--limit" and i + 1 < len(args): s["limit"] = int(args[i+1])
        if a == "--cap" and i + 1 < len(args): s["cap"] = int(args[i+1])
    s["start"] = time.time()
    s["acked"] = []
    save(s)
    print(f"Tracking started. Soft limit {s['limit']} min, daily cap {s['cap']} min. "
          f"{s.get('used_today',0)} min already logged today.")

def elapsed_session(s):
    return 0 if not s.get("start") else int((time.time() - s["start"]) / 60)

def cmd_check(_):
    """Prints a JSON line for Claude to read each turn."""
    s = fresh_day(load())
    sess = elapsed_session(s)
    total = s.get("used_today", 0) + sess
    limit, cap = s.get("limit", 50), s.get("cap", 90)
    acked = s.get("acked", [])
    nudge = None
    if s.get("start"):
        if total >= cap and "cap" not in acked:
            nudge = "cap"
        elif sess >= limit and "limit" not in acked:
            nudge = "limit"
    print(json.dumps({
        "active": bool(s.get("start")),
        "session_min": sess, "today_min": total,
        "limit": limit, "cap": cap, "nudge": nudge
    }))

def cmd_ack(args):
    s = fresh_day(load())
    which = args[0] if args else None
    if which in ("limit", "cap"):
        s.setdefault("acked", []).append(which)
        save(s)
    print("ok")

def cmd_stop(_):
    s = fresh_day(load())
    s["used_today"] = s.get("used_today", 0) + elapsed_session(s)
    s["start"] = None
    s["acked"] = []
    save(s)
    print(f"Session paused. {s['used_today']} min logged today.")

def cmd_status(_):
    s = fresh_day(load())
    sess = elapsed_session(s)
    print(f"Active: {bool(s.get('start'))} | this session: {sess} min | "
          f"today: {s.get('used_today',0)+sess} min | limit {s.get('limit',50)} | cap {s.get('cap',90)}")

def cmd_reset(_):
    save({"day": today(), "limit": 50, "cap": 90, "used_today": 0, "start": None, "acked": []})
    print("Reset for today.")

CMDS = {"start": cmd_start, "check": cmd_check, "ack": cmd_ack,
        "stop": cmd_stop, "status": cmd_status, "reset": cmd_reset}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print("usage: timecheck.py {start|check|ack|stop|status|reset} [args]")
        sys.exit(1)
    CMDS[sys.argv[1]](sys.argv[2:])
