from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-pwd"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/home", create_parents=False)
    await fs._mkdir("/home/user", create_parents=False)
    await fs._mkdir("/home/user/projects", create_parents=False)
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_pwd_root(vfs: MatrxAsyncFS) -> None:
    cmd = get("pwd")
    assert cmd is not None
    result = await cmd(make_ctx(["pwd"], vfs, cwd="/"))
    assert result.exit_code == 0
    assert result.stdout == b"/\n"
    assert result.stderr == b""


async def test_pwd_home(vfs: MatrxAsyncFS) -> None:
    cmd = get("pwd")
    assert cmd is not None
    result = await cmd(make_ctx(["pwd"], vfs, cwd="/home/user"))
    assert result.exit_code == 0
    assert result.stdout == b"/home/user\n"


async def test_pwd_nested(vfs: MatrxAsyncFS) -> None:
    cmd = get("pwd")
    assert cmd is not None
    result = await cmd(make_ctx(["pwd"], vfs, cwd="/home/user/projects"))
    assert result.exit_code == 0
    assert result.stdout == b"/home/user/projects\n"


async def test_pwd_missing_cwd(vfs: MatrxAsyncFS) -> None:
    cmd = get("pwd")
    assert cmd is not None
    result = await cmd(make_ctx(["pwd"], vfs, cwd="/does/not/exist"))
    assert result.exit_code == 1
    assert result.stderr == (
        b"pwd: error retrieving current directory: "
        b"getcwd: cannot access parent directories: "
        b"No such file or directory\n"
    )
    assert result.stdout == b""


async def test_pwd_dash_p_matches_default(vfs: MatrxAsyncFS) -> None:
    cmd = get("pwd")
    assert cmd is not None
    plain = await cmd(make_ctx(["pwd"], vfs, cwd="/home/user"))
    physical = await cmd(make_ctx(["pwd", "-P"], vfs, cwd="/home/user"))
    logical = await cmd(make_ctx(["pwd", "-L"], vfs, cwd="/home/user"))
    assert plain.stdout == physical.stdout == logical.stdout == b"/home/user\n"
    assert plain.exit_code == physical.exit_code == logical.exit_code == 0
