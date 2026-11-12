---
name: carbon-water-footprint
description: Use when the user wants to monitor, track or see the carbon footprint, energy use or water usage of an AI coding session - including "how much CO2 has this session used", "what is my footprint", "how much water", "show the footprint marker", "track my carbon", "is this session getting heavy", or asks for a usage-style environmental alert. Once tracking is on, keep honoring it on every turn until the user stops it.
---

# Carbon and Water Footprint

Shows a small usage-style marker for the session's estimated footprint: a dot for carbon (green, yellow, red) and one to three drops for water.

Token counts come from the session transcript, so they are measured. Energy, CO2e and water are **estimates** from public factors. No AI provider publishes exact per-token figures. Always call the numbers estimates, and never invent or adjust them: read them from the script.

## Each turn while tracking

Run this once, quietly, at the end of your work for the turn:

```bash
python3 scripts/footprint.py check
```

It prints one JSON line, for example:

`{"co2_g": 77.0, "water_ml": 601, "carbon_level": 2, "water_level": 2, "marker": "🟡 ~77 g CO2e  💧💧 ~601 mL", "alert": true, ...}`

- `alert` is false → say nothing about footprint. Just help.
- `alert` is true → a level went up. End your reply with the `marker` line as given, plus one short plain sentence (see below). Then run `python3 scripts/footprint.py ack` so it does not repeat every turn.
- The user asks about the footprint → show the `marker`, the token counts and `energy_wh`, and say these are estimates.

If the script prints `{"error": ...}`, say the transcript was not found and offer `--transcript PATH` or `--session ID`.

## What to say at each level

| Level | Carbon | Water | Say |
|---|---|---|---|
| 1 | 🟢 under 50 g | 💧 under 500 mL | Nothing, unless asked. |
| 2 | 🟡 from 50 g | 💧💧 from 500 mL | One line: the session is getting heavier. Offer a lighter path if one exists. |
| 3 | 🔴 from 250 g | 💧💧💧 from 2 L | One line, a lighter path, and the donation link in `donate`. |

### Example: a real heavy session

A day-long archive search for precovery images of the asteroid 2026 ED138 (28 October 2026) made 197 requests. The script reports:

| Tokens | Count | Energy |
|---|---|---|
| Output | 164,549 | 82 Wh |
| Fresh input | 733,631 | 73 Wh |
| Cache read | 46,413,307 | 464 Wh |

Total: about 620 Wh, `🔴 ~293 g CO2e  💧💧💧 ~2287 mL`. Three quarters of it is cache reads: the long context being read again on every request. That is why a fresh session is the first lighter path to offer. The red thresholds sit just under this session.

Lighter paths that work: start a fresh session (long sessions re-read a big context on every request), use a smaller model for routine work, ask for shorter answers, and batch small questions into one message.

At level 3, add once: "If you want to give something back, Greenpeace takes donations at https://www.greenpeace.org/international/act/donate/". Share the link again only when the user asks. A donation does not cancel the footprint, so do not call it an offset.

## Tone

Inform, do not scold. The user asked for a meter, not a lecture. No guilt, no moralising, and no refusing work because the marker is red. If the user says to carry on, carry on, and stay quiet until the next level.

## Always-on marker (optional)

For a marker that is always visible, offer to set it as the Claude Code status line. In `~/.claude/settings.json`, with the full path to the script:

```json
{ "statusLine": { "type": "command", "command": "python3 /path/to/scripts/footprint.py statusline" } }
```

Change settings only when the user says yes.

## Factors and limits

Defaults are in the first lines of `scripts/footprint.py`, with sources. Set an environment variable to change one:

| Variable | Default | Meaning |
|---|---|---|
| `FOOTPRINT_WH_OUT` / `_IN` / `_CACHE` | 0.5 / 0.1 / 0.01 | Wh per 1000 output, input and cache-read tokens |
| `FOOTPRINT_GRID_G_PER_KWH` | 473 | Grid carbon intensity, world average 2024 |
| `FOOTPRINT_WATER_L_PER_KWH` | 3.69 | Cooling water plus water used to generate the electricity |

Not counted: model training, hardware manufacturing, the user's own computer, and subagent transcripts. The true figure can differ from the estimate by several times in either direction. Say so if the user plans to quote the numbers.
