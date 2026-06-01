#!/usr/bin/env python3
"""Extract the CHANGELOG.md section for a given release tag.

Usage:
    python scripts/extract_changelog_section.py v0.1.125

Prints the section from `## [0.1.125] — <date>` (inclusive) through the
heading line of the next `## [` release (exclusive). Exits 1 if the
section is not found — used by the post-release-triage workflow to
prepend a "What's new" block above the deterministic triage output, so
the GitHub Release page describes what shipped, not just that it shipped
cleanly (#328 follow-up).

The CHANGELOG format follows Keep a Changelog loosely; sections start
with `## [VERSION]` (no `v` prefix). The tag may be passed with or
without the `v` prefix.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def extract_section(changelog_text: str, tag: str) -> str:
    """Return the CHANGELOG section for `tag`, or empty string if missing."""
    version = tag.lstrip("v")
    # Match `## [<version>]` at the start of a line; capture through the
    # next `## [` heading (exclusive) or end-of-file.
    pattern = rf"^(## \[{re.escape(version)}\][^\n]*\n.*?)(?=^## \[|\Z)"
    match = re.search(pattern, changelog_text, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).rstrip() + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <tag>", file=sys.stderr)
        return 2
    tag = sys.argv[1]
    changelog_path = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
    if not changelog_path.is_file():
        print(f"error: CHANGELOG.md not found at {changelog_path}", file=sys.stderr)
        return 1
    text = changelog_path.read_text(encoding="utf-8")
    section = extract_section(text, tag)
    if not section:
        print(f"error: no CHANGELOG section for tag {tag!r}", file=sys.stderr)
        return 1
    sys.stdout.write(section)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
