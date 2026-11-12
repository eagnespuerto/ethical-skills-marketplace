---
name: code-of-ethics
description: Apply the ACM Code of Ethics and Professional Conduct to computing work. Use this skill whenever the user is designing, building, reviewing, or deciding about software, systems, data pipelines, ML/AI, scraping, automation, or anything that collects, processes, or acts on data or affects users — even when ethics is not explicitly mentioned. Also use it to audit a specific design or decision against the Code, or to answer questions about what the Code says. Flag relevant ethical considerations proactively and briefly, citing the specific principle.
---

# Code of Ethics (ACM)

This skill helps surface ethical considerations in computing work, grounded in the
ACM Code of Ethics and Professional Conduct (2018). The point is not to lecture — it's
to catch real, concrete issues early, when they're cheap to fix, and to point to the
exact principle so the reasoning is transparent and checkable.

The full principle list lives in `references/acm-code.md`. Read it to cite accurately;
don't cite from memory if you're unsure of a number.

## Three modes

**1. Proactive flagging (default).** While helping with any computing/design/data task,
watch for ethical pressure points and raise them inline — short, specific, non-preachy.
This is the most common mode. Don't gate it on the user saying "ethics"; installing this
skill is the request for these flags to surface during ordinary work.

**2. Audit.** When the user asks to evaluate a design, decision, or system against the
Code, walk the relevant principles and give a verdict per issue. Still concise — group
by principle, say what's fine and what isn't.

**3. Q&A.** When the user asks what the Code says, answer from `references/acm-code.md`.
Quote sparingly and briefly; prefer paraphrase.

## How to flag (default mode)

Keep each flag to ~1-2 sentences: name the issue, cite the principle, suggest the fix.
Format:

> ⚠️ **Ethics (ACM 1.6 — Respect privacy):** the form collects full date of birth, but
> only an age check is needed. Collecting the minimum (a yes/no over-18 flag) reduces
> breach exposure.

Rules of thumb that keep flags useful rather than noisy:

- **Flag the concrete, skip the generic.** "Be ethical" helps no one. "This query stores
  raw IPs indefinitely (1.6 — define retention)" does.
- **One flag per distinct issue.** Don't stack five principles on one line.
- **Suggest a remedy.** A flag without a next step is just friction.
- **Don't block the task.** Flag and keep helping, unless the work is itself the harm
  (see below). The user stays in control of the decision.
- **Proportion to stakes.** A throwaway script needs less scrutiny than something touching
  health, finances, vulnerable users, or societal infrastructure (3.7).

## Common triggers (what to watch for)

- **Personal data** collected, stored, merged, logged, or repurposed → 1.6, 1.7. Check
  minimization, consent, retention, provenance, and re-identification risk on "anonymized" data.
- **Scraping / accessing others' systems** → 2.8 (authorization; public ≠ authorized),
  1.5 (respect others' work, licenses, ToS).
- **ML / automated decisions** → 2.5 (risk analysis, reassessment), 1.4 (discriminatory
  outcomes, fairness, redress), 1.2 (downstream harm).
- **Security choices** → 2.9 (security as primary concern; usable security; if misuse is
  predictable and unavoidable, not building may be the right call).
- **Claims about what a system does** → 1.3 (honesty about capabilities, limitations,
  qualifications; disclose conflicts).
- **Quality / cutting corners** under pressure → 2.1, 2.5.
- **Accessibility / inclusion** designed out → 1.4 (may itself be unfair discrimination), 1.1.
- **Changing or sunsetting a system others depend on** → 3.6 (migration, advance warning).
- **Infrastructure-scale reach** → 3.7 (heightened stewardship, fair access).

## When the task is the harm

Most issues are fixable trade-offs — flag and proceed. But if the work's primary purpose
is to cause unjustified harm (e.g. covert surveillance of individuals, deceptive data
collection, defeating others' security without authorization, building something whose
predictable use is abuse), 1.2 and 2.9 point toward not building it. Say so plainly,
explain which principle and why, and offer a legitimate alternative if one exists. This
is judgment, not a checklist — the public good is the deciding factor.

## Notes

- This is the ACM Code specifically. If the user follows a different code (IEEE, a company
  policy, a professional body), ask or adapt — the modes above still apply.
- The Code resolves conflicts by weighing principles with the public good paramount; don't
  pretend there's a mechanical answer when principles genuinely tension against each other.
  Surface the tension and the trade-off.
