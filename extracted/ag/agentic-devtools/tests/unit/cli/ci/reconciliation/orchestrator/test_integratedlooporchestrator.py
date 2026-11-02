"""Unit tests for the integrated loop safety boundary."""

from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.reconciliation.loop_control import LoopController
from agentic_devtools.cli.ci.reconciliation.models import RunEventContext
from agentic_devtools.cli.ci.reconciliation.orchestrator import (
    IntegratedLoopOrchestrator,
    ReliabilitySliceEvent,
    coalesce_wakeups,
)
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStore


def _event(target_type: str = "pull_request") -> ReliabilitySliceEvent:
    return ReliabilitySliceEvent(
        RunEventContext(target_type=target_type, target_id=42),
        Mock(),
    )


def test_constructor_rejects_missing_dispatch() -> None:
    controller = LoopController(lambda _: True, lambda: datetime.now(UTC))
    with pytest.raises(ValueError, match="dispatch"):
        IntegratedLoopOrchestrator(controller, QueueStore("owner/repo"), Mock(spec=[]))


def test_constructor_rejects_invalid_dependencies() -> None:
    controller = LoopController(lambda _: True, lambda: datetime.now(UTC))
    provider = Mock()
    provider.dispatch = Mock()
    with pytest.raises(ValueError, match="controller"):
        IntegratedLoopOrchestrator(Mock(), QueueStore("owner/repo"), provider)
    with pytest.raises(ValueError, match="queue store"):
        IntegratedLoopOrchestrator(controller, Mock(), provider)
    with pytest.raises(ValueError, match="kill-switch"):
        IntegratedLoopOrchestrator(controller, QueueStore("owner/repo"), provider, global_hold=None)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="kill-switch"):
        IntegratedLoopOrchestrator(  # type: ignore[arg-type]
            controller,
            QueueStore("owner/repo"),
            provider,
            capacity_available=None,  # type: ignore[arg-type]
        )


def test_constructor_accepts_valid_dependencies() -> None:
    controller = LoopController(lambda _: True, lambda: datetime.now(UTC))
    provider = Mock()
    provider.dispatch = Mock()
    IntegratedLoopOrchestrator(controller, QueueStore("owner/repo"), provider)


def test_run_blocks_invalid_context_and_global_hold() -> None:
    orchestrator = IntegratedLoopOrchestrator.__new__(IntegratedLoopOrchestrator)
    orchestrator._global_hold = lambda: True
    orchestrator._store = Mock()
    assert orchestrator.run(_event("issue")).reason == "event does not target a pull request"
    assert orchestrator.run(_event()).reason == "global hold is active"
    orchestrator._store.load.assert_not_called()


def test_coalesce_wakeups_keeps_first_event() -> None:
    first = _event()
    assert coalesce_wakeups([first, first]) == [first]
