from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.commands.ln import cmd_ln
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
async def test_ln_symlink_basic(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/target", b"hi")
    ctx = make_ctx(["ln", "-s", "/target", "/link"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 0
    assert r.stderr == b""
    info = await vfs._info("/link")
    assert info["type"] == "link"
    assert info["symlink_target"] == "/target"


@pytest.mark.asyncio
async def test_ln_symlink_dangling(vfs: MatrxAsyncFS):
    # POSIX: target need not exist.
    ctx = make_ctx(["ln", "-s", "/nonexistent", "/link"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 0
    info = await vfs._info("/link")
    assert info["type"] == "link"


@pytest.mark.asyncio
async def test_ln_link_exists(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/L", b"x")
    ctx = make_ctx(["ln", "-s", "/T", "/L"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"ln: failed to create symbolic link '/L': File exists\n"


@pytest.mark.asyncio
async def test_ln_sf_overwrites(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/L", b"x")
    ctx = make_ctx(["ln", "-sf", "/T", "/L"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 0
    info = await vfs._info("/L")
    assert info["type"] == "link"


@pytest.mark.asyncio
async def test_ln_into_dir(vfs: MatrxAsyncFS):
    await vfs._mkdir("/dir")
    ctx = make_ctx(["ln", "-s", "/target", "/dir"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 0
    info = await vfs._info("/dir/target")
    assert info["type"] == "link"
    assert info["symlink_target"] == "/target"


@pytest.mark.asyncio
async def test_ln_hard_unsupported(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/a", b"x")
    ctx = make_ctx(["ln", "/a", "/b"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"ln: failed to create hard link '/b': Operation not supported\n"


@pytest.mark.asyncio
async def test_ln_v_verbose(vfs: MatrxAsyncFS):
    ctx = make_ctx(["ln", "-sv", "/T", "/L"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 0
    assert r.stdout == b"'/L' -> '/T'\n"


@pytest.mark.asyncio
async def test_ln_no_args(vfs: MatrxAsyncFS):
    ctx = make_ctx(["ln"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 1
    assert b"missing file operand" in r.stderr


@pytest.mark.asyncio
async def test_ln_multi_to_dir(vfs: MatrxAsyncFS):
    await vfs._mkdir("/dst")
    ctx = make_ctx(["ln", "-s", "/T1", "/T2", "/dst"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 0
    assert (await vfs._info("/dst/T1"))["type"] == "link"
    assert (await vfs._info("/dst/T2"))["type"] == "link"


@pytest.mark.asyncio
async def test_ln_multi_to_non_dir(vfs: MatrxAsyncFS):
    await vfs._pipe_file("/notdir", b"x")
    ctx = make_ctx(["ln", "-s", "/T1", "/T2", "/notdir"], vfs)
    r = await cmd_ln(ctx)
    assert r.exit_code == 1
    assert r.stderr == b"ln: target '/notdir' is not a directory\n"


@pytest.mark.asyncio
async def test_ln_relative(vfs: MatrxAsyncFS):
    await vfs._mkdir("/w")
    ctx = make_ctx(["ln", "-s", "target", "linkname"], vfs, cwd="/w")
    r = await cmd_ln(ctx)
    assert r.exit_code == 0
    info = await vfs._info("/w/linkname")
    assert info["type"] == "link"
    assert info["symlink_target"] == "target"
