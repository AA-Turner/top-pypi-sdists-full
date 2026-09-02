from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-which"
    await backend.ensure_workspace_root(workspace_id)
    return MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_which_finds_registered(vfs: MatrxAsyncFS) -> None:
    cmd = get("which")
    assert cmd is not None
    result = await cmd(make_ctx(["which", "ls"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/usr/bin/ls\n"
    assert result.stderr == b""


async def test_which_not_found_silent(vfs: MatrxAsyncFS) -> None:
    cmd = get("which")
    assert cmd is not None
    result = await cmd(make_ctx(["which", "definitely_not_real"], vfs))
    assert result.exit_code == 1
    assert result.stdout == b""
    assert result.stderr == b""


async def test_which_multiple_args_all_found(vfs: MatrxAsyncFS) -> None:
    cmd = get("which")
    assert cmd is not None
    result = await cmd(make_ctx(["which", "ls", "cat", "echo"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/usr/bin/ls\n/usr/bin/cat\n/usr/bin/echo\n"


async def test_which_partial_failure(vfs: MatrxAsyncFS) -> None:
    cmd = get("which")
    assert cmd is not None
    result = await cmd(make_ctx(["which", "ls", "missing_xyz"], vfs))
    assert result.exit_code == 1
    assert result.stdout == b"/usr/bin/ls\n"


async def test_which_no_args_returns_zero(vfs: MatrxAsyncFS) -> None:
    cmd = get("which")
    assert cmd is not None
    result = await cmd(make_ctx(["which"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b""


async def test_which_a_flag(vfs: MatrxAsyncFS) -> None:
    cmd = get("which")
    assert cmd is not None
    result = await cmd(make_ctx(["which", "-a", "ls"], vfs))
    assert result.exit_code == 0
    # We pretend a single fake path exists.
    assert result.stdout == b"/usr/bin/ls\n"


async def test_which_double_dash(vfs: MatrxAsyncFS) -> None:
    cmd = get("which")
    assert cmd is not None
    result = await cmd(make_ctx(["which", "--", "-foo"], vfs))
    assert result.exit_code == 1
    assert result.stdout == b""
