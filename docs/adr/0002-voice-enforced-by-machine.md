# ADR-0002: Voice enforced by machine

**Status:** Accepted (2026-05-02; reconstructed 2026-08-13)

## Context

`ice_cream_linter.py` existed before it was a hard gate. PR #58 ("Add
content linter as PR validation gate," merged 2026-05-02) wired it into
`compile-book.yml`'s validate job and fixed four bugs that would have made
it unusable as a CI gate (a CWD-relative `ROOT`, silent encoding-error
suppression, structural checks running against non-recipe files, and an
exit code that blocked PRs on style *warnings* rather than only on hard
*errors*). The PR's own baseline — 0 errors, 92 warnings against `main` at
the time — shows the split was deliberate: structure/encoding/forbidden-
character violations block a PR; voice-drift and profanity-count tuning
are informational only.

CLAUDE.md later restates the resulting rule directly: "The linter is the
QA gate, not a checklist. `ice_cream_linter.py` enforces required sections
..., required metadata..., forbidden characters, broken encoding, and
minimum profanity/address-term counts for voice... Don't maintain a
parallel checklist in this file — when the rules change, change the
linter." That wording was consolidated into CLAUDE.md by PR #106
(2026-05-26, the 898-to-112-line fleet-audit restructure) but the
underlying decision — the linter as the sole, executable QA authority for
required sections, encoding, and forbidden-character/voice rules — dates
to PR #58.

## Decision

Enforce the "HOMIE voice" and structural conventions with an executable
linter (`ice_cream_linter.py`), run in CI via `lint.yml` and as part of
`compile-book.yml`'s validate job, rather than maintaining the rules as
prose guidance for humans (or AI assistants) to self-check. When a rule
changes, the linter's logic changes — CLAUDE.md and STYLE_GUIDE.md
explicitly do not carry a parallel, hand-maintained checklist of the same
rules.

## Alternatives

- **Recorded, explicitly rejected:** a parallel checklist maintained in
  CLAUDE.md alongside the linter. CLAUDE.md states the rejection directly
  — a checklist and a linter drift apart the moment one is updated without
  the other, so the linter is treated as the only authoritative copy of
  the rules it covers.
- *Retrospective — not considered at the time:* ship the linter as
  warnings-only, never a hard-blocking gate. **Worse.** PR #58's own
  baseline shows 92 pre-existing warnings sitting on `main` un-fixed; the
  PR's explicit fix was to stop blocking PRs on warnings precisely
  *because* warning-only enforcement wasn't getting content into
  compliance. A pure-warning linter would have left the required-section
  and encoding checks just as unenforced as the checklist it replaced.
- *Retrospective — not considered at the time:* an LLM-based reviewer that
  judges voice adherence per PR (plausible given `claude.yml` already runs
  an interactive `@claude` responder in this repo). **Worse for this
  role.** The current linter's checks — required headings present,
  metadata fields present, forbidden characters, encoding validity,
  profanity/address-term counts — are deterministic and cheap to run
  against every PR. An LLM judgment call on "does this sound like HOMIE
  voice" would be non-deterministic and harder to debug when CI fails,
  which matters more for a hard-blocking required check than for the
  interactive assistant `claude.yml` already provides alongside it.

## Consequences

- Rule changes are code changes to `ice_cream_linter.py`, reviewed like
  any other PR, rather than documentation edits that could silently
  diverge from what CI actually checks.
- CLAUDE.md and STYLE_GUIDE.md stay focused on canonical content rules and
  do not re-derive the linter's pass/fail logic in prose.
- New contributors (human or AI) get authoritative, actionable feedback
  (which rule, which file) from CI output instead of having to cross-check
  a document against the content by hand.
