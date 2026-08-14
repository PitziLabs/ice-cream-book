# ADR-0003: The editorial redesign over the punk-zine redesign

**Status:** Accepted (2026-07-11; reconstructed 2026-08-13)

## Context

PR #123 ("Redesign the site as a dated punk-zine blog," merged
2026-07-06T20:17:39Z) shipped a substantial visual and information-
architecture change: a reverse-chronological "issues" blog framing with
synthesized publication dates, and a Riso-inspired fluoro-pink/teal
photocopy-zine visual style, replacing the prior difficulty-tier
food-magazine layout.

It did not stay live. PR #124 ("Revert 'Redesign the site as a punk-zine
blog' (#123)," merged 2026-07-06T21:28:02Z — roughly one hour later)
reverted it in full: "The punk-zine redesign is being set aside in favor
of a fresh design started directly in Claude Design. Reverting keeps a
clean, familiar layout at the live URL in the meantime... The reverted
work remains in history (commit f62d2c3) if any of it is wanted later."

PR #127 ("Implement the editorial redesign from Claude Design," merged
2026-07-11T01:54:02Z) then shipped the replacement: a warm-paper/ink
editorial design (Bricolage Grotesque / Newsreader / Space Mono, a
heat-ramp difficulty palette, filmstrip navigation in book order, the
homepage repurposed as the book's Introduction) built from a Claude
Design project ("Ice Cream Blog Redesign"), explicitly framed as "the
design restart follows the reverted punk-zine experiment (#123/#124);
this is the intended destination."

## Decision

Adopt the editorial/magazine design from PR #127 as the site's visual and
IA direction. The punk-zine blog framing from PR #123 — dated "issues,"
reverse-chronological feed, photocopy-zine visual style — is discarded,
not merged or blended; it survives only as reverted history (commit
f62d2c3) and is available to revisit if wanted.

## Alternatives

- **Recorded, genuinely tried and discarded:** the punk-zine dated-blog
  redesign (PR #123). This was not a proposal weighed on paper — it was
  built, merged, and lived on the production site before being reverted
  within about an hour in favor of restarting design from scratch.
- *Retrospective — not considered at the time:* iterate on the punk-zine
  design in place instead of reverting to the old layout and starting a
  fresh design. **Worse for this project.** PR #124's own rationale was to
  restore "a clean, familiar layout at the live URL in the meantime" while
  a proper replacement was designed via Claude Design — i.e., minimize
  what's live on a real public URL while retaining option value (the
  zine work stays in git history). Iterating on a direction already being
  "set aside" would have kept an abandoned design live on production
  instead.
- *Retrospective — not considered at the time:* A/B test the punk-zine and
  editorial designs before committing to one. **Lateral, and not a fit for
  this project.** This is a low-traffic exhibit site with no analytics
  infrastructure evidenced in this repo for statistically meaningful
  A/B results; the added infrastructure and decision latency would not
  have been repaid by better signal, and neither design's proponents are
  in dispute here — both PRs were driven by the same author/session.

## Consequences

- The dated-blog / reverse-chronological IA (synthesized recipe `date`
  frontmatter, RSS `pubDate` driven by it, older/newer-by-date navigation)
  is gone; recipe organization returned to difficulty tiers and PR #127's
  book-order filmstrip.
- The punk-zine visual assets and `dispatch.ts` date-formatting helper are
  not part of the current site; recovering any of it means reaching into
  history at commit f62d2c3 rather than reading current source.
- The editorial design's own scope cuts (search/Pagefind, tier/cuisine
  index pages, dark mode, homepage filters removed per PR #127) are a
  consequence of this decision, not a separate one — they were part of
  "the designed surface" PR #127 shipped as the intended destination.
