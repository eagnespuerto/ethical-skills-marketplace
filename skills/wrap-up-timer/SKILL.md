---
name: wrap-up-timer
description: Tracks real elapsed time during a coding session and proactively tells the user to wrap up after a set stretch, then again at a daily cap. Use this skill whenever the user is doing a coding, building, or "vibe coding" session in Claude Code and wants help not losing track of time — including when they say things like "start a coding session," "keep me on a timer," "stop me after an hour," "don't let me go too long," "time-box this," or set up a daily coding limit. Once a session is started, keep honoring it on every turn until the user stops it.
---

# Wrap-Up Timer

Helps a user who tends to over-invest in coding sessions stop at a healthy point. It uses the real system clock (via a bundled script) so the nudges reflect actual elapsed time, not guesswork — each turn is a fresh invocation, so the elapsed time MUST be read from the script, never estimated.

## When this is active

A session is "active" once the user starts one. While active, run the check at the **start of every turn** where the user is doing coding work, before diving into their request. Do the check quietly with one bash call; only surface something to the user when a nudge is due.

## Starting a session

When the user asks to be timed / time-boxed / kept on track for a coding session, start tracking. Defaults are a 50-minute soft stretch and a 90-minute daily cap. Honor any limits the user gives ("stop me after an hour" → `--limit 60`; "cap me at two hours a day" → `--cap 120`).

```bash
python3 scripts/timecheck.py start --limit 50 --cap 90
```

Confirm briefly, e.g. "Timer's on — I'll flag a good stopping point around 50 minutes and remind you again at your 90-minute daily cap." Then get to work.

## Each turn while coding

Run this first:

```bash
python3 scripts/timecheck.py check
```

It prints one JSON line, e.g. `{"active": true, "session_min": 52, "today_min": 52, "limit": 50, "cap": 90, "nudge": "limit"}`.

- If `active` is false → no session running, behave normally.
- If `nudge` is `null` → say nothing about time; just help with the request.
- If `nudge` is `"limit"` → the user has passed their soft stretch. Deliver a **gentle** wrap-up nudge (see below), help them reach a clean stopping point (finish the current thought, commit, jot a TODO for next time), then run `python3 scripts/timecheck.py ack limit` so it doesn't repeat every turn.
- If `nudge` is `"cap"` → the user has hit their daily cap. Deliver a **firmer** nudge, and do not start new, large pieces of work. Run `python3 scripts/timecheck.py ack cap` afterward.

## How to nudge (tone)

Be warm, brief, and on their side — never nagging or shaming, never using guilt. The goal is a graceful exit, not an alarm. Acknowledge momentum is real and the work will still be here.

- Soft (limit): "You're about {session_min} minutes into this stretch — past the {limit} you set. Want to find a stopping point? I can commit what we have and leave a note for where to pick up." Then help them land the plane if they agree. If they say "a few more minutes," respect it and don't re-nudge until the cap.
- Firm (cap): "That's your {cap}-minute coding budget for today. Good place to step away — the rest keeps until tomorrow. Want me to write a quick handoff note of where things stand?" Offer to summarize next steps so stopping feels safe, not lossy.

If the user mentioned someone to reconnect with, you can lightly suggest it. Don't moralize.

## Other commands

- `python3 scripts/timecheck.py status` — show elapsed/today/limits (use if the user asks "how long have I been at this?").
- `python3 scripts/timecheck.py stop` — pause the session and bank the minutes toward today's total (use when the user says they're done or stepping away).
- `python3 scripts/timecheck.py reset` — clear today's state.

The day's totals and limits reset automatically at midnight (the script checks the date on every call).

## Important

- Always read elapsed time from the script. Never invent or estimate minutes.
- Respect the user's autonomy. If they decline to stop, don't argue or repeat the nudge for the same threshold — note it and move on.
- This is a wellbeing guardrail the user asked for. Keep it light, kind, and easy to follow.
