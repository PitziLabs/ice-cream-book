# ADR-0001: Two compilers, one source

**Status:** Accepted (2026-05-26; reconstructed 2026-08-13)

## Context

This repo started life (2025-11-19) as a book-only project: `recipes/*.md`
plus `compile_book.py`, which strips each file's YAML frontmatter and
concatenates the prose into `Ice_Cream_to_Fight_With_COMPLETE.md`.

On 2026-05-26, PR #83 imported the Astro website application (previously
built and deployed from `foundry-platform-demo/app/`, per solidago#55) into
this repo, bringing `sync_recipes.py` alongside `compile_book.py`. From that
point the repo has run two build pipelines reading the same `recipes/*.md`
files: the book pipeline strips the YAML frontmatter block for pure prose,
and the website pipeline (`sync_recipes.py`) parses that same frontmatter
into an Astro content collection so the site can render metadata cards
(cuisine, time, yield, dietary tags).

This means every recipe file carries information that looks redundant —
the YAML frontmatter often restates facts the prose body also states in
words. CLAUDE.md addresses this directly: "Frontmatter is intentional
duplication... Don't 'consolidate' — the YAML feeds the website's metadata
card and the prose feeds the book."

## Decision

Keep `recipes/*.md` as the single source of truth for both outputs, and
keep the two compilers separate and format-specific rather than building
one unified renderer:

- `compile_book.py` strips YAML, concatenates prose → the printable book.
- `sync_recipes.py` parses YAML (+ select prose lines like
  `**Difficulty:**` / `**Total Time:**`) → the Astro content collection.

The apparent duplication between frontmatter and prose is not to be
merged away; each field serves a different consumer.

## Alternatives

No alternative to the two-pipeline split itself is recorded in the
repo's own evidence — PR #83 is a mechanical migration of an already-built
Astro app into the existing book repo, not a design debate about compiler
architecture. The "don't consolidate frontmatter and prose" instruction in
CLAUDE.md is the one explicit, recorded rejection in-repo: someone was
tempted to treat the YAML/prose overlap as redundant and was told not to.

- *Recorded at the website pipeline's origin (2026-03-19, per early-era
  session records):* **Craft** (the note-taking app) was considered as the
  content home and rejected as adding no value over a direct
  Markdown → SSG pipeline. **Astro** and the `sync_recipes.py`
  frontmatter-parsing bridge were chosen then — the same bridge that
  survives unchanged as today's website compiler — and Astro went on to
  become the default stack for every subsequent Lentago site. **Worse**
  (Craft): an app-shaped silo in front of content that wants to be plain
  files feeding two compilers.

- *Retrospective — not considered at the time:* separate book and site
  repos (one repo owning `compile_book.py` and the Markdown book, another
  owning `sync_recipes.py` and the Astro site, each with its own copy of
  `recipes/*.md`). **Worse.** `ice_cream_linter.py` is the single QA gate
  for voice, structure, and encoding across both outputs (see
  [ADR-0002](0002-voice-enforced-by-machine.md)); splitting the source
  across two repos means either running two copies of that linter against
  two copies of the content (drift risk — the two `recipes/` directories
  silently diverge) or building cross-repo sync tooling that does not
  otherwise need to exist. A single repo with two format-specific
  compilers gets shared linting and a single edit landing in both outputs
  for free.

## Consequences

- Editing a recipe's prose affects both outputs on the next compile/deploy;
  editing only the frontmatter affects the website but not the book.
- Anyone reading a recipe file cold sees fields that look duplicated
  between the YAML block and the prose — this is expected, not a cleanup
  target (see `docs/INFRASTRUCTURE_RELATIONSHIP.md`).
- `ice_cream_linter.py` only has to validate one copy of the content for
  both pipelines.
