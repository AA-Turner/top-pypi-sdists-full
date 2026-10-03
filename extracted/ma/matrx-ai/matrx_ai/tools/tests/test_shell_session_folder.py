"""The shell is a session: ``cd`` in one shell_execute call carries into the next (SPEC §6.1 parity).

The sandbox daemon (cloud, per sandbox) and the Matrx 2 core (desktop, per ``cwd_key``) both run a
command with NO cwd in the folder the previous command ended in, and a command WITH a cwd there.
So the tools must send a cwd only when the agent names one. Until 2026-10-02 shell_execute sent the
workspace root on every call (and shell_python reset the folder to the root), so ``cd`` never stuck.
The end-to-end proof against both real daemons is the live parity run
(aidream/services/sandboxes/tests/test_sandbox_parity_live.py, test_desktop_tools_live.py).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.tools import _sandbox_proxy as sp
from matrx_ai.tools.implementations import shell

pytestmark = pytest.mark.asyncio

BINDING = SimpleNamespace(root_path="/Users/pat", target_kind="local_machine")
CTX = SimpleNamespace(
    call_id="call-1", tool_name="shell_execute", conversation_id="conv-1", user_id="u-1"
)


@pytest.fixture
def sent(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []

    async def fake_exec(_binding: Any, command: str, **kw: Any) -> dict[str, Any]:
        calls.append({"command": command, **kw})
        return {"exit_code": 0, "stdout": "", "stderr": "", "cwd": "/Users/pat/src"}

    async def no_log(**_kw: Any) -> None:
        return None

    monkeypatch.setattr(shell, "get_active_sandbox", lambda: BINDING)
    monkeypatch.setattr(shell, "_proxy_exec", fake_exec)
    monkeypatch.setattr(shell, "write_tool_call_log", no_log)
    return calls


async def test_no_working_dir_runs_where_the_last_command_ended(sent: list[dict[str, Any]]) -> None:
    r = await shell.shell_execute({"command": "pwd"}, CTX)
    assert sent[-1]["cwd"] is None
    assert r.output["cwd"] == "/Users/pat/src"  # the daemon's word on where the session now is


async def test_a_named_folder_wins(sent: list[dict[str, Any]]) -> None:
    await shell.shell_execute({"command": "ls", "working_dir": "/tmp/x"}, CTX)
    assert sent[-1]["cwd"] == "/tmp/x"
    await shell.shell_execute({"command": "ls", "working_dir": "C:/Users/pat/x"}, CTX)
    assert sent[-1]["cwd"] == "C:/Users/pat/x"
    await shell.shell_execute({"command": "ls", "working_dir": "proj"}, CTX)
    assert sent[-1]["cwd"] == "/Users/pat/proj"


async def test_python_runs_in_the_session_folder_and_never_resets_it(
    sent: list[dict[str, Any]],
) -> None:
    await shell.shell_python(
        {"code": "print(1)"}, SimpleNamespace(**{**vars(CTX), "tool_name": "shell_python"})
    )
    assert sent[-1]["cwd"] is None


async def test_the_session_key_is_the_conversation(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_connect

    ctx = SimpleNamespace(
        conversation_id="conv-9", request_id="req-1", execution_id=None, user_id=None
    )
    monkeypatch.setattr(matrx_connect, "try_get_app_context", lambda: ctx)
    binding = sp.SandboxBinding(
        "dev", "https://x/api/local-proxy/1", "t", "/Users/pat", "local_machine"
    )
    assert sp._headers(binding)[sp.SHELL_SESSION_HEADER] == "conv-9"
    ctx.conversation_id = None
    assert sp._headers(binding)[sp.SHELL_SESSION_HEADER] == "req-1"
