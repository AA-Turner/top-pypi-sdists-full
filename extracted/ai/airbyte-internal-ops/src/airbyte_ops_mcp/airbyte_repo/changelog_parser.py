# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Pure parsing helpers for connector documentation changelogs."""

from __future__ import annotations

import re


def parse_changelog_entries(
    content: str,
    github_repo: str,
    *,
    allow_prerelease: bool = False,
    allow_pr_cell_text: bool = False,
) -> list[tuple[int, str, str, int, int, str]]:
    """Parse version, date, and first PR link from changelog table rows."""
    version_pattern = (
        r"[0-9]+\.[0-9]+\.[0-9]+(?:-rc\.[0-9]+)?"
        if allow_prerelease
        else r"[0-9]+\.[0-9]+\.[0-9]+"
    )
    row_re = re.compile(
        rf"^\|\s*(?P<version>{version_pattern})\s*\|\s*"
        r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\s*\|\s*"
        r"(?P<pr_cell>.*?)\s*\|\s*(?P<comment>.*?)\s*\|\s*$"
    )
    pr_re = re.compile(
        r"\[?(?P<displayed_pr>[0-9]+)\]?\s*\(https://github\.com/"
        + re.escape(github_repo)
        + r"/pull/(?P<url_pr>[0-9]+)\)"
    )
    entries = []
    for line_num, line in enumerate(content.splitlines(), start=1):
        row_match = row_re.match(line)
        if not row_match:
            continue
        pr_match = (
            pr_re.search(row_match.group("pr_cell"))
            if allow_pr_cell_text
            else pr_re.fullmatch(row_match.group("pr_cell").strip())
        )
        if not pr_match:
            continue
        entries.append(
            (
                line_num,
                row_match.group("version"),
                row_match.group("date"),
                int(pr_match.group("displayed_pr")),
                int(pr_match.group("url_pr")),
                line,
            )
        )
    return entries
