#!/usr/bin/env python3
"""Render the .prs/ review files as a verdict-grouped markdown table.

Reads every ``.prs/<number>.md`` review file (ignoring ``.reply.md`` drafts),
extracts the header fields and the summary paragraph, and prints one table per
verdict group. Pure extraction - no network access, no inference.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

VERDICT_ORDER = ["GO", "NO-GO", "NEEDS-DISCUSSION"]
SUMMARY_MAX = 200

TITLE_RE = re.compile(r"^# PR #\d+ - (.*)$")
AUTHOR_RE = re.compile(r"^\*\*Author:\*\* (.*)$")
UPDATED_RE = re.compile(r"^\*\*PR Updated:\*\* (.*)$")
VERDICT_RE = re.compile(r"^## Verdict: (.*)$")


class Review:
    def __init__(self, number: int, title: str, author: str, updated: str, verdict: str, note: str):
        self.number = number
        self.title = title
        self.author = author
        self.updated = updated
        self.verdict = verdict
        self.note = note


def prs_dir() -> Path:
    root = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()
    return Path(root) / ".prs"


def first_match(lines: list[str], pattern: re.Pattern[str]) -> str:
    for line in lines:
        m = pattern.match(line)
        if m:
            return m.group(1).strip()
    return ""


def extract_summary(lines: list[str]) -> str:
    collecting = False
    summary: list[str] = []
    for line in lines:
        if VERDICT_RE.match(line):
            collecting = True
            continue
        if collecting:
            if line.startswith("#"):
                break
            summary.append(line)
    text = " ".join(part.strip() for part in summary if part.strip())
    text = re.sub(r"\s+", " ", text)
    if len(text) > SUMMARY_MAX:
        text = text[:SUMMARY_MAX].rsplit(" ", 1)[0] + "…"
    return text


def parse(path: Path) -> Review | None:
    lines = path.read_text().splitlines()
    verdict = first_match(lines, VERDICT_RE)
    if not verdict:
        return None
    return Review(
        number=int(path.stem),
        title=first_match(lines, TITLE_RE),
        author=first_match(lines, AUTHOR_RE),
        updated=first_match(lines, UPDATED_RE),
        verdict=verdict,
        note=extract_summary(lines),
    )


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def date_only(timestamp: str) -> str:
    return timestamp.split("T", 1)[0]


def render(reviews: list[Review]) -> str:
    by_verdict: dict[str, list[Review]] = {v: [] for v in VERDICT_ORDER}
    other: list[Review] = []
    for review in reviews:
        by_verdict.get(review.verdict, other).append(review)

    out: list[str] = ["# PR Review Summary", ""]
    for verdict in VERDICT_ORDER:
        group = sorted(by_verdict[verdict], key=lambda r: r.number)
        out.append(f"## {verdict} ({len(group)})")
        out.append("")
        if not group:
            out.append("_None._")
            out.append("")
            continue
        out.append("| ID | Title | Author | Last Update | Note / Blocker / Question |")
        out.append("| --- | --- | --- | --- | --- |")
        for r in group:
            out.append(
                f"| #{r.number} | {cell(r.title)} | @{cell(r.author)} | "
                f"{date_only(r.updated)} | {cell(r.note)} |"
            )
        out.append("")

    if other:
        out.append("## Unrecognised verdict")
        out.append("")
        for r in sorted(other, key=lambda r: r.number):
            out.append(f"- #{r.number} ({r.verdict})")
        out.append("")

    return "\n".join(out)


def main() -> int:
    directory = prs_dir()
    reviews: list[Review] = []
    for path in sorted(directory.glob("[0-9]*.md")):
        if path.name.endswith(".reply.md"):
            continue
        review = parse(path)
        if review is not None:
            reviews.append(review)

    if not reviews:
        print(f"No review files found in {directory}", file=sys.stderr)
        return 1

    print(render(reviews))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
