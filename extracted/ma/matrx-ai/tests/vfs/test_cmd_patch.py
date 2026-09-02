from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext
from matrx_ai.tools.vfs.commands.patch import cmd_patch
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-test"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/work")
    await fs._pipe_file("/work/a.txt", b"line1\nline2\nline3\n")
    return fs


def _ctx(
    vfs: MatrxAsyncFS, argv: list[str], stdin: bytes = b"", cwd: str = "/work"
) -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


_PATCH = (
    b"--- a.txt\t2026-01-01\n"
    b"+++ a.txt\t2026-01-01\n"
    b"@@ -1,3 +1,3 @@\n"
    b" line1\n"
    b"-line2\n"
    b"+LINE2\n"
    b" line3\n"
)


async def test_apply_unified_diff(vfs: MatrxAsyncFS) -> None:
    res = await cmd_patch(_ctx(vfs, ["patch"], stdin=_PATCH))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"line1\nLINE2\nline3\n"
    assert b"patching file a.txt" in res.stdout


async def test_reverse_with_R(vfs: MatrxAsyncFS) -> None:
    # First apply then reverse.
    await cmd_patch(_ctx(vfs, ["patch"], stdin=_PATCH))
    res = await cmd_patch(_ctx(vfs, ["patch", "-R"], stdin=_PATCH))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"line1\nline2\nline3\n"


async def test_input_file(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/p.diff", _PATCH)
    res = await cmd_patch(_ctx(vfs, ["patch", "-i", "p.diff"]))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"line1\nLINE2\nline3\n"


async def test_patch_directory_d(vfs: MatrxAsyncFS) -> None:
    await vfs._mkdir("/work/sub")
    await vfs._pipe_file("/work/sub/a.txt", b"line1\nline2\nline3\n")
    res = await cmd_patch(
        _ctx(vfs, ["patch", "-d", "sub"], stdin=_PATCH)
    )
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/sub/a.txt")
    assert data == b"line1\nLINE2\nline3\n"


async def test_strip_p1(vfs: MatrxAsyncFS) -> None:
    patch_with_dir = (
        b"--- old/a.txt\n"
        b"+++ new/a.txt\n"
        b"@@ -1,3 +1,3 @@\n"
        b" line1\n"
        b"-line2\n"
        b"+LINE2\n"
        b" line3\n"
    )
    res = await cmd_patch(_ctx(vfs, ["patch", "-p1"], stdin=patch_with_dir))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"line1\nLINE2\nline3\n"


async def test_missing_input_file(vfs: MatrxAsyncFS) -> None:
    res = await cmd_patch(_ctx(vfs, ["patch", "-i", "missing.diff"]))
    assert res.exit_code == 1
    assert b"Can't open patch file" in res.stderr


async def test_empty_input(vfs: MatrxAsyncFS) -> None:
    res = await cmd_patch(_ctx(vfs, ["patch"], stdin=b""))
    assert res.exit_code == 1
    assert b"garbage" in res.stderr.lower() or b"only garbage" in res.stderr.lower()


async def test_failed_hunk(vfs: MatrxAsyncFS) -> None:
    # File has been altered so the hunk won't match.
    await vfs._pipe_file("/work/a.txt", b"completely\ndifferent\ncontent\n")
    res = await cmd_patch(_ctx(vfs, ["patch"], stdin=_PATCH))
    assert res.exit_code == 1
    assert b"FAILED" in res.stderr


async def test_malformed_patch(vfs: MatrxAsyncFS) -> None:
    bad = b"--- a.txt\n@@ broken\n"
    res = await cmd_patch(_ctx(vfs, ["patch"], stdin=bad))
    assert res.exit_code == 1
    assert b"malformed" in res.stderr


async def test_apply_multi_hunk(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file(
        "/work/multi.txt",
        b"a\nb\nc\nd\ne\nf\ng\nh\ni\nj\n",
    )
    multi_patch = (
        b"--- multi.txt\n"
        b"+++ multi.txt\n"
        b"@@ -1,3 +1,3 @@\n"
        b"-a\n"
        b"+A\n"
        b" b\n"
        b" c\n"
        b"@@ -8,3 +8,3 @@\n"
        b" h\n"
        b"-i\n"
        b"+I\n"
        b" j\n"
    )
    res = await cmd_patch(_ctx(vfs, ["patch"], stdin=multi_patch))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/multi.txt")
    assert data == b"A\nb\nc\nd\ne\nf\ng\nh\nI\nj\n"
