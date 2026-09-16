"""Integration checks for WP5 wakeup safety and replay coalescing."""

from unittest.mock import Mock

from agentic_devtools.cli.ci.reconciliation.models import RunEventContext
from agentic_devtools.cli.ci.reconciliation.orchestrator import (
    IntegratedLoopOrchestrator,
    ReliabilitySliceEvent,
    coalesce_wakeups,
)


def _event(number: int = 42) -> ReliabilitySliceEvent:
    return ReliabilitySliceEvent(
        context=RunEventContext(
            target_type="pull_request",
            target_id=number,
            repository_full_name="owner/repo",
            event_type="pull_request",
            action="synchronize",
        ),
        observation=Mock(),
    )


def test_replayed_wakeups_are_coalesced() -> None:
    event = _event()
    assert coalesce_wakeups([event, event]) == [event]


def test_global_hold_stops_before_loading_state() -> None:
    orchestrator = IntegratedLoopOrchestrator.__new__(IntegratedLoopOrchestrator)
    orchestrator._global_hold = lambda: True
    orchestrator._store = Mock()
    assert orchestrator.run(_event()).status == "blocked"
    orchestrator._store.load.assert_not_called()


def test_invalid_context_is_blocked() -> None:
    event = _event()
    invalid = ReliabilitySliceEvent(
        context=RunEventContext(target_type="issue", target_id=42),
        observation=event.observation,
    )
    orchestrator = IntegratedLoopOrchestrator.__new__(IntegratedLoopOrchestrator)
    assert orchestrator.run(invalid).reason == "event does not target a pull request"
