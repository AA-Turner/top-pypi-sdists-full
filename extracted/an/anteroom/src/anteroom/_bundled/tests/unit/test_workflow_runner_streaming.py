"""Tests for incremental transcript streaming in opaque runners (#1117).

Verifies that transcript_stdout/transcript_stderr events are emitted
per-line during execution, not buffered until process exit.
"""

from __future__ import annotations

from typing import Any

import pytest

from anteroom.services.workflow_runners import execute_opaque_runner


class TestOpaqueRunnerIncrementalTranscript:
    """Tests for per-line transcript emission during opaque runner execution."""

    @pytest.mark.asyncio
    async def test_stdout_emitted_per_line(self) -> None:
        """Each line of stdout triggers a separate transcript_stdout callback."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        result = await execute_opaque_runner(
            mode="shell",
            command="echo line1 && echo line2 && echo line3",
            timeout=10,
            transcript_cb=cb,
            step_id="test_step",
        )

        assert result.status == "success"
        stdout_events = [(e, s, p) for e, s, p in events if e == "transcript_stdout"]
        assert len(stdout_events) == 3
        assert stdout_events[0][2]["content"] == "line1"
        assert stdout_events[1][2]["content"] == "line2"
        assert stdout_events[2][2]["content"] == "line3"
        # All events tied to the correct step_id
        assert all(s == "test_step" for _, s, _ in stdout_events)

    @pytest.mark.asyncio
    async def test_stderr_emitted_per_line(self) -> None:
        """Each line of stderr triggers a separate transcript_stderr callback."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        await execute_opaque_runner(
            mode="shell",
            command="echo err1 >&2 && echo err2 >&2",
            timeout=10,
            transcript_cb=cb,
            step_id="test_step",
        )

        stderr_events = [(e, s, p) for e, s, p in events if e == "transcript_stderr"]
        assert len(stderr_events) == 2
        assert stderr_events[0][2]["content"] == "err1"
        assert stderr_events[1][2]["content"] == "err2"

    @pytest.mark.asyncio
    async def test_mixed_stdout_stderr(self) -> None:
        """Both stdout and stderr events are emitted during the same run."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        result = await execute_opaque_runner(
            mode="shell",
            command="echo out1 && echo err1 >&2 && echo out2",
            timeout=10,
            transcript_cb=cb,
            step_id="mixed",
        )

        assert result.status == "success"
        stdout_events = [p for e, _, p in events if e == "transcript_stdout"]
        stderr_events = [p for e, _, p in events if e == "transcript_stderr"]
        assert len(stdout_events) == 2
        assert len(stderr_events) == 1
        assert stdout_events[0]["content"] == "out1"
        assert stdout_events[1]["content"] == "out2"
        assert stderr_events[0]["content"] == "err1"

    @pytest.mark.asyncio
    async def test_no_callback_no_error(self) -> None:
        """Runs without transcript_cb still work correctly."""
        result = await execute_opaque_runner(
            mode="shell",
            command="echo hello",
            timeout=10,
            transcript_cb=None,
        )
        assert result.status == "success"
        assert "hello" in result.summary

    @pytest.mark.asyncio
    async def test_truncation_per_line(self) -> None:
        """Individual lines are truncated to max_stdout_chars."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        # Emit a line longer than the limit
        result = await execute_opaque_runner(
            mode="shell",
            command="python3 -c \"print('x' * 200)\"",
            timeout=10,
            transcript_cb=cb,
            transcript_max_stdout_chars=50,
            step_id="trunc",
        )

        assert result.status == "success"
        stdout_events = [p for e, _, p in events if e == "transcript_stdout"]
        assert len(stdout_events) == 1
        assert len(stdout_events[0]["content"]) == 50

    @pytest.mark.asyncio
    async def test_exec_mode_incremental(self, tmp_path: Any) -> None:
        """Python script runner also emits per-line transcript events."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        script = tmp_path / "multi_line.py"
        script.write_text("print('a')\nprint('b')\nimport sys; print('c', file=sys.stderr)")

        result = await execute_opaque_runner(
            mode="exec",
            command=str(script),
            timeout=10,
            transcript_cb=cb,
            step_id="exec_step",
        )

        assert result.status == "success"
        stdout_events = [p for e, _, p in events if e == "transcript_stdout"]
        stderr_events = [p for e, _, p in events if e == "transcript_stderr"]
        assert len(stdout_events) == 2
        assert stdout_events[0]["content"] == "a"
        assert stdout_events[1]["content"] == "b"
        assert len(stderr_events) == 1
        assert stderr_events[0]["content"] == "c"

    @pytest.mark.asyncio
    async def test_exec_mode_sets_pythonunbuffered(self, tmp_path: Any) -> None:
        """Python script runners inherit PYTHONUNBUFFERED=1 by default."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        script = tmp_path / "show_unbuffered.py"
        script.write_text("import os\nprint(os.getenv('PYTHONUNBUFFERED', 'missing'))\n")

        result = await execute_opaque_runner(
            mode="exec",
            command=str(script),
            timeout=10,
            transcript_cb=cb,
            step_id="env_step",
        )

        assert result.status == "success"
        stdout_events = [p for e, _, p in events if e == "transcript_stdout"]
        assert stdout_events == [{"content": "1"}]

    @pytest.mark.asyncio
    async def test_empty_output_no_events(self) -> None:
        """No transcript events emitted for empty stdout/stderr."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        result = await execute_opaque_runner(
            mode="shell",
            command="true",
            timeout=10,
            transcript_cb=cb,
            step_id="empty",
        )

        assert result.status == "success"
        assert len(events) == 0

    @pytest.mark.asyncio
    async def test_timeout_during_streaming(self) -> None:
        """Timeout kills process and returns failed even with streaming."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        result = await execute_opaque_runner(
            mode="shell",
            command="echo before_timeout && sleep 60",
            timeout=2,
            transcript_cb=cb,
            step_id="timeout_step",
        )

        assert result.status == "failed"
        assert "timed out" in result.summary.lower()
        # May have emitted some events before timeout
        stdout_events = [e for e in events if e[0] == "transcript_stdout"]
        assert len(stdout_events) >= 1
        assert stdout_events[0][2]["content"] == "before_timeout"

    @pytest.mark.asyncio
    async def test_invalid_working_dir(self) -> None:
        """Invalid working_dir returns failed without streaming."""
        events: list[tuple[str, str | None, dict[str, Any]]] = []

        def cb(etype: str, sid: str | None, payload: dict[str, Any]) -> None:
            events.append((etype, sid, payload))

        result = await execute_opaque_runner(
            mode="shell",
            command="echo hello",
            working_dir="/nonexistent/path/that/does/not/exist",
            timeout=10,
            transcript_cb=cb,
            step_id="bad_dir",
        )

        assert result.status == "failed"
        assert "does not exist" in result.summary
        assert len(events) == 0
