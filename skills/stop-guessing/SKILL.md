---
name: stop-guessing
description: Use when about to state, write or use a value or fact you have not checked - a version number, API field, flag, file path, function name, config key, constant, default, URL, date, price, DOI, coordinate or any "probably" or "usually" - in code, commands, docs or answers. Also when the user says "stop guessing", "/stop-guessing", "look it up" or "don't make things up".
---

# Stop guessing

If a value matters and you have not seen it this session, look it up before you use it. A wrong guess costs more than a search. Most guesses come out as plausible text, so they are hard for the person to spot.

## The check

Before you write a value, ask: **where did I see this?**

- **In this session** (a file you read, a command's output, a page you fetched, the user's message): use it.
- **Only from memory or "it is usually"**: stop and search first.

Values that need the check include versions, package and module names, function and method signatures, CLI flags, config keys, environment variables, file paths, URLs and endpoints, API fields, defaults and limits, constants, dates, prices, IDs (DOIs, issue numbers, catalogue IDs), coordinates, and names of people.

## Where to search

Search the closest source first.

1. **The code in front of you.** Grep or glob the repo for the name, read the file, the lockfile or the config. Run `--help` or `--version` for a CLI. Read the installed package source if the docs are unclear.
2. **Official docs or the source repo.** Search the web for the project's own docs, changelog or README. Prefer these over blogs and forum answers.
3. **The live system.** Query the API, list the directory, check the actual output. Follow any fetch etiquette that applies (robots.txt, rate limits).
4. **The user.** If 1 to 3 cannot answer it (their own preference, a private value, a password), ask. Do not invent a placeholder that looks real.

## When you still cannot confirm

- Say so plainly: "I could not confirm X. I used Y because Z."
- Mark it in code with a short comment, or use an obvious placeholder (`YOUR_API_URL`), never a realistic fake.
- Do not dress a guess in a confident tone or false precision.

## Red flags

These thoughts mean you are about to guess:

| Thought | Do this instead |
|---|---|
| "It is probably called..." | Grep for it. |
| "The default is usually..." | Read the docs or the source. |
| "I think the latest version is..." | Check the registry or release page. |
| "This flag should work" | Run `--help`. |
| "The path is likely..." | List the directory. |
| "Searching takes too long" | One search is faster than one bug. |

## What does not need a search

Common knowledge that is not about this project (how a `for` loop works), values you just read this session, and values you are choosing on purpose (a new variable name). Keep searching proportionate: one good lookup, not ten.
