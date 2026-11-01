"""lines of work: a project's or experiment's branches and the best-pick history."""

from __future__ import annotations
from typing import Any
from ...delivery import accounting
from . import branch_projection as _branches
from ....shared.reads.search_contract import (
    EnvelopeState,
    MissingMarker)
from ...delivery.context import source_changed
from probe.mcp.tools.shaping.shaping import _budget_cost, _largest
from probe.mcp.tools.view import _Req, _ViewData
#: Pick events a best read returns: the server's own ceiling (`MAX_PICK_HISTORY`).
_PICK_HISTORY_MAX = 50
#: The share of a `browse mode=branches` page the workspace's pick history may
#: take on its first page; the branches page in the rest.
_PICK_HISTORY_SHARE = 1 / 3
#: What a browse page costs beyond its data -- completeness markers and the
#: delivery cursor (~150 base64 characters) -- left free beside the first row.
_BROWSE_PAGE_SLACK = 150


class BranchesViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the ResearchReadService; compose() folds them into ResearchReadService."""

    def _workspace_pick_history(
        self,
        data: dict[str, Any],
        workspace_id: str,
        token_budget: int,
        missing: list[str],
        *,
        rows: dict[str, list],
    ) -> None:
        """`pick_history` on the first compact page of `browse mode=branches`
        (#3624, R13): the workspace pick's events, newest first, in the picks
        view's shape (`GET /v1/workspaces/{W}/best?history=50`).

        The branch rows are the page's answer and the history its optional
        part, so the history never costs the page a row: when every row fits
        one page, it takes only the room they leave; when the rows page anyway,
        it takes up to `_PICK_HISTORY_SHARE` of the budget, never the room the
        header and the first row need. Measured exactly. When that is not every
        event, `pick_history_total` says how many were read and `missing` says
        `pick_history_beyond_page` (delivery also drops the history before it
        would refuse a page that cannot hold one row). A failed read is
        `pick_history` in `missing`, never an absent key."""
        try:
            body = self.source.workspace_best(workspace_id, history=_PICK_HISTORY_MAX)
        except Exception:  # noqa: BLE001 -- an additive read never breaks the branches page
            missing.append(MissingMarker.PICK_HISTORY)
            return
        _, events = _branches.pick_history(body)

        def whole_page(n: int) -> dict:
            # The page as delivery will send it when every row fits: no cursor.
            out_data: dict[str, Any] = {**data, **rows}
            marked = list(missing)
            if n:
                out_data["pick_history"] = events[:n]
            if n < len(events):
                out_data["pick_history_total"] = len(events)
                marked.append(MissingMarker.PICK_HISTORY_BEYOND_PAGE)
            page: dict[str, Any] = {"data": out_data}
            if marked:
                page["completeness"] = {"state": EnvelopeState.PARTIAL, "missing": marked}
            return page

        share = int(token_budget * _PICK_HISTORY_SHARE)
        if _budget_cost(whole_page(0)) <= token_budget:
            # Every row fits one page: the history takes only what they leave.
            shown = _largest(
                len(events),
                lambda n: _budget_cost({"pick_history": events[:n]}) <= share
                and _budget_cost(whole_page(n)) <= token_budget,
            )
        else:
            first = {key: listed[:1] for key, listed in rows.items()}
            room = token_budget - _budget_cost({"data": {**data, **first}}) - _BROWSE_PAGE_SLACK
            shown = _largest(
                len(events), lambda n: _budget_cost({"pick_history": events[:n]}) <= min(share, room)
            )
        if shown:
            data["pick_history"] = events[:shown]
        if shown < len(events):
            data["pick_history_total"] = len(events)
            missing.append(MissingMarker.PICK_HISTORY_BEYOND_PAGE)
        if len(events) >= _PICK_HISTORY_MAX:
            missing.append(MissingMarker.PICKS_BEYOND_SERVER_LIMIT)

    def _view_project_branches(self, entity: dict, request: _Req) -> _ViewData:
        return self._branches_view(self.source.project_branches(str(entity["id"])), request)

    def _view_experiment_branches(self, entity: dict, request: _Req) -> _ViewData:
        home = entity.get("project_id") or entity.get("parent_project_id")
        body = self.source.experiment_branch(
            str(entity["id"]), project_id=str(home) if home else None
        )
        return self._branches_view(body, request)

    def _view_project_picks(self, entity: dict, request: _Req) -> _ViewData:
        """The project's best pick and its history (#3624), from
        `GET /v1/projects/{P}/best?history=50`: `pick` is the current one (null
        with none), the ROWS every pick and clear, newest first -- its `id` (the
        event's order), what was picked (`experiment`, `name`; `gone` when it is
        in the trash or left the tree), the `reason`, who (`by`, an agent read
        as its person; `source` human or agent) and when (`at`). Events naming
        an experiment the caller cannot read are left out by the server; under
        `X-Probe-Hide-Session-Work`, those naming the session's own experiments
        are left out here.

        Rows resume after the last event `id` sent, not at an offset: the route
        is read again for each page, and a pick made mid-walk would otherwise
        repeat a row (inflating the churn this view exists to show). The route
        reads at most 50 events and takes no offset; a full 50 is flagged
        `picks_beyond_server_limit` (older events are not reachable -- it hides
        unreadable ones AFTER that limit, so fewer than 50 can still sit on
        more)."""
        body = self.source.project_best(str(entity["id"]), history=_PICK_HISTORY_MAX)
        read = len((body or {}).get("history") or []) if isinstance(body, dict) else 0
        pick, events = _branches.pick_history(body, hidden=request.hidden() or frozenset())
        if request.after is not None:
            try:
                last = int(request.after)
            except ValueError:
                raise source_changed("the pick this page stopped after is not an event id") from None
            events = [e for e in events if isinstance(e.get("id"), int) and e["id"] < last]
        return _ViewData(
            payload={"pick": pick},
            rows=events,
            rows_key="picks",
            missing=[MissingMarker.PICKS_BEYOND_SERVER_LIMIT] if read >= _PICK_HISTORY_MAX else [],
            resume_key="id",
        )

    @staticmethod
    def _branches_view(body: dict, request: _Req) -> _ViewData:
        """The compact tier, or `view_options.branch` in full (`branches.project`).
        Rows resume after the last ref sent. A branch is an aggregate the
        session-work hiding cannot take its own work out of, so it says so."""
        tier = _branches.project(body, branch=request.filters.get("branch"), after=request.after)
        missing = []
        if accounting.session_work_to_hide() is not None:
            missing.append(MissingMarker.SESSION_WORK_EXCLUSION_UNSUPPORTED)
        return _ViewData(
            payload=tier.payload,
            rows=tier.rows,
            rows_key=tier.rows_key,
            missing=missing,
            resume_key="ref",
        )
