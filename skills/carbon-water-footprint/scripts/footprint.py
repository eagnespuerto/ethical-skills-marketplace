#!/usr/bin/env python3
"""Estimate the carbon and water footprint of a Claude Code session.

Token counts are read from the session transcript (measured). Energy, CO2e and
water are ESTIMATES from the public factors below. Standard library only.

  footprint.py check        one JSON line for the current session
  footprint.py statusline   one short marker line; reads Claude Code's status JSON on stdin
  footprint.py ack          remember the levels just shown, so the alert does not repeat

Options: --transcript PATH, or --session ID. With neither, the newest transcript
for the current folder is used.
"""
import json
import os
import re
import sys
from pathlib import Path

# --- Factors. Every one can be changed with an environment variable. ----------
# Energy per 1000 tokens, in Wh. Anthropic publishes no figure. The output value
# is an order of magnitude taken from Google's measured 0.24 Wh median Gemini text
# prompt (arXiv:2508.15734). Input and cache-read values are assumptions that
# follow the usual API price ratios (5:1 and 50:1), as a stand-in for compute.
WH_PER_KTOK = {
    "output": float(os.environ.get("FOOTPRINT_WH_OUT", 0.5)),
    "input": float(os.environ.get("FOOTPRINT_WH_IN", 0.1)),
    "cache_read": float(os.environ.get("FOOTPRINT_WH_CACHE", 0.01)),
}
# World average grid, 2024: 473 gCO2/kWh (Ember, Global Electricity Review 2025).
GRID_G_PER_KWH = float(os.environ.get("FOOTPRINT_GRID_G_PER_KWH", 473))
# US average: 0.55 L/kWh on-site cooling + 3.14 L/kWh for generating the
# electricity (Li et al., "Making AI Less Thirsty", arXiv:2304.03271).
WATER_L_PER_KWH = float(os.environ.get("FOOTPRINT_WATER_L_PER_KWH", 0.55 + 3.14))

# Where the marker turns yellow, then red. The red marks sit just under a real
# day-long research session (197 requests, 46 million cache-read tokens), which
# came to about 293 g CO2e and 2.3 L. Yellow for water is a 500 mL bottle.
THRESHOLDS = {
    "carbon": (50, 250),    # grams of CO2e
    "water": (500, 2000),   # millilitres
}

DONATE_URL = "https://www.greenpeace.org/international/act/donate/"
STATE = Path.home() / ".carbon-water-footprint" / "state.json"
DOTS = {1: "\U0001F7E2", 2: "\U0001F7E1", 3: "\U0001F534"}  # green, yellow, red
DROP = "\U0001F4A7"


def level(value: float, kind: str) -> int:
    """Return the alert level for a session total: 1 (low), 2 (medium) or 3 (high).

    `kind` is "carbon" (value in grams of CO2e) or "water" (value in millilitres).
    Level 1 shows as green / one drop, 2 as yellow / two drops, 3 as red / three drops.
    """
    yellow_at, red_at = THRESHOLDS[kind]
    return 3 if value >= red_at else 2 if value >= yellow_at else 1


def find_transcript(args: list[str], stdin_json: dict) -> Path | None:
    if "--transcript" in args:
        return Path(args[args.index("--transcript") + 1])
    if stdin_json.get("transcript_path"):
        return Path(stdin_json["transcript_path"])
    projects = Path.home() / ".claude" / "projects"
    if "--session" in args:
        hits = list(projects.glob(f"*/{args[args.index('--session') + 1]}.jsonl"))
        return hits[0] if hits else None
    # Claude Code names the project folder after the working directory.
    here = projects / re.sub(r"[^A-Za-z0-9]", "-", os.getcwd())
    files = list(here.glob("*.jsonl")) or list(projects.glob("*/*.jsonl"))
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def read_tokens(transcript: Path) -> dict:
    """Sum token usage over the assistant messages in a transcript."""
    usage_by_id = {}
    with open(transcript, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                msg = json.loads(line).get("message") or {}
            except (ValueError, AttributeError):
                continue
            # One message is logged once per content block, with the same usage
            # each time. Keying on the id keeps it from being counted twice.
            if isinstance(msg, dict) and msg.get("usage") and msg.get("id"):
                usage_by_id[msg["id"]] = msg["usage"]
    total = {"output": 0, "input": 0, "cache_read": 0}
    for u in usage_by_id.values():
        total["output"] += u.get("output_tokens") or 0
        total["input"] += (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
        total["cache_read"] += u.get("cache_read_input_tokens") or 0
    total["requests"] = len(usage_by_id)
    return total


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def report(transcript: Path) -> dict:
    tokens = read_tokens(transcript)
    wh = sum(tokens[k] / 1000 * WH_PER_KTOK[k] for k in WH_PER_KTOK)
    co2_g = wh / 1000 * GRID_G_PER_KWH
    water_ml = wh * WATER_L_PER_KWH  # Wh x L/kWh = mL
    c, w = level(co2_g, "carbon"), level(water_ml, "water")
    shown = load_state().get(transcript.stem, {})
    return {
        "session": transcript.stem,
        "tokens": tokens,
        "energy_wh": round(wh, 1),
        "co2_g": round(co2_g, 1),
        "water_ml": round(water_ml),
        "carbon_level": c,
        "water_level": w,
        "marker": f"{DOTS[c]} ~{co2_g:.0f} g CO2e  {DROP * w} ~{water_ml:.0f} mL",
        # True when either level is higher than the one last acknowledged.
        "alert": c > shown.get("carbon", 1) or w > shown.get("water", 1),
        "donate": DONATE_URL,
        "estimate": True,
    }


def main() -> int:
    args = sys.argv[1:]
    cmd = args[0] if args else "check"
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252

    stdin_json = {}
    if cmd == "statusline" and not sys.stdin.isatty():
        try:
            stdin_json = json.load(sys.stdin)
        except ValueError:
            pass

    transcript = find_transcript(args, stdin_json)
    if transcript is None or not transcript.is_file():
        print("" if cmd == "statusline" else json.dumps({"error": "no session transcript found"}))
        return 0 if cmd == "statusline" else 1

    r = report(transcript)
    if cmd == "statusline":
        print(r["marker"])
    elif cmd == "ack":
        state = load_state()
        state[r["session"]] = {"carbon": r["carbon_level"], "water": r["water_level"]}
        STATE.parent.mkdir(exist_ok=True)
        STATE.write_text(json.dumps(state), encoding="utf-8")
        print("ok")
    elif cmd == "check":
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
