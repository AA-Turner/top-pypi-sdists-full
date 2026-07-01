import enum
from typing import assert_never

from dreadnode.app.tui.turn_lifecycle import TurnPhase as LifecyclePhase


class TurnStatePhase(enum.StrEnum):
    """Detailed reducer/UI phase for one session turn."""

    IDLE = "idle"
    GENERATING = "generating"
    RUNNING_TOOLS = "running_tools"
    AWAITING_PERMISSION = "awaiting_permission"
    AWAITING_INPUT = "awaiting_input"
    COMPLETED = "completed"
    FAILED = "failed"


def phase_from_wire(value: str) -> TurnStatePhase | None:
    """Parse a wire/session snapshot phase into the shared enum."""
    try:
        return TurnStatePhase(value)
    except ValueError:
        return None


def phase_for_human_prompt() -> TurnStatePhase:
    """All ``ask_user`` prompts share the AWAITING_INPUT phase.

    The runtime permission flow is a separate concern and uses
    ``AWAITING_PERMISSION`` directly via its own pending-permissions
    state path.
    """
    return TurnStatePhase.AWAITING_INPUT


def is_running_phase(phase: TurnStatePhase) -> bool:
    return phase in {TurnStatePhase.GENERATING, TurnStatePhase.RUNNING_TOOLS}


def is_blocked_phase(phase: TurnStatePhase) -> bool:
    return phase in {TurnStatePhase.AWAITING_INPUT, TurnStatePhase.AWAITING_PERMISSION}


def subscription_reason_for_phase(phase: TurnStatePhase) -> str | None:
    if is_running_phase(phase):
        return "running"
    if phase is TurnStatePhase.AWAITING_PERMISSION:
        return "awaiting_permission"
    if phase is TurnStatePhase.AWAITING_INPUT:
        return "awaiting_input"
    return None


def lifecycle_projection_for_phase(phase: TurnStatePhase) -> tuple[LifecyclePhase, str]:
    if phase is TurnStatePhase.AWAITING_PERMISSION:
        return (LifecyclePhase.AWAITING, "Awaiting approval")
    if phase is TurnStatePhase.AWAITING_INPUT:
        return (LifecyclePhase.AWAITING, "Awaiting input")
    if phase is TurnStatePhase.RUNNING_TOOLS:
        return (LifecyclePhase.ACTIVE, "Running")
    if phase is TurnStatePhase.GENERATING:
        return (LifecyclePhase.ACTIVE, "Thinking")
    if phase in {TurnStatePhase.IDLE, TurnStatePhase.COMPLETED, TurnStatePhase.FAILED}:
        return (LifecyclePhase.IDLE, "Ready")
    assert_never(phase)
