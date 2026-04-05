"""Tests for _run_interruptibly() fallback path (no add_signal_handler).

Exercises the Windows-equivalent code path where add_signal_handler is
unavailable and KeyboardInterrupt must be caught on the fallback await.
"""

from __future__ import annotations

import asyncio
import os
import re
import signal
import subprocess
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

from anteroom.cli.workflow_cli import _run_interruptibly

# ---------------------------------------------------------------------------
# Unit tests: normal (non-interrupt) fallback behavior
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fallback_path_returns_result_without_interrupt() -> None:
    """When add_signal_handler is unavailable but no interrupt occurs,
    _run_interruptibly returns the result normally."""

    async def _return_value() -> str:
        return "done"

    loop = asyncio.get_running_loop()

    with patch.object(loop, "add_signal_handler", side_effect=NotImplementedError):
        result, interrupted = await _run_interruptibly(_return_value())

    assert result == "done"
    assert interrupted is False


@pytest.mark.asyncio
async def test_fallback_path_not_used_when_signal_handler_works() -> None:
    """When add_signal_handler succeeds, the signal-based path is used."""

    async def _return_value() -> str:
        return "done"

    result, interrupted = await _run_interruptibly(_return_value())

    assert result == "done"
    assert interrupted is False


# ---------------------------------------------------------------------------
# Integration test: interrupt on the fallback path
# ---------------------------------------------------------------------------

_PYTHON = sys.executable

_SLOW_WORKFLOW = """\
kind: workflow
id: test_slow
version: 0.1.0
inputs: {}
steps:
  - id: slow_step
    type: runner
    runner: shell
    command: "sleep 30"
    timeout: 60
"""


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    anteroom_dir = tmp_path / ".anteroom"
    anteroom_dir.mkdir()
    config_file = anteroom_dir / "config.yaml"
    config_file.write_text('ai:\n  base_url: "http://localhost:1/v1"\n  api_key: "test"\n  model: "test"\n')
    monkeypatch.setenv("HOME", str(tmp_path))


@pytest.mark.skipif(os.name == "nt", reason="Uses SIGINT; Windows variant is the code under test")
def test_interrupt_on_fallback_path_exits_cleanly(tmp_path: Path) -> None:
    """Force the non-add_signal_handler path via monkey-patch in a
    subprocess wrapper, send SIGINT, and verify the run pauses cleanly
    with resume guidance.

    Uses a thin wrapper script that patches add_signal_handler to raise
    NotImplementedError before running anteroom, simulating the Windows
    ProactorEventLoop behavior on a Unix host.
    """
    workflow_file = tmp_path / "slow.yaml"
    workflow_file.write_text(_SLOW_WORKFLOW)

    # Wrapper script that patches add_signal_handler at the event loop level
    wrapper = tmp_path / "run_patched.py"
    wrapper.write_text(
        textwrap.dedent(f"""\
        import asyncio
        import sys

        _orig_add = asyncio.SelectorEventLoop.add_signal_handler

        def _broken_add(self, *a, **kw):
            raise NotImplementedError("simulated Windows")

        asyncio.SelectorEventLoop.add_signal_handler = _broken_add

        sys.argv = ["aroom", "workflow", "run", "{workflow_file}"]
        from anteroom.__main__ import main
        main()
    """)
    )

    import threading

    proc = subprocess.Popen(
        [_PYTHON, str(wrapper)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    found = threading.Event()
    lines: list[str] = []

    def _reader() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            lines.append(line)
            if "slow_step" in line:
                found.set()
                return

    t = threading.Thread(target=_reader, daemon=True)
    t.start()
    assert found.wait(timeout=30), "Timed out waiting for step progress"

    proc.send_signal(signal.SIGINT)
    remainder, _ = proc.communicate(timeout=30)
    output = "".join(lines) + (remainder or "")

    # Should not have application-level tracebacks
    for line in output.splitlines():
        if line.strip().startswith("Traceback"):
            idx = output.splitlines().index(line)
            nearby = output.splitlines()[idx : idx + 5]
            assert not any("anteroom" in ln for ln in nearby), (
                f"Application traceback on fallback path:\\n{'chr(10)'.join(nearby)}"
            )

    assert "Workflow interrupted." in output

    match = re.search(r"Run ID:\s*([0-9a-f-]{36})", output)
    assert match, f"No Run ID in output: {output}"
    run_id = match.group(1)
    assert f"aroom workflow resume {run_id}" in output
