#!/usr/bin/env python3
"""
Ice Cream Book Linter v3 (Grouped Output + Suggestions + Prioritized Ordering)
"""

import argparse
import sys
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
RECIPE_DIR = ROOT / "recipes"
FRONT_DIR = ROOT / "front_matter"
BACK_DIR = ROOT / "back_matter"
CANONICAL_DIR = ROOT / "canonical_samples"

PROFANITY = ["fuck", "shit", "damn", "hell", "ass"]
ADDRESS_TERMS = ["homie", "chief", "buddy", "pal", "boss", "dawg", "friendo"]
FORBIDDEN_CHARS = ["✓", "→", "★", "🔥", "🍨"]
ENCODING_BROKEN = ["â€", "Ã", "�"]

REQUIRED_SECTIONS = ["## Ingredients", "## Instructions", "## Notes"]
REQUIRED_METADATA = ["**Difficulty:**", "**Total Time:**"]

VOICE_THRESHOLD = 0.65

# --- Helpers ---

def read_file(path):
    return path.read_text(encoding="utf-8", errors="replace")


def tokenize(text):
    return re.sub(r"[^a-z\s]", "", text.lower()).split()


def vectorize(text):
    return Counter(tokenize(text))


def cosine_similarity(v1, v2):
    common = set(v1) & set(v2)
    dot = sum(v1[x] * v2[x] for x in common)
    mag1 = sum(v*v for v in v1.values()) ** 0.5
    mag2 = sum(v*v for v in v2.values()) ** 0.5
    return dot / (mag1 * mag2) if mag1 and mag2 else 0


def build_canonical_profile():
    if not CANONICAL_DIR.exists():
        return Counter()
    return vectorize("\n".join(read_file(f) for f in CANONICAL_DIR.glob("*.md")))

CANONICAL_PROFILE = build_canonical_profile()


def count_occurrences(text, words):
    text = text.lower()
    return sum(text.count(w) for w in words)


def split_paragraphs(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def split_sentences(text):
    return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]


def suggest(msg, fix):
    return f"{msg} → SUGGEST: {fix}"

# --- Checks ---

def check_blockers(text, is_recipe):
    errors = []

    for ch in FORBIDDEN_CHARS:
        if ch in text:
            errors.append(suggest(f"Forbidden character '{ch}'", "Remove or replace"))

    for bad in ENCODING_BROKEN:
        if bad in text:
            errors.append(suggest(f"Encoding corruption: {bad}", "Re-save as UTF-8"))

    if not is_recipe:
        return errors

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(suggest(f"Missing section: {section}", "Add required section"))

    for meta in REQUIRED_METADATA:
        if meta not in text:
            errors.append(suggest(f"Missing metadata: {meta}", "Add metadata"))

    if "what it tastes like" not in text.lower():
        errors.append(suggest("Missing 'What it Tastes Like'", "Add final section"))

    return errors


def check_all(text):
    warnings = []

    if count_occurrences(text, PROFANITY) > 5:
        warnings.append(suggest("Too much profanity", "Remove 1–3 uses"))

    if count_occurrences(text, ADDRESS_TERMS) > 4:
        warnings.append(suggest("Too many address terms", "Reduce to ≤4"))

    if CANONICAL_PROFILE:
        sim = cosine_similarity(vectorize(text), CANONICAL_PROFILE)
        if sim < VOICE_THRESHOLD:
            warnings.append(suggest(f"Voice drift ({sim:.2f})", "Align intro/notes to canonical"))

    sentences = split_sentences(text)
    if sentences:
        avg = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg > 22:
            warnings.append(suggest("Sentences too long", "Split long sentences"))

    for i, p in enumerate(split_paragraphs(text)):
        if count_occurrences(p, PROFANITY) > 2:
            warnings.append(suggest(f"Profanity clustering (para {i+1})", "Spread or remove"))
            break

    if "## Instructions" in text:
        instr = text.split("## Instructions", 1)[1]
        if count_occurrences(instr, PROFANITY) > 2:
            warnings.append(suggest("Too much profanity in instructions", "Keep neutral tone"))

    return warnings


def lint_file(path, is_recipe):
    text = read_file(path)
    errors = check_blockers(text, is_recipe)
    warnings = check_all(text)
    return errors, warnings

# --- Main ---

def render_text(results, total_files, files_with_issues, total_errors, total_warnings):
    out = []
    for f, errors, warnings in results:
        out.append(f"\n{f}")
        if errors:
            out.append(f"  ERROR ({len(errors)})")
            for e in errors:
                out.append(f"    - {e}")
        if warnings:
            out.append(f"  WARN ({len(warnings)})")
            for w in warnings:
                out.append(f"    - {w}")
    out.append("\nSUMMARY")
    out.append(f"  Files checked: {total_files}")
    out.append(f"  Files with issues: {files_with_issues}")
    out.append(f"  Errors: {total_errors}")
    out.append(f"  Warnings: {total_warnings}")
    return "\n".join(out)


def render_markdown(results, total_files, total_errors, total_warnings):
    out = ["## Linter Report", ""]
    out.append(
        f"**Files checked:** {total_files} · "
        f"**Errors:** {total_errors} · "
        f"**Warnings:** {total_warnings}"
    )
    out.append("")

    if total_errors:
        out.append("### Errors")
        out.append("")
        for f, errors, _ in results:
            if not errors:
                continue
            out.append(f"**`{f.relative_to(ROOT)}`**")
            for e in errors:
                out.append(f"- {e}")
            out.append("")
    else:
        out.append("No errors.")
        out.append("")

    if total_warnings:
        out.append("<details>")
        out.append(f"<summary>{total_warnings} warnings across {sum(1 for _, _, w in results if w)} files</summary>")
        out.append("")
        for f, _, warnings in results:
            if not warnings:
                continue
            out.append(f"**`{f.relative_to(ROOT)}`**")
            for w in warnings:
                out.append(f"- {w}")
            out.append("")
        out.append("</details>")

    return "\n".join(out)


def run_lint(fmt="text"):
    files = (
        [(f, True) for f in RECIPE_DIR.glob("*.md")]
        + [(f, False) for f in FRONT_DIR.glob("*.md")]
        + [(f, False) for f in BACK_DIR.glob("*.md")]
    )

    results = []
    total_errors = 0
    total_warnings = 0

    for f, is_recipe in files:
        errors, warnings = lint_file(f, is_recipe)
        if errors or warnings:
            results.append((f, errors, warnings))
            total_errors += len(errors)
            total_warnings += len(warnings)

    results.sort(key=lambda x: (len(x[1]) == 0, -len(x[1]), -len(x[2])))

    total_files = len(files)
    files_with_issues = len(results)

    if fmt == "markdown":
        print(render_markdown(results, total_files, total_errors, total_warnings))
    else:
        print(render_text(results, total_files, files_with_issues, total_errors, total_warnings))

    return 1 if total_errors else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["text", "markdown"], default="text")
    args = parser.parse_args()
    sys.exit(run_lint(fmt=args.format))
