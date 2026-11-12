---
name: sarc-check
description: Check whether archival astrometry is from an archive listed by the MPC Singletons and Archival Observations Committee (SARC), and who to contact before submitting. Use when preparing archival / precovery / singleton observations for the MPC, when an obs file (80-col, ADES PSV or XML) uses archive station codes, or when the user says "sarc check", "who do I contact at SARC", or "can I submit these archival obs".
---

# SARC check

Source: https://docs.minorplanetcenter.net/mpc-ops-docs/data-and-services/sarc/#list-of-public-archives-and-corresponding-sarc-contact
(table copied 2026-11-06; re-read the page if it may have changed)

## What the MPC asks

- If you plan to submit archival observations from a listed archive, **contact the SARC member for that archive before submitting**. They help with extraction, vetting, and review.
- Archive **not on the list** → contact the MPC directly for guidance.
- SARC members are volunteers. Reach out **well in advance** of the planned submission date.
- **Singletons** (one measurement in an opposition with no other data) get extra scrutiny, since they can move orbits and Sentry impact probabilities. Only listed users may submit single measurements.
- SARC only recommends. The MPC makes the final call.

## Steps

1. Find the station codes. If there is an obs file, run:
   ```bash
   python -I <this skill's folder>/sarc_check.py <file> [more files...]
   ```
   It reads 80-column, ADES PSV and ADES XML, or takes bare codes (`sarc_check.py 809 W84 675`).
   No file? Ask which telescope/archive the data came from.
2. For each code, report: archive, SARC contact, number of obs, and whether any object has
   only one obs in the file (possible singleton).
3. Flag unlisted codes as "not on SARC list → ask the MPC directly".
4. Give the user a short checklist: who to email, what to send (the obs file, how positions were
   measured, reference catalogue, image IDs/URLs, residuals vs a current orbit), and a reminder
   to wait for the SARC reply before submitting.
5. Do not send any email or submit anything. The user does that.

SARC Chair is Tyler Linder. The page lists no email addresses; find contacts via the MPC
or ask the MPC helpdesk to forward.

## Archive table

| Archive | Observatory codes | Contact |
|---|---|---|
| Asiago Observatory, Cima Ekar | 098, 209 | SARC Chair |
| ATLAS | M22, R17, T05, T08, W68 | Larry Denneau |
| Catalina Sky Survey | 703, G83, G96, I52, V06, V00 | David Rankin |
| Cerro Tololo | 807 | Tyler Linder |
| DECAM | W84 | Tyler Linder |
| ESA various telescopes | 033, 204, 246, B63, J04, J75, L80, Q12, W57, W98, Z33, Z58, Z84 | Marco Micheli |
| Euclid | 273 | SARC Chair |
| European Southern Observatory | 262, 309, 809 | Marco Micheli |
| Gemini North | I11 | SARC Chair |
| Gemini South | T15 | SARC Chair |
| Haleakala-NEAT/GEODSS | 566 | SARC Chair |
| Hubble | 250 | SARC Chair |
| Kitt Peak | 695 | SARC Chair |
| JWST | 274 | SARC Chair |
| La Palma | 950 | SARC Chair |
| LCO | E10, F65, K91, K92, K93, L09, Q58, Q63, Q64, T03, T04, V37, V38, V39, W85, W86, W87, W89, W97, Z17, Z21, Z24, Z31 | SARC Chair |
| Lowell Observatory Near-Earth Objects Survey | 699 | SARC Chair |
| MaunaKea | 568, T09, T10, T11, T12, T13, T14, T16, T17 | SARC Chair |
| Near-Earth Asteroid Tracking (NEAT) | 644 | SARC Chair |
| NEOSSat | C53 | SARC Chair |
| New Horizons | 266, 267 | SARC Chair |
| NEO Surveyor | C58 | Joe Masiero |
| Perth Observatory, Bickley | 323 | SARC Chair |
| SDSS | 645 | Tyler Linder |
| Siding Spring | 413 | SARC Chair |
| Siding Spring - Skymapper | Q55 | SARC Chair |
| SOAR | I33 | SARC Chair |
| SOHO / STEREO | 249, C49, C50 | SARC Chair |
| Spacewatch 0.9m Mosaic Camera Survey | 291, 691 | SARC Chair |
| PanSTARRS | F51, F52 | Rob Weryk |
| Spitzer | 245 | Joe Masiero |
| TESS | C57 | SARC Chair |
| Vera Rubin Observatory / LSST | X05 | Mario Juric |
| VLT Survey Telescope (VST) | X11 | Marco Micheli |
| WISE/NEOWISE | C51 | Joe Masiero |
| ZTF | I41 | Joe Masiero |

The table is not exhaustive. Common codes NOT on it (so: ask the MPC directly) include
675 Palomar plates, 260 Siding Spring UK Schmidt, and W91 VISTA.
