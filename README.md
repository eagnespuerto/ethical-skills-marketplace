# Ethical Skills Marketplace

[![Release](https://img.shields.io/github/v/release/eagnespuerto/ethical-skills-marketplace?label=release)](https://github.com/eagnespuerto/ethical-skills-marketplace/releases/latest)
[![License: MIT](https://img.shields.io/github/license/eagnespuerto/ethical-skills-marketplace)](LICENSE)
[![Deploy site](https://github.com/eagnespuerto/ethical-skills-marketplace/actions/workflows/pages.yml/badge.svg)](https://github.com/eagnespuerto/ethical-skills-marketplace/actions/workflows/pages.yml)
[![Site](https://img.shields.io/website?url=https%3A%2F%2Feagnespuerto.github.io%2Fethical-skills-marketplace%2F&label=site)](https://eagnespuerto.github.io/ethical-skills-marketplace/)
[![Skills](https://img.shields.io/badge/skills-7-1f6f54)](#the-skills)
[![Claude Code plugin marketplace](https://img.shields.io/badge/Claude%20Code-plugin%20marketplace-d97757)](#claude-code)
[![Downloads](https://img.shields.io/github/downloads/eagnespuerto/ethical-skills-marketplace/total)](https://github.com/eagnespuerto/ethical-skills-marketplace/releases)

Seven agent skills that teach an AI assistant some manners. I wrote six of them for my own work with Claude. The seventh is Peter Yang's `no-ai-slop`, included with credit.

**Download site: https://eagnespuerto.github.io/ethical-skills-marketplace/**

## The skills

| Skill | What it does | Author |
|---|---|---|
| [`fetch-rules`](skills/fetch-rules) | House rules for pulling data from other people's servers. Read `robots.txt`, send an honest User-Agent, wait 2 minutes after a 429 or 503, never work around a 403, and stop at 3 GB per source per night. | Ella Agnes Puerto |
| [`code-of-ethics`](skills/code-of-ethics) | Applies the ACM Code of Ethics to computing work. Each flag is one or two sentences with the principle number and a fix. It can also audit a design or answer questions about the Code. | Ella Agnes Puerto |
| [`no-generated-art`](skills/no-generated-art) | When a task needs names, icons, photos or art, the assistant searches open libraries made by people and generates nothing. | Ella Agnes Puerto |
| [`wrap-up-timer`](skills/wrap-up-timer) | Reads the real clock during a coding session. It tells you to wrap up after 50 minutes and again at a 90-minute daily cap. You can change both numbers. | Ella Agnes Puerto |
| [`carbon-water-footprint`](skills/carbon-water-footprint) | Estimates the carbon and water footprint of a session from its real token counts. A small marker goes from green to yellow to red for carbon and from one to three drops for water. At red it shares a Greenpeace donation link. The numbers are estimates, and you can change every factor. | Ella Agnes Puerto |
| [`sarc-check`](skills/sarc-check) | For astronomers. Before you send archival astrometry to the Minor Planet Center, it checks which station codes are on the SARC list and names the committee member to contact first. | Ella Agnes Puerto |
| [`no-ai-slop`](skills/no-ai-slop) | Edits a draft into sharper writing that still sounds like you, or lists the AI patterns in it without rewriting. | [Peter Yang](https://github.com/petergyang/no-ai-slop) |

## Install

### Claude Code

Add the marketplace once:

```
/plugin marketplace add eagnespuerto/ethical-skills-marketplace
```

Then install everything, or one skill:

```
/plugin install ethical-skills@ethical-skills
/plugin install fetch-rules@ethical-skills
```

### Claude apps

Download one skill's zip from the [site](https://eagnespuerto.github.io/ethical-skills-marketplace/) or the [latest release](https://github.com/eagnespuerto/ethical-skills-marketplace/releases/latest). In Claude, open Settings, find Skills, and upload the zip.

### By hand

Each skill is one folder with a `SKILL.md` inside. Unzip the bundle into your skills folder:

```bash
unzip ethical-skills-all.zip -d ~/.claude/skills/
```

`downloads/SHA256SUMS` on the site lists a checksum for every zip.

### npm, from GitHub Packages

Each release is also published as `@eagnespuerto/ethical-skills-marketplace`. GitHub Packages asks for a personal access token with `read:packages`, even for public packages, so the zip is the easier route for most people.

```bash
npm install @eagnespuerto/ethical-skills-marketplace --registry=https://npm.pkg.github.com
```

## Set up fetch-rules before you use it

`fetch-rules` sends a User-Agent with a name and a contact address, so a server admin can reach the person behind the script. The copy here has placeholders. Open `skills/fetch-rules/SKILL.md` and replace `YOUR NAME` and `you@example.org` with your own, in the header block and in the Python example.

## How the repo works

`.claude-plugin/marketplace.json` is the catalogue. `scripts/build.py` reads it, checks every skill, zips each one, and writes the site into `dist/`. It needs Python 3.9 or later and no packages.

```bash
python scripts/build.py
```

GitHub Actions runs the same script on every push to `main` and deploys `dist/` to GitHub Pages. When I publish a release, a second workflow attaches the zips to it and publishes the npm package.

## Credits and licences

My five skills are under the [MIT License](LICENSE).

`no-ai-slop` is by Peter Yang, copied unchanged from [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) under its own [MIT License](skills/no-ai-slop/LICENSE). I also ran this README through it.

`code-of-ethics` includes a paraphrased summary of the [ACM Code of Ethics and Professional Conduct](https://www.acm.org/code-of-ethics). The ACM holds the copyright on the Code and does not endorse this project. The SARC table in `sarc-check` comes from the [Minor Planet Center's public page](https://docs.minorplanetcenter.net/mpc-ops-docs/data-and-services/sarc/), which changes, so read it again before you rely on the table.

More detail is in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Add a skill

Pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) has the steps.
