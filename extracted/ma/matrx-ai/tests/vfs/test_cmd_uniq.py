from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, load_all
from matrx_ai.tools.vfs.commands.registry import get
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv

load_all()


@pytest.fixture
async def vfs():
    backend = MemoryBackend()
    ws = "ws-test"
    await backend.ensure_workspace_root(ws)
    fs = MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)
    await fs._mkdir("/work")
    await fs._pipe_file("/work/dupes.txt", b"a\na\nb\nc\nc\nc\nd\n")
    await fs._pipe_file("/work/case.txt", b"Apple\napple\nBanana\n")
    await fs._pipe_file("/work/fields.txt", b"x foo\ny foo\nz bar\n")
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/work"):
    cmd = get("uniq")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_uniq_collapses_adjacent(vfs):
    r = await _run(vfs, ["uniq", "dupes.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"a\nb\nc\nd\n"


async def test_uniq_count(vfs):
    r = await _run(vfs, ["uniq", "-c", "dupes.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"      2 a\n      1 b\n      3 c\n      1 d\n"


async def test_uniq_repeated_only(vfs):
    r = await _run(vfs, ["uniq", "-d", "dupes.txt"])
    assert r.stdout == b"a\nc\n"


async def test_uniq_unique_only(vfs):
    r = await _run(vfs, ["uniq", "-u", "dupes.txt"])
    assert r.stdout == b"b\nd\n"


async def test_uniq_ignore_case(vfs):
    r = await _run(vfs, ["uniq", "-i", "case.txt"])
    assert r.stdout == b"Apple\nBanana\n"


async def test_uniq_skip_fields(vfs):
    r = await _run(vfs, ["uniq", "-f", "1", "fields.txt"])
    # After skipping field 1, "x foo" "y foo" both have key " foo" -> collapse
    assert r.stdout == b"x foo\nz bar\n"


async def test_uniq_skip_chars(vfs):
    await vfs._pipe_file("/work/sc.txt", b"abcfoo\nxyzfoo\nxxxbar\n")
    r = await _run(vfs, ["uniq", "-s", "3", "sc.txt"])
    assert r.stdout == b"abcfoo\nxxxbar\n"


async def test_uniq_stdin(vfs):
    r = await _run(vfs, ["uniq"], stdin=b"a\na\nb\n")
    assert r.stdout == b"a\nb\n"


async def test_uniq_no_collapse_non_adjacent(vfs):
    r = await _run(vfs, ["uniq"], stdin=b"a\nb\na\n")
    assert r.stdout == b"a\nb\na\n"


async def test_uniq_missing_file(vfs):
    r = await _run(vfs, ["uniq", "missing.txt"])
    assert r.exit_code == 1
    assert r.stderr == b"uniq: missing.txt: No such file or directory\n"


async def test_uniq_output_file(vfs):
    r = await _run(vfs, ["uniq", "dupes.txt", "/work/out.txt"])
    assert r.exit_code == 0
    data = await vfs._cat_file("/work/out.txt")
    assert data == b"a\nb\nc\nd\n"


async def test_uniq_count_single_line(vfs):
    r = await _run(vfs, ["uniq", "-c"], stdin=b"only\n")
    assert r.stdout == b"      1 only\n"


async def test_uniq_empty_input(vfs):
    r = await _run(vfs, ["uniq"], stdin=b"")
    assert r.exit_code == 0
    assert r.stdout == b""


async def test_uniq_invalid_skip_fields(vfs):
    r = await _run(vfs, ["uniq", "-f", "abc"], stdin=b"")
    assert r.exit_code == 1
    assert b"uniq:" in r.stderr
