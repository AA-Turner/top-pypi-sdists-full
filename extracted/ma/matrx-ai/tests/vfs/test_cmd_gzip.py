from __future__ import annotations

import gzip as gzip_mod
import io

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext
from matrx_ai.tools.vfs.commands.gzip import cmd_gunzip, cmd_gzip
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-test"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/work")
    await fs._pipe_file("/work/hello.txt", b"hello, world\n")
    return fs


def _ctx(
    vfs: MatrxAsyncFS, argv: list[str], stdin: bytes = b"", cwd: str = "/work"
) -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


async def test_compress_creates_gz_and_removes_original(vfs: MatrxAsyncFS) -> None:
    res = await cmd_gzip(_ctx(vfs, ["gzip", "hello.txt"]))
    assert res.exit_code == 0
    assert not await vfs._exists("/work/hello.txt")
    assert await vfs._exists("/work/hello.txt.gz")
    archive = await vfs._cat_file("/work/hello.txt.gz")
    assert archive[:2] == b"\x1f\x8b"


async def test_compress_keep_with_k(vfs: MatrxAsyncFS) -> None:
    res = await cmd_gzip(_ctx(vfs, ["gzip", "-k", "hello.txt"]))
    assert res.exit_code == 0
    assert await vfs._exists("/work/hello.txt")
    assert await vfs._exists("/work/hello.txt.gz")


async def test_compress_to_stdout(vfs: MatrxAsyncFS) -> None:
    res = await cmd_gzip(_ctx(vfs, ["gzip", "-c", "hello.txt"]))
    assert res.exit_code == 0
    assert res.stdout[:2] == b"\x1f\x8b"
    # Original still present.
    assert await vfs._exists("/work/hello.txt")


async def test_roundtrip_via_gunzip(vfs: MatrxAsyncFS) -> None:
    await cmd_gzip(_ctx(vfs, ["gzip", "hello.txt"]))
    res = await cmd_gunzip(_ctx(vfs, ["gunzip", "hello.txt.gz"]))
    assert res.exit_code == 0
    assert await vfs._exists("/work/hello.txt")
    data = await vfs._cat_file("/work/hello.txt")
    assert data == b"hello, world\n"


async def test_decompress_with_gzip_d(vfs: MatrxAsyncFS) -> None:
    await cmd_gzip(_ctx(vfs, ["gzip", "hello.txt"]))
    res = await cmd_gzip(_ctx(vfs, ["gzip", "-d", "hello.txt.gz"]))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/hello.txt")
    assert data == b"hello, world\n"


async def test_test_integrity(vfs: MatrxAsyncFS) -> None:
    await cmd_gzip(_ctx(vfs, ["gzip", "hello.txt"]))
    res = await cmd_gzip(_ctx(vfs, ["gzip", "-t", "hello.txt.gz"]))
    assert res.exit_code == 0


async def test_missing_file(vfs: MatrxAsyncFS) -> None:
    res = await cmd_gzip(_ctx(vfs, ["gzip", "nope.txt"]))
    assert res.exit_code == 1
    assert b"No such file" in res.stderr


async def test_decompress_bad_format(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/fake.gz", b"not a gzip\n")
    res = await cmd_gunzip(_ctx(vfs, ["gunzip", "fake.gz"]))
    assert res.exit_code == 1
    assert b"not in gzip format" in res.stderr


async def test_already_exists(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/hello.txt.gz", b"existing")
    res = await cmd_gzip(_ctx(vfs, ["gzip", "hello.txt"]))
    assert res.exit_code == 2
    assert b"already exists" in res.stderr


async def test_stdin_compress(vfs: MatrxAsyncFS) -> None:
    res = await cmd_gzip(_ctx(vfs, ["gzip"], stdin=b"streamed\n"))
    assert res.exit_code == 0
    assert res.stdout[:2] == b"\x1f\x8b"
    # Verify roundtrip.
    decompressed = gzip_mod.decompress(res.stdout)
    assert decompressed == b"streamed\n"


async def test_stdin_decompress(vfs: MatrxAsyncFS) -> None:
    buf = io.BytesIO()
    with gzip_mod.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(b"streamed\n")
    res = await cmd_gunzip(_ctx(vfs, ["gunzip"], stdin=buf.getvalue()))
    assert res.exit_code == 0
    assert res.stdout == b"streamed\n"


async def test_gunzip_unknown_suffix(vfs: MatrxAsyncFS) -> None:
    # Build a real gzip with an unsupported extension.
    buf = io.BytesIO()
    with gzip_mod.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(b"x\n")
    await vfs._pipe_file("/work/oddname", buf.getvalue())
    res = await cmd_gunzip(_ctx(vfs, ["gunzip", "oddname"]))
    assert res.exit_code == 1
    assert b"unknown suffix" in res.stderr
