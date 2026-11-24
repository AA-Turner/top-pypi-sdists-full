"""Each conversation on a Cloud Computer works in its OWN folder (ruling 18, zone 2).

Use case: a bakery owner runs two chats on one machine — one drafts this week's price list,
the other cleans up a customer spreadsheet. Both agents write ``notes.txt`` with a relative
path. Before this change both landed in the machine's home and the second silently
overwrote the first. Now each chat's binding names its own working folder and every
relative path, folder-less command and Python script of that chat starts there; ``~/`` is
still the home (where the shared ``Cloud`` folder lives).

The machine here is a fake ``/agent`` door over a REAL temporary home: commands really run
in ``bash`` in the folder the tool sent (no folder = the home, exactly as the machine
worker's ``run_exec`` does), and files are really written. Only the network is replaced.
Break any of: the binding's ``working_dir`` read, ``_resolve_sandbox_path``'s anchor, or
the shell tools' default folder — and a test below fails.
"""

from __future__ import annotations

import json
import subprocess
import sys
import types
from pathlib import Path
from typing import Any

import httpx
import pytest

from matrx_ai.tools import _sandbox_proxy as proxy
from matrx_ai.tools.implementations import filesystem, shell
from matrx_ai.tools.models import ToolContext

pytestmark = pytest.mark.asyncio

CHAT_A = "aaaaaaaa-1111-4111-8111-111111111111"
CHAT_B = "bbbbbbbb-2222-4222-8222-222222222222"


class _Machine:
    """The machine worker's ``/agent`` door, over a real home folder."""

    def __init__(self, home: Path) -> None:
        self.home = home
        self.exec_cwds: list[str | None] = []

    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path.split("/agent", 1)[1]
        if path == "/exec":
            body = json.loads(request.content)
            self.exec_cwds.append(body.get("cwd"))
            cwd = body.get("cwd") or str(self.home)  # machine_agent.run_exec: no folder = home
            done = subprocess.run(
                ["bash", "-c", body["command"]], cwd=cwd, input=body.get("stdin"),
                capture_output=True, text=True, timeout=30,
            )
            return httpx.Response(
                200, json={"exit_code": done.returncode, "stdout": done.stdout,
                           "stderr": done.stderr, "cwd": cwd},
            )
        if path == "/fs/write":
            body = json.loads(request.content)
            target = Path(body["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body["content"], encoding="utf-8")
            return httpx.Response(200, json={"path": str(target), "size": target.stat().st_size})
        if path == "/fs/read":
            target = Path(request.url.params["path"])
            if not target.is_file():
                return httpx.Response(404, json={"detail": "not found"})
            text = target.read_text(encoding="utf-8")
            return httpx.Response(
                200, text=text,
                headers={"X-Matrx-File-Size": str(len(text.encode())),
                         "X-Matrx-Next-Offset": str(len(text.encode())),
                         "X-Matrx-Truncated": "false"},
            )
        if path == "/fs/mkdir":
            Path(json.loads(request.content)["path"]).mkdir(parents=True, exist_ok=True)
            return httpx.Response(200, json={})
        return httpx.Response(404, json={"detail": f"no route {path}"})


class _AppContext:
    def __init__(self, metadata: dict[str, Any], conversation_id: str | None) -> None:
        self.metadata = metadata
        self.conversation_id = conversation_id
        self.user_id = "user-1"
        self.request_id = f"req-{conversation_id}"
        self.execution_id = None


@pytest.fixture
def machine(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> _Machine:
    home = tmp_path / "home"
    (home / "Cloud").mkdir(parents=True)
    m = _Machine(home)
    real = httpx.AsyncClient
    monkeypatch.setattr(
        proxy.httpx, "AsyncClient", lambda **kw: real(transport=httpx.MockTransport(m.handle), **kw)
    )

    async def _no_emit(**_: Any) -> None:
        return None

    monkeypatch.setattr(filesystem, "emit_fs_changed", _no_emit)
    monkeypatch.setattr(filesystem, "_should_use_durable_vfs", lambda: False)
    return m


def _in_chat(monkeypatch: pytest.MonkeyPatch, machine: _Machine, conversation_id: str | None) -> Path | None:
    """Arm the run exactly as the host does: ``ctx.metadata["active_sandbox"]``."""
    working = machine.home / "Work" / conversation_id if conversation_id else None
    if working is not None:
        working.mkdir(parents=True, exist_ok=True)  # the host creates it at binding time
    binding = {
        "sandbox_id": "cc-bakery",
        "base_url": "http://10.0.0.5:8002/agent",
        "access_token": "agent-token",
        "root_path": str(machine.home),
        "target_kind": "sandbox",
        **({"working_dir": str(working)} if working is not None else {}),
    }
    ctx = _AppContext({"active_sandbox": binding}, conversation_id)
    monkeypatch.setitem(
        sys.modules, "matrx_connect", types.SimpleNamespace(try_get_app_context=lambda: ctx)
    )
    return working


async def test_two_chats_writing_the_same_relative_name_never_collide(monkeypatch, machine) -> None:
    folder_a = _in_chat(monkeypatch, machine, CHAT_A)
    result = await shell.shell_execute({"command": "echo 'price list' > notes.txt"}, ToolContext(call_id="a1"))
    assert result.success, result

    folder_b = _in_chat(monkeypatch, machine, CHAT_B)
    result = await shell.shell_execute({"command": "echo 'spreadsheet' > notes.txt"}, ToolContext(call_id="b1"))
    assert result.success, result

    assert folder_a != folder_b
    assert (folder_a / "notes.txt").read_text() == "price list\n"
    assert (folder_b / "notes.txt").read_text() == "spreadsheet\n"
    assert not (machine.home / "notes.txt").exists(), "a chat wrote into the shared home"
    assert machine.exec_cwds == [str(folder_a), str(folder_b)]


async def test_a_later_turn_finds_what_the_chat_wrote_and_the_other_chat_does_not(
    monkeypatch, machine
) -> None:
    _in_chat(monkeypatch, machine, CHAT_A)
    wrote = await filesystem.fs_write({"path": "draft.md", "content": "# Week 46\n"}, ToolContext(call_id="a1"))
    assert wrote.success, wrote

    # A later turn of the same chat (a fresh binding, same conversation).
    _in_chat(monkeypatch, machine, CHAT_A)
    read = await filesystem.fs_read({"path": "draft.md"}, ToolContext(call_id="a2"))
    assert read.success and "Week 46" in json.dumps(read.output, default=str), read
    listed = await shell.shell_execute({"command": "ls"}, ToolContext(call_id="a3"))
    assert "draft.md" in json.dumps(listed.output, default=str)

    _in_chat(monkeypatch, machine, CHAT_B)
    other = await shell.shell_execute({"command": "ls"}, ToolContext(call_id="b1"))
    assert "draft.md" not in json.dumps(other.output, default=str)


async def test_home_relative_paths_still_reach_the_shared_cloud_folder(monkeypatch, machine) -> None:
    _in_chat(monkeypatch, machine, CHAT_A)
    wrote = await filesystem.fs_write(
        {"path": "~/Cloud/menu.txt", "content": "croissant 3.50\n"}, ToolContext(call_id="a1")
    )
    assert wrote.success, wrote
    assert (machine.home / "Cloud" / "menu.txt").read_text() == "croissant 3.50\n"


async def test_a_python_script_runs_in_the_chats_folder(monkeypatch, machine) -> None:
    folder = _in_chat(monkeypatch, machine, CHAT_B)
    result = await shell.shell_python({"code": "import os; print(os.getcwd())"}, ToolContext(call_id="b1"))
    assert result.success, result
    assert str(folder) in json.dumps(result.output, default=str)


async def test_a_run_with_no_chat_folder_keeps_the_home_and_the_sticky_shell(monkeypatch, machine) -> None:
    """No working folder (a desktop, a run with no conversation): nothing changes — no folder is
    sent, so a target's own sticky shell session keeps deciding where the command runs."""
    _in_chat(monkeypatch, machine, None)
    result = await shell.shell_execute({"command": "pwd"}, ToolContext(call_id="x1"))
    assert result.success, result
    assert machine.exec_cwds == [None]
    assert proxy.get_active_sandbox().default_dir == str(machine.home)
