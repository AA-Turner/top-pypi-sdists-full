"""A tool that needs the person's machine refuses honestly when it is down.

THE LIE THIS CLOSES. With no sandbox bound, ``shell_execute`` and the ``fs_*``
tools serve the durable-VFS emulator over the person's code library, and
``shell_python`` runs the script on the AIDREAM SERVER. For an ordinary
conversation those are the right answers: nobody attached a box, so there is no
box to be down.

For a Personal Staff person they are not. They have a machine, it is supposed
to be up, and a turn that quietly runs coreutils in an emulator while they
believe their own files are being read is the silent-degrade class the sandbox
hard-gate exists to prevent — reaching them through the one door that gate
cannot close, because a conversation with NO binding raises no refusal and
never should.

The host stamps ``workspace_outage`` on the run; these tools read it and return
one sentence written for a person instead of a substitute.

WHAT THE AST TEST IS FOR. Seven ``fs_*`` tools take the same fallback, and the
eighth one somebody adds next month will not remember this file exists. The
test walks ``filesystem.py`` and fails if any ``if _should_use_durable_vfs():``
branch does not check first.

Run: ``uv run pytest packages/matrx-ai/tests/test_a_tool_that_needs_the_box_says_so.py``
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.workspace_outage import (
    WORKSPACE_OUTAGE_KEY,
    active_workspace_outage,
    refuse_if_workspace_is_down,
)

SENTENCE = (
    "Your workspace is down right now and the platform is bringing it back. "
    "Until it is up I cannot run commands, read or write your files, or use "
    "your cloud browser — I can still answer questions, look things up on the "
    "web and take notes."
)


class _Ctx:
    """Only what the refusal reads."""

    call_id = "call-1"


class _AppContext:
    def __init__(self, metadata: dict):
        self.metadata = metadata


def _stamp(monkeypatch, metadata: dict | None) -> None:
    """Install an AppContext the tools' reader will find.

    Through ``sys.modules`` on ``matrx_connect``'s accessor, because building a
    real AppContext needs the host wired — which is the process-global leak the
    repo-root conftest warns about.
    """

    import sys
    import types

    monkeypatch.setitem(
        sys.modules,
        "matrx_connect",
        types.SimpleNamespace(
            try_get_app_context=lambda: (_AppContext(metadata) if metadata is not None else None)
        ),
    )


def test_no_stamp_means_carry_on(monkeypatch):
    """The overwhelmingly common answer, and it must change nothing.

    A bare matrx-ai install, and every conversation the host does not stamp,
    behaves exactly as it always has.
    """

    _stamp(monkeypatch, None)
    assert active_workspace_outage() is None
    assert refuse_if_workspace_is_down("shell_execute", _Ctx()) is None

    _stamp(monkeypatch, {})
    assert refuse_if_workspace_is_down("shell_execute", _Ctx()) is None


def test_a_stamp_with_no_sentence_is_ignored(monkeypatch):
    """This module never invents the words a person reads.

    The host owns the sentence. A stamp that carries none would otherwise make
    a tool refuse with something nobody decided to say.
    """

    _stamp(monkeypatch, {WORKSPACE_OUTAGE_KEY: {"status": "down"}})
    assert active_workspace_outage() is None
    assert refuse_if_workspace_is_down("shell_execute", _Ctx()) is None


def test_the_refusal_carries_the_host_sentence_verbatim(monkeypatch):
    """One sentence, for a person, naming what still works."""

    _stamp(
        monkeypatch,
        {
            WORKSPACE_OUTAGE_KEY: {
                "status": "resuming",
                "sentence": SENTENCE,
                "since": "2026-09-22T07:00:00+00:00",
            }
        },
    )
    result = refuse_if_workspace_is_down("shell_execute", _Ctx())

    assert result is not None
    assert result.success is False
    assert SENTENCE in result.error.message
    assert result.error.error_type == "unavailable"
    # The workspace is coming back; a later turn may well find it up.
    assert result.error.is_retryable is True
    # And the model is told to SAY it rather than route around it — an agent
    # handed a bare failure reaches for the next tool, and the person receives
    # a silent non-answer instead of the sentence somebody wrote for them.
    action = result.error.suggested_action.lower()
    assert "tell them" in action
    assert "do not" in action
    assert "imply the command ran" in action


@pytest.mark.asyncio
async def test_shell_execute_refuses_instead_of_using_the_emulator(monkeypatch):
    """The real tool, on the real fallback path."""

    from matrx_ai.tools.implementations import shell

    monkeypatch.setattr(shell, "sandbox_mode_active", lambda: False)
    monkeypatch.setattr(shell, "get_active_sandbox", lambda: None)
    # `has_durable_backend` is imported inside the function, so it is patched at
    # its source rather than on the shell module.
    monkeypatch.setattr(
        "matrx_ai.tools.vfs.workspace.has_durable_backend", lambda: True
    )

    used_the_emulator: list[str] = []

    async def _never(args, ctx):  # noqa: ARG001
        used_the_emulator.append("yes")
        raise AssertionError("the emulator answered for a machine that is down")

    import sys
    import types

    monkeypatch.setitem(
        sys.modules,
        "matrx_ai.tools.implementations.vfs_shell",
        types.SimpleNamespace(shell_execute=_never),
    )
    _stamp(monkeypatch, {WORKSPACE_OUTAGE_KEY: {"status": "down", "sentence": SENTENCE}})

    result = await shell.shell_execute({"command": "uname -a"}, ToolContext(call_id="c1"))

    assert used_the_emulator == []
    assert result.success is False
    assert SENTENCE in result.error.message


@pytest.mark.asyncio
async def test_fs_read_refuses_instead_of_serving_the_code_library(monkeypatch):
    from matrx_ai.tools.implementations import filesystem

    monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: True)

    import sys
    import types

    async def _never(args, ctx):  # noqa: ARG001
        raise AssertionError("the code library answered for a machine that is down")

    monkeypatch.setitem(
        sys.modules,
        "matrx_ai.tools.implementations.vfs_filesystem",
        types.SimpleNamespace(fs_read=_never),
    )
    _stamp(monkeypatch, {WORKSPACE_OUTAGE_KEY: {"status": "down", "sentence": SENTENCE}})

    result = await filesystem.fs_read(
        {"path": "/home/agent/notes.md"}, ToolContext(call_id="c1")
    )

    assert result.success is False
    assert SENTENCE in result.error.message


@pytest.mark.asyncio
async def test_shell_python_refuses_instead_of_running_on_the_server(monkeypatch):
    """The worse half of the same lie: a script reads and writes files."""

    from matrx_ai.tools.implementations import shell

    monkeypatch.setattr(shell, "get_active_sandbox", lambda: None)
    _stamp(monkeypatch, {WORKSPACE_OUTAGE_KEY: {"status": "down", "sentence": SENTENCE}})

    result = await shell.shell_python(
        {"code": "print('hello')"}, ToolContext(call_id="c1")
    )

    assert result.success is False
    assert SENTENCE in result.error.message


def test_every_durable_vfs_branch_checks_first():
    """🚨 THE FORCING FUNCTION FOR THE EIGHTH TOOL.

    Seven ``fs_*`` tools take the same fallback today. The next one somebody
    writes will copy a neighbour and will not remember this file exists — and
    the failure it reintroduces is SILENT, which is why a grep-shaped guard is
    worth more here than another behavioural test.
    """

    from matrx_ai.tools.implementations import filesystem

    source = Path(inspect.getsourcefile(filesystem)).read_text()
    tree = ast.parse(source)

    def _is_the_branch(node: ast.If) -> bool:
        test = node.test
        return (
            isinstance(test, ast.Call)
            and isinstance(test.func, ast.Name)
            and test.func.id == "_should_use_durable_vfs"
        )

    def _checks_first(node: ast.If) -> bool:
        return any(
            isinstance(inner, ast.Name) and inner.id == "_refuse_if_their_machine_is_down"
            for stmt in node.body[:2]
            for inner in ast.walk(stmt)
        )

    branches = [n for n in ast.walk(tree) if isinstance(n, ast.If) and _is_the_branch(n)]
    assert branches, "the durable-VFS branch has been renamed; this guard now proves nothing"

    unguarded = [n.lineno for n in branches if not _checks_first(n)]
    assert not unguarded, (
        "these durable-VFS fallbacks serve the emulator without first asking whether "
        f"the person's machine is DOWN (filesystem.py lines {unguarded}). A tool that "
        "substitutes for somebody's machine while they believe it ran there is the "
        "silent degrade the sandbox hard-gate exists to prevent."
    )
