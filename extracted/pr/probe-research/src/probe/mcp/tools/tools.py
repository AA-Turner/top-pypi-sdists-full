"""Framework-independent implementation of the read-only MCP operations."""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

from ..generated.sql import MAX_ROWS_CEILING
from ...sdk import errors
from ...shared.reads.search_contract import (
    EnvelopeState,
    MissingMarker)
from ..generated.views import View
from ..delivery.delivery import omit_defaults
from ..source.source import ResearchOSSource
from ...foundation.compose.compose import compose
from probe.mcp.tools.browse import BrowseMixin
from probe.mcp.tools.corpora.docs import DocsSearchMixin
from probe.mcp.tools.entity import GetEntityMixin
from probe.mcp.tools.listing import BrowseListMixin
from probe.mcp.tools.listings.catalog import CatalogRowsMixin
from probe.mcp.tools.listings.files import FileRowsMixin
from probe.mcp.tools.listings.notes import NoteRowsMixin
from probe.mcp.tools.listings.runs import RunRowsMixin
from probe.mcp.tools.listings.workspaces import WorkspaceRowsMixin
from probe.mcp.tools.literature import LiteratureMixin
from probe.mcp.tools.metrics import MetricsMixin
from probe.mcp.tools.search import SearchMixin
from probe.mcp.tools.shaping.shaping import _fit_sections, _tokens
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


def _text(record: dict) -> str:
    fields = [
        record.get("id"),
        record.get("slug"),
        record.get("name"),
        record.get("description"),
        record.get("question"),
        record.get("conclusion"),
        " ".join(record.get("tags") or []),
    ]
    return " ".join(str(value) for value in fields if value).lower()


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
      and `scripts/mcp_budget_bench.py` uses `.get`), and for a model "absent"
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

    def research_context(
        self,
        task: str,
        project_ref: str | None = None,
        session_id: str | None = None,
        token_budget: int = 1800,
    ) -> dict:
        projects = self.source.projects(limit=50)
        project = None
        if project_ref:
            needle = project_ref.lower()
            project = next(
                (
                    item
                    for item in projects
                    if needle
                    in {str(item.get("id", "")).lower(), str(item.get("slug", "")).lower()}
                ),
                None,
            )
        elif len(projects) == 1:
            project = projects[0]
        experiments = self.source.experiments(
            project_id=str(project["id"]) if project else None, limit=30
        )
        terms = set(task.lower().split())
        relevant = sorted(
            experiments,
            key=lambda item: len(terms.intersection(_text(item).split())),
            reverse=True,
        )[:5]
        active_runs: list[dict] = []
        for experiment in relevant[:3]:
            active_runs.extend(
                run
                for run in self.source.runs(experiment_id=str(experiment["id"]), limit=10)
                if run.get("status") in {"created", "running"}
            )
        if project is not None:
            # PROJECT-DIRECT runs (research-os 0054) belong to no experiment, so
            # the sweep above can never see them. direct=True filters server-side
            # (so ten attached runs can't mask an active direct one); the
            # client-side experiment_id filter stays as belt-and-braces, and the
            # SDK's project_id guard raises on a pre-0054 backend that would
            # have returned unscoped rows — degrade to the experiment sweep.
            try:
                direct_runs = self.source.runs(project_id=str(project["id"]), direct=True, limit=10)
            except errors.NotFoundError:
                direct_runs = []
            active_runs.extend(
                run
                for run in direct_runs
                if run.get("status") in {"created", "running"} and not run.get("experiment_id")
            )
        # The separate asset registry is retired: a reusable asset IS an artifact
        # now, so there is no second inventory to fetch and nothing here can be
        # missing on its account.
        missing: list[str] = []

        fixed: dict[str, Any] = {
            "task": task,
            "session_id": session_id,
            "project": project,
            "warnings": [],
        }
        # `missing` is what THIS response lacks, NOT an inventory of everything the
        # backend cannot do. Deriving it from every False capability is what pinned
        # every context envelope to partial forever: portable_snapshots is honestly
        # and permanently False, so `missing` could never be empty and stopped
        # carrying information. Only versioned_assets gates content returned here.
        sections, truncated = _fit_sections(
            [
                ("relevant_experiments", relevant),
                ("active_runs", active_runs[:10]),
                ("projects", [] if project is not None else projects),
            ],
            max(0, token_budget - _tokens(fixed)),
        )
        if truncated:
            missing.append(MissingMarker.TRUNCATED_BY_TOKEN_BUDGET)
        if project is not None:
            sections["projects"] = None
        return self._envelope(
            {**fixed, **sections},
            state=EnvelopeState.PARTIAL if missing else EnvelopeState.COMPLETE,
            missing=missing,
        )

    def query_sql(
        self,
        sql: str | None = None,
        tables: list[str] | None = None,
        token_budget: int = 2000,
    ) -> dict:
        """Read-only SQL, passed straight through: the server already bounds it.

        ``max_rows`` is DERIVED from the delivery budget rather than exposed, so
        the database is not asked for 200 rows the response can only carry 20 of.
        ~20 tokens per row is a deliberate over-estimate of a narrow row; the
        delivery branch in ``continuation`` still trims whatever does not fit.
        """
        max_rows = None if sql is None else max(1, min(MAX_ROWS_CEILING, token_budget // 20))
        return self.source.query_sql(sql=sql, tables=tables, max_rows=max_rows)

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

    def research_compare(
        self,
        refs: list[str],
        dimensions: list[str] | None = None,
    ) -> dict:
        if len(refs) < 2:
            raise ValueError("compare requires at least two refs")
        rows = []
        for ref in refs:
            kind, entity = self.source.get(ref)
            rows.append({"ref": ref, "entity_type": kind, "entity": entity})
        requested = dimensions or ["config", "metadata", "summary", "status", "question"]
        comparison = {
            dimension: [row["entity"].get(dimension) for row in rows] for dimension in requested
        }
        return self._envelope({"entities": rows, "comparison": comparison})
