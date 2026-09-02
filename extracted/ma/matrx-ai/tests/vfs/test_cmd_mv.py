from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.commands.mv import cmd_mv
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest.fixture
async def vfs():
    backend = MemoryBackend()
    ws = "ws-test"
    await backend.ensure_workspace_root(ws)
    fs = MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)
    return fs


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/", stdin: bytes = b"") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


@pytest.mark.asyncio
async def test_mv_rename(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"hi")
    ctx = make_ctx(["mv", "/a", "/b"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""
    assert not await vfs._exists("/a")
    assert await vfs._cat_file("/b") == b"hi"


@pytest.mark.asyncio
async def test_mv_into_existing_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"x")
    await vfs._mkdir("/dir")
    ctx = make_ctx(["mv", "/a", "/dir"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert await vfs._exists("/dir/a")
    assert not await vfs._exists("/a")


@pytest.mark.asyncio
async def test_mv_missing_source(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mv", "/missing", "/b"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"mv: cannot stat '/missing': No such file or directory\n"


@pytest.mark.asyncio
async def test_mv_overwrite_file(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"new")
    await vfs._pipe_file("/b", b"old")
    ctx = make_ctx(["mv", "/a", "/b"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/b") == b"new"


@pytest.mark.asyncio
async def test_mv_n_no_clobber(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"new")
    await vfs._pipe_file("/b", b"old")
    ctx = make_ctx(["mv", "-n", "/a", "/b"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/b") == b"old"
    assert await vfs._exists("/a")


@pytest.mark.asyncio
async def test_mv_v_verbose(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"x")
    ctx = make_ctx(["mv", "-v", "/a", "/b"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert r.stdout == b"renamed '/a' -> '/b'\n"


@pytest.mark.asyncio
async def test_mv_multi_source_to_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"1")
    await vfs._pipe_file("/b", b"2")
    await vfs._mkdir("/dst")
    ctx = make_ctx(["mv", "/a", "/b", "/dst"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert await vfs._exists("/dst/a")
    assert await vfs._exists("/dst/b")


@pytest.mark.asyncio
async def test_mv_multi_to_non_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"1")
    await vfs._pipe_file("/b", b"2")
    await vfs._pipe_file("/c", b"3")
    ctx = make_ctx(["mv", "/a", "/b", "/c"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"mv: target '/c' is not a directory\n"


@pytest.mark.asyncio
async def test_mv_t_target_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"1")
    await vfs._mkdir("/dst")
    ctx = make_ctx(["mv", "-t", "/dst", "/a"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert await vfs._exists("/dst/a")


@pytest.mark.asyncio
async def test_mv_no_args(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mv"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 1
    assert b"missing destination file operand" in r.stderr


@pytest.mark.asyncio
async def test_mv_relative(vfs: MatrxAsyncFS):
    await vfs._mkdir("/w")
    await vfs._pipe_file("/w/a", b"x")
    ctx = make_ctx(["mv", "a", "b"], vfs, cwd="/w")
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert await vfs._exists("/w/b")


@pytest.mark.asyncio
async def test_mv_dir_to_dir(vfs: MatrxAsyncFS):
    await vfs._makedirs("/src/sub")
    await vfs._pipe_file("/src/sub/f", b"hi")
    ctx = make_ctx(["mv", "/src", "/dst"], vfs)
    r = await cmd_mv(ctx)
    assert r.exit_code == 0
    assert not await vfs._exists("/src")
    assert await vfs._exists("/dst/sub/f")
