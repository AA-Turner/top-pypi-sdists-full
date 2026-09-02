from __future__ import annotations

from unittest.mock import call, patch

from agentic_devtools.orchestration.safety.mode import (
    ExecutionMode,
    _is_truthy,
    persist_execution_mode,
    resolve_execution_mode_from_state,
)


class TestStateHelpers:
    """Tests for state-backed execution mode helpers."""

    def test_resolve_execution_mode_from_state_reads_expected_keys(self) -> None:
        with patch(
            "agentic_devtools.state.get_value",
            side_effect=["restricted", True],
        ) as mock_get_value:
            mode = resolve_execution_mode_from_state()

        assert mode == ExecutionMode.restricted
        assert mock_get_value.call_args_list == [
            call("orchestration.execution_mode"),
            call("dry_run"),
        ]

    def test_persist_execution_mode_writes_state_value(self) -> None:
        with patch("agentic_devtools.state.set_value") as mock_set_value:
            persist_execution_mode(ExecutionMode.dry_run)

        mock_set_value.assert_called_once_with("orchestration.execution_mode", "dry_run")

    def test_is_truthy_uses_bool_for_non_string_values(self) -> None:
        assert _is_truthy(7) is True
        assert _is_truthy([]) is False
