"""Unit tests for CLI hook developer tooling (#1495)."""

from __future__ import annotations

import argparse
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.hooks import (
    HookDecision,
    HookReplayEntry,
    ReplayResult,
    replay_hook_event,
)
from tests.support.hook_fixtures import make_entry, make_hooks_config

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(
    pre: list | None = None,
    post: list | None = None,
) -> MagicMock:
    """Build a minimal AppConfig mock with a real HooksConfig."""
    from anteroom.config import HooksConfig

    config = MagicMock()
    config.hooks = HooksConfig(pre_tool=pre or [], post_tool=post or [])
    config.ai.allowed_domains = []
    config.ai.block_localhost_api = False
    return config


def _replay_args(
    event: str = "pre_tool", tool: str = "bash", arguments: str = "{}", output: str | None = None
) -> argparse.Namespace:
    ns = argparse.Namespace()
    ns.hook_event = event
    ns.tool = tool
    ns.arguments = arguments
    ns.output = output
    return ns


# ---------------------------------------------------------------------------
# ReplayResult properties
# ---------------------------------------------------------------------------


class TestReplayResult:
    def _entry(self, matched: bool, executable: bool, skipped_reason: str = "") -> HookReplayEntry:
        return HookReplayEntry(
            hook_id="h",
            trust_source="personal" if executable else "pack",
            is_executable=executable,
            matched=matched,
            skipped_reason=skipped_reason,
            decision=None,
            execution_ms=0.0,
        )

    def test_executable_count(self) -> None:
        result = ReplayResult(
            event="pre_tool",
            tool_name="bash",
            entries=[self._entry(True, True), self._entry(False, False, "no_match")],
            final_decision=HookDecision(),
        )
        assert result.executable_count == 1

    def test_skipped_count(self) -> None:
        result = ReplayResult(
            event="pre_tool",
            tool_name="bash",
            entries=[
                self._entry(True, True),
                self._entry(False, False, "no_match"),
                self._entry(True, False, "not_executable"),
            ],
            final_decision=HookDecision(),
        )
        assert result.skipped_count == 2

    def test_matched_count(self) -> None:
        result = ReplayResult(
            event="pre_tool",
            tool_name="bash",
            entries=[self._entry(True, True), self._entry(False, True, "no_match")],
            final_decision=HookDecision(),
        )
        assert result.matched_count == 1


# ---------------------------------------------------------------------------
# replay_hook_event — core semantics
# ---------------------------------------------------------------------------


class TestReplayHookEvent:
    @pytest.mark.asyncio
    async def test_no_hooks_returns_allow(self) -> None:
        hooks = make_hooks_config()
        result = await replay_hook_event(hooks, "pre_tool", "bash", {})
        assert result.final_decision.outcome == "allow"
        assert result.entries == []

    @pytest.mark.asyncio
    async def test_non_matching_hook_recorded_as_no_match(self) -> None:
        entry = make_entry("h1", tool_name="write_file")
        hooks = make_hooks_config(pre=[entry])
        result = await replay_hook_event(hooks, "pre_tool", "bash", {})
        assert len(result.entries) == 1
        assert result.entries[0].skipped_reason == "no_match"
        assert not result.entries[0].matched
        assert result.entries[0].decision is None

    @pytest.mark.asyncio
    async def test_pack_hook_is_not_executed(self) -> None:
        entry = make_entry("pack-hook", trust_source="pack", tool_name="*")
        hooks = make_hooks_config(pre=[entry])
        result = await replay_hook_event(hooks, "pre_tool", "bash", {})
        assert len(result.entries) == 1
        e = result.entries[0]
        assert e.matched is True
        assert e.skipped_reason == "not_executable"
        assert e.is_executable is False
        assert e.decision is None

    @pytest.mark.asyncio
    async def test_pack_hook_does_not_affect_final_decision(self) -> None:
        entry = make_entry("pack-hook", trust_source="pack", tool_name="*")
        hooks = make_hooks_config(pre=[entry])
        result = await replay_hook_event(hooks, "pre_tool", "bash", {})
        assert result.final_decision.outcome == "allow"

    @pytest.mark.asyncio
    async def test_no_short_circuit_all_hooks_evaluated(self) -> None:
        deny_entry = make_entry("deny-hook", command='echo \'{"decision":"deny"}\'')
        allow_entry = make_entry("allow-hook", command='echo \'{"decision":"allow"}\'')
        hooks = make_hooks_config(pre=[deny_entry, allow_entry])

        with patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = [
                HookDecision(outcome="deny", hook_id="deny-hook"),
                HookDecision(outcome="allow", hook_id="allow-hook"),
            ]
            result = await replay_hook_event(hooks, "pre_tool", "bash", {})

        assert len(result.entries) == 2
        assert mock_run.call_count == 2

    @pytest.mark.asyncio
    async def test_final_decision_is_first_non_allow(self) -> None:
        h1 = make_entry("h1", command='echo \'{"decision":"allow"}\'')
        h2 = make_entry("h2", command='echo \'{"decision":"deny","message":"no"}\'')
        h3 = make_entry("h3", command='echo \'{"decision":"deny","message":"later"}\'')
        hooks = make_hooks_config(pre=[h1, h2, h3])

        with patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = [
                HookDecision(outcome="allow", hook_id="h1"),
                HookDecision(outcome="deny", message="no", hook_id="h2"),
                HookDecision(outcome="deny", message="later", hook_id="h3"),
            ]
            result = await replay_hook_event(hooks, "pre_tool", "bash", {})

        assert result.final_decision.outcome == "deny"
        assert result.final_decision.message == "no"

    @pytest.mark.asyncio
    async def test_no_audit_writer_called(self) -> None:
        entry = make_entry("h1", command='echo \'{"decision":"allow"}\'')
        hooks = make_hooks_config(pre=[entry])

        with (
            patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_run,
            patch("anteroom.services.hooks._emit_hook_audit") as mock_audit,
        ):
            mock_run.return_value = HookDecision(outcome="allow", hook_id="h1")
            await replay_hook_event(hooks, "pre_tool", "bash", {})

        mock_audit.assert_not_called()

    @pytest.mark.asyncio
    async def test_webhook_runner_dispatched(self) -> None:
        entry = make_entry("wh-hook", runner_type="webhook", url="http://localhost/hook")
        hooks = make_hooks_config(pre=[entry])

        with patch("anteroom.services.hooks.run_webhook_hook", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = HookDecision(outcome="allow", hook_id="wh-hook")
            result = await replay_hook_event(hooks, "pre_tool", "bash", {})

        assert mock_run.call_count == 1
        assert result.entries[0].skipped_reason == ""
        assert result.entries[0].decision is not None

    @pytest.mark.asyncio
    async def test_unknown_runner_type_skipped_not_dispatched(self) -> None:
        """Unknown runner types must be skipped (mirrors _run_single_hook production behaviour)."""
        entry = make_entry("bad-hook", command="echo ok")
        # Bypass __post_init__ normalisation to simulate a future/unknown runner type
        object.__setattr__(entry.runner, "type", "grpc")
        hooks = make_hooks_config(pre=[entry])

        with (
            patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_cmd,
            patch("anteroom.services.hooks.run_webhook_hook", new_callable=AsyncMock) as mock_wh,
        ):
            result = await replay_hook_event(hooks, "pre_tool", "bash", {})

        assert mock_cmd.call_count == 0
        assert mock_wh.call_count == 0
        assert len(result.entries) == 1
        e = result.entries[0]
        assert e.skipped_reason == "unknown_runner"
        assert e.decision is None
        assert result.final_decision.outcome == "allow"

    @pytest.mark.asyncio
    async def test_post_tool_uses_post_list(self) -> None:
        pre_entry = make_entry("pre-h", event="pre_tool")
        post_entry = make_entry("post-h", event="post_tool")
        hooks = make_hooks_config(pre=[pre_entry], post=[post_entry])

        with patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = HookDecision(outcome="allow", hook_id="post-h")
            result = await replay_hook_event(hooks, "post_tool", "bash", {}, {})

        assert len(result.entries) == 1
        assert result.entries[0].hook_id == "post-h"


# ---------------------------------------------------------------------------
# _run_hook_list
# ---------------------------------------------------------------------------


class TestRunHookList:
    def test_empty_hooks_prints_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_list

        config = _make_config()
        _run_hook_list(config)
        out = capsys.readouterr().out
        assert "No hooks configured" in out

    def test_shows_hook_ids(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_list

        config = _make_config(pre=[make_entry("my-hook", command="echo ok")])
        _run_hook_list(config)
        out = capsys.readouterr().out
        assert "my-hook" in out

    def test_pack_hook_shown_as_not_executable(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_list

        config = _make_config(pre=[make_entry("pack-hook", trust_source="pack", command="echo ok")])
        _run_hook_list(config)
        out = capsys.readouterr().out
        assert "pack" in out


# ---------------------------------------------------------------------------
# _run_hook_validate (resolved-snapshot display, called after valid config load)
# ---------------------------------------------------------------------------


class TestRunHookValidate:
    def test_empty_hooks(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_validate

        config = _make_config()
        _run_hook_validate(config)
        out = capsys.readouterr().out
        assert "No hooks configured" in out

    def test_valid_hook_exits_zero(self) -> None:
        from anteroom.cli.hook_cli import _run_hook_validate

        config = _make_config(pre=[make_entry("h1", command="echo ok")])
        _run_hook_validate(config)

    def test_pack_hook_warns_but_does_not_exit_one(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_validate

        config = _make_config(pre=[make_entry("pack-hook", trust_source="pack", command="echo ok")])
        _run_hook_validate(config)
        out = capsys.readouterr().out
        assert "not executable" in out


# ---------------------------------------------------------------------------
# run_hook_validate_standalone — raw-YAML path catches invalid entries
# ---------------------------------------------------------------------------


class TestRunHookValidateStandalone:
    def _write_config(self, tmp_path: pytest.TempPathFactory, content: str) -> pytest.Path:
        p = tmp_path / "config.yaml"
        p.write_text(content)
        return p

    def test_empty_command_exits_one(self, tmp_path: pytest.TempPathFactory) -> None:
        """Empty runner.command is caught before config load and reported per-hook."""
        import yaml

        from anteroom.cli.hook_cli import run_hook_validate_standalone

        cfg_path = self._write_config(
            tmp_path,
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost", "api_key": "test"},
                    "hooks": {
                        "pre_tool": [
                            {"id": "bad-hook", "runner": {"type": "command", "command": ""}},
                        ]
                    },
                }
            ),
        )
        with patch("anteroom.config._get_config_path", return_value=cfg_path):
            with pytest.raises(SystemExit) as exc_info:
                run_hook_validate_standalone()
        assert exc_info.value.code == 1

    def test_unknown_runner_type_exits_one(self, tmp_path: pytest.TempPathFactory) -> None:
        """Unknown runner type is caught before config load and reported per-hook."""
        import yaml

        from anteroom.cli.hook_cli import run_hook_validate_standalone

        cfg_path = self._write_config(
            tmp_path,
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost", "api_key": "test"},
                    "hooks": {
                        "pre_tool": [
                            {"id": "grpc-hook", "runner": {"type": "grpc"}},
                        ]
                    },
                }
            ),
        )
        with patch("anteroom.config._get_config_path", return_value=cfg_path):
            with pytest.raises(SystemExit) as exc_info:
                run_hook_validate_standalone()
        assert exc_info.value.code == 1

    def test_no_config_file_exits_zero(self, tmp_path: pytest.TempPathFactory) -> None:
        """Missing config file exits cleanly (no hooks to validate)."""
        from anteroom.cli.hook_cli import run_hook_validate_standalone

        missing = tmp_path / "config.yaml"
        with patch("anteroom.config._get_config_path", return_value=missing):
            with patch("anteroom.services.team_config.discover_team_config", return_value=None):
                run_hook_validate_standalone()  # should not raise

    def test_team_config_invalid_hook_exits_one(self, tmp_path: pytest.TempPathFactory) -> None:
        """Invalid hook in team config is caught even when personal config is valid."""
        import yaml

        from anteroom.cli.hook_cli import run_hook_validate_standalone

        # Valid personal config with no hooks.
        personal_path = self._write_config(
            tmp_path,
            yaml.dump({"ai": {"base_url": "http://localhost", "api_key": "test"}}),
        )
        # Team config with an invalid runner type.
        team_path = tmp_path / "team.yaml"
        team_path.write_text(yaml.dump({"hooks": {"pre_tool": [{"id": "grpc-hook", "runner": {"type": "grpc"}}]}}))
        with patch("anteroom.config._get_config_path", return_value=personal_path):
            with patch("anteroom.services.team_config.discover_team_config", return_value=team_path):
                with patch(
                    "anteroom.services.team_config.load_team_config",
                    return_value=({"hooks": {"pre_tool": [{"id": "grpc-hook", "runner": {"type": "grpc"}}]}}, []),
                ):
                    with pytest.raises(SystemExit) as exc_info:
                        run_hook_validate_standalone()
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# _run_hook_replay
# ---------------------------------------------------------------------------


class TestRunHookReplay:
    def test_invalid_event_exits_one(self) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config()
        args = _replay_args(event="bad_event")
        with pytest.raises(SystemExit) as exc_info:
            _run_hook_replay(config, args)
        assert exc_info.value.code == 1

    def test_invalid_json_args_exits_one(self) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config()
        args = _replay_args(arguments="not json")
        with pytest.raises(SystemExit) as exc_info:
            _run_hook_replay(config, args)
        assert exc_info.value.code == 1

    def test_non_dict_json_args_exits_one(self) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config()
        args = _replay_args(arguments="null")
        with pytest.raises(SystemExit) as exc_info:
            _run_hook_replay(config, args)
        assert exc_info.value.code == 1

    def test_non_dict_json_output_exits_one(self) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config()
        args = _replay_args(event="post_tool", output="[1, 2]")
        with pytest.raises(SystemExit) as exc_info:
            _run_hook_replay(config, args)
        assert exc_info.value.code == 1

    def test_invalid_json_output_exits_one(self) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config()
        args = _replay_args(event="post_tool", output="not json")
        with pytest.raises(SystemExit) as exc_info:
            _run_hook_replay(config, args)
        assert exc_info.value.code == 1

    def test_no_hooks_prints_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config()
        args = _replay_args()
        _run_hook_replay(config, args)
        out = capsys.readouterr().out
        assert "No hooks configured" in out

    def test_allow_result_printed(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config(pre=[make_entry("h1", command="echo ok")])
        args = _replay_args()

        with patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = HookDecision(outcome="allow", hook_id="h1")
            _run_hook_replay(config, args)

        out = capsys.readouterr().out
        assert "allow" in out

    def test_deny_result_printed(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config(pre=[make_entry("h1", command="echo ok")])
        args = _replay_args()

        with patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = HookDecision(outcome="deny", message="blocked", hook_id="h1")
            _run_hook_replay(config, args)

        out = capsys.readouterr().out
        assert "deny" in out

    def test_pack_hook_shown_as_skipped(self, capsys: pytest.CaptureFixture[str]) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config(pre=[make_entry("pack-hook", trust_source="pack")])
        args = _replay_args()
        _run_hook_replay(config, args)
        out = capsys.readouterr().out
        assert "pack" in out

    def test_dry_run_no_audit_emitted(self) -> None:
        from anteroom.cli.hook_cli import _run_hook_replay

        config = _make_config(pre=[make_entry("h1", command="echo ok")])
        args = _replay_args()

        with (
            patch("anteroom.services.hooks.run_command_hook", new_callable=AsyncMock) as mock_run,
            patch("anteroom.services.hooks._emit_hook_audit") as mock_audit,
        ):
            mock_run.return_value = HookDecision(outcome="allow", hook_id="h1")
            _run_hook_replay(config, args)

        mock_audit.assert_not_called()


# ---------------------------------------------------------------------------
# _run_hook dispatch
# ---------------------------------------------------------------------------


class TestRunHookDispatch:
    def test_unknown_action_exits_one(self) -> None:
        from anteroom.cli.hook_cli import _run_hook

        config = _make_config()
        args = argparse.Namespace(hook_action="unknown")
        with pytest.raises(SystemExit) as exc_info:
            _run_hook(config, args)
        assert exc_info.value.code == 1

    def test_none_action_exits_one(self) -> None:
        from anteroom.cli.hook_cli import _run_hook

        config = _make_config()
        args = argparse.Namespace(hook_action=None)
        with pytest.raises(SystemExit) as exc_info:
            _run_hook(config, args)
        assert exc_info.value.code == 1
