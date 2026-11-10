"""ResearchReadService: the read-only MCP tools composed from their reads/ and views/ mixins, and the
envelope every tool answers in."""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

from ...sdk import errors
from ...shared.reads.search_contract import EnvelopeState
from ..generated.views import View
from ..delivery.delivery import omit_defaults
from ..source.source import ResearchOSSource
from ...foundation.compose.compose import compose
from probe.mcp.tools.corpora.docs import DocsSearchMixin
from probe.mcp.tools.reads.browse import BrowseMixin
from probe.mcp.tools.reads.compare import CompareMixin
from probe.mcp.tools.reads.context import ContextMixin
from probe.mcp.tools.reads.entity import GetEntityMixin
from probe.mcp.tools.reads.listing import BrowseListMixin
from probe.mcp.tools.reads.listings.catalog import CatalogRowsMixin
from probe.mcp.tools.reads.listings.files import FileRowsMixin
from probe.mcp.tools.reads.listings.notes import NoteRowsMixin
from probe.mcp.tools.reads.listings.runs import RunRowsMixin
from probe.mcp.tools.reads.listings.workspaces import WorkspaceRowsMixin
from probe.mcp.tools.reads.literature import LiteratureMixin
from probe.mcp.tools.reads.samples import SamplesToolMixin
from probe.mcp.tools.reads.metrics import MetricsMixin
from probe.mcp.tools.reads.search import SearchMixin
from probe.mcp.tools.reads.sql import SqlMixin
from probe.mcp.tools.view import _VIEWS, _VIEW_OPTIONS, _views_offered
from probe.mcp.tools.views.branches import BranchesViewsMixin
from probe.mcp.tools.views.catalog import CatalogViewsMixin
from probe.mcp.tools.views.code import CodeViewsMixin
from probe.mcp.tools.views.files import FileViewsMixin
from probe.mcp.tools.views.lineage import LineageViewsMixin
from probe.mcp.tools.views.notes import NotesViewsMixin
from probe.mcp.tools.views.overview import OverviewViewsMixin
from probe.mcp.tools.views.runs import RunViewsMixin
from probe.mcp.tools.views.sessions import SessionsViewsMixin


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _compact(envelope: dict) -> dict:
    """Strip envelope bookkeeping an agent does not reason over.

    The reader is a model, not code, so ABSENCE IS THE CONTRACT: a key appears
    only when it says something (see `continuation.omit_defaults`, which the
    delivery layer applies again to what it builds). What is KEPT and why is
    the interesting half -- a drop-list without one rots into dropping
    something load-bearing:

    - `completeness` survives whenever it is not complete-with-nothing-missing.
      It is the only field that says what the response could not cover, and
      stripping a partial one would turn it into a confident answer. A complete
      one used to ride every call -- every ROW of an `entity` batch -- saying
      "nothing to see here" ahead of the content.
    - `next_cursor` survives when there is a next page. It used to be emitted
      null too, so code doing `page["next_cursor"]` would not KeyError on the
      last page; no code reads this wire (the daemon's reader is a model too,
      and `scripts/benches/mcp_budget_bench.py` uses `.get`), and for a model "absent"
      and "null" are the same instruction: stop.
    - `capabilities` goes. `source.capabilities()` is STATIC for the hosted
      backend, so the map is constant per release like `scope`/`as_of`/
      `schema_version` -- and its one False flag (`portable_snapshots`, "not
      yet") rode every read of every entity. A capability that fails at call
      time says so where the caller can act: a `completeness.missing` marker
      (`web_search`, `semantic_search`, ...) on that response. `verbose=True`
      still returns the map.
    - `scope`, `as_of`, `schema_version` go. They are constant per token and per
      release; re-sending them on every call costs context and tells the agent
      nothing it can act on.
    - `evidence` goes when empty, stays when populated.
    """
    return omit_defaults(
        {
            "data": envelope["data"],
            "completeness": envelope["completeness"],
            "next_cursor": envelope.get("next_cursor"),
            "evidence": envelope.get("evidence"),
        }
    )


@compose
class ResearchReadService(
    BrowseMixin,
    BrowseListMixin,
    RunRowsMixin,
    CatalogRowsMixin,
    NoteRowsMixin,
    WorkspaceRowsMixin,
    FileRowsMixin,
    LiteratureMixin,
    SearchMixin,
    DocsSearchMixin,
    GetEntityMixin,
    MetricsMixin,
    RunViewsMixin,
    FileViewsMixin,
    NotesViewsMixin,
    BranchesViewsMixin,
    CodeViewsMixin,
    OverviewViewsMixin,
    LineageViewsMixin,
    SessionsViewsMixin,
    CatalogViewsMixin,
    ContextMixin,
    SqlMixin,
    CompareMixin,
    SamplesToolMixin,
):
    """Compact, provenance-bearing read model exposed through MCP."""

    def __init__(self, source: ResearchOSSource):
        self.source = source

    @property
    def _api_base_url(self) -> str | None:
        """API origin this service actually calls, for deriving dashboard links.

        Read off the live client rather than re-resolving config: the server
        builds one source per token with an explicit base URL, and a second
        resolution could name a different host than the one being read from --
        which would mint links into the wrong deployment.
        """
        client = getattr(self.source, "client", None)
        settings = getattr(client, "settings", None)
        return getattr(settings, "base_url", None)

    def _envelope(
        self,
        data: Any,
        *,
        evidence: list[dict] | None = None,
        state: str = EnvelopeState.COMPLETE,
        missing: list[str] | None = None,
        next_cursor: str | None = None,
        verbose: bool = False,
    ) -> dict:
        """The MCP wire shape. COMPACT BY DEFAULT.

        This default used to be True, and the result was that a tool got the
        lean envelope only if it remembered to ask: `search` and
        `get_entity` passed `verbose=False`, and the other five tools --
        `browse_research`, `read_metrics` and the three metric aliases -- shipped
        `schema_version`, `as_of`, `scope` and all seven capability flags (six of
        them True) in front of their answer on EVERY call. None of that is readable by the
        agent as anything it can act on, and it is ~350 characters ahead of the
        first byte of data, which is what a person watching the tool scroll past
        actually sees.

        Opt-OUT is the right polarity because the compact shape is the contract
        (`_compact` keeps every field that carries signal); verbose is the
        debugging affordance. A new tool added here is then quiet by default
        instead of noisy until someone notices.
        """
        identity = self.source.identity()
        envelope = {
            "schema_version": "1.0",
            "as_of": _now(),
            "scope": {
                "customer_id": identity.get("customer_id"),
                "researcher": identity.get("email") or identity.get("user_id"),
            },
            "capabilities": self.source.capabilities(),
            "data": data,
            "evidence": evidence or [],
            "completeness": {"state": state, "missing": missing or []},
            "next_cursor": next_cursor,
        }
        return envelope if verbose else _compact(envelope)

    def _checked_view(self, kind: str, view: str) -> str:
        """The view must EXIST for this kind. Rejecting loudly beats the old
        behavior — an unknown view used to fall through to a card-shaped payload,
        and contract/versions/usage returned an envelope that always said
        `missing`, which reads as "temporarily degraded" rather than "not a
        thing". The error names what this kind actually supports."""
        if (kind, view) in _VIEWS:
            return view
        raise errors.ValidationError(
            f"view={view!r} is not available for a {kind}; {kind} supports:\n"
            f"{_views_offered(kind)}",
            status=422,
        )

    def _checked_view_options(
        self, kind: str, view: str, filters: dict[str, Any] | None
    ) -> dict[str, Any]:
        # The WIRE name is `view_options` (server.py); inside the service the bag
        # is still `filters`, and every view echoes it under that key. Renaming
        # the echoed payload key is a response-shape change for its own PR.
        # Empty values are dropped, not passed through: `{"key": ""}` is not a
        # filter. Kept, it would echo back in the payload as though it had been
        # applied while every truthiness check downstream ignored it.
        supplied = {
            key: value
            for key, value in (filters or {}).items()
            if view == View.RECORD or (value is not None and value != "")
        }
        allowed = _VIEW_OPTIONS.get((kind, view), set())
        unknown = sorted(set(supplied) - allowed)
        if not unknown:
            return supplied
        detail = (
            f"view={view!r} on a {kind} accepts no view options"
            if not allowed
            else f"supported view options for view={view!r} on a {kind}: {sorted(allowed)}"
        )
        raise errors.ValidationError(f"unknown view option(s) {unknown}: {detail}", status=422)
