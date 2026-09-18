"""The closed vocabularies of the Block Ledger, declared once.

The database carries the same three sets as CHECK constraints
(`matrx-frontend/migrations/acq_01_a_block_is_a_finding.sql`). They are repeated here — not
duplicated by accident — so a caller gets a Python refusal with a sentence instead of a 23514
from Postgres, and so the screen's facets have a name for every value.

The RUNGS are NOT redeclared: they are imported from `matrx_scraper.ladder`, which the capture
ladder's contract makes the one place they exist
(`common-docs/projects/acquisition-frontier/extension-ladder/CONTRACT.md` §1).
"""

from __future__ import annotations

from matrx_scraper.ladder import RUNGS

__all__ = [
    "ENGINES",
    "ENGINE_LABELS",
    "RUNGS",
    "SOURCE_TYPES",
    "SOURCE_TYPE_LABELS",
    "STATUSES",
    "engine_label",
    "source_type_label",
]

#: WHO tried. An engine is a thing that can be pointed at an input and can fail.
ENGINES: tuple[str, ...] = (
    "scraper",           # rung 1 — plain HTTP fetch + extraction
    "server_browser",    # rung 2 — the pooled Playwright browser on our servers
    "own_browser",       # rung 3 — the person's own logged-in Chrome, via matrx-extend
    "human",             # rung 4 — the person, driving
    "file_reader",       # matrx-files: ebooks, office, video, PDF
    "catalog_adapter",   # media_catalog: YouTube, podcast, blog, slide deck
    "export_reader",     # bring_your_export: a service's own export file
    "connected_account", # Google Workspace, Microsoft Graph, and the rest
)

ENGINE_LABELS: dict[str, str] = {
    "scraper": "Scraper",
    "server_browser": "Server browser",
    "own_browser": "Your own browser",
    "human": "You, driving",
    "file_reader": "File reader",
    "catalog_adapter": "Catalog adapter",
    "export_reader": "Export reader",
    "connected_account": "Connected account",
}

#: WHAT we were trying to get. Broad on purpose: the facet has to stay readable.
SOURCE_TYPES: tuple[str, ...] = (
    "web_page",
    "video_channel",
    "podcast_feed",
    "blog_feed",
    "slide_deck",
    "file",
    "export",
    "connected_account",
    "search",
)

SOURCE_TYPE_LABELS: dict[str, str] = {
    "web_page": "Web page",
    "video_channel": "Video channel",
    "podcast_feed": "Podcast feed",
    "blog_feed": "Blog or feed",
    "slide_deck": "Slide deck",
    "file": "File",
    "export": "Export",
    "connected_account": "Connected account",
    "search": "Search",
}

#: WHAT WE DID about it. `decision` is the one that is not ours to clear: a route that crosses
#: DRM, a paywall, somebody else's login or a bot wall is Arman's call, never an agent's
#: (`HUNTER-RULES.md` law 6).
STATUSES: tuple[str, ...] = (
    "open",
    "retrying",
    "resolved",
    "escalated",
    "decision",
)


def engine_label(engine: str) -> str:
    """The words a non-technical person reads. Unknown engines answer with themselves."""
    return ENGINE_LABELS.get(engine, engine)


def source_type_label(source_type: str) -> str:
    return SOURCE_TYPE_LABELS.get(source_type, source_type)
