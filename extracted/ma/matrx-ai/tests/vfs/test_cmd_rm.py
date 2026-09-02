from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.commands.rm import cmd_rm
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
async def test_rm_file(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/f", b"x")
    ctx = make_ctx(["rm", "/f"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""
    assert not await vfs._exists("/f")


@pytest.mark.asyncio
async def test_rm_missing(vfs: MatrxAsyncFS):
    ctx = make_ctx(["rm", "/missing"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"rm: cannot remove '/missing': No such file or directory\n"


@pytest.mark.asyncio
async def test_rm_dir_without_r(vfs: MatrxAsyncFS):
    await vfs._mkdir("/d")
    ctx = make_ctx(["rm", "/d"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"rm: cannot remove '/d': Is a directory\n"


@pytest.mark.asyncio
async def test_rm_f_silent_on_missing(vfs: MatrxAsyncFS):
    ctx = make_ctx(["rm", "-f", "/missing"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""


@pytest.mark.asyncio
async def test_rm_r_recursive(vfs: MatrxAsyncFS):
    await vfs._makedirs("/d/sub")
    await vfs._pipe_file("/d/a.txt", b"x")
    await vfs._pipe_file("/d/sub/b.txt", b"y")
    ctx = make_ctx(["rm", "-r", "/d"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 0
    assert not await vfs._exists("/d")


@pytest.mark.asyncio
async def test_rm_rf_missing(vfs: MatrxAsyncFS):
    ctx = make_ctx(["rm", "-rf", "/none"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""


@pytest.mark.asyncio
async def test_rm_v_verbose(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/f", b"x")
    ctx = make_ctx(["rm", "-v", "/f"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 0
    assert r.stdout == b"removed '/f'\n"


@pytest.mark.asyncio
async def test_rm_d_empty_dir(vfs: MatrxAsyncFS):
    await vfs._mkdir("/empty")
    ctx = make_ctx(["rm", "-d", "/empty"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 0
    assert not await vfs._exists("/empty")


@pytest.mark.asyncio
async def test_rm_refuses_root(vfs: MatrxAsyncFS):
    ctx = make_ctx(["rm", "-rf", "/"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 1
    assert r.stderr == (
        b"rm: it is dangerous to operate recursively on '/'\n"
        b"rm: use --no-preserve-root to override this failsafe\n"
    )


@pytest.mark.asyncio
async def test_rm_multiple_partial_failure(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"")
    ctx = make_ctx(["rm", "/a", "/missing", "/a"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 1
    # First /a is removed, then missing fails, then second /a fails because already gone.
    assert b"rm: cannot remove '/missing': No such file or directory\n" in r.stderr


@pytest.mark.asyncio
async def test_rm_relative(vfs: MatrxAsyncFS):
    await vfs._mkdir("/w")
    await vfs._pipe_file("/w/f", b"x")
    ctx = make_ctx(["rm", "f"], vfs, cwd="/w")
    r = await cmd_rm(ctx)
    assert r.exit_code == 0
    assert not await vfs._exists("/w/f")


@pytest.mark.asyncio
async def test_rm_no_args(vfs: MatrxAsyncFS):
    ctx = make_ctx(["rm"], vfs)
    r = await cmd_rm(ctx)
    assert r.exit_code == 1
    assert b"missing operand" in r.stderr
