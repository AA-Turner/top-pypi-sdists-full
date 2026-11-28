"""plan view: a project's plan stages in order, each with its done-when, status and the runs and experiments
behind it; and the short plan block the project card carries (plan stages R21)."""

from __future__ import annotations

from typing import Any

from probe.mcp.delivery.context import current_delivery
from probe.mcp.tools.view import _Req, _ViewData
from probe.sdk import errors
from probe.sdk.values.stage_key import PLAN_STAGES_FEATURE

#: What a server without plan stages, or a project without a plan, answers: one plain line, never an error.
PLAN_OFF_NOTE = "This Probe server has no plan stages yet."
NO_PLAN_NOTE = "No plan saved for this project yet: `probe plan save <file>`."
#: Stages the card lists; `view="plan"` has every one.
CARD_STAGES = 12
#: A stage's fields as the view sends them, in this order.
_STAGE_FIELDS = ("key", "title", "criterion", "status", "status_source", "criterion_changed", "stale",
                 "live_run_count", "record_count", "status_counts", "last_activity_at")
_PLAN_FIELDS = ("revision", "state", "approved_at", "approved_revision", "source", "updated_at")
_RECORD_FIELDS = ("kind", "id", "name", "status", "updated_at", "via")


def build_stage_row(stage: dict[str, Any]) -> dict[str, Any]:
    """One stage as a reader quotes it; falsy flags and empty counts dropped, records as `name (id:<uuid>)`."""
    row = {key: stage[key] for key in _STAGE_FIELDS if stage.get(key) not in (None, False, {}, [])}
    last = stage.get("last_update") or {}
    if last:
        row["last_update"] = {key: last[key] for key in ("status", "note", "evidence", "by", "at") if last.get(key)}
    records = [{key: record[key] for key in _RECORD_FIELDS if record.get(key)}
               for record in stage.get("records") or [] if isinstance(record, dict)]
    if records:
        row["records"] = records
    if stage.get("records_cursor"):
        row["records_truncated"] = True  # `record_count` is the whole count
        row["records_cursor"] = stage["records_cursor"]  # the rest, from `.../plan/stages/{key}/records`
    return row


def build_plan_card_block(answer: dict[str, Any]) -> dict[str, Any] | None:
    """The card's plan block: revision, state and up to `CARD_STAGES` stages (key, title, status); None
    without a plan."""
    meta = answer.get("plan")
    if not meta:
        return None
    stages = [stage for stage in answer.get("stages") or [] if isinstance(stage, dict)]
    block: dict[str, Any] = {
        "revision": meta.get("revision"),
        "state": meta.get("state"),
        "stages": [{key: stage.get(key) for key in ("key", "title", "status")} for stage in stages[:CARD_STAGES]],
        "read_all": 'view="plan"',
    }
    if len(stages) > CARD_STAGES:
        block["count"] = len(stages)
    return block


class PlanViewsMixin:
    """Part of ResearchReadService: its methods run with `self` the service; compose() folds them in."""

    def _build_project_plan_view(self, entity: dict, request: _Req) -> _ViewData:
        """The plan's stages in order; one plain line on a server without plan stages or a project without a plan."""
        if not self.source.has_feature(PLAN_STAGES_FEATURE):
            return _ViewData(payload={"note": PLAN_OFF_NOTE}, rows=[], rows_key="stages")
        answer = self.source.fetch_plan(str(entity["id"]))
        meta = answer.get("plan")
        if not meta:
            return _ViewData(payload={"note": NO_PLAN_NOTE}, rows=[], rows_key="stages")
        rows = [build_stage_row(stage) for stage in answer.get("stages") or [] if isinstance(stage, dict)]
        return _ViewData(payload={"plan": {key: meta[key] for key in _PLAN_FIELDS if meta.get(key) is not None}},
                         rows=rows, rows_key="stages")

    def _get_plan_card_block(self, entity: dict) -> dict[str, Any] | None:
        """The card's plan block, or None: an experiment, one card of a multi-ref read (one more request per
        project; `view="plan"` reads it), a server without plan stages, or no plan."""
        if entity.get("kind") == "experiment":
            return None
        context = current_delivery()
        if context is not None and context.is_batch:
            return None
        if not self.source.has_feature(PLAN_STAGES_FEATURE):
            return None
        try:
            return build_plan_card_block(self.source.fetch_plan(str(entity["id"])))
        except errors.NotFoundError:  # the project is gone, or the server lost the route: no block
            return None
