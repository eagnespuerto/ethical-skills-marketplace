# Adding a skill

Open a pull request. Every change goes through a branch and a PR, including mine.

1. Put the skill in `skills/<name>/` with a `SKILL.md`. The `name` in its front matter must match the folder.
2. Add an entry to `.claude-plugin/marketplace.json` with `name`, `description`, `category`, `license` and `author`. Copy an existing entry. Add the skill path to the `ethical-skills` bundle too.
3. If you did not write the skill, keep its licence file in the folder, set `homepage` to the original repo, and add a section to `THIRD_PARTY_NOTICES.md`.
4. Run `python scripts/build.py`. It checks every skill and builds the site into `dist/`.

Take personal details out of the skill first: names, email addresses, home paths, tokens.

## What belongs here

A skill belongs here if it makes an assistant behave better toward someone: the people who run a server, the people a system affects, the people who made a work, or the user.
