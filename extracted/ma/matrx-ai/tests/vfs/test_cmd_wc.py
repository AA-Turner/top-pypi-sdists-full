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
    await fs._mkdir("/tmp", create_parents=False)
    await fs._pipe_file("/tmp/a.txt", b"hello world\nbye\n")
    await fs._pipe_file("/tmp/b.txt", b"one two three four\n")
    await fs._pipe_file("/tmp/empty.txt", b"")
    await fs._pipe_file("/tmp/no_newline.txt", b"single line no newline")
    await fs._pipe_file("/tmp/utf.txt", "héllo\n".encode())
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/tmp"):
    cmd = get("wc")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_wc_default_single_file(vfs):
    r = await _run(vfs, ["wc", "a.txt"])
    assert r.exit_code == 0
    # 2 lines, 3 words, 16 bytes (hello world\nbye\n -> 16).
    assert r.stdout == b"2 3 16 a.txt\n"


async def test_wc_l(vfs):
    r = await _run(vfs, ["wc", "-l", "a.txt"])
    assert r.stdout == b"2 a.txt\n"


async def test_wc_w(vfs):
    r = await _run(vfs, ["wc", "-w", "b.txt"])
    assert r.stdout == b"4 b.txt\n"


async def test_wc_c(vfs):
    r = await _run(vfs, ["wc", "-c", "b.txt"])
    assert r.stdout == b"19 b.txt\n"


async def test_wc_m_utf8(vfs):
    # héllo\n is 6 bytes, 6 chars (é is 2 bytes; 5 letters + newline = 6 chars).
    r = await _run(vfs, ["wc", "-m", "utf.txt"])
    assert r.stdout == b"6 utf.txt\n"


async def test_wc_L(vfs):
    r = await _run(vfs, ["wc", "-L", "a.txt"])
    # "hello world" is 11 characters.
    assert r.stdout == b"11 a.txt\n"


async def test_wc_multi_file_total_with_padding(vfs):
    r = await _run(vfs, ["wc", "a.txt", "b.txt"])
    # Two files plus total row, all padded to max width.
    out = r.stdout.decode()
    lines = out.split("\n")
    # 3 lines (2 files + total) + final empty.
    assert lines[0].endswith("a.txt")
    assert lines[1].endswith("b.txt")
    assert lines[2].endswith("total")
    # All columns must align (split fields produce same widths).
    cols0 = lines[0].split()
    cols2 = lines[2].split()
    assert len(cols0) == 4 and len(cols2) == 4


async def test_wc_directory_error(vfs):
    r = await _run(vfs, ["wc", "/tmp"])
    assert r.exit_code == 1
    assert r.stderr == b"wc: /tmp: Is a directory\n"


async def test_wc_missing_file(vfs):
    r = await _run(vfs, ["wc", "missing.txt"])
    assert r.exit_code == 1
    assert r.stderr == b"wc: missing.txt: No such file or directory\n"


async def test_wc_stdin_no_filename_column(vfs):
    r = await _run(vfs, ["wc"], stdin=b"hi there\nyou\n")
    assert r.exit_code == 0
    # 2 lines, 3 words, 13 bytes.
    assert r.stdout == b"2 3 13\n"


async def test_wc_no_newline_file(vfs):
    r = await _run(vfs, ["wc", "-l", "no_newline.txt"])
    # GNU wc -l counts \n only, not unterminated trailing line: 0.
    assert r.stdout == b"0 no_newline.txt\n"
