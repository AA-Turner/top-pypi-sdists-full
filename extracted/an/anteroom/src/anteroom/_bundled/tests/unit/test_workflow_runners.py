"""Tests for workflow runner execution and normalization.

Tests both agent and opaque runners to prove they are equally first-class.
Uses domain-neutral test data — no GitHub/PR-specific concepts.
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.workflow_runners import (
    RunnerRegistry,
    RunnerResult,
    _kill_subprocess,
    create_default_registry,
    execute_agent_runner,
    execute_opaque_runner,
)


class TestRunnerRegistry:
    def test_default_registry_has_four_types(self) -> None:
        reg = create_default_registry()
        runners = reg.list_runners()
        assert len(runners) == 4
        assert runners["cli_claude"] == "agent"
        assert runners["cli_codex"] == "agent"
        assert runners["shell"] == "opaque"
        assert runners["python_script"] == "opaque"

    def test_custom_runner_registration(self) -> None:
        reg = RunnerRegistry()
        reg.register("my_runner", "opaque")
        assert reg.is_opaque_runner("my_runner")
        assert not reg.is_agent_runner("my_runner")

    def test_invalid_category_raises(self) -> None:
        reg = RunnerRegistry()
        with pytest.raises(ValueError, match="Invalid runner category"):
            reg.register("bad", "unknown")


class TestRunnerResult:
    def test_to_dict(self) -> None:
        r = RunnerResult(
            status="success",
            summary="Done",
            artifacts={"count": 5},
            findings=[{"type": "info"}],
            duration_ms=100,
        )
        d = r.to_dict()
        assert d["status"] == "success"
        assert d["artifacts"]["count"] == 5
        assert d["duration_ms"] == 100

    def test_frozen(self) -> None:
        r = RunnerResult(status="success")
        with pytest.raises(AttributeError):
            r.status = "failed"  # type: ignore[misc]


class TestOpaqueRunnerStdinClosed:
    """Regression tests for #1298: opaque runner must close stdin."""

    @pytest.mark.asyncio
    async def test_shell_mode_stdin_is_devnull(self) -> None:
        """Shell subprocess cannot read from stdin (it is /dev/null)."""
        import sys

        check = f"{sys.executable} -c \"import sys; data=sys.stdin.read(); print(f'stdin_len={{len(data)}}')\""
        result = await execute_opaque_runner(mode="shell", command=check, timeout=5)
        assert result.status == "success"
        assert "stdin_len=0" in result.summary

    @pytest.mark.asyncio
    async def test_exec_mode_stdin_is_devnull(self, tmp_path: Any) -> None:
        """Exec subprocess cannot read from stdin (it is /dev/null)."""
        script = tmp_path / "check_stdin.py"
        script.write_text("import sys; data=sys.stdin.read(); print(f'stdin_len={len(data)}')")
        result = await execute_opaque_runner(mode="exec", command=str(script), timeout=5)
        assert result.status == "success"
        assert "stdin_len=0" in result.summary


class TestOpaqueRunner:
    @pytest.mark.asyncio
    async def test_shell_echo(self) -> None:
        """Shell runner executes a command and returns stdout as summary."""
        result = await execute_opaque_runner(
            mode="shell",
            command="echo hello world",
            timeout=10,
        )
        assert result.status == "success"
        assert "hello world" in result.summary
        assert result.artifacts.get("exit_code") == 0

    @pytest.mark.asyncio
    async def test_shell_failure(self) -> None:
        """Shell runner returns failed on non-zero exit code."""
        result = await execute_opaque_runner(
            mode="shell",
            command="exit 1",
            timeout=10,
        )
        assert result.status == "failed"
        assert result.artifacts.get("exit_code") == 1

    @pytest.mark.asyncio
    async def test_shell_timeout(self) -> None:
        """Shell runner kills process on timeout."""
        result = await execute_opaque_runner(
            mode="shell",
            command="sleep 60",
            timeout=1,
        )
        assert result.status == "failed"
        assert "timed out" in result.summary.lower()

    @pytest.mark.asyncio
    async def test_shell_stderr_in_findings(self) -> None:
        """Stderr captured in findings for successful commands."""
        result = await execute_opaque_runner(
            mode="shell",
            command="echo output && echo warning >&2",
            timeout=10,
        )
        assert result.status == "success"
        if result.findings:
            assert any("warning" in str(f) for f in result.findings)

    @pytest.mark.asyncio
    async def test_shell_empty_output(self) -> None:
        """Empty output returns success with default summary."""
        result = await execute_opaque_runner(
            mode="shell",
            command="true",
            timeout=10,
        )
        assert result.status == "success"
        assert result.summary  # should have a default, not empty

    @pytest.mark.asyncio
    async def test_exec_mode_python_script(self, tmp_path: Any) -> None:
        """Python script runner executes via create_subprocess_exec."""
        script = tmp_path / "test_script.py"
        script.write_text("import sys; print('hello from script'); sys.exit(0)")
        result = await execute_opaque_runner(
            mode="exec",
            command=str(script),
            timeout=10,
        )
        assert result.status == "success"
        assert "hello from script" in result.summary

    @pytest.mark.asyncio
    async def test_exec_mode_with_argv(self, tmp_path: Any) -> None:
        """Python script runner passes argv correctly."""
        script = tmp_path / "args_script.py"
        script.write_text("import sys; print(' '.join(sys.argv[1:]))")
        result = await execute_opaque_runner(
            mode="exec",
            command=str(script),
            argv=["arg1", "arg2"],
            timeout=10,
        )
        assert result.status == "success"
        assert "arg1 arg2" in result.summary

    @pytest.mark.asyncio
    async def test_exec_mode_failure(self, tmp_path: Any) -> None:
        """Python script runner returns failed on non-zero exit."""
        script = tmp_path / "fail_script.py"
        script.write_text("import sys; print('error msg', file=sys.stderr); sys.exit(1)")
        result = await execute_opaque_runner(
            mode="exec",
            command=str(script),
            timeout=10,
        )
        assert result.status == "failed"
        assert "error msg" in result.summary

    @pytest.mark.asyncio
    async def test_invalid_mode_raises(self) -> None:
        """Unknown mode raises ValueError."""
        result = await execute_opaque_runner(
            mode="unknown",
            command="echo",
            timeout=10,
        )
        assert result.status == "failed"
        assert "Unknown" in result.summary

    @pytest.mark.asyncio
    async def test_env_vars_passed(self) -> None:
        """Additional env vars are available in the subprocess."""
        result = await execute_opaque_runner(
            mode="shell",
            command="echo $MY_TEST_VAR",
            env={"MY_TEST_VAR": "hello_env"},
            timeout=10,
        )
        assert result.status == "success"
        assert "hello_env" in result.summary


class TestAgentRunner:
    @pytest.mark.asyncio
    async def test_no_ai_service_raises(self) -> None:
        """Agent runner without AI service raises RuntimeError."""
        with pytest.raises(RuntimeError, match="ai_service"):
            await execute_agent_runner(prompt="Do something", timeout=10)

    @pytest.mark.asyncio
    async def test_uses_workflow_agent_iteration_cap(self) -> None:
        """Workflow agent runner falls back to the default iteration cap."""
        captured_kwargs: dict[str, Any] = {}

        async def _fake_run_agent_loop(**kwargs: Any):
            captured_kwargs.update(kwargs)
            yield type("Evt", (), {"kind": "done", "data": {}})()

        with patch("anteroom.services.agent_loop.run_agent_loop", _fake_run_agent_loop):
            result = await execute_agent_runner(
                prompt="Inspect and implement",
                timeout=10,
                ai_service=object(),
                tool_executor=lambda *_a, **_k: None,
            )

        assert result.status == "success"
        assert captured_kwargs["max_iterations"] == 30

    @pytest.mark.asyncio
    async def test_uses_configured_workflow_agent_iteration_cap(self) -> None:
        """Workflow agent runner accepts an explicit iteration cap."""
        captured_kwargs: dict[str, Any] = {}

        async def _fake_run_agent_loop(**kwargs: Any):
            captured_kwargs.update(kwargs)
            yield type("Evt", (), {"kind": "done", "data": {}})()

        with patch("anteroom.services.agent_loop.run_agent_loop", _fake_run_agent_loop):
            result = await execute_agent_runner(
                prompt="Inspect and implement",
                timeout=10,
                max_iterations=42,
                ai_service=object(),
                tool_executor=lambda *_a, **_k: None,
            )

        assert result.status == "success"
        assert captured_kwargs["max_iterations"] == 42

    @pytest.mark.asyncio
    async def test_prompt_transcript_emitted_before_agent_events(self) -> None:
        """Agent runner emits a prompt preview before tool/assistant transcript events."""
        transcript_events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            transcript_events.append((etype, sid, payload))

        async def _fake_run_agent_loop(**_kwargs: Any):
            yield type("Evt", (), {"kind": "done", "data": {}})()

        with patch("anteroom.services.agent_loop.run_agent_loop", _fake_run_agent_loop):
            result = await execute_agent_runner(
                prompt="Inspect the workflow and explain the current step.",
                timeout=10,
                ai_service=object(),
                tool_executor=lambda *_a, **_k: None,
                transcript_cb=cb,
                step_id="agent_step",
            )

        assert result.status == "success"
        assert transcript_events[0][0] == "transcript_prompt"
        assert transcript_events[0][2]["content"] == "Inspect the workflow and explain the current step."

    @pytest.mark.asyncio
    async def test_tool_result_transcript_preserves_dict_shape(self) -> None:
        """Agent runner should keep structured tool outputs for generic transcript compaction."""
        transcript_events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            transcript_events.append((etype, sid, payload))

        async def _fake_run_agent_loop(**_kwargs: Any):
            yield type(
                "Evt",
                (),
                {
                    "kind": "tool_call_end",
                    "data": {
                        "tool_name": "read_file",
                        "status": "success",
                        "output": {
                            "path": "/tmp/example.py",
                            "content": "x" * 5000,
                            "meta": {"note": "y" * 5000},
                        },
                    },
                },
            )()

        with patch("anteroom.services.agent_loop.run_agent_loop", _fake_run_agent_loop):
            result = await execute_agent_runner(
                prompt="Inspect file",
                timeout=10,
                ai_service=object(),
                tool_executor=lambda *_a, **_k: None,
                transcript_cb=cb,
                transcript_max_tool_output_chars=120,
                step_id="agent_step",
            )

        assert result.status == "success"
        tool_events = [payload for etype, _, payload in transcript_events if etype == "transcript_tool_result"]
        assert len(tool_events) == 1
        payload = tool_events[0]
        assert isinstance(payload["output"], dict)
        assert payload["output"]["path"] == "/tmp/example.py"
        assert len(payload["output"]["content"]) == 120
        assert len(payload["output"]["meta"]["note"]) == 120


# ---------------------------------------------------------------------------
# Subprocess teardown on cancellation (#1149)
# ---------------------------------------------------------------------------


class TestOpaqueRunnerCancellation:
    """Verify subprocess cleanup when the runner task is cancelled (Ctrl-C)."""

    @pytest.mark.asyncio
    async def test_opaque_runner_kills_subprocess_on_cancel(self) -> None:
        """Subprocess is killed when CancelledError propagates through the runner."""
        task = asyncio.ensure_future(execute_opaque_runner(mode="shell", command="sleep 60", timeout=300))
        await asyncio.sleep(0.3)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    @pytest.mark.asyncio
    async def test_opaque_runner_cancellation_propagates(self) -> None:
        """CancelledError re-raises after subprocess cleanup, not swallowed."""
        task = asyncio.ensure_future(execute_opaque_runner(mode="shell", command="sleep 60", timeout=300))
        await asyncio.sleep(0.3)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    @pytest.mark.asyncio
    async def test_opaque_runner_already_exited_no_kill(self) -> None:
        """No kill attempt when process has already exited before cancellation."""
        proc_mock = MagicMock()
        proc_mock.returncode = 0
        proc_mock.pid = 12345
        proc_mock.kill = MagicMock()

        await _kill_subprocess(proc_mock)

        proc_mock.kill.assert_not_called()

    @pytest.mark.asyncio
    async def test_kill_subprocess_escalates_to_sigkill_on_timeout(self) -> None:
        """_kill_subprocess escalates to SIGKILL when SIGTERM doesn't stop the process."""
        proc_mock = MagicMock()
        proc_mock.returncode = None
        proc_mock.pid = 12345
        proc_mock.kill = MagicMock()

        call_count = 0

        async def _wait_side_effect() -> None:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                await asyncio.sleep(60)
            # Second call (after kill) returns immediately

        proc_mock.wait = _wait_side_effect

        with patch("anteroom.services.workflow_runners.os.killpg"):
            await _kill_subprocess(proc_mock)

        proc_mock.kill.assert_called_once()

    @pytest.mark.asyncio
    async def test_kill_subprocess_falls_back_on_killpg_failure(self) -> None:
        """_kill_subprocess falls back to proc.kill() when os.killpg fails."""
        proc_mock = MagicMock()
        proc_mock.returncode = None
        proc_mock.pid = 12345
        proc_mock.kill = MagicMock()

        wait_future: asyncio.Future[None] = asyncio.Future()
        wait_future.set_result(None)
        proc_mock.wait = AsyncMock(return_value=None)

        with patch(
            "anteroom.services.workflow_runners.os.killpg",
            side_effect=ProcessLookupError,
        ):
            await _kill_subprocess(proc_mock)

        proc_mock.kill.assert_called_once()
