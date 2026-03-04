from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from plato.utils import subprocess as subprocess_utils


class _DummyProc:
    def __init__(self, *, returncode: int = 0, stdout: bytes = b"", stderr: bytes = b"") -> None:
        self.returncode = returncode
        self._stdout = stdout
        self._stderr = stderr
        self.stdout = None

    async def communicate(self) -> tuple[bytes, bytes]:
        return self._stdout, self._stderr


class _LineReader:
    def __init__(self, lines: list[bytes]) -> None:
        self._lines = list(lines)

    async def readline(self) -> bytes:
        if self._lines:
            return self._lines.pop(0)
        return b""


class _StreamingProc:
    def __init__(self, *, returncode: int = 0, lines: list[bytes] | None = None) -> None:
        self.returncode = returncode
        self.stdout = _LineReader(lines or [])

    async def wait(self) -> int:
        return self.returncode


@pytest.mark.asyncio
async def test_run_ssh_quotes_non_root_command_without_outer_expansion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    async def fake_create_subprocess_exec(*args, **kwargs):  # noqa: ANN001
        captured["args"] = args
        captured["kwargs"] = kwargs
        return _DummyProc()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

    command = 'for i in $(seq 1 3); do echo "$i"; done'
    exit_code, _stdout, _stderr = await subprocess_utils.run_ssh(
        Path("/tmp/fake-key"),
        "10.0.0.1",
        command,
        user="superman",
    )

    assert exit_code == 0
    args = captured["args"]
    assert isinstance(args, tuple)
    wrapped = str(args[-1])
    assert wrapped == "sudo -u superman -- bash -c 'for i in $(seq 1 3); do echo \"$i\"; done'"
    assert "$(seq 1 3)" in wrapped
    assert "\n2\n" not in wrapped


@pytest.mark.asyncio
async def test_run_ssh_streaming_quotes_non_root_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    async def fake_create_subprocess_exec(*args, **kwargs):  # noqa: ANN001
        captured["args"] = args
        captured["kwargs"] = kwargs
        return _StreamingProc(lines=[b"line\n"])

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

    command = 'echo "$(date)"'
    exit_code = await subprocess_utils.run_ssh_streaming(
        Path("/tmp/fake-key"),
        "10.0.0.1",
        command,
        user="superman",
    )

    assert exit_code == 0
    args = captured["args"]
    assert isinstance(args, tuple)
    wrapped = str(args[-1])
    assert wrapped == "sudo -u superman -- bash -c 'echo \"$(date)\"'"
    assert "$(date)" in wrapped
