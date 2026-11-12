#!/usr/bin/env python3
"""Build the download site.

Reads .claude-plugin/marketplace.json, checks every skill, then writes into dist/:

  index.html, style.css      the static site
  skills.json                machine-readable catalogue
  downloads/<skill>.zip      one zip per skill (the folder claude.ai and ~/.claude/skills expect)
  downloads/ethical-skills-all.zip
  downloads/SHA256SUMS

Standard library only. Run from anywhere: python scripts/build.py
"""
import hashlib
import html
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
REPO = "eagnespuerto/ethical-skills-marketplace"
REPO_URL = f"https://github.com/{REPO}"
ZIP_DATE = (2026, 1, 1, 0, 0, 0)  # fixed, so the same source always gives the same zip
SKIP = {"__pycache__", ".DS_Store"}


def frontmatter(skill_md: Path) -> dict:
    """Read the simple `key: value` YAML block at the top of a SKILL.md."""
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, sep, value = line.partition(":")
        if sep and not key.startswith(" "):
            out[key.strip()] = value.strip().strip("\"'")
    return out


def check_skill(skill_dir: Path, plugin: dict) -> list[str]:
    """Return the reasons this skill may not be published. An empty list means it passes."""
    name = plugin["name"]
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{name}: no SKILL.md in {skill_dir}"]
    problems = []
    meta = frontmatter(skill_md)
    if meta.get("name") != name:
        problems.append(f"{name}: SKILL.md name is {meta.get('name')!r}")
    if not meta.get("description"):
        problems.append(f"{name}: SKILL.md has no description")

    # TODO(human): the marketplace's own policy checks go here. The lines above only
    # check that the skill is well formed. Append a message to `problems` for anything
    # a skill must have before it is listed (see CONTRIBUTING.md).

    return problems


def skill_files(skill_dir: Path) -> list[Path]:
    return sorted(p for p in skill_dir.rglob("*")
                  if p.is_file() and not (set(p.parts) & SKIP) and p.suffix != ".pyc")


def write_zip(target: Path, skill_dirs: list[Path]) -> None:
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for skill_dir in skill_dirs:
            for f in skill_files(skill_dir):
                arcname = f"{skill_dir.name}/{f.relative_to(skill_dir).as_posix()}"
                info = zipfile.ZipInfo(arcname, ZIP_DATE)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, f.read_bytes())


def size(path: Path) -> str:
    kb = path.stat().st_size / 1024
    return f"{kb:.0f} KB" if kb >= 10 else f"{kb:.1f} KB"


def card(s: dict) -> str:
    e = html.escape
    credit = f'<a href="{e(s["author_url"])}">{e(s["author"])}</a>'
    upstream = (f' · <a href="{e(s["homepage"])}">original repo</a>' if s.get("homepage") else "")
    return f"""
      <article class="card" id="{e(s['name'])}">
        <p class="tag">{e(s['category'])}</p>
        <h3>{e(s['name'])}</h3>
        <p>{e(s['description'])}</p>
        <p class="meta">By {credit} · {e(s['license'])}{upstream}</p>
        <p class="actions">
          <a class="button" href="{e(s['zip'])}" download>Download .zip <span>{e(s['size'])}</span></a>
          <a href="{e(s['source'])}">Read the source</a>
        </p>
        <pre><code>/plugin install {e(s['name'])}@{e(s['marketplace'])}</code></pre>
      </article>"""


def main() -> int:
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    version = market["metadata"]["version"]
    singles = [p for p in market["plugins"] if len(p["skills"]) == 1]

    problems, skills = [], []
    for p in singles:
        skill_dir = ROOT / p["skills"][0]
        problems += check_skill(skill_dir, p)
        skills.append((p, skill_dir))
    listed = {s for p in market["plugins"] for s in p["skills"]}
    for d in sorted((ROOT / "skills").iterdir()):
        if d.is_dir() and f"./skills/{d.name}" not in listed:
            problems.append(f"{d.name}: in skills/ but not in marketplace.json")
    if problems:
        print("Build stopped:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1

    shutil.rmtree(DIST, ignore_errors=True)
    downloads = DIST / "downloads"
    downloads.mkdir(parents=True)

    catalogue = []
    for p, skill_dir in skills:
        z = downloads / f"{p['name']}.zip"
        write_zip(z, [skill_dir])
        catalogue.append({
            "name": p["name"],
            "description": p["description"],
            "category": p["category"],
            "license": p["license"],
            "author": p["author"]["name"],
            "author_url": p["author"]["url"],
            "homepage": p.get("homepage"),
            "keywords": p.get("keywords", []),
            "marketplace": market["name"],
            "zip": f"downloads/{z.name}",
            "size": size(z),
            "source": f"{REPO_URL}/tree/main/skills/{p['name']}",
        })
    all_zip = downloads / "ethical-skills-all.zip"
    write_zip(all_zip, [d for _, d in skills])

    sums = "".join(f"{hashlib.sha256(z.read_bytes()).hexdigest()}  {z.name}\n"
                   for z in sorted(downloads.glob("*.zip")))
    (downloads / "SHA256SUMS").write_text(sums, encoding="utf-8", newline="\n")
    (DIST / "skills.json").write_text(
        json.dumps({"version": version, "skills": catalogue}, indent=2) + "\n",
        encoding="utf-8", newline="\n")

    page = (ROOT / "site" / "index.template.html").read_text(encoding="utf-8")
    for key, value in {
        "{{VERSION}}": html.escape(version),
        "{{COUNT}}": str(len(catalogue)),
        "{{ALL_SIZE}}": size(all_zip),
        "{{MARKETPLACE}}": html.escape(market["name"]),
        "{{REPO}}": REPO,
        "{{REPO_URL}}": REPO_URL,
        "{{CARDS}}": "".join(card(s) for s in catalogue),
    }.items():
        page = page.replace(key, value)
    (DIST / "index.html").write_text(page, encoding="utf-8", newline="\n")
    shutil.copy(ROOT / "site" / "style.css", DIST / "style.css")
    (DIST / ".nojekyll").touch()

    print(f"Built {len(catalogue)} skills, version {version}, into {DIST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
