from dataclasses import replace

from agentic_devtools.cli.ci.reconciliation.models import AttemptStatus
from agentic_devtools.cli.ci.reconciliation.reliability_metrics import calculate_reliability_metrics


def test_reliability_metrics_uses_all_attempted_obligations(foundation):
    fixture = foundation()
    metrics = calculate_reliability_metrics(fixture.state)
    assert metrics.attempted_obligations == 1
    assert metrics.completion_rate == 0.0


def test_reliability_metrics_counts_success_and_quarantine(foundation):
    fixture = foundation()
    fixture.state.attempts["attempt-0"] = replace(fixture.state.attempts["attempt-0"], status=AttemptStatus.SUCCEEDED)
    metrics = calculate_reliability_metrics(fixture.state)
    assert metrics.completed_obligations == 1
