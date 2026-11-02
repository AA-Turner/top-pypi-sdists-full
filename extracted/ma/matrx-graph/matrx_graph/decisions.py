"""Decision provenance + timed human→AI escalation — the engine primitive.

A **decision point** is any step a graph cannot decide by itself: it asks a
person. Today that person may never answer, and the run waits forever. This
module makes the wait *bounded* and, crucially, makes the answer *attributed*.

Two things live here, deliberately node-agnostic so the future "one step,
three pipes" selector consumes them unchanged:

``EscalationPolicy``
    The author's declaration: how long we wait for the human, who decides
    instead, and how much notice the human is owed first. Serialized into the
    interrupt payload (durable checkpoint state), so a worker that boots hours
    later reads the same policy the node declared.

``DecisionProvenance``
    WHO actually decided, stamped onto the decision's output under the reserved
    key ``matrx_decision`` and therefore carried downstream with the value
    itself. A run that completed because an agent answered for an absent human
    says so, forever, in the same row as the answer.

**The laundering rule.** Provenance is never taken from the caller. The engine
strips any caller-supplied ``matrx_decision`` and re-stamps it from the
authenticated admission seam (the HTTP route knows the signed-in human; the
escalation worker knows the agent). A client cannot dress an AI decision as a
human one, and a bug cannot do it by accident — the strip is unconditional.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, JsonValue
from matrx_graph.content_ir.model import KindSubModel

logger = logging.getLogger(__name__)

# ── CAPS — config, not env vars ──────────────────────────────────────────────

#: Reserved output key carrying provenance. Never rename: it is persisted in
#: wf_node_outcome rows and read by every downstream consumer.
DECISION_KEY = "matrx_decision"

#: Default wait before the fallback decides. A working day: long enough that a
#: person who steps away still owns their decision, short enough that a run
#: does not silently die because someone went on holiday.
DEFAULT_DEADLINE_SECONDS = 86_400

#: A deadline shorter than this is a trap, not a deadline — nobody can be
#: notified and respond inside it. Enforced at config validation.
MIN_DEADLINE_SECONDS = 300

#: The human must have held a live notification for at least this long before
#: the fallback may decide. The host enforces it against the recorded
#: ``notified_at``; the deadline slides forward if notice landed late.
DEFAULT_MIN_NOTICE_SECONDS = 300


class DecisionAuthority(StrEnum):
    """Who authored a decision."""

    HUMAN = "human"
    #: An agent decided because the human did not answer in time.
    AGENT = "agent"
    #: The author's declared default answer was applied on timeout.
    DEFAULT = "default"


class DecisionFallback(StrEnum):
    """What happens when the deadline passes."""

    AGENT = "agent"
    DEFAULT_ANSWER = "default_answer"


class EscalationPolicy(BaseModel):
    """Author-declared timeout behavior for one decision point.

    Absent (``None``) means the historical behavior: wait forever. Escalation
    is **opt-in per node** — turning it on changes who may author a decision,
    and that is never a change the platform makes on a run's behalf.
    """

    model_config = ConfigDict(extra="forbid")

    after_seconds: int = Field(
        default=DEFAULT_DEADLINE_SECONDS,
        ge=MIN_DEADLINE_SECONDS,
        description=(
            "How long to wait for the person before the fallback decides. "
            "Minimum 5 minutes — a shorter deadline cannot be answered."
        ),
    )
    fallback: DecisionFallback = Field(
        default=DecisionFallback.AGENT,
        description=(
            "Who decides on timeout: 'agent' (an AI reads the same prompt and "
            "context the person saw) or 'default_answer' (apply this node's "
            "configured default answer verbatim)."
        ),
    )
    agent_id: str | None = Field(
        default=None,
        description=(
            "Optional specific agent to decide. Omitted, the platform's "
            "decision-fallback agent is used."
        ),
    )
    min_notice_seconds: int = Field(
        default=DEFAULT_MIN_NOTICE_SECONDS,
        ge=0,
        description=(
            "The person must have held a live notification for at least this "
            "long before the fallback may decide. Notice that lands late "
            "pushes the deadline out — it never shortens the person's chance."
        ),
    )


class DecisionProvenance(KindSubModel):
    """WHO decided, stamped onto the decision's own output.

    ``extra="forbid"``: this shape is an audit record, and an unrecognized key
    in an audit record is a defect, not a feature. ``KindSubModel`` declares
    the nested ``__kind`` as ``const ""`` (no identity of its own), so the
    marker is accepted and ignored, never refused and never invented.
    """

    model_config = ConfigDict(extra="forbid")

    authority: DecisionAuthority = Field(
        description="Who authored the decision: 'human', 'agent' (deadline fallback), or 'default' (declared default answer applied)."
    )
    decided_at: datetime = Field(description="When the decision was recorded (UTC).")
    actor_id: str | None = Field(
        default=None,
        description="The deciding human's user_id or the deciding agent's id. Never empty for human/agent authority.",
    )
    actor_label: str | None = Field(
        default=None,
        description="Display name of the decider, for surfaces that show this record later.",
    )
    escalated: bool = Field(
        default=False,
        description="True when the person's deadline passed and something else (agent or default answer) decided instead.",
    )
    deadline_at: datetime | None = Field(
        default=None,
        description="The answer-by deadline that applied to this decision, when one did.",
    )
    reason: str | None = Field(
        default=None,
        description="Plain-English one-liner for the user: why this decision has this author.",
    )


def build_escalation_payload(
    policy: EscalationPolicy | None,
    *,
    now: datetime | None = None,
) -> dict[str, JsonValue] | None:
    """Freeze ``policy`` into the durable interrupt payload.

    The deadline is absolute (not a duration) so a worker that boots after a
    restart resolves the same instant the node did, with no clock arithmetic
    over an unknown downtime.
    """
    if policy is None:
        return None
    started = now or datetime.now(UTC)
    return {
        "deadline_at": (started + timedelta(seconds=policy.after_seconds)).isoformat(),
        "waiting_since": started.isoformat(),
        "after_seconds": policy.after_seconds,
        "fallback": policy.fallback.value,
        "agent_id": policy.agent_id,
        "min_notice_seconds": policy.min_notice_seconds,
    }


def escalation_from_interrupt(
    interrupt_payload: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Read the escalation block out of a durable interrupt payload.

    Returns ``None`` for every interrupt that did not declare one — which is
    every legacy interrupt, and every node whose author chose to wait forever.
    """
    if not isinstance(interrupt_payload, dict):
        return None
    block = interrupt_payload.get("escalation")
    if not isinstance(block, dict) or not block.get("deadline_at"):
        return None
    return block


def stamp_decision(
    resume_value: dict[str, Any] | None,
    provenance: DecisionProvenance,
) -> dict[str, Any]:
    """Return ``resume_value`` with authoritative provenance attached.

    Any caller-supplied ``matrx_decision`` is DISCARDED — loudly, because a
    caller trying to author its own provenance is either a bug or an attempt to
    launder an AI decision as a human one, and both need to be visible. We
    reconcile rather than raise (a live run is never killed over a field the
    engine can decide itself).
    """
    value = dict(resume_value or {})
    supplied = value.pop(DECISION_KEY, None)
    if supplied is not None:
        logger.warning(
            "COERCED: caller-supplied '%s' discarded and re-stamped by the engine "
            "(supplied=%r, authoritative=%s/%s). Provenance is never client-authored.",
            DECISION_KEY,
            supplied,
            provenance.authority.value,
            provenance.actor_id,
        )
    value[DECISION_KEY] = provenance.model_dump(mode="json")
    return value


def sanitize_decision_value(resume_value: dict[str, Any] | None) -> dict[str, Any]:
    """Strip ANY provenance stamp from an un-attributed resume — unconditionally.

    Used on the engine's inner path when no admission seam supplied provenance.
    A ``matrx_decision`` inside a resume value is caller data, however well it
    parses: keeping a parseable one let any caller who could queue a resume name
    another person as the decider. Trusted provenance travels BESIDE the value
    (``Scheduler.resume(decision=...)``; for a queued job, the job row's
    ``metadata.decision`` written by ``enqueue(decision=...)``), never inside it.
    """
    value = dict(resume_value or {})
    raw = value.pop(DECISION_KEY, None)
    if raw is not None:
        logger.warning(
            "COERCED: dropping caller-supplied '%s' from a resume value (%r) — provenance "
            "is stamped only by a trusted seam, never carried in the answer.",
            DECISION_KEY,
            raw,
        )
    return value


def describe_decision(output: dict[str, Any] | None) -> DecisionProvenance | None:
    """Read provenance back off a decision node's output (``None`` if absent)."""
    if not isinstance(output, dict):
        return None
    raw = output.get(DECISION_KEY)
    if raw is None:
        return None
    try:
        return DecisionProvenance.model_validate(raw)
    except Exception:  # noqa: BLE001 — a malformed stamp reads as "unknown author"
        logger.warning("unparseable %s on node output: %r", DECISION_KEY, raw)
        return None


def human_decision(
    *,
    user_id: str | None,
    deadline_at: datetime | None = None,
    actor_label: str | None = None,
) -> DecisionProvenance:
    return DecisionProvenance(
        authority=DecisionAuthority.HUMAN,
        decided_at=datetime.now(UTC),
        actor_id=user_id or None,
        actor_label=actor_label,
        escalated=False,
        deadline_at=deadline_at,
        reason="Answered by the person who was asked.",
    )


def agent_decision(
    *,
    agent_id: str | None,
    agent_label: str | None,
    deadline_at: datetime | None,
    reason: str | None = None,
) -> DecisionProvenance:
    return DecisionProvenance(
        authority=DecisionAuthority.AGENT,
        decided_at=datetime.now(UTC),
        actor_id=agent_id,
        actor_label=agent_label,
        escalated=True,
        deadline_at=deadline_at,
        reason=reason or "Nobody answered before the deadline, so an AI agent decided instead.",
    )


def default_answer_decision(
    *,
    deadline_at: datetime | None,
) -> DecisionProvenance:
    return DecisionProvenance(
        authority=DecisionAuthority.DEFAULT,
        decided_at=datetime.now(UTC),
        actor_id=None,
        actor_label=None,
        escalated=True,
        deadline_at=deadline_at,
        reason=(
            "Nobody answered before the deadline, so the workflow's preset default answer was used."
        ),
    )
