from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-realpath"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/a", create_parents=False)
    await fs._mkdir("/a/b", create_parents=False)
    await fs._pipe_file("/a/b/file.txt", b"hi\n")
    await fs._symlink("/a/b/file.txt", "/abs_link")
    await fs._symlink("file.txt", "/a/b/rel_link")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_realpath_simple(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "/a/b/file.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/b/file.txt\n"


async def test_realpath_collapses_dots(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "/a/b/../b/file.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/b/file.txt\n"


async def test_realpath_resolves_absolute_symlink(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "/abs_link"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/b/file.txt\n"


async def test_realpath_resolves_relative_symlink(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "/a/b/rel_link"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/a/b/file.txt\n"


async def test_realpath_missing_default(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "/no/such/dir/x"], vfs))
    assert result.exit_code == 1
    assert b"No such file or directory" in result.stderr


async def test_realpath_m_allows_missing(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "-m", "/no/such/dir/x"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/no/such/dir/x\n"


async def test_realpath_e_requires_existence(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    # last component missing — should fail under -e
    result = await cmd(make_ctx(["realpath", "-e", "/a/b/notthere"], vfs))
    assert result.exit_code == 1


async def test_realpath_s_no_symlink_resolve(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "-s", "/abs_link"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/abs_link\n"


async def test_realpath_relative_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("realpath")
    assert cmd is not None
    result = await cmd(make_ctx(["realpath", "file.txt"], vfs, cwd="/a/b"))
    assert result.exit_code == 0
    assert result.stdout == b"/a/b/file.txt\n"
