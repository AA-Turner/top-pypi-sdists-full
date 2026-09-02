"""Kinds for the client-tool LOADER results (KIND_TOOL_LEDGER, ``lead-w2d``).

``load_chrome_tools`` and ``load_desktop_tools`` are the discovery loaders that
queue client-executed tool subsets into the active toolset. They are TWO kinds,
not one: the chrome loader reports tools LOADED now (registered references with
their filters), the desktop loader reports tools QUEUED for the turn-boundary
drain — different facts with different receipt fields, and papering over that
with a shared shape would hide which promise was made.

Each loader has a short-circuit "already loaded" branch that returns the same
shape with the ``already_loaded``/``message`` fields set — union rule, optional
fields, one kind per tool.

PLACEHOLDER tier: the receipts are lists of our own tool names.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind

_FAMILY = "tooling"


@kind(
    "chrome_tools_load_result",
    label="Chrome Tools Loaded",
    family=_FAMILY,
    example={
        "category": "page",
        "tools_loaded": ["read_page", "find"],
        "count": 2,
        "missing_from_catalog": [],
        "skipped_admin_only": [],
        "skipped_missing_permission": [],
        "skipped_desktop_unavailable": [],
        "already_loaded": None,
        "message": None,
    },
    maturity="placeholder",
)
class ChromeToolsLoadResult(KindModel):
    """``load_chrome_tools`` receipt — what was loaded for the category, and
    exactly why each filtered candidate was skipped."""

    category: str = ""
    tools_loaded: list[str] = []
    count: int = 0
    #: tools in the category routing with no registry entry (data integrity
    #: error, reported rather than hidden).
    missing_from_catalog: list[str] = []
    skipped_admin_only: list[str] = []
    skipped_missing_permission: list[str] = []
    skipped_desktop_unavailable: list[str] = []
    #: short-circuit branch only.
    already_loaded: bool | None = None
    message: str | None = None


@kind(
    "desktop_tools_load_result",
    label="Desktop Tools Queued",
    family=_FAMILY,
    example={
        "category": "files",
        "tools_queued": ["local_file"],
        "queued_count": 1,
        "skipped_policy": [],
        "skipped_platform": [],
        "already_loaded": None,
        "message": None,
    },
    maturity="placeholder",
)
class DesktopToolsLoadResult(KindModel):
    """``load_desktop_tools`` receipt — queued INTENT for the turn-boundary
    drain (the drain's RESOURCE_CHANGED event reports the applied delta)."""

    category: str = ""
    tools_queued: list[str] = []
    queued_count: int = 0
    skipped_policy: list[str] = []
    skipped_platform: list[str] = []
    #: short-circuit branch only.
    already_loaded: bool | None = None
    message: str | None = None
