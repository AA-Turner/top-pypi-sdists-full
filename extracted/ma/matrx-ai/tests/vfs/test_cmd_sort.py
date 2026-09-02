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
    await fs._pipe_file("/work/words.txt", b"banana\napple\ncherry\n")
    await fs._pipe_file("/work/nums.txt", b"10\n2\n100\n1\n22\n")
    await fs._pipe_file("/work/dupes.txt", b"a\nb\na\nc\nb\n")
    await fs._pipe_file(
        "/work/keys.txt", b"3 zebra\n1 apple\n2 mango\n"
    )
    await fs._pipe_file("/work/sizes.txt", b"1K\n2M\n500\n1G\n")
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/work"):
    cmd = get("sort")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_sort_basic_lexicographic(vfs):
    r = await _run(vfs, ["sort", "words.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"apple\nbanana\ncherry\n"


async def test_sort_numeric(vfs):
    r = await _run(vfs, ["sort", "-n", "nums.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"1\n2\n10\n22\n100\n"


async def test_sort_reverse(vfs):
    r = await _run(vfs, ["sort", "-r", "words.txt"])
    assert r.stdout == b"cherry\nbanana\napple\n"


async def test_sort_unique(vfs):
    r = await _run(vfs, ["sort", "-u", "dupes.txt"])
    assert r.stdout == b"a\nb\nc\n"


async def test_sort_ignore_case(vfs):
    await vfs._pipe_file("/work/case.txt", b"banana\nApple\nCherry\n")
    r = await _run(vfs, ["sort", "-f", "case.txt"])
    assert r.stdout == b"Apple\nbanana\nCherry\n"


async def test_sort_human_numeric(vfs):
    r = await _run(vfs, ["sort", "-h", "sizes.txt"])
    assert r.stdout == b"500\n1K\n2M\n1G\n"


async def test_sort_key_field(vfs):
    r = await _run(vfs, ["sort", "-k", "2", "keys.txt"])
    assert r.stdout == b"1 apple\n2 mango\n3 zebra\n"


async def test_sort_with_separator(vfs):
    await vfs._pipe_file("/work/csv.txt", b"3,c\n1,a\n2,b\n")
    r = await _run(vfs, ["sort", "-t", ",", "-k", "1,1", "csv.txt"])
    assert r.stdout == b"1,a\n2,b\n3,c\n"


async def test_sort_output_file(vfs):
    r = await _run(vfs, ["sort", "-o", "out.txt", "words.txt"])
    assert r.exit_code == 0
    data = await vfs._cat_file("/work/out.txt")
    assert data == b"apple\nbanana\ncherry\n"
    assert r.stdout == b""


async def test_sort_check_passes(vfs):
    await vfs._pipe_file("/work/sorted.txt", b"a\nb\nc\n")
    r = await _run(vfs, ["sort", "-c", "sorted.txt"])
    assert r.exit_code == 0


async def test_sort_check_fails(vfs):
    r = await _run(vfs, ["sort", "-c", "words.txt"])
    assert r.exit_code == 1


async def test_sort_stdin(vfs):
    r = await _run(vfs, ["sort"], stdin=b"c\na\nb\n")
    assert r.stdout == b"a\nb\nc\n"


async def test_sort_missing_file(vfs):
    r = await _run(vfs, ["sort", "missing.txt"])
    assert r.exit_code == 2
    assert (
        r.stderr == b"sort: cannot read: 'missing.txt': No such file or directory\n"
    )


async def test_sort_multiple_files_concatenated(vfs):
    await vfs._pipe_file("/work/a.txt", b"b\na\n")
    await vfs._pipe_file("/work/b.txt", b"d\nc\n")
    r = await _run(vfs, ["sort", "a.txt", "b.txt"])
    assert r.stdout == b"a\nb\nc\nd\n"


async def test_sort_unique_with_numeric(vfs):
    r = await _run(vfs, ["sort", "-nu"], stdin=b"3\n1\n2\n1\n3\n")
    assert r.stdout == b"1\n2\n3\n"
