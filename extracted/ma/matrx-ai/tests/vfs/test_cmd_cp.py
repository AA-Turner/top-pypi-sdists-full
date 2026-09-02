from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.commands.cp import cmd_cp
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
async def test_cp_file(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"hi")
    ctx = make_ctx(["cp", "/a", "/b"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""
    assert await vfs._cat_file("/a") == b"hi"
    assert await vfs._cat_file("/b") == b"hi"


@pytest.mark.asyncio
async def test_cp_into_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"x")
    await vfs._mkdir("/dst")
    ctx = make_ctx(["cp", "/a", "/dst"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert await vfs._exists("/dst/a")


@pytest.mark.asyncio
async def test_cp_missing_source(vfs: MatrxAsyncFS):
    ctx = make_ctx(["cp", "/missing", "/b"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"cp: cannot stat '/missing': No such file or directory\n"


@pytest.mark.asyncio
async def test_cp_dir_without_r(vfs: MatrxAsyncFS):
    await vfs._mkdir("/d")
    ctx = make_ctx(["cp", "/d", "/dst"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"cp: -r not specified; omitting directory '/d'\n"


@pytest.mark.asyncio
async def test_cp_r_recursive(vfs: MatrxAsyncFS):
    await vfs._makedirs("/src/sub")
    await vfs._pipe_file("/src/a", b"1")
    await vfs._pipe_file("/src/sub/b", b"2")
    ctx = make_ctx(["cp", "-r", "/src", "/dst"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/dst/a") == b"1"
    assert await vfs._cat_file("/dst/sub/b") == b"2"


@pytest.mark.asyncio
async def test_cp_v_verbose(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"x")
    ctx = make_ctx(["cp", "-v", "/a", "/b"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert r.stdout == b"'/a' -> '/b'\n"


@pytest.mark.asyncio
async def test_cp_n_no_clobber(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"new")
    await vfs._pipe_file("/b", b"old")
    ctx = make_ctx(["cp", "-n", "/a", "/b"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/b") == b"old"


@pytest.mark.asyncio
async def test_cp_multi_to_non_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"1")
    await vfs._pipe_file("/b", b"2")
    await vfs._pipe_file("/c", b"3")
    ctx = make_ctx(["cp", "/a", "/b", "/c"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"cp: target '/c' is not a directory\n"


@pytest.mark.asyncio
async def test_cp_multi_to_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"1")
    await vfs._pipe_file("/b", b"2")
    await vfs._mkdir("/dst")
    ctx = make_ctx(["cp", "/a", "/b", "/dst"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/dst/a") == b"1"
    assert await vfs._cat_file("/dst/b") == b"2"


@pytest.mark.asyncio
async def test_cp_t_target_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"x")
    await vfs._mkdir("/dst")
    ctx = make_ctx(["cp", "-t", "/dst", "/a"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert await vfs._exists("/dst/a")


@pytest.mark.asyncio
async def test_cp_p_preserve(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"x")
    ctx = make_ctx(["cp", "-p", "/a", "/b"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/b") == b"x"


@pytest.mark.asyncio
async def test_cp_no_args(vfs: MatrxAsyncFS):
    ctx = make_ctx(["cp"], vfs)
    r = await cmd_cp(ctx)
    assert r.exit_code == 1


@pytest.mark.asyncio
async def test_cp_relative(vfs: MatrxAsyncFS):
    await vfs._mkdir("/w")
    await vfs._pipe_file("/w/a", b"x")
    ctx = make_ctx(["cp", "a", "b"], vfs, cwd="/w")
    r = await cmd_cp(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/w/b") == b"x"
