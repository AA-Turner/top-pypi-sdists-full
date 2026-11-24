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
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
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

#: The wait used ONLY when no host told the engine its standard wait
#: (``configure_standard_wait``) — a bare install of this package. A host's
#: standard wait is a setting it owns (ours: the ``workflow_decisions.
#: standard_wait_seconds`` knob), never this number.
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
    #: The run ENDS, saying in plain words that nobody answered. Nothing is
    #: decided for the person. What an asking step with no declared policy gets.
    END_RUN = "end_run"


class EscalationPolicy(BaseModel):
    """Author-declared timeout behavior for one decision point.

    Absent (``None``) no longer means "wait forever" (2026-11-14): every wait
    on a person has a deadline. A step that declares nothing waits the host's
    standard wait and then the run ENDS with a plain reason — the one outcome
    that never decides anything for the person. Letting an agent or a default
    answer decide stays **opt-in per node**: it changes who may author a
    decision, and that is never a change the platform makes on a run's behalf.
    """

    model_config = ConfigDict(extra="forbid")

    after_seconds: int | None = Field(
        default=None,
        ge=MIN_DEADLINE_SECONDS,
        description=(
            "How long to wait for the person before the deadline passes. Leave "
            "empty to use the standard wait (an admin setting). Minimum 5 "
            "minutes — a shorter deadline cannot be answered."
        ),
    )
    fallback: DecisionFallback = Field(
        default=DecisionFallback.AGENT,
        description=(
            "What happens when the deadline passes: 'default_answer' (the run "
            "continues with this step's default answer), 'end_run' (the run "
            "ends and says nobody answered), or 'agent' (an AI reads the same "
            "prompt and context the person saw and decides)."
        ),
    )
    end_reason: str | None = Field(
        default=None,
        max_length=500,
        description=(
            "For 'end_run': the plain-English sentence shown on the run when "
            "it ends because nobody answered. Leave empty for the standard one."
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
    over an unknown downtime. A policy that names no wait of its own carries no
    ``deadline_at`` yet: the engine fills it from the host's standard wait as
    the run parks (``with_wait_deadline``), still before anything is saved.
    """
    if policy is None:
        return None
    started = now or datetime.now(UTC)
    block: dict[str, JsonValue] = {
        "waiting_since": started.isoformat(),
        "after_seconds": policy.after_seconds,
        "fallback": policy.fallback.value,
        "agent_id": policy.agent_id,
        "min_notice_seconds": policy.min_notice_seconds,
    }
    if policy.after_seconds is not None:
        block["deadline_at"] = (started + timedelta(seconds=policy.after_seconds)).isoformat()
    if policy.end_reason:
        block["end_reason"] = policy.end_reason
    return block


# ── every wait on a person has a deadline ────────────────────────────────────


@dataclass(frozen=True)
class StandardWait:
    """The host's answer to "how long does a question wait when its step did not say"."""

    after_seconds: int
    #: What happens at the deadline for a step that declared NO policy.
    fallback: DecisionFallback = DecisionFallback.END_RUN
    min_notice_seconds: int = DEFAULT_MIN_NOTICE_SECONDS


#: ``provider(organization_id=..., user_id=...)`` → the standard wait, or None
#: when the host says this wait has no deadline (ours: an organization that
#: chose "always wait for a person").
StandardWaitProvider = Callable[..., Awaitable[StandardWait | None]]

_standard_wait: StandardWaitProvider | None = None


def configure_standard_wait(provider: StandardWaitProvider | None) -> None:
    """Register (or clear, with None) the host's standard wait for a person."""
    global _standard_wait
    _standard_wait = provider


def adopted_escalation(
    wait: StandardWait,
    *,
    asked_at: datetime | None = None,
    now: datetime | None = None,
) -> dict[str, JsonValue]:
    """The escalation block for a wait whose step declared none.

    ``source: "standard"`` marks it as the platform's, so a reader can tell a
    deadline the author chose from the one every wait gets. The deadline counts
    from ``now`` (when the wait first learned it had one), never from an older
    ``asked_at`` — a run parked for weeks gets the whole wait, not a deadline
    that had already passed before anyone was told of it.
    """
    started = now or datetime.now(UTC)
    return {
        "deadline_at": (started + timedelta(seconds=wait.after_seconds)).isoformat(),
        "waiting_since": (asked_at or started).isoformat(),
        "after_seconds": wait.after_seconds,
        "fallback": wait.fallback.value,
        "agent_id": None,
        "min_notice_seconds": wait.min_notice_seconds,
        "source": "standard",
    }


async def with_wait_deadline(
    payload: dict[str, Any],
    *,
    organization_id: str | None = None,
    user_id: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """``payload`` as it is saved: a wait on a person always carries its deadline.

    Called by the scheduler at the ONE place a run parks, so every asking step
    — today's and any written later — gets a deadline without declaring one:

    * a block that already has ``deadline_at`` is the author's and is untouched;
    * a declared policy with no wait of its own gets the host's standard wait;
    * no policy at all gets the host's standard wait and its standard outcome.

    A timer park (the caller checks the sleep marker) never comes here. With no
    host registered a declared policy falls back to ``DEFAULT_DEADLINE_SECONDS``
    and says so; an undeclared wait is left as it is, because nothing in a bare
    install would ever act on a deadline. Never raises: a failed lookup parks
    the run as it was asked (the host's sweep adopts it on its next pass).
    """
    declared = payload.get("escalation")
    declared = declared if isinstance(declared, dict) else None
    if declared is not None and declared.get("deadline_at"):
        return payload
    wait: StandardWait | None = None
    if _standard_wait is not None:
        try:
            wait = await _standard_wait(organization_id=organization_id, user_id=user_id)
        except Exception:  # noqa: BLE001 — the park must still happen
            logger.exception("standard wait lookup failed — parking without a frozen deadline")
            return payload
        if wait is None:
            return payload
    started = now or datetime.now(UTC)
    if declared is None:
        if wait is None:
            return payload
        return {**payload, "escalation": adopted_escalation(wait, now=started)}
    if wait is None:
        logger.warning(
            "no standard wait is registered — a declared deadline with no wait of its own "
            "uses the package fallback of %d seconds",
            DEFAULT_DEADLINE_SECONDS,
        )
    seconds = wait.after_seconds if wait is not None else DEFAULT_DEADLINE_SECONDS
    asked = declared.get("waiting_since")
    try:
        since = datetime.fromisoformat(asked) if isinstance(asked, str) and asked else started
    except ValueError:
        since = started
    block = {
        **declared,
        "after_seconds": seconds,
        "waiting_since": since.isoformat(),
        "deadline_at": (since + timedelta(seconds=seconds)).isoformat(),
    }
    return {**payload, "escalation": block}


def unanswered_reason(
    payload: dict[str, Any] | None,
    *,
    waited: str | None = None,
    because: str | None = None,
) -> str:
    """The plain sentence a run carries when it ends because nobody answered.

    The author's own ``end_reason`` wins. Otherwise it names the question (its
    title, else the start of its prompt), how long it waited when known, and
    ``because`` — why nothing else could answer, when a fallback was tried.
    """
    block = payload.get("escalation") if isinstance(payload, dict) else None
    authored = block.get("end_reason") if isinstance(block, dict) else None
    if isinstance(authored, str) and authored.strip():
        return authored.strip()
    subject = ""
    if isinstance(payload, dict):
        subject = str(payload.get("title") or payload.get("step_name") or "").strip()
        if not subject:
            prompt = " ".join(str(payload.get("prompt") or "").split())
            subject = prompt[:117].rstrip() + "…" if len(prompt) > 120 else prompt
    asked = f"“{subject}”" if subject else "this workflow's question"
    within = f" within {waited}" if waited else " before the deadline"
    reason = f"Nobody answered {asked}{within}, so this run was ended."
    if because:
        reason += f" {because.strip()}"
    return reason


def escalation_from_interrupt(
    interrupt_payload: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Read the escalation block out of a durable interrupt payload.

    Returns ``None`` for an interrupt that carries none: one parked before
    every wait had a deadline (the host's sweep adopts it), or one in a host
    that said this wait has none.
    """
    if not isinstance(interrupt_payload, dict):
        return None
    inner = interrupt_payload.get("payload")
    if isinstance(inner, dict) and "escalation" not in interrupt_payload:
        # The run row keeps the ``{"node_id", "payload"}`` envelope; the
        # checkpoint keeps the node payload itself. Either reads the same.
        interrupt_payload = inner
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
