from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, load_all
from matrx_ai.tools.vfs.commands.registry import get
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv

load_all()


def _seed_lines(n: int) -> bytes:
    return b"".join(f"line{i}\n".encode() for i in range(1, n + 1))


@pytest.fixture
async def vfs():
    backend = MemoryBackend()
    ws = "ws-test"
    await backend.ensure_workspace_root(ws)
    fs = MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)
    await fs._mkdir("/tmp", create_parents=False)
    await fs._pipe_file("/tmp/big.txt", _seed_lines(20))
    await fs._pipe_file("/tmp/short.txt", b"a\nb\nc\n")
    await fs._pipe_file("/tmp/bytes.txt", b"abcdefghij")
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/tmp"):
    cmd = get("tail")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_tail_default_last_10_lines(vfs):
    r = await _run(vfs, ["tail", "big.txt"])
    assert r.exit_code == 0
    expected = b"".join(f"line{i}\n".encode() for i in range(11, 21))
    assert r.stdout == expected


async def test_tail_n_3(vfs):
    r = await _run(vfs, ["tail", "-n", "3", "big.txt"])
    expected = b"".join(f"line{i}\n".encode() for i in range(18, 21))
    assert r.stdout == expected


async def test_tail_n_plus_18(vfs):
    r = await _run(vfs, ["tail", "-n", "+18", "big.txt"])
    expected = b"".join(f"line{i}\n".encode() for i in range(18, 21))
    assert r.stdout == expected


async def test_tail_c_5(vfs):
    r = await _run(vfs, ["tail", "-c", "5", "bytes.txt"])
    assert r.stdout == b"fghij"


async def test_tail_c_plus_3(vfs):
    # +3: from byte 3 (1-based) onward = "cdefghij".
    r = await _run(vfs, ["tail", "-c", "+3", "bytes.txt"])
    assert r.stdout == b"cdefghij"


async def test_tail_multi_file_headers(vfs):
    r = await _run(vfs, ["tail", "-n", "2", "short.txt", "bytes.txt"])
    assert r.stdout == (
        b"==> short.txt <==\n"
        b"b\nc\n"
        b"\n"
        b"==> bytes.txt <==\n"
        b"abcdefghij"
    )


async def test_tail_missing_file(vfs):
    r = await _run(vfs, ["tail", "missing.txt"])
    assert r.exit_code == 1
    assert r.stderr == b"tail: cannot open 'missing.txt' for reading: No such file or directory\n"


async def test_tail_stdin(vfs):
    r = await _run(vfs, ["tail", "-n", "2"], stdin=b"a\nb\nc\nd\n")
    assert r.stdout == b"c\nd\n"


async def test_tail_follow_emits_and_returns(vfs):
    # In VFS mode, -f should not block; it emits the current tail and returns.
    r = await _run(vfs, ["tail", "-f", "-n", "2", "big.txt"])
    assert r.exit_code == 0
    expected = b"line19\nline20\n"
    assert r.stdout == expected


async def test_tail_short_form_minus_n_5(vfs):
    r = await _run(vfs, ["tail", "-5", "big.txt"])
    expected = b"".join(f"line{i}\n".encode() for i in range(16, 21))
    assert r.stdout == expected
