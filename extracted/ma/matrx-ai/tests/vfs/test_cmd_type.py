from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-type"
    await backend.ensure_workspace_root(workspace_id)
    return MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_type_file(vfs: MatrxAsyncFS) -> None:
    cmd = get("type")
    assert cmd is not None
    result = await cmd(make_ctx(["type", "ls"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"ls is /usr/bin/ls\n"


async def test_type_builtin(vfs: MatrxAsyncFS) -> None:
    cmd = get("type")
    assert cmd is not None
    result = await cmd(make_ctx(["type", "cd"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"cd is a shell builtin\n"


async def test_type_not_found(vfs: MatrxAsyncFS) -> None:
    cmd = get("type")
    assert cmd is not None
    result = await cmd(make_ctx(["type", "nope_xyz"], vfs))
    assert result.exit_code == 1
    assert result.stderr == b"bash: type: nope_xyz: not found\n"


async def test_type_t_returns_kind(vfs: MatrxAsyncFS) -> None:
    cmd = get("type")
    assert cmd is not None
    result = await cmd(make_ctx(["type", "-t", "ls"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"file\n"
    result_b = await cmd(make_ctx(["type", "-t", "cd"], vfs))
    assert result_b.exit_code == 0
    assert result_b.stdout == b"builtin\n"


async def test_type_p_returns_path_only(vfs: MatrxAsyncFS) -> None:
    cmd = get("type")
    assert cmd is not None
    result = await cmd(make_ctx(["type", "-p", "ls"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/usr/bin/ls\n"
    # Builtins emit nothing for -p
    result_b = await cmd(make_ctx(["type", "-p", "cd"], vfs))
    assert result_b.exit_code == 0
    assert result_b.stdout == b""


async def test_type_multiple_with_one_missing(vfs: MatrxAsyncFS) -> None:
    cmd = get("type")
    assert cmd is not None
    result = await cmd(make_ctx(["type", "ls", "nope"], vfs))
    assert result.exit_code == 1
    assert b"ls is /usr/bin/ls" in result.stdout
    assert b"bash: type: nope: not found" in result.stderr


async def test_command_v_file(vfs: MatrxAsyncFS) -> None:
    cmd = get("command")
    assert cmd is not None
    result = await cmd(make_ctx(["command", "-v", "ls"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/usr/bin/ls\n"


async def test_command_v_builtin(vfs: MatrxAsyncFS) -> None:
    cmd = get("command")
    assert cmd is not None
    result = await cmd(make_ctx(["command", "-v", "cd"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"cd\n"


async def test_command_v_not_found(vfs: MatrxAsyncFS) -> None:
    cmd = get("command")
    assert cmd is not None
    result = await cmd(make_ctx(["command", "-v", "nope_xyz"], vfs))
    assert result.exit_code == 1
    assert result.stdout == b""
