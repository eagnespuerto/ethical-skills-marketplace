"""Map MPC station codes in obs files to SARC archive contacts.

Usage:
  python -I sarc_check.py obs.txt [obs.psv obs.xml ...]
  python -I sarc_check.py 809 W84 675
Reads 80-column, ADES PSV and ADES XML. No dependencies.
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# From https://docs.minorplanetcenter.net/mpc-ops-docs/data-and-services/sarc/ (2026-11-06)
TABLE = [
    ("Asiago Observatory, Cima Ekar", "098 209", "SARC Chair"),
    ("ATLAS", "M22 R17 T05 T08 W68", "Larry Denneau"),
    ("Catalina Sky Survey", "703 G83 G96 I52 V06 V00", "David Rankin"),
    ("Cerro Tololo", "807", "Tyler Linder"),
    ("DECAM", "W84", "Tyler Linder"),
    ("ESA various telescopes", "033 204 246 B63 J04 J75 L80 Q12 W57 W98 Z33 Z58 Z84", "Marco Micheli"),
    ("Euclid", "273", "SARC Chair"),
    ("European Southern Observatory", "262 309 809", "Marco Micheli"),
    ("Gemini North", "I11", "SARC Chair"),
    ("Gemini South", "T15", "SARC Chair"),
    ("Haleakala-NEAT/GEODSS", "566", "SARC Chair"),
    ("Hubble", "250", "SARC Chair"),
    ("Kitt Peak", "695", "SARC Chair"),
    ("JWST", "274", "SARC Chair"),
    ("La Palma", "950", "SARC Chair"),
    ("LCO", "E10 F65 K91 K92 K93 L09 Q58 Q63 Q64 T03 T04 V37 V38 V39 W85 W86 W87 W89 W97 Z17 Z21 Z24 Z31", "SARC Chair"),
    ("Lowell Observatory Near-Earth Objects Survey", "699", "SARC Chair"),
    ("MaunaKea", "568 T09 T10 T11 T12 T13 T14 T16 T17", "SARC Chair"),
    ("Near-Earth Asteroid Tracking (NEAT)", "644", "SARC Chair"),
    ("NEOSSat", "C53", "SARC Chair"),
    ("New Horizons", "266 267", "SARC Chair"),
    ("NEO Surveyor", "C58", "Joe Masiero"),
    ("Perth Observatory, Bickley", "323", "SARC Chair"),
    ("SDSS", "645", "Tyler Linder"),
    ("Siding Spring", "413", "SARC Chair"),
    ("Siding Spring - Skymapper", "Q55", "SARC Chair"),
    ("SOAR", "I33", "SARC Chair"),
    ("SOHO / STEREO", "249 C49 C50", "SARC Chair"),
    ("Spacewatch 0.9m Mosaic Camera Survey", "291 691", "SARC Chair"),
    ("PanSTARRS", "F51 F52", "Rob Weryk"),
    ("Spitzer", "245", "Joe Masiero"),
    ("TESS", "C57", "SARC Chair"),
    ("Vera Rubin Observatory / LSST", "X05", "Mario Juric"),
    ("VLT Survey Telescope (VST)", "X11", "Marco Micheli"),
    ("WISE/NEOWISE", "C51", "Joe Masiero"),
    ("ZTF", "I41", "Joe Masiero"),
]
LOOKUP = {c: (arch, who) for arch, codes, who in TABLE for c in codes.split()}
CODE_RE = re.compile(r"^[0-9A-Z]\d\d$")


def parse_file(path):
    """Return list of (object, station) pairs."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    out = []
    if "<stn>" in text:  # ADES XML
        for block in re.findall(r"<optical>(.*?)</optical>", text, re.S):
            stn = re.search(r"<stn>\s*(\w+)\s*</stn>", block)
            obj = re.search(r"<(?:provID|permID|trkSub)>\s*([^<]+?)\s*</", block)
            if stn:
                out.append((obj.group(1) if obj else "?", stn.group(1)))
        return out
    lines = text.splitlines()
    header = next((l for l in lines if "|" in l and not l.startswith(("#", "!"))), None)
    if header and "stn" in [h.strip() for h in header.split("|")]:  # ADES PSV
        cols = [h.strip() for h in header.split("|")]
        i_stn = cols.index("stn")
        i_obj = next((cols.index(k) for k in ("provID", "permID", "trkSub") if k in cols), None)
        for l in lines[lines.index(header) + 1:]:
            if "|" not in l or l.startswith(("#", "!")):
                continue
            f = [x.strip() for x in l.split("|")]
            if len(f) > i_stn:
                obj = f[i_obj] if i_obj is not None and f[i_obj] else "?"
                out.append((obj, f[i_stn]))
        return out
    for l in lines:  # 80-column
        if len(l) >= 80 and l[14] not in "sv" and CODE_RE.match(l[77:80]):
            out.append((l[:12].strip() or "?", l[77:80]))
    return out


def main(args):
    if not args:
        print(__doc__)
        return 1
    pairs = []
    for a in args:
        if Path(a).is_file():
            got = parse_file(a)
            print(f"{a}: {len(got)} obs")
            pairs += got
        elif CODE_RE.match(a.upper()):
            pairs.append(("-", a.upper()))
        else:
            print(f"skip {a}: not a file or station code")
    per_stn = Counter(s for _, s in pairs)
    per_obj_stn = defaultdict(Counter)
    for o, s in pairs:
        per_obj_stn[s][o] += 1
    print()
    print(f"{'stn':4} {'n':>4}  {'archive':40} contact")
    for stn, n in sorted(per_stn.items()):
        arch, who = LOOKUP.get(stn, ("NOT ON SARC LIST", "ask the MPC directly"))
        print(f"{stn:4} {n:>4}  {arch:40} {who}")
        singles = [o for o, k in per_obj_stn[stn].items() if k == 1 and o != "-"]
        if singles:
            print(f"           possible singletons: {', '.join(singles[:10])}"
                  + (" ..." if len(singles) > 10 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
