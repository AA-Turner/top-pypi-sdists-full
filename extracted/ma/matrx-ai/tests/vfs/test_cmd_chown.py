from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-chown"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/d", create_parents=False)
    await fs._mkdir("/d/sub", create_parents=False)
    await fs._pipe_file("/d/a.txt", b"abc")
    await fs._pipe_file("/d/sub/b.txt", b"def")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_chown_user_only(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result = await cmd(make_ctx(["chown", "user", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["uid"] == 1000


async def test_chown_user_group(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result = await cmd(make_ctx(["chown", "user:user", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["uid"] == 1000
    assert info["gid"] == 1000


async def test_chown_root_uid_zero(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result = await cmd(make_ctx(["chown", "root", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["uid"] == 0


async def test_chown_unknown_user_deterministic(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result1 = await cmd(make_ctx(["chown", "alice", "/d/a.txt"], vfs))
    assert result1.exit_code == 0
    info1 = await vfs._info("/d/a.txt")
    uid_first = info1["uid"]
    # Change to something else then back.
    await cmd(make_ctx(["chown", "user", "/d/a.txt"], vfs))
    result2 = await cmd(make_ctx(["chown", "alice", "/d/a.txt"], vfs))
    assert result2.exit_code == 0
    info2 = await vfs._info("/d/a.txt")
    assert info2["uid"] == uid_first
    assert uid_first >= 1001


async def test_chown_recursive(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result = await cmd(make_ctx(["chown", "-R", "user:user", "/d"], vfs))
    assert result.exit_code == 0
    assert (await vfs._info("/d/a.txt"))["uid"] == 1000
    assert (await vfs._info("/d/sub/b.txt"))["uid"] == 1000


async def test_chown_missing(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result = await cmd(make_ctx(["chown", "user", "/no_such"], vfs))
    assert result.exit_code == 1
    assert (
        result.stderr
        == b"chown: cannot access '/no_such': No such file or directory\n"
    )


async def test_chown_verbose(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result = await cmd(make_ctx(["chown", "-v", "user:user", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    assert b"changed ownership of '/d/a.txt' to user:user" in result.stdout


async def test_chown_group_only(vfs: MatrxAsyncFS) -> None:
    cmd = get("chown")
    assert cmd is not None
    result = await cmd(make_ctx(["chown", ":root", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["gid"] == 0
