"""Changelog / "What's New" builder.

The changelog page is aimed at end users. Entries can come from two sources:

* a local ``CHANGELOG.md`` written in the *Keep a Changelog* format, or
* the GitHub Releases API for a repository (``owner/name``).

The parsed :class:`~.models.ChangelogEntry` list is rendered to a self-contained
HTML page that can be served dynamically or written out as a static file.
"""
from __future__ import annotations

import logging
import re
from datetime import date
from pathlib import Path
from typing import Optional

from .models import ChangelogEntry

logger = logging.getLogger(__name__)

# "## [1.2.3] - 2024-05-01" or "## 1.2.3 - 2024-05-01" or "## [Unreleased]"
_VERSION_RE = re.compile(
    r"^##\s+\[?(?P<version>[^\]\s]+)\]?(?:\s*-\s*(?P<date>\d{4}-\d{2}-\d{2}))?\s*$"
)
# "### Added"
_SECTION_RE = re.compile(r"^###\s+(?P<section>.+?)\s*$")
# "- something" / "* something"
_ITEM_RE = re.compile(r"^\s*[-*]\s+(?P<item>.+?)\s*$")


def parse_keepachangelog(text: str) -> list[ChangelogEntry]:
    """Parse *Keep a Changelog* style markdown into changelog entries.

    Args:
        text: Raw markdown content of a ``CHANGELOG.md`` file.

    Returns:
        Entries in file order (typically newest first).
    """
    entries: list[ChangelogEntry] = []
    current: Optional[ChangelogEntry] = None
    section: Optional[str] = None

    for line in text.splitlines():
        version_match = _VERSION_RE.match(line)
        if version_match:
            current = ChangelogEntry(
                version=version_match.group("version"),
                released_on=(
                    date.fromisoformat(version_match.group("date"))
                    if version_match.group("date")
                    else None
                ),
            )
            entries.append(current)
            section = None
            continue

        if current is None:
            continue

        section_match = _SECTION_RE.match(line)
        if section_match:
            section = section_match.group("section")
            current.sections.setdefault(section, [])
            continue

        item_match = _ITEM_RE.match(line)
        if item_match:
            bucket = section or "Changes"
            current.sections.setdefault(bucket, []).append(item_match.group("item"))

    return [e for e in entries if not e.is_empty]


def _github_body_to_sections(body: str) -> dict[str, list[str]]:
    """Best-effort split of a GitHub release body into sections.

    Falls back to a single ``Changes`` bucket of bullet lines when the body
    contains no ``### Section`` headers.
    """
    sections: dict[str, list[str]] = {}
    section: Optional[str] = None
    for line in (body or "").splitlines():
        section_match = _SECTION_RE.match(line)
        if section_match:
            section = section_match.group("section")
            sections.setdefault(section, [])
            continue
        item_match = _ITEM_RE.match(line)
        if item_match:
            sections.setdefault(section or "Changes", []).append(
                item_match.group("item")
            )
    return sections


class ChangelogBuilder:
    """Load and render changelog entries from a file or GitHub Releases.

    Args:
        source_path: Path to a local ``CHANGELOG.md``.
        github_repo: ``owner/name`` slug to pull releases from GitHub.
        github_token: Optional token to raise the GitHub API rate limit.
        title: Page heading for the rendered HTML.
    """

    def __init__(
        self,
        *,
        source_path: Optional[Path] = None,
        github_repo: Optional[str] = None,
        github_token: Optional[str] = None,
        title: str = "What's New",
    ) -> None:
        self.source_path = Path(source_path) if source_path else None
        self.github_repo = github_repo
        self.github_token = github_token
        self.title = title
        self.logger = logger

    async def load_entries(self) -> list[ChangelogEntry]:
        """Load entries, preferring GitHub Releases then a local file.

        Never raises for missing/unreachable sources — returns an empty list
        and logs instead, so the page always renders.
        """
        if self.github_repo:
            try:
                entries = await self._load_from_github()
                if entries:
                    return entries
            except Exception as err:  # network / parsing best-effort
                self.logger.warning(
                    "Changelog: GitHub source failed (%s); trying local file.", err
                )
        if self.source_path and self.source_path.exists():
            try:
                text = self.source_path.read_text(encoding="utf-8")
                return parse_keepachangelog(text)
            except OSError as err:
                self.logger.warning("Changelog: cannot read %s: %s", self.source_path, err)
        return []

    async def _load_from_github(self) -> list[ChangelogEntry]:
        """Fetch releases from the GitHub API (async, via aiohttp)."""
        import aiohttp

        url = f"https://api.github.com/repos/{self.github_repo}/releases"
        headers = {"Accept": "application/vnd.github+json"}
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, params={"per_page": 30}) as resp:
                resp.raise_for_status()
                releases = await resp.json()
        return [self._release_to_entry(r) for r in releases if not r.get("draft")]

    @staticmethod
    def _release_to_entry(release: dict) -> ChangelogEntry:
        """Convert one GitHub release payload into a :class:`ChangelogEntry`."""
        published = release.get("published_at")
        released_on: Optional[date] = None
        if published:
            try:
                released_on = date.fromisoformat(published[:10])
            except ValueError:
                released_on = None
        return ChangelogEntry(
            version=release.get("tag_name") or release.get("name") or "unreleased",
            title=release.get("name") or "",
            url=release.get("html_url") or "",
            released_on=released_on,
            sections=_github_body_to_sections(release.get("body") or ""),
        )

    def render_html(self, entries: list[ChangelogEntry]) -> str:
        """Render the entries to a self-contained HTML page."""
        from .templates import render_changelog

        return render_changelog(self.title, entries)
