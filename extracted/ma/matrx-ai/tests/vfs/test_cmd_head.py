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
    cmd = get("head")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_head_default_first_10_lines(vfs):
    r = await _run(vfs, ["head", "big.txt"])
    assert r.exit_code == 0
    assert r.stdout == _seed_lines(10)


async def test_head_n_5(vfs):
    r = await _run(vfs, ["head", "-n", "5", "big.txt"])
    assert r.stdout == _seed_lines(5)


async def test_head_n_minus_5_drops_last_5(vfs):
    r = await _run(vfs, ["head", "-n", "-5", "big.txt"])
    # 20 lines - 5 = first 15 lines.
    assert r.stdout == _seed_lines(15)


async def test_head_c_first_4_bytes(vfs):
    r = await _run(vfs, ["head", "-c", "4", "bytes.txt"])
    assert r.stdout == b"abcd"


async def test_head_c_minus_3_drops_last_3_bytes(vfs):
    r = await _run(vfs, ["head", "-c", "-3", "bytes.txt"])
    assert r.stdout == b"abcdefg"


async def test_head_multi_file_headers(vfs):
    r = await _run(vfs, ["head", "-n", "2", "short.txt", "bytes.txt"])
    assert r.exit_code == 0
    assert r.stdout == (
        b"==> short.txt <==\n"
        b"a\nb\n"
        b"\n"
        b"==> bytes.txt <==\n"
        b"abcdefghij"
    )


async def test_head_q_suppresses_headers(vfs):
    r = await _run(vfs, ["head", "-q", "-n", "1", "short.txt", "bytes.txt"])
    assert b"==>" not in r.stdout


async def test_head_v_forces_header_with_one_file(vfs):
    r = await _run(vfs, ["head", "-v", "-n", "1", "short.txt"])
    assert r.stdout.startswith(b"==> short.txt <==\n")


async def test_head_missing_file(vfs):
    r = await _run(vfs, ["head", "missing.txt"])
    assert r.exit_code == 1
    assert r.stderr == b"head: cannot open 'missing.txt' for reading: No such file or directory\n"


async def test_head_stdin(vfs):
    data = _seed_lines(15)
    r = await _run(vfs, ["head"], stdin=data)
    assert r.stdout == _seed_lines(10)


async def test_head_short_form_minus_n_5(vfs):
    r = await _run(vfs, ["head", "-5", "big.txt"])
    assert r.stdout == _seed_lines(5)


async def test_head_n_with_K_suffix(vfs):
    # 1K bytes = 1024.
    big_payload = b"x" * 5000
    await vfs._pipe_file("/tmp/blob.bin", big_payload)
    r = await _run(vfs, ["head", "-c", "1K", "blob.bin"])
    assert r.stdout == b"x" * 1024
