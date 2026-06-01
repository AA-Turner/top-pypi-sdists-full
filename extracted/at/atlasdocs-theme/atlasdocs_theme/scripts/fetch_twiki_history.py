from __future__ import annotations

"""
TWiki revision history utilities.

Converts TWiki page revision records (from pages_history_lut.json) into the
same Commit format used by fetch_git_history, so TWiki history and git history
can be merged and sorted together in a single timeline.
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

# Base URL for constructing TWiki revision links
TWIKI_BASE_URL = "https://twiki.cern.ch/twiki/bin/view"

# TWiki web names checked when parsing page identifiers (most specific first)
TWIKI_KNOWN_WEBS = ["AtlasProtected", "AtlasComputing", "AtlasArchive", "Atlas"]

# Default web when no known prefix is found
TWIKI_DEFAULT_WEB = "Atlas"

# Default path to the TWiki page history lookup table
TWIKI_HISTORY_LUT = Path("docs/twikiregistry/pages_history_lut.json")

# How far back to include TWiki revisions (days)
TWIKI_HISTORY_WINDOW_DAYS = 2 * 365

# Date format used in pages_history_lut.json
TWIKI_DATE_FORMAT = "%Y-%m-%d - %H:%M"


# ── Fetch ──────────────────────────────────────────────────────────────────────

def extract_twiki_web_and_page(twiki_ancestor: str) -> tuple[str, str]:
    """Parse a TWiki page identifier into (web, page_name).

    Examples:
        "view_AtlasProtected_Foo.html" → ("AtlasProtected", "Foo")
        "view_Atlas_Bar.html"          → ("Atlas", "Bar")
        "view_Unknown.html"            → ("Atlas", "Unknown")
    """
    content = twiki_ancestor.replace("view_", "").replace(".html", "")
    for web in TWIKI_KNOWN_WEBS:
        if content.startswith(web + "_"):
            return web, content[len(web) + 1:]
    return TWIKI_DEFAULT_WEB, content


def convert_twiki_revision_to_commit(twiki_ancestor: str, revision: dict) -> dict:
    """Convert a TWiki revision record into the Commit TypedDict format.

    Args:
        twiki_ancestor: TWiki page identifier (e.g. "view_AtlasComputing_Foo.html")
        revision:       Dict with keys: revision, date, username
    """
    web, page_name = extract_twiki_web_and_page(twiki_ancestor)

    date_str = revision.get("date", "")
    try:
        iso_date = datetime.strptime(date_str, TWIKI_DATE_FORMAT).isoformat() + "Z"
    except Exception:
        iso_date = date_str

    rev_num = revision.get("revision", "")
    username = revision.get("username", "Unknown")
    twiki_link = f"{TWIKI_BASE_URL}/{web}/{page_name}?rev={rev_num}"

    return {
        "sha": f"rev{rev_num}",
        "author": username,
        "email": "",
        "date": iso_date,
        "message": f"Edit made on Twiki - [view revision {rev_num}]({twiki_link})",
    }


def append_twiki_history(
    result: dict,
    lut_path: str | Path = TWIKI_HISTORY_LUT,
) -> dict:
    """Append TWiki revisions (last TWIKI_HISTORY_WINDOW_DAYS days) to result["meta"].

    Does nothing if result["meta"]["twiki_ancestor"] is not set.
    Revisions are appended to result["meta"]["twiki_recent_revisions"] in Commit format.
    """
    twiki_ancestor = result.get("meta", {}).get("twiki_ancestor")
    if not twiki_ancestor:
        return result

    try:
        with open(lut_path, "r", encoding="utf-8") as f:
            pages_history: dict = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"[twiki_history] Could not read {lut_path}: {exc}")
        return result

    history = pages_history.get(twiki_ancestor, [])
    cutoff = datetime.now(timezone.utc) - timedelta(days=TWIKI_HISTORY_WINDOW_DAYS)

    converted: list[dict] = []
    for rev in history:
        try:
            rev_date = datetime.strptime(
                rev.get("date", ""), TWIKI_DATE_FORMAT
            ).replace(tzinfo=timezone.utc)
            if rev_date >= cutoff:
                converted.append(convert_twiki_revision_to_commit(twiki_ancestor, rev))
        except Exception:
            pass

    result.setdefault("meta", {}).setdefault("twiki_recent_revisions", []).extend(converted)
    return result
