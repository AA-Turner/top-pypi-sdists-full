from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext
from matrx_ai.tools.vfs.commands.diff import cmd_diff
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
    await fs._pipe_file("/work/b.txt", b"line1\nLINE2\nline3\n")
    await fs._pipe_file("/work/same.txt", b"line1\nline2\nline3\n")
    await fs._pipe_file("/work/blank.txt", b"line1\n\n\nline2\n")
    await fs._pipe_file("/work/blank2.txt", b"line1\nline2\n")
    await fs._pipe_file("/work/case.txt", b"Hello\n")
    await fs._pipe_file("/work/case2.txt", b"hello\n")

    await fs._mkdir("/work/dirA")
    await fs._mkdir("/work/dirB")
    await fs._pipe_file("/work/dirA/common.txt", b"alpha\n")
    await fs._pipe_file("/work/dirB/common.txt", b"beta\n")
    await fs._pipe_file("/work/dirA/onlyA.txt", b"x\n")
    await fs._pipe_file("/work/dirB/onlyB.txt", b"y\n")
    return fs


def _ctx(vfs: MatrxAsyncFS, argv: list[str], cwd: str = "/work") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_identical_files_exit_0(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "a.txt", "same.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b""


async def test_differing_files_exit_1(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "a.txt", "b.txt"]))
    assert res.exit_code == 1
    assert b"line2" in res.stdout
    assert b"LINE2" in res.stdout


async def test_unified_format(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-u", "a.txt", "b.txt"]))
    assert res.exit_code == 1
    out = res.stdout
    assert out.startswith(b"--- a.txt")
    assert b"+++ b.txt" in out
    assert b"@@ -1,3 +1,3 @@" in out
    assert b"-line2\n" in out
    assert b"+LINE2\n" in out


async def test_unified_short_form_U2(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-U2", "a.txt", "b.txt"]))
    assert res.exit_code == 1
    assert b"+++ b.txt" in res.stdout


async def test_brief_q(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-q", "a.txt", "b.txt"]))
    assert res.exit_code == 1
    assert res.stdout == b"Files a.txt and b.txt differ\n"


async def test_brief_identical_silent(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-q", "a.txt", "same.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b""


async def test_ignore_case(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-i", "case.txt", "case2.txt"]))
    assert res.exit_code == 0


async def test_ignore_blank_lines(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-B", "blank.txt", "blank2.txt"]))
    assert res.exit_code == 0


async def test_recursive(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-r", "dirA", "dirB"]))
    assert res.exit_code == 1
    out = res.stdout.decode()
    assert "Only in dirA: onlyA.txt" in out
    assert "Only in dirB: onlyB.txt" in out
    assert "diff dirA/common.txt dirB/common.txt" in out


async def test_missing_file_exit_2(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "missing.txt", "a.txt"]))
    assert res.exit_code == 2
    assert res.stderr.startswith(b"diff: missing.txt: No such file")


async def test_missing_with_N(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "-uN", "missing.txt", "a.txt"]))
    assert res.exit_code == 1
    assert b"+line1\n" in res.stdout


async def test_default_ed_style(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "a.txt", "b.txt"]))
    assert res.exit_code == 1
    out = res.stdout
    assert b"2c2\n" in out
    assert b"< line2\n" in out
    assert b"> LINE2\n" in out


async def test_missing_operand(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff"]))
    assert res.exit_code == 2
    assert b"missing operand" in res.stderr


async def test_directory_default_compares_files(vfs: MatrxAsyncFS) -> None:
    res = await cmd_diff(_ctx(vfs, ["diff", "dirA", "dirB"]))
    assert res.exit_code == 1
    assert b"Only in dirA" in res.stdout or b"diff dirA/" in res.stdout
