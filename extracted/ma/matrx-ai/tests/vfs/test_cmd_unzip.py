from __future__ import annotations

import io
import zipfile

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext
from matrx_ai.tools.vfs.commands.unzip import cmd_unzip
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


def _build_zip(entries: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
    return buf.getvalue()


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-test"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/work")
    archive = _build_zip({"a.txt": b"hello\n", "sub/b.txt": b"world\n"})
    await fs._pipe_file("/work/test.zip", archive)
    return fs


def _ctx(
    vfs: MatrxAsyncFS, argv: list[str], stdin: bytes = b"", cwd: str = "/work"
) -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


async def test_extract_basic(vfs: MatrxAsyncFS) -> None:
    res = await cmd_unzip(_ctx(vfs, ["unzip", "test.zip"]))
    assert res.exit_code == 0
    assert b"Archive:  test.zip" in res.stdout
    assert b"inflating: a.txt" in res.stdout
    assert await vfs._exists("/work/a.txt")
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"hello\n"
    assert await vfs._exists("/work/sub/b.txt")
    sub = await vfs._cat_file("/work/sub/b.txt")
    assert sub == b"world\n"


async def test_extract_to_directory_d(vfs: MatrxAsyncFS) -> None:
    res = await cmd_unzip(_ctx(vfs, ["unzip", "-d", "extract", "test.zip"]))
    assert res.exit_code == 0
    assert await vfs._exists("/work/extract/a.txt")
    assert await vfs._exists("/work/extract/sub/b.txt")


async def test_list_l(vfs: MatrxAsyncFS) -> None:
    res = await cmd_unzip(_ctx(vfs, ["unzip", "-l", "test.zip"]))
    assert res.exit_code == 0
    out = res.stdout.decode()
    assert "a.txt" in out
    assert "sub/b.txt" in out
    assert "Archive:" in out


async def test_overwrite_o(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/a.txt", b"prior content\n")
    res = await cmd_unzip(_ctx(vfs, ["unzip", "-o", "test.zip"]))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"hello\n"


async def test_no_overwrite_n(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/a.txt", b"prior content\n")
    res = await cmd_unzip(_ctx(vfs, ["unzip", "-n", "test.zip"]))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"prior content\n"
    assert b"skipping" in res.stdout


async def test_missing_file(vfs: MatrxAsyncFS) -> None:
    res = await cmd_unzip(_ctx(vfs, ["unzip", "nope.zip"]))
    assert res.exit_code == 9
    assert b"cannot find or open" in res.stderr


async def test_bad_zip(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/junk.zip", b"not a real zip file")
    res = await cmd_unzip(_ctx(vfs, ["unzip", "junk.zip"]))
    assert res.exit_code == 9
    assert b"End-of-central-directory" in res.stderr


async def test_no_args(vfs: MatrxAsyncFS) -> None:
    res = await cmd_unzip(_ctx(vfs, ["unzip"]))
    assert res.exit_code == 9


async def test_quiet_mode(vfs: MatrxAsyncFS) -> None:
    res = await cmd_unzip(_ctx(vfs, ["unzip", "-q", "test.zip"]))
    assert res.exit_code == 0
    assert b"Archive:" not in res.stdout
    assert b"inflating" not in res.stdout


async def test_directory_archive_member(vfs: MatrxAsyncFS) -> None:
    # Build a zip that includes an explicit directory entry.
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("emptydir/", b"")
        zf.writestr("emptydir/inside.txt", b"x\n")
    await vfs._pipe_file("/work/dir.zip", buf.getvalue())
    res = await cmd_unzip(_ctx(vfs, ["unzip", "dir.zip"]))
    assert res.exit_code == 0
    assert await vfs._isdir("/work/emptydir")
    data = await vfs._cat_file("/work/emptydir/inside.txt")
    assert data == b"x\n"
