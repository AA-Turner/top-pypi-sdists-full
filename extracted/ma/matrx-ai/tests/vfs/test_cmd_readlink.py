from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-readlink"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/a", create_parents=False)
    await fs._pipe_file("/a/file.txt", b"hi\n")
    await fs._symlink("/a/file.txt", "/abs_link")
    await fs._symlink("file.txt", "/a/rel_link")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_readlink_emits_target_only(vfs: MatrxAsyncFS) -> None:
    cmd = get("readlink")
    assert cmd is not None
    result = await cmd(make_ctx(["readlink", "/abs_link"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/file.txt\n"


async def test_readlink_relative_target(vfs: MatrxAsyncFS) -> None:
    cmd = get("readlink")
    assert cmd is not None
    result = await cmd(make_ctx(["readlink", "/a/rel_link"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"file.txt\n"


async def test_readlink_non_symlink_silent(vfs: MatrxAsyncFS) -> None:
    cmd = get("readlink")
    assert cmd is not None
    result = await cmd(make_ctx(["readlink", "/a/file.txt"], vfs))
    assert result.exit_code == 1
    assert result.stdout == b""
    assert result.stderr == b""


async def test_readlink_missing(vfs: MatrxAsyncFS) -> None:
    cmd = get("readlink")
    assert cmd is not None
    result = await cmd(make_ctx(["readlink", "/no_such"], vfs))
    assert result.exit_code == 1
    assert result.stdout == b""


async def test_readlink_f_canonicalize(vfs: MatrxAsyncFS) -> None:
    cmd = get("readlink")
    assert cmd is not None
    result = await cmd(make_ctx(["readlink", "-f", "/abs_link"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/file.txt\n"


async def test_readlink_f_on_regular_file(vfs: MatrxAsyncFS) -> None:
    cmd = get("readlink")
    assert cmd is not None
    result = await cmd(make_ctx(["readlink", "-f", "/a/file.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/file.txt\n"


async def test_readlink_m_missing_ok(vfs: MatrxAsyncFS) -> None:
    cmd = get("readlink")
    assert cmd is not None
    result = await cmd(make_ctx(["readlink", "-m", "/a/nope"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/nope\n"
