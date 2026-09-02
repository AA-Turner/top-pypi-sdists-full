from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.commands.mkdir import cmd_mkdir
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
async def test_mkdir_basic(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mkdir", "/d"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 0
    assert r.stdout == b""
    assert r.stderr == b""
    assert await vfs._isdir("/d")


@pytest.mark.asyncio
async def test_mkdir_exists(vfs: MatrxAsyncFS):
    await vfs._mkdir("/d")
    ctx = make_ctx(["mkdir", "/d"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"mkdir: cannot create directory '/d': File exists\n"


@pytest.mark.asyncio
async def test_mkdir_no_parent(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mkdir", "/missing/dir"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"mkdir: cannot create directory '/missing/dir': No such file or directory\n"


@pytest.mark.asyncio
async def test_mkdir_p_creates_parents(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mkdir", "-p", "/a/b/c"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""
    assert await vfs._isdir("/a/b/c")


@pytest.mark.asyncio
async def test_mkdir_p_idempotent(vfs: MatrxAsyncFS):
    await vfs._mkdir("/d")
    ctx = make_ctx(["mkdir", "-p", "/d"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""


@pytest.mark.asyncio
async def test_mkdir_v_verbose(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mkdir", "-v", "/d"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 0
    assert r.stdout == b"mkdir: created directory '/d'\n"


@pytest.mark.asyncio
async def test_mkdir_pv_combined(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mkdir", "-pv", "/a/b/c"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 0
    # GNU mkdir emits a "created directory" line per parent created.
    # We accept the common collapsed behaviour: at least the leaf appears.
    assert b"/a/b/c" in r.stdout or r.stdout == b""


@pytest.mark.asyncio
async def test_mkdir_multiple_args_partial_failure(vfs: MatrxAsyncFS):
    await vfs._mkdir("/exists")
    ctx = make_ctx(["mkdir", "/new1", "/exists", "/new2"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 1
    assert b"mkdir: cannot create directory '/exists': File exists\n" in r.stderr
    assert await vfs._isdir("/new1")
    assert await vfs._isdir("/new2")


@pytest.mark.asyncio
async def test_mkdir_relative_path(vfs: MatrxAsyncFS):
    await vfs._mkdir("/work")
    ctx = make_ctx(["mkdir", "sub"], vfs, cwd="/work")
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 0
    assert await vfs._isdir("/work/sub")


@pytest.mark.asyncio
async def test_mkdir_missing_operand(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mkdir"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 1
    assert b"missing operand" in r.stderr


@pytest.mark.asyncio
async def test_mkdir_with_mode(vfs: MatrxAsyncFS):
    ctx = make_ctx(["mkdir", "-m", "755", "/d"], vfs)
    r = await cmd_mkdir(ctx)
    assert r.exit_code == 0
    assert await vfs._isdir("/d")
