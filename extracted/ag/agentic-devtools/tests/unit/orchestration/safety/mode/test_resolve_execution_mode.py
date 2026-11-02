"""Tests for resolve_execution_mode() — FR-001 most-restrictive-wins."""

from __future__ import annotations

from agentic_devtools.orchestration.safety.mode import ExecutionMode, resolve_execution_mode


class TestResolveExecutionMode:
    """Tests for execution mode resolution."""

    def test_no_signals_returns_live(self) -> None:
        mode = resolve_execution_mode()
        assert mode == ExecutionMode.live

    def test_cli_mode_dry_run(self) -> None:
        mode = resolve_execution_mode(cli_mode="dry_run")
        assert mode == ExecutionMode.dry_run

    def test_cli_mode_restricted(self) -> None:
        mode = resolve_execution_mode(cli_mode="restricted")
        assert mode == ExecutionMode.restricted

    def test_state_mode_dry_run(self) -> None:
        mode = resolve_execution_mode(state_mode="dry_run")
        assert mode == ExecutionMode.dry_run

    def test_env_dry_run_1(self) -> None:
        mode = resolve_execution_mode(env_dry_run="1")
        assert mode == ExecutionMode.dry_run

    def test_env_dry_run_true(self) -> None:
        mode = resolve_execution_mode(env_dry_run="true")
        assert mode == ExecutionMode.dry_run

    def test_state_dry_run_true_string(self) -> None:
        mode = resolve_execution_mode(state_dry_run="true")
        assert mode == ExecutionMode.dry_run

    def test_state_dry_run_bool(self) -> None:
        mode = resolve_execution_mode(state_dry_run=True)
        assert mode == ExecutionMode.dry_run

    def test_most_restrictive_wins_restricted_over_dry_run(self) -> None:
        mode = resolve_execution_mode(cli_mode="restricted", state_dry_run=True)
        assert mode == ExecutionMode.restricted

    def test_most_restrictive_wins_dry_run_over_live(self) -> None:
        mode = resolve_execution_mode(cli_mode="live", env_dry_run="1")
        assert mode == ExecutionMode.dry_run

    def test_all_signals_most_restrictive(self) -> None:
        mode = resolve_execution_mode(cli_mode="live", state_mode="dry_run", env_dry_run="1", state_dry_run=True)
        assert mode == ExecutionMode.dry_run

    def test_invalid_mode_string_ignored(self) -> None:
        mode = resolve_execution_mode(cli_mode="invalid", env_dry_run="1")
        assert mode == ExecutionMode.dry_run

    def test_state_dry_run_false_not_counted(self) -> None:
        mode = resolve_execution_mode(state_dry_run="false")
        assert mode == ExecutionMode.live

    def test_state_dry_run_none_not_counted(self) -> None:
        mode = resolve_execution_mode(state_dry_run=None)
        assert mode == ExecutionMode.live

    def test_env_dry_run_0_not_counted(self) -> None:
        mode = resolve_execution_mode(env_dry_run="0")
        assert mode == ExecutionMode.live

    def test_invalid_state_mode_string_ignored(self) -> None:
        mode = resolve_execution_mode(state_mode="bogus")
        assert mode == ExecutionMode.live
