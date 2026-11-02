"""Tests for _get_copilot_gate_verdict."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.pipeline.gate_verdict import REASON_API_ERROR, CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.snapshot_builder import _get_copilot_gate_verdict


def test_returns_evaluated_gate_verdict(monkeypatch) -> None:
    """Successful gate evaluation is returned unchanged."""
    expected = CopilotGateVerdict(passed=True, reason="clean", review_id=8)
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict",
        lambda **_kwargs: expected,
    )

    result = _get_copilot_gate_verdict(MagicMock(), 7, [], "head", "main", "")

    assert result is expected


def test_gate_evaluation_failure_fails_closed() -> None:
    """Unexpected gate errors become a blocking API-error verdict."""

    def fail(**_kwargs):
        raise RuntimeError("provider unavailable")

    from unittest.mock import patch

    with patch(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict",
        side_effect=fail,
    ):
        result = _get_copilot_gate_verdict(MagicMock(), 7, [], "head", "main", "")

    assert result.passed is False
    assert result.reason == REASON_API_ERROR
    assert "provider unavailable" in result.details


def test_promotion_failure_overrides_a_successful_gate_verdict(monkeypatch) -> None:
    """Incomplete finding promotion prevents an otherwise passing gate."""
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.pipeline.snapshot_builder.evaluate_copilot_gate_verdict",
        lambda **_kwargs: CopilotGateVerdict(passed=True, reason="clean"),
    )

    result = _get_copilot_gate_verdict(MagicMock(), 7, [], "head", "main", "promotion failed")

    assert result.passed is False
    assert result.reason == REASON_API_ERROR
    assert "promotion failed" in result.details
