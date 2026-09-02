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
    await fs._pipe_file("/work/a.txt", b"alpha\n")
    await fs._pipe_file("/work/b.txt", b"beta\n")
    await fs._pipe_file("/work/c.txt", b"gamma\n")
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/work"):
    cmd = get("xargs")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_xargs_default_invokes_echo(vfs):
    r = await _run(vfs, ["xargs", "echo"], stdin=b"hello world\n")
    assert r.exit_code == 0
    assert r.stdout == b"hello world\n"


async def test_xargs_passes_stdin_words_as_args(vfs):
    r = await _run(vfs, ["xargs", "cat"], stdin=b"a.txt b.txt\n")
    assert r.exit_code == 0
    assert r.stdout == b"alpha\nbeta\n"


async def test_xargs_n_one_per_invocation(vfs):
    r = await _run(vfs, ["xargs", "-n", "1", "echo"], stdin=b"a b c\n")
    assert r.stdout == b"a\nb\nc\n"


async def test_xargs_n_two(vfs):
    r = await _run(vfs, ["xargs", "-n", "2", "echo"], stdin=b"a b c d e\n")
    assert r.stdout == b"a b\nc d\ne\n"


async def test_xargs_replace(vfs):
    r = await _run(vfs, ["xargs", "-I", "FILE", "cat", "FILE"], stdin=b"a.txt\nb.txt\n")
    assert r.stdout == b"alpha\nbeta\n"


async def test_xargs_null_separator(vfs):
    r = await _run(vfs, ["xargs", "-0", "echo"], stdin=b"hello\x00world\x00there\x00")
    assert r.stdout == b"hello world there\n"


async def test_xargs_no_run_if_empty(vfs):
    r = await _run(vfs, ["xargs", "-r", "echo", "ran"], stdin=b"")
    assert r.exit_code == 0
    assert r.stdout == b""


async def test_xargs_default_runs_with_no_input(vfs):
    # Without -r, default behavior runs once with no extra args.
    r = await _run(vfs, ["xargs", "echo", "hi"], stdin=b"")
    assert r.exit_code == 0
    assert r.stdout == b"hi\n"


async def test_xargs_unknown_command_returns_127(vfs):
    r = await _run(vfs, ["xargs", "no-such-cmd"], stdin=b"x\n")
    assert r.exit_code == 127
    assert b"command not found" in r.stderr


async def test_xargs_trace_outputs_invocations(vfs):
    r = await _run(vfs, ["xargs", "-t", "-n", "1", "echo"], stdin=b"a b\n")
    assert r.exit_code == 0
    assert b"echo a" in r.stderr
    assert b"echo b" in r.stderr
    assert r.stdout == b"a\nb\n"


async def test_xargs_passes_base_args(vfs):
    r = await _run(vfs, ["xargs", "echo", "prefix:"], stdin=b"a b\n")
    assert r.stdout == b"prefix: a b\n"


async def test_xargs_replace_inserts_each_line(vfs):
    r = await _run(vfs, ["xargs", "-I", "{}", "echo", "got:", "{}"], stdin=b"foo\nbar\n")
    assert r.stdout == b"got: foo\ngot: bar\n"


async def test_xargs_parallelism_flag_accepted(vfs):
    r = await _run(vfs, ["xargs", "-P", "4", "-n", "1", "echo"], stdin=b"a b\n")
    assert r.exit_code == 0
    assert r.stdout == b"a\nb\n"


async def test_xargs_failed_invocation_propagates_123(vfs):
    # cat on a missing file exits 1; xargs translates 1..125 to 123.
    r = await _run(vfs, ["xargs", "cat"], stdin=b"missing.txt\n")
    assert r.exit_code == 123


async def test_xargs_word_split_on_whitespace_runs(vfs):
    r = await _run(vfs, ["xargs", "-n", "1", "echo"], stdin=b"a   b\n\n  c\n")
    assert r.stdout == b"a\nb\nc\n"
