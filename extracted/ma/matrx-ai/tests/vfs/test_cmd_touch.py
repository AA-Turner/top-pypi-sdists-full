from __future__ import annotations

from datetime import UTC, datetime

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.commands.touch import cmd_touch
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
async def test_touch_creates_empty(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "/f.txt"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0
    assert r.stdout == b""
    assert r.stderr == b""
    assert await vfs._isfile("/f.txt")
    assert await vfs._cat_file("/f.txt") == b""


@pytest.mark.asyncio
async def test_touch_existing_does_not_truncate(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/f.txt", b"keep")
    ctx = make_ctx(["touch", "/f.txt"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0
    assert await vfs._cat_file("/f.txt") == b"keep"


@pytest.mark.asyncio
async def test_touch_c_no_create_missing(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "-c", "/missing.txt"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""
    assert not await vfs._exists("/missing.txt")


@pytest.mark.asyncio
async def test_touch_c_existing_updates(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/f", b"x")
    ctx = make_ctx(["touch", "-c", "/f"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0


@pytest.mark.asyncio
async def test_touch_no_parent(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "/no/such/dir/f"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"touch: cannot touch '/no/such/dir/f': No such file or directory\n"


@pytest.mark.asyncio
async def test_touch_d_iso_format(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "-d", "2023-01-15 10:00", "/f"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0
    info = await vfs._info("/f")
    mt = info["mtime"]
    if isinstance(mt, datetime):
        assert mt.year == 2023 and mt.month == 1 and mt.day == 15
    else:
        # Float epoch fallback
        d = datetime.fromtimestamp(float(mt), tz=UTC)
        assert d.year == 2023 and d.month == 1 and d.day == 15


@pytest.mark.asyncio
async def test_touch_d_epoch(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "-d", "@1700000000", "/f"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0


@pytest.mark.asyncio
async def test_touch_d_invalid(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "-d", "not-a-date", "/f"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"touch: invalid date format 'not-a-date'\n"


@pytest.mark.asyncio
async def test_touch_t_format(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "-t", "202301151000", "/f"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0


@pytest.mark.asyncio
async def test_touch_multiple(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch", "/a", "/b", "/c"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 0
    assert await vfs._isfile("/a")
    assert await vfs._isfile("/b")
    assert await vfs._isfile("/c")


@pytest.mark.asyncio
async def test_touch_missing_operand(vfs: MatrxAsyncFS):
    ctx = make_ctx(["touch"], vfs)
    r = await cmd_touch(ctx)
    assert r.exit_code == 1
    assert b"missing file operand" in r.stderr


@pytest.mark.asyncio
async def test_touch_relative(vfs: MatrxAsyncFS):
    await vfs._mkdir("/w")
    ctx = make_ctx(["touch", "f.txt"], vfs, cwd="/w")
    r = await cmd_touch(ctx)
    assert r.exit_code == 0
    assert await vfs._isfile("/w/f.txt")
