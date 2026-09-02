from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.commands.rmdir import cmd_rmdir
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
async def test_rmdir_basic(vfs: MatrxAsyncFS):
    await vfs._mkdir("/d")
    ctx = make_ctx(["rmdir", "/d"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""
    assert not await vfs._exists("/d")


@pytest.mark.asyncio
async def test_rmdir_not_empty(vfs: MatrxAsyncFS):
    await vfs._mkdir("/d")
    await vfs._pipe_file("/d/f", b"x")
    ctx = make_ctx(["rmdir", "/d"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"rmdir: failed to remove '/d': Directory not empty\n"


@pytest.mark.asyncio
async def test_rmdir_not_a_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/f", b"x")
    ctx = make_ctx(["rmdir", "/f"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"rmdir: failed to remove '/f': Not a directory\n"


@pytest.mark.asyncio
async def test_rmdir_missing(vfs: MatrxAsyncFS):
    ctx = make_ctx(["rmdir", "/nope"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"rmdir: failed to remove '/nope': No such file or directory\n"


@pytest.mark.asyncio
async def test_rmdir_p_clears_chain(vfs: MatrxAsyncFS):
    await vfs._makedirs("/a/b/c")
    ctx = make_ctx(["rmdir", "-p", "/a/b/c"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 0
    assert not await vfs._exists("/a/b/c")
    assert not await vfs._exists("/a/b")
    assert not await vfs._exists("/a")


@pytest.mark.asyncio
async def test_rmdir_p_stops_at_non_empty(vfs: MatrxAsyncFS):
    await vfs._makedirs("/a/b/c")
    await vfs._pipe_file("/a/sibling", b"x")
    ctx = make_ctx(["rmdir", "-p", "/a/b/c"], vfs)
    r = await cmd_rmdir(ctx)
    # /a/b/c removed; /a/b removed; /a not empty -> error
    assert r.exit_code == 1
    assert b"Directory not empty" in r.stderr
    assert not await vfs._exists("/a/b/c")
    assert not await vfs._exists("/a/b")
    assert await vfs._exists("/a")


@pytest.mark.asyncio
async def test_rmdir_multiple(vfs: MatrxAsyncFS):
    await vfs._mkdir("/a")
    await vfs._mkdir("/b")
    ctx = make_ctx(["rmdir", "/a", "/b"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 0
    assert not await vfs._exists("/a")
    assert not await vfs._exists("/b")


@pytest.mark.asyncio
async def test_rmdir_no_args(vfs: MatrxAsyncFS):
    ctx = make_ctx(["rmdir"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 1
    assert b"missing operand" in r.stderr


@pytest.mark.asyncio
async def test_rmdir_ignore_fail_on_non_empty(vfs: MatrxAsyncFS):
    await vfs._mkdir("/d")
    await vfs._pipe_file("/d/f", b"x")
    ctx = make_ctx(["rmdir", "--ignore-fail-on-non-empty", "/d"], vfs)
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 0


@pytest.mark.asyncio
async def test_rmdir_relative(vfs: MatrxAsyncFS):
    await vfs._makedirs("/w/sub")
    ctx = make_ctx(["rmdir", "sub"], vfs, cwd="/w")
    r = await cmd_rmdir(ctx)
    assert r.exit_code == 0
    assert not await vfs._exists("/w/sub")
