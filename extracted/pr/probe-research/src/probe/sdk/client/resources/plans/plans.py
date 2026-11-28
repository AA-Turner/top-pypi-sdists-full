"""PlansMixin, Client's methods: a project's plan stages -- save the plan, read it, link a run or experiment
to a stage, add a stage update -- and the stage a run or experiment create carries (twin: app/projects/plans)."""

from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from typing import Any
from urllib.parse import quote

from probe.foundation.compat.compat import StrEnum

from .... import errors
from ....delivery.transport.deadlines import deadline_scope, without_patience
from ....values.stage_key import (
    PLAN_STAGES_FEATURE,
    STAGE_KEY_RULE,
    StageStatus,
    is_stage_key,
    warn_stage_once,
)

#: Seconds a create waits to learn whether the server takes `stage`, within the create's own deadline: a stalled
#: lookup leaves the create its time.
STAGE_LOOKUP_SECONDS = 2.0
#: The server's 409 codes on a plan save.
PLAN_REVISION_CONFLICT = "plan_revision_conflict"
PLAN_SOURCE_CONFLICT = "plan_source_conflict"


class LinkRole(StrEnum):
    """How a record joins a stage: its one assignment, or cited as evidence."""

    ASSIGNED = "assigned"
    EVIDENCE = "evidence"


def get_error_code(exc: BaseException) -> str | None:
    """The server's `code` on an error answer, in either shape it sends it."""
    if not isinstance(exc, errors.RosError):
        return None
    code = getattr(getattr(exc, "server_message", None), "code", None)
    if code:
        return str(code)
    detail = exc.detail
    if isinstance(detail, Mapping) and detail.get("code"):
        return str(detail["code"])
    return None


class PlansMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client.

    Sent straight, never queued: a plan save must carry the file as it is when sent, and a refusal
    (409 on a stale revision, 422 on an unknown stage) is the answer the caller acts on."""

    def get_plan(self, project_id: str) -> dict[str, Any]:
        """``GET /v1/projects/{ref}/plan``: ``{plan, stages}``; ``{plan: None, stages: []}`` before any save."""
        return self.transport.get(f"/v1/projects/{_quote(project_id)}/plan") or {
            "plan": None,
            "stages": [],
        }

    def list_plan_stage_records(
        self, project_id: str, stage: str, *, cursor: str | None = None
    ) -> dict[str, Any]:
        """``GET /v1/projects/{ref}/plan/stages/{key}/records``: ``{records, next_cursor}``, one page of a stage's
        records, oldest first. Start from the stage's ``records_cursor``."""
        return self.transport.get(
            f"/v1/projects/{_quote(project_id)}/plan/stages/{_quote(stage)}/records",
            params={"cursor": cursor} if cursor else None,
        ) or {"records": [], "next_cursor": None}

    def save_plan(self, project_id: str, body: Mapping[str, Any]) -> dict[str, Any]:
        """``PUT /v1/projects/{ref}/plan`` with the whole plan and its ``base_revision``: the saved plan."""
        return self.transport.put(f"/v1/projects/{_quote(project_id)}/plan", dict(body))

    def set_plan_link(
        self,
        project_id: str,
        record: str,
        *,
        role: LinkRole | str,
        stage: str | None,
        should_remove: bool = False,
    ) -> dict[str, Any]:
        """``PUT /v1/projects/{ref}/plan/links``. `record` is ``run:<id>`` or ``experiment:<id>``. `assigned`
        replaces the record's stage (None clears it); `evidence` cites it on `stage`, or with
        `should_remove` drops the citation."""
        body: dict[str, Any] = {"record": record, "role": LinkRole(role).value, "stage": stage}
        if should_remove:
            body["remove"] = True
        answer = self.transport.put(f"/v1/projects/{_quote(project_id)}/plan/links", body) or {}
        return {} if _is_elided(answer) else answer

    def add_plan_update(
        self,
        project_id: str,
        stage: str,
        *,
        note: str,
        update_key: str,
        status: StageStatus | str | None = None,
        evidence: Sequence[str] = (),
        criterion: str | None = None,
    ) -> dict[str, Any]:
        """``POST /v1/projects/{ref}/plan/stages/{key}/updates``: progress, a blocker, or `complete` (which
        needs a note saying how the stage's `Done when` was met). The same `update_key` again is a replay.
        `criterion`, with complete: the `Done when` checked; a 409 `plan_criterion_changed` when the stage's
        differs now. The answer's `confirmed_criterion` is the one it confirmed."""
        body: dict[str, Any] = {"note": note, "evidence": list(evidence), "update_key": update_key}
        if status is not None:
            body["status"] = StageStatus(status).value
        if criterion is not None:
            body["criterion"] = criterion
        answer = (
            self.transport.post(
                f"/v1/projects/{_quote(project_id)}/plan/stages/{_quote(stage)}/updates", body
            )
            or {}
        )
        if not _is_elided(answer):
            return answer
        stages = self.get_plan(project_id).get("stages") or []
        return next((row.get("last_update") or {} for row in stages if row.get("key") == stage), {})

    def _get_stage_to_send(self, stage: str | None) -> str | None:
        """The `stage` a run or experiment create may carry: None (one warning) when it is not a key, the
        server predates plan stages, or the feature lookup itself failed. Never fails the create."""
        if stage is None:
            return None
        if not is_stage_key(stage):
            warn_stage_once(
                f"bad:{stage}",
                f"probe: {stage!r} is not a stage key ({STAGE_KEY_RULE}); "
                "created without a stage. `probe plan show` lists the keys.",
            )
            return None
        if getattr(self, "_has_stage_lookup_failed", False):
            is_supported = None
        else:
            try:
                with without_patience(), deadline_scope(time.monotonic() + STAGE_LOOKUP_SECONDS):
                    is_supported = self.supports_feature(PLAN_STAGES_FEATURE)
            except Exception:  # noqa: BLE001 -- network, 5xx or out of time: unknown is unsupported, for the stage
                self._has_stage_lookup_failed = (
                    True  # asked once per client: the next create does not wait again
                )
                is_supported = None
        if is_supported is None:
            warn_stage_once(
                "lookup",
                f"probe: could not ask the server about plan stages; created without "
                f"stage {stage!r}. Set it later: probe run set <run> --stage {stage}",
            )
            return None
        if not is_supported:
            warn_stage_once(
                "old",
                f"probe: this Probe server has no plan stages yet; created without "
                f"stage {stage!r}.",
            )
            return None
        return stage


def _is_elided(answer: object) -> bool:
    """A daemon retry's replay of a link or update answer too large to store: `{idempotent_replay, body_elided}`."""
    return isinstance(answer, Mapping) and answer.get("body_elided") is True


def _quote(segment: str) -> str:
    """One path segment; an empty one would reach another route."""
    if not str(segment).strip():
        raise errors.ValidationError("name the project or stage: it can't be empty")
    return quote(str(segment).strip().removeprefix("id:"), safe="")
