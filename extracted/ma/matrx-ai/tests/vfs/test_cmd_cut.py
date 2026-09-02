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
    await fs._pipe_file("/work/csv.txt", b"a,b,c,d\n1,2,3,4\nx,y,z,w\n")
    await fs._pipe_file("/work/tab.txt", b"a\tb\tc\n1\t2\t3\n")
    await fs._pipe_file("/work/plain.txt", b"hello world\nABCDEFGHIJ\n")
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/work"):
    cmd = get("cut")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_cut_fields_with_delim(vfs):
    r = await _run(vfs, ["cut", "-d", ",", "-f", "1,3", "csv.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"a,c\n1,3\nx,z\n"


async def test_cut_default_tab_delim(vfs):
    r = await _run(vfs, ["cut", "-f", "2", "tab.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"b\n2\n"


async def test_cut_field_range(vfs):
    r = await _run(vfs, ["cut", "-d", ",", "-f", "2-3", "csv.txt"])
    assert r.stdout == b"b,c\n2,3\ny,z\n"


async def test_cut_field_open_range(vfs):
    r = await _run(vfs, ["cut", "-d", ",", "-f", "3-", "csv.txt"])
    assert r.stdout == b"c,d\n3,4\nz,w\n"


async def test_cut_field_left_open(vfs):
    r = await _run(vfs, ["cut", "-d", ",", "-f", "-2", "csv.txt"])
    assert r.stdout == b"a,b\n1,2\nx,y\n"


async def test_cut_chars(vfs):
    r = await _run(vfs, ["cut", "-c", "1-5", "plain.txt"])
    assert r.stdout == b"hello\nABCDE\n"


async def test_cut_chars_open_range(vfs):
    r = await _run(vfs, ["cut", "-c", "7-"], stdin=b"hello world\n")
    assert r.stdout == b"world\n"


async def test_cut_output_delimiter(vfs):
    r = await _run(
        vfs, ["cut", "-d", ",", "-f", "1,3", "--output-delimiter=|", "csv.txt"]
    )
    assert r.stdout == b"a|c\n1|3\nx|z\n"


async def test_cut_suppress_no_delim(vfs):
    await vfs._pipe_file("/work/mixed.txt", b"a,b\nnokomma\nc,d\n")
    r = await _run(vfs, ["cut", "-d", ",", "-f", "1", "-s", "mixed.txt"])
    assert r.stdout == b"a\nc\n"


async def test_cut_invalid_range(vfs):
    r = await _run(vfs, ["cut", "-c", "abc", "plain.txt"])
    assert r.exit_code == 1
    assert b"invalid field range" in r.stderr


async def test_cut_missing_file(vfs):
    r = await _run(vfs, ["cut", "-c", "1-3", "missing.txt"])
    assert r.exit_code == 1
    assert r.stderr == b"cut: missing.txt: No such file or directory\n"


async def test_cut_stdin(vfs):
    r = await _run(vfs, ["cut", "-d", ":", "-f", "1"], stdin=b"foo:bar\nbaz:qux\n")
    assert r.stdout == b"foo\nbaz\n"


async def test_cut_complement(vfs):
    r = await _run(
        vfs, ["cut", "-d", ",", "-f", "1", "--complement", "csv.txt"]
    )
    assert r.stdout == b"b,c,d\n2,3,4\ny,z,w\n"


async def test_cut_no_field_spec_error(vfs):
    r = await _run(vfs, ["cut", "csv.txt"])
    assert r.exit_code == 1
    assert b"cut:" in r.stderr
