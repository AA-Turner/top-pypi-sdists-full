"""lineage views: a run's parents and reads, a file's writer, a project's or experiment's own links and children."""

from __future__ import annotations
from typing import Any
from ....foundation.compat.compat import StrEnum
from ....sdk import errors
from . import branch_projection as _branches
from ....shared.reads.search_contract import MissingMarker
from probe.mcp.tools.shaping.cards import _card_text
from probe.mcp.tools.shaping.session_work import _names_session_work
from probe.mcp.tools.shaping.shaping import _budget_cost
from probe.mcp.tools.view import _Req, _ViewData

#: The run -> run family, spelled literally rather than imported.
#: (Mirrors `app.lineage.schemas.GENEALOGY_RELATIONS`, a module the MCP cannot
#: import -- same reason `_CAPTURED_AGENTS` is spelled out in `accounting.py`.
#: Deliberately NOT read from `probe.models.LineageRelation` either: that file is
#: a build artifact of `make regen`, and this filter must hold on an install whose
#: regen has not run yet.)
#: Genealogy is reported under `run_ancestry`; letting it into `edges` too would
#: report every retry twice.
_GENEALOGY_RELATIONS = frozenset({"forked_from", "resumed_from", "retried_from", "branched_from"})

#: What a lineage read says to a server without the read routes (0255).
_NO_READ_LINEAGE = (
    "this server does not record what runs read yet (it lacks the run_inputs "
    "feature): file readers and the upstream walk need a newer server"
)

#: Links a project or experiment `lineage` view shows per list on its first
#: page (`built_on`, `used_by`, an experiment's `run_edges`). They are the fixed
#: part of a view whose rows are its children, so each list is a glance: at most
#: this many, fewer when they would take more than `_LINEAGE_LINKS_SHARE` of the
#: budget, its `total` kept and `view_options.links` paging the whole list.
_LINEAGE_LINKS_GLANCE = 10
#: The share of `token_budget` the glance may take; the rest pages children.
_LINEAGE_LINKS_SHARE = 0.5
#: Links among an experiment's runs and files read for `view_options.links=
#: run_edges`: the edges route's own ceiling (`limit` 1-1000).
_LINEAGE_RUN_EDGES_MAX = 1000
#: A link's stored `reason`, as the first page's glance shows it.
_LINK_REASON_CHARS = 200
#: The end type a lineage read names a paper with: no `entity` kind.
_PAPER_END = "paper"


class _LineageLinks(StrEnum):
    """`view_options.links` on a project or experiment lineage view: which of
    its link lists to page in full as the rows."""

    BUILT_ON = "built_on"
    USED_BY = "used_by"
    #: An experiment's only: the links among its own runs and files.
    RUN_EDGES = "run_edges"


def _end_ref(end_type: Any, end_id: Any, end: dict | None) -> dict:
    """A link's far end as `entity` takes it: `kind:slug` and its name, from
    the lineage read's `ends` (swarm friction P6); `kind:<uuid>` for a slug past
    what `entity` takes, and the edge's own end type, unnamed, when the read did
    not name it (an older server). A paper is no `entity` kind, so a paper end
    is its `paper_id` and title, never a ref `entity` would refuse."""
    kind = (end or {}).get("type") or end_type
    out: dict[str, Any]
    if kind == _PAPER_END:
        out = {"paper_id": end_id}
    else:
        slug = (end or {}).get("slug")
        ref = f"{kind}:{slug}"
        out = {"ref": ref if slug and len(ref) <= _branches.MAX_REF_CHARS else f"{kind}:{end_id}"}
    if end and end.get("name"):
        out["name"] = end["name"]
    return out


def _lineage_link(
    edge: dict, *, outgoing: bool, ends: dict[str, dict], reason_chars: int | None
) -> dict:
    """One of a project's or experiment's OWN links, compact: the far end
    named, the relation, how it is known, its reason and date. `edge_id` only
    on a stored link (a derived one has no row); a derived one carries how many
    runs and files it was derived from instead. `reason_chars` cuts the reason
    for the first page's glance (`reason_truncated`); paged rows carry it whole
    (the server keeps at most 500 characters)."""
    end_type, end_id = (
        (edge.get("target_type"), edge.get("target_id"))
        if outgoing
        else (edge.get("source_type"), edge.get("source_id"))
    )
    out: dict[str, Any] = {
        **_end_ref(end_type, end_id, ends.get(str(end_id).lower())),
        "relation": edge.get("relation"),
    }
    if edge.get("provenance"):
        out["provenance"] = edge["provenance"]
    if edge.get("derived"):
        out["derived"] = True
        meta = edge.get("meta") if isinstance(edge.get("meta"), dict) else {}
        for key in ("runs", "files"):
            if meta.get(key) is not None:
                out[key] = meta[key]
    if reason_chars is None:
        if edge.get("reason"):
            out["reason"] = edge["reason"]
    else:
        _card_text(out, edge, "reason", reason_chars)
    if edge.get("created_at"):
        out["at"] = _branches.minute(edge["created_at"])
    if edge.get("id"):
        out["edge_id"] = edge["id"]
    return out


def _among_link(edge: dict) -> dict:
    """One link among an experiment's runs and files, compact: both ends as
    typed ids (the edges route names neither), the relation, how it is known,
    and a stored link's `edge_id` (what `probe edge remove` takes)."""
    out: dict[str, Any] = {
        "from": f"{edge.get('source_type')}:{edge.get('source_id')}",
        "relation": edge.get("relation"),
        "to": f"{edge.get('target_type')}:{edge.get('target_id')}",
    }
    if edge.get("provenance"):
        out["provenance"] = edge["provenance"]
    if edge.get("derived"):
        out["derived"] = True
    if edge.get("id"):
        out["edge_id"] = edge["id"]
    return out


class LineageViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _view_run_lineage(self, entity: dict, request: _Req) -> _ViewData:
        """Both lineage relations, under distinct keys.

        `run_ancestry` is the `parent_run_id` walk -- fork/retry parentage,
        run-to-run. `edges` is the artifact / asset-version provenance graph.
        They answer different questions and this view used to return only the
        first, which made `ancestors: [] / descendants: []` the answer for a run
        that consumed a dataset version and produced three artifacts. An agent
        reads that as "this run has no lineage", a confident wrong answer.

        Deliberately NOT merged into one list: they are different relation types
        over different endpoint kinds, and flattening them recreates exactly the
        ambiguity that made the empty response unreadable.

        That separation is why `edges` FILTERS OUT the genealogy relations. Server
        0166 moved run -> run parentage into `lineage_edges` as
        `retried_from`/`forked_from`/`resumed_from`/`branched_from`, so without this
        filter every retry would arrive under BOTH keys -- the same edge counted
        twice, which is the exact ambiguity the split above exists to prevent.
        `run_ancestry` remains the single home for the parent CHAIN (every
        genealogy parent, both directions); `origin` (lineage plan 2, L18) is the
        one-line answer to "what did this run come from" -- its first parent,
        else what it built on, else its container.
        """
        run_id = str(entity["id"])
        edges = [
            edge
            for edge in self.source.run_edges(run_id)
            if str(edge.get("relation") or "") not in _GENEALOGY_RELATIONS
        ]
        ancestry = dict(self.source.lineage(run_id))
        payload: dict[str, Any] = {}
        # Lineage plan 2 (L18): where the run came from, derived by the server
        # -- its first parent, else what it built on, else its group, its
        # experiment or project, else `unfiled`. Lifted out of the ancestry read
        # so every lineage view answers "where did this come from" under one key.
        if "origin" in ancestry:
            payload["origin"] = ancestry.pop("origin")
        payload["run_ancestry"] = ancestry
        payload["edges"] = edges
        # `view_options.depth` (1-5): the upstream walk -- what this run built
        # on, N hops back, across parents, runs it built on and the runs that
        # made what it used (0255). "What produced this number?" is this walk
        # from the run that logged it. Edges carry `provenance` (observed_call /
        # inferred / human), so a guess never reads like an observation.
        depth = request.filters.get("depth")
        if depth is not None:
            try:
                depth = max(1, min(int(depth), 5))
            except (TypeError, ValueError):
                raise errors.ValidationError(
                    "view_options.depth must be an integer from 1 to 5", status=422
                ) from None
            payload["upstream"] = (
                self.source.run_upstream(run_id, depth)
                if self.source.server_records_reads()
                else {"unsupported": _NO_READ_LINEAGE}
            )
        return _ViewData(payload=payload)

    def _view_artifact_lineage(self, entity: dict, request: _Req) -> _ViewData:
        """Which run WROTE this file (or only carried it: its start snapshot
        copied it in, or a script logged an input) and which runs READ it --
        matched by content hash across every version (0255). The server's
        `origin` (L18: the run that wrote it, else where it is filed) passes
        through as it is."""
        if not self.source.server_records_reads():
            return _ViewData(payload={"unsupported": _NO_READ_LINEAGE})
        return _ViewData(payload=self.source.artifact_lineage(str(entity["id"])))

    def _view_project_lineage(self, entity: dict, request: _Req) -> _ViewData:
        """A project's or experiment's OWN lineage (server 0278, lineage plan 2
        L12/L13/L18), read from `GET /v1/projects/{id}/lineage` (an experiment's
        through the experiment API, `.../experiments/{E}/lineage`).

        `origin`: a project it builds on or replaces, else its parent project;
        null for a root. Its links, split by direction (swarm friction P6):
        `built_on` -- what it builds on, replaces or drew on (it is the link's
        source) -- and `used_by` -- what builds on or replaced it (the target).
        Each link names its far end (`ref`, `name`, from the read's `ends`) and
        says how it is known (`provenance`; `derived: true` for "built on"
        derived from what its runs used), so a fact never reads like a guess.
        On an experiment, `run_edges` is the graph AMONG its runs and files
        (`GET /v1/projects/{P}/experiments/{E}/edges`). The ROWS are its
        children (its experiments, groups, runs filed directly under it), each
        with its own origin, which is what connects the graph.

        The links are the FIXED part, so the first page shows a glance of each
        list -- at most `_LINEAGE_LINKS_GLANCE`, fewer when they would take
        more than `_LINEAGE_LINKS_SHARE` of the budget -- with its `total` and,
        when cut, a `read_more` naming `view_options.links`; later pages carry
        none. `view_options.links` makes one list the rows instead, paged whole.
        Rows are fitted exactly, so a page is whole JSON at any budget, never a
        text fragment of it. A window the SERVER stopped at -- children past the
        route's limit, stored links past its 500, "built on" over only the
        newest runs -- is flagged (`*_truncated`) with `lineage_beyond_window`.
        """
        ident = str(entity["id"])
        has_run_edges = entity.get("kind") == "experiment"
        experiment_home = entity.get("project_id") if has_run_edges else None
        # Checked before any read: a refused option costs no lineage read.
        side = self._lineage_side(request.filters.get("links"), has_run_edges=has_run_edges)
        if side is _LineageLinks.RUN_EDGES:
            # Their own route alone: the lineage read (its derived roll-up over
            # 500 runs) would be thrown away. The route takes no offset, so each
            # page reads its ceiling again (as `_bounded`'s routes do).
            fetched = self.source.experiment_edges(
                ident, _LINEAGE_RUN_EDGES_MAX, project_id=experiment_home
            )
            return self._lineage_rows(
                side,
                self._among_links(fetched, request.hidden()),
                {"run_edges_truncated": len(fetched) >= _LINEAGE_RUN_EDGES_MAX},
            )
        if has_run_edges:
            read = self.source.experiment_lineage(ident, project_id=experiment_home)
        else:
            read = self.source.project_lineage(ident)
        glance = side is None and not request.offset
        among_fetched = (
            self.source.experiment_edges(
                ident, _LINEAGE_LINKS_GLANCE + 1, project_id=experiment_home
            )
            if glance and has_run_edges
            else []
        )
        # After every read: the session's work made meanwhile is in the set.
        hidden = request.hidden()
        ends = {
            str(key).lower(): end
            for key, end in (read.get("ends") or {}).items()
            if isinstance(end, dict)
        }
        here = ident.lower()
        own: dict[_LineageLinks, list[dict]] = {
            _LineageLinks.BUILT_ON: [],
            _LineageLinks.USED_BY: [],
        }
        for edge in read.get("edges") or []:
            if not isinstance(edge, dict) or (hidden and _names_session_work(edge, hidden)):
                continue
            outgoing = str(edge.get("source_id") or "").lower() == here
            own[_LineageLinks.BUILT_ON if outgoing else _LineageLinks.USED_BY].append(
                _lineage_link(
                    edge,
                    outgoing=outgoing,
                    ends=ends,
                    reason_chars=_LINK_REASON_CHARS if glance else None,
                )
            )
        # Windows the SERVER stopped at: no paging here reaches past them.
        # Present only when true: a flag that is always there stops being read.
        windows = {
            "edges_truncated": bool(read.get("edges_truncated")),
            "derived_truncated": bool(read.get("derived_truncated")),
        }
        if side is not None:
            return self._lineage_rows(side, own[side], windows)

        payload: dict[str, Any] = {"origin": read.get("origin")}
        windows["nodes_truncated"] = bool(read.get("truncated"))
        missing: list[str] = []
        if not glance:
            payload["links_on_first_page"] = True
        else:
            lists: dict[_LineageLinks, list[dict]] = {k: v for k, v in own.items() if v}
            # Known totals; the links among an experiment's runs are read one
            # past the glance, so past it there is only "more" -- kept even when
            # the session's own work filled the whole window it read.
            totals: dict[_LineageLinks, int | None] = {k: len(v) for k, v in lists.items()}
            among = self._among_links(among_fetched, hidden)
            more_among = len(among_fetched) > _LINEAGE_LINKS_GLANCE
            if among or more_among:
                lists[_LineageLinks.RUN_EDGES] = among[:_LINEAGE_LINKS_GLANCE]
                totals[_LineageLinks.RUN_EDGES] = None if more_among else len(among)
            shown = {k: min(len(v), _LINEAGE_LINKS_GLANCE) for k, v in lists.items()}
            asked = request.ref or f"{entity.get('kind')}:{ident}"

            def glance_payload() -> dict[str, Any]:
                out: dict[str, Any] = dict(payload)
                for key, count in shown.items():
                    block: dict[str, Any] = (
                        {"more": True} if totals[key] is None else {"total": totals[key]}
                    )
                    block["links"] = lists[key][:count]
                    if totals[key] is None or count < totals[key]:
                        # A whole call: the page's own cursor walks the children
                        # and is bound to these options, so it must not ride along.
                        block["read_more"] = (
                            f'entity(refs=["{asked}"], view="lineage", '
                            f'view_options={{"links": "{key}"}}) without cursor'
                        )
                    out[str(key)] = block
                return out

            # Fewer links, never a text fragment: the widest list gives one up
            # until the glance fits its share of the budget, measured exactly.
            share = max(1, int(request.token_budget * _LINEAGE_LINKS_SHARE))
            while any(shown.values()) and _budget_cost(glance_payload()) > share:
                widest = max(shown, key=lambda key: shown[key])
                shown[widest] -= 1
            payload = glance_payload()
            if any("read_more" in payload[str(key)] for key in lists):
                missing.append(MissingMarker.LINKS_BEYOND_PAGE)
        payload.update({flag: True for flag, cut in windows.items() if cut})
        if any(windows.values()):
            missing.append(MissingMarker.LINEAGE_BEYOND_WINDOW)
        return _ViewData(
            payload=payload,
            rows=list(read.get("nodes") or []),
            rows_key="nodes",
            missing=missing,
            exact_fit=True,
        )

    @staticmethod
    def _lineage_rows(side: _LineageLinks, rows: list[dict], windows: dict[str, bool]) -> _ViewData:
        """`view_options.links`: that whole list as the rows, paged."""
        payload: dict[str, Any] = {"links": str(side), "total": len(rows)}
        payload.update({flag: True for flag, cut in windows.items() if cut})
        return _ViewData(
            payload=payload,
            rows=rows,
            rows_key=str(side),
            missing=[MissingMarker.LINEAGE_BEYOND_WINDOW] if any(windows.values()) else [],
            exact_fit=True,
        )

    @staticmethod
    def _lineage_side(value: Any, *, has_run_edges: bool) -> _LineageLinks | None:
        """`view_options.links`, checked: a list this view has, or None."""
        if value is None:
            return None
        valid = [m.value for m in _LineageLinks if has_run_edges or m is not _LineageLinks.RUN_EDGES]
        if value not in valid:
            raise errors.ValidationError(
                f"view_options.links takes one of {valid} on this "
                f"{'experiment' if has_run_edges else 'project'}, not {value!r}",
                status=422,
            )
        return _LineageLinks(value)

    @staticmethod
    def _among_links(fetched: list, hidden: frozenset[str] | None) -> list[dict]:
        """The links among an experiment's runs and files, compact, less those
        naming the session's own work when it is hidden."""
        return [
            _among_link(edge)
            for edge in fetched
            if isinstance(edge, dict) and not (hidden and _names_session_work(edge, hidden))
        ]
