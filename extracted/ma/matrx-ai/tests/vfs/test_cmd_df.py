from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-df"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/data", create_parents=False)
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_df_default(vfs: MatrxAsyncFS) -> None:
    cmd = get("df")
    assert cmd is not None
    result = await cmd(make_ctx(["df"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    lines = out.splitlines()
    assert "Filesystem" in lines[0]
    assert "Mounted on" in lines[0]
    assert "1K-blocks" in lines[0]
    assert "vfs" in lines[1]
    assert lines[1].rstrip().endswith("/")


async def test_df_h_flag(vfs: MatrxAsyncFS) -> None:
    cmd = get("df")
    assert cmd is not None
    result = await cmd(make_ctx(["df", "-h"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    lines = out.splitlines()
    assert "Size" in lines[0]
    assert "Avail" in lines[0]
    assert "G" in lines[1]


async def test_df_inodes(vfs: MatrxAsyncFS) -> None:
    cmd = get("df")
    assert cmd is not None
    result = await cmd(make_ctx(["df", "-i"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    lines = out.splitlines()
    assert "Inodes" in lines[0]
    assert "IUsed" in lines[0]
    assert "IFree" in lines[0]


async def test_df_with_existing_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("df")
    assert cmd is not None
    result = await cmd(make_ctx(["df", "/data"], vfs))
    assert result.exit_code == 0
    assert b"vfs" in result.stdout


async def test_df_with_missing_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("df")
    assert cmd is not None
    result = await cmd(make_ctx(["df", "/missing"], vfs))
    assert result.exit_code == 1
    assert result.stderr == b"df: /missing: No such file or directory\n"


async def test_df_root_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("df")
    assert cmd is not None
    result = await cmd(make_ctx(["df", "/"], vfs))
    assert result.exit_code == 0
    assert b"vfs" in result.stdout
