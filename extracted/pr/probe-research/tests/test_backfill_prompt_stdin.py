"""The prompt reaches the agent on STDIN, at any size.

This is the other half of `test_backfill_agent_argv`: that file proves the
prompt is not IN the argv, this one proves it still arrives. Both are needed --
dropping the prompt from the argv without wiring stdin would pass every
argv-shaped assertion and run every agent against an empty instruction.

The child here is a real `/bin/sh` script rather than a mock, because the thing
under test is the kernel's execve limit and a mock cannot fail an exec.
"""

from __future__ import annotations

import os

import pytest

from probe.cli import backfill


@pytest.fixture
def echoing_agent(tmp_path):
    """An 'agent' that copies its stdin to a file, then emits one event."""
    seen = tmp_path / "seen.txt"
    binary = tmp_path / "fake-agent"
    binary.write_text(
        "#!/bin/sh\n"
        f"cat > {seen}\n"
        'printf \'{"type":"turn.started"}\\n\'\n'
    )
    binary.chmod(0o755)
    return binary, seen


def _launch(binary, prompt, tmp_path, monkeypatch):
    monkeypatch.setattr(backfill, "which_agent", lambda _agent: str(binary))
    monkeypatch.setattr(backfill, "supported_flags", lambda *_a, **_k: frozenset())
    folder = tmp_path / "folder"
    folder.mkdir(exist_ok=True)
    return backfill.launch_agent(folder, prompt, progress=False, stream=None)


def test_the_agent_receives_the_prompt_on_stdin(echoing_agent, tmp_path, monkeypatch):
    binary, seen = echoing_agent
    _launch(binary, "CLASSIFY THIS FOLDER", tmp_path, monkeypatch)
    assert seen.read_text() == "CLASSIFY THIS FOLDER"


def test_a_prompt_far_past_the_exec_ceiling_survives(echoing_agent, tmp_path, monkeypatch):
    """290KB: the measured size of a real single-shot classification prompt,
    2.2x the per-element execve limit. As an argv element this was E2BIG."""
    prompt = "x" * 290_000
    assert len(prompt) > backfill.MAX_ARG_STRLEN * 2
    binary, seen = echoing_agent
    ok, _tail = _launch(binary, prompt, tmp_path, monkeypatch)
    assert ok, "the launch must not fail the way it did when the prompt was argv"
    assert seen.read_text() == prompt


def test_a_multibyte_prompt_survives_intact(echoing_agent, tmp_path, monkeypatch):
    """Encoding is explicit UTF-8 at the write, so a research folder full of
    accented paths and CJK samples round-trips rather than raising."""
    prompt = "héllo 世界 " * 20_000
    binary, seen = echoing_agent
    _launch(binary, prompt, tmp_path, monkeypatch)
    assert seen.read_text(encoding="utf-8") == prompt


def test_the_prompt_file_is_not_left_behind(echoing_agent, tmp_path, monkeypatch):
    """An unnamed temp file, so a long import does not accumulate one staged
    prompt per unit in the state directory."""
    binary, _seen = echoing_agent
    before = len(os.listdir("/tmp"))
    for _ in range(3):
        _launch(binary, "p" * 200_000, tmp_path, monkeypatch)
    assert len(os.listdir("/tmp")) <= before + 1, "prompt files are unlinked on close"


def test_a_missing_binary_reports_instead_of_raising(tmp_path, monkeypatch):
    """The failure path still closes the staged prompt; it must not leak an
    open file handle or turn an ordinary 'not installed' into a traceback."""
    monkeypatch.setattr(backfill, "which_agent", lambda _agent: None)
    ok, message = backfill.launch_agent(tmp_path, "p", progress=False)
    assert ok is False and "not on PATH" in message
