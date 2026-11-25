"""The versions of myOrb with what each changed, from its releases on GitHub: opened from the
version under the welcome screen.

A release does not change once it is made, so the notes are read once for each version myOrb
runs (at its start, after an upgrade) and kept in the data directory; read again only when
reading them failed.

When each version first started on this server is kept there too (started.json), so the list
says when it came to run here, not only when it was released.
"""

import html
import json
import logging
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import httpx2
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse, Response

from myorb import __version__

logger = logging.getLogger(__name__)

router = APIRouter()

RELEASES = "https://api.github.com/repos/eriktelepovsky/myorb/releases"
RELEASES_PAGE = "https://github.com/eriktelepovsky/myorb/releases"
FEED = RELEASES_PAGE + ".atom"
ATOM = "{http://www.w3.org/2005/Atom}"
# After GitHub could not be read, asked again only this long after (seconds).
RETRY = 15 * 60
SHOWN = 30
# "* Title by @someone in https://github.com/…/pull/146"
CHANGE = re.compile(r"^\*\s+(?P<title>.+?)(?:\s+by\s+@\S+)?(?:\s+in\s+(?P<url>https://\S+))?\s*$")
# A change that only says the version moved on says nothing.
ONLY_VERSION = re.compile(r"^version\s+\d+(\.\d+)*$", re.I)


def changes(body: str) -> list[dict[str, str]]:
    """A release's changes, from the notes GitHub writes: each pull request's title and link."""
    found = []
    for line in (body or "").splitlines():
        match = CHANGE.match(line.strip())
        if match and not ONLY_VERSION.match(match["title"].strip()):
            found.append({"title": match["title"].strip(), "url": match["url"] or ""})
    return found


def _parsed(data: list[Any]) -> list[dict[str, Any]]:
    return [
        {
            "version": str(r.get("tag_name", "")).removeprefix("v"),
            "published": r.get("published_at") or "",
            "url": r.get("html_url", ""),
            "changes": changes(r.get("body", "")),
        }
        for r in data
        if isinstance(r, dict) and not r.get("draft")
    ]


def _file(app: FastAPI) -> Path:
    return app.state.settings.data_dir / "releases.json"


def _stored(app: FastAPI) -> dict[str, Any] | None:
    try:
        return json.loads(_file(app).read_text())
    except (OSError, ValueError):
        return None


async def _feed(app: FastAPI) -> list[dict[str, Any]] | None:
    """The newest releases from GitHub's Atom feed of them, which is not counted against the
    API's limit for unsigned requests (60 an hour for the address, shared with whatever else
    asks from it). None when it could not be read."""
    try:
        response = await app.state.http.get(FEED, timeout=10)
        response.raise_for_status()
        return feed_releases(response.text)
    except (httpx2.HTTPError, ElementTree.ParseError) as error:
        logger.warning("Reading the release feed from GitHub failed: %s", error)
        return None


def feed_releases(text: str) -> list[dict[str, Any]]:
    """Releases from the Atom feed: its entries' titles (tags), times, links, and the changes
    in their HTML notes."""
    found = []
    for entry in ElementTree.fromstring(text).iter(f"{ATOM}entry"):
        link = entry.find(f"{ATOM}link")
        found.append(
            {
                "version": (entry.findtext(f"{ATOM}title") or "").strip().removeprefix("v"),
                "published": entry.findtext(f"{ATOM}updated") or "",
                "url": link.get("href", "") if link is not None else "",
                "changes": html_changes(entry.findtext(f"{ATOM}content") or ""),
            }
        )
    return [r for r in found if r["version"]]


def html_changes(notes: str) -> list[dict[str, str]]:
    """The changes in a release's notes as HTML: each item's title and pull request link."""
    found = []
    for item in re.findall(r"<li>(.*?)</li>", notes, re.S):
        pulls = re.findall(r'href="(https://github\.com/[^"]+/pull/\d+)"', item)
        text = html.unescape(re.sub(r"<[^>]+>", "", item)).strip()
        title = re.sub(r"\s+by\s+@\S+(?:\s+in\s+\S+)?\s*$", "", text).strip()
        if title and not ONLY_VERSION.match(title):
            found.append({"title": title, "url": pulls[-1] if pulls else ""})
    return found


async def fetch(app: FastAPI) -> list[dict[str, Any]] | None:
    """The release notes, kept for the running version; read from GitHub when there are none
    for it yet: from its API, else its feed. None when they were never read. After both fail,
    not asked again for a while: the API's limit, once spent, would only stay spent."""
    stored = _stored(app)
    kept = stored["releases"] if stored else None
    if stored and stored.get("version") == __version__:
        return kept
    if time.monotonic() < getattr(app.state, "releases_retry", 0):
        return kept
    try:
        response = await app.state.http.get(
            RELEASES,
            params={"per_page": SHOWN},
            headers={"Accept": "application/vnd.github+json"},
            timeout=10,
        )
        response.raise_for_status()
        found = _parsed(response.json())
    except (httpx2.HTTPError, ValueError) as error:
        logger.warning("Reading the release notes from GitHub failed: %s", error)
        newest = await _feed(app)
        if newest is None:
            app.state.releases_retry = time.monotonic() + RETRY
            return kept
        # The feed has only the newest ten: the older ones kept stay below them.
        versions = {r["version"] for r in newest}
        found = newest + [r for r in kept or [] if r["version"] not in versions]
    # Kept for this version once it is among them; else read again next time.
    has_running = any(r["version"] == __version__ for r in found)
    try:
        _file(app).write_text(
            json.dumps({"version": __version__ if has_running else "", "releases": found})
        )
    except OSError:
        logger.exception("Keeping the release notes failed")
    return found


def _started_file(app: FastAPI) -> Path:
    return app.state.settings.data_dir / "started.json"


def started(app: FastAPI) -> dict[str, str]:
    """When each version first started here: {"0.92.0": "2026-11-24T10:02:00+00:00"}."""
    try:
        found = json.loads(_started_file(app).read_text())
    except (OSError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


def mark_started(app: FastAPI, now: datetime | None = None) -> None:
    """Notes that the running version started, the first time it does: a restart of the same
    version (a deploy of something else) keeps the time it came."""
    known = started(app)
    if __version__ in known:
        return
    known[__version__] = (now or datetime.now(UTC)).isoformat()
    try:
        _started_file(app).write_text(json.dumps(known))
    except OSError:
        logger.exception("Keeping when the version started failed")


def _dated(release: dict[str, Any], since: dict[str, str]) -> dict[str, Any]:
    published = release.get("published")
    date = datetime.fromisoformat(published.replace("Z", "+00:00")) if published else None
    here = since.get(release["version"])
    return {**release, "date": date, "started": datetime.fromisoformat(here) if here else None}


@router.get("/releases", response_class=HTMLResponse)
async def release_notes(request: Request) -> Response:
    found = await fetch(request.app)
    since = started(request.app)
    # The running version is always there, with when it started, if not what it changed.
    shown = list(found or [])
    if not any(r["version"] == __version__ for r in shown):
        shown.insert(
            0,
            {
                "version": __version__,
                "published": "",
                "url": f"{RELEASES_PAGE}/tag/v{__version__}",
                "changes": [],
            },
        )
    return request.app.state.templates.TemplateResponse(
        request,
        "releases.html",
        {
            "releases": [_dated(r, since) for r in shown],
            "unread": found is None,
            "running": __version__,
            "running_since": datetime.fromisoformat(since[__version__])
            if __version__ in since
            else None,
            "releases_page": RELEASES_PAGE,
        },
    )
