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
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/"):
    cmd = get("tr")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_tr_basic_translate(vfs):
    r = await _run(vfs, ["tr", "abc", "xyz"], stdin=b"cabbage\n")
    assert r.exit_code == 0
    assert r.stdout == b"zxyyxge\n"


async def test_tr_lowercase_to_uppercase_with_ranges(vfs):
    r = await _run(vfs, ["tr", "a-z", "A-Z"], stdin=b"hello world\n")
    assert r.exit_code == 0
    assert r.stdout == b"HELLO WORLD\n"


async def test_tr_uppercase_to_lower_with_classes(vfs):
    r = await _run(vfs, ["tr", "[:upper:]", "[:lower:]"], stdin=b"HELLO\n")
    assert r.exit_code == 0
    assert r.stdout == b"hello\n"


async def test_tr_delete(vfs):
    r = await _run(vfs, ["tr", "-d", "aeiou"], stdin=b"hello world\n")
    assert r.exit_code == 0
    assert r.stdout == b"hll wrld\n"


async def test_tr_delete_digits(vfs):
    r = await _run(vfs, ["tr", "-d", "[:digit:]"], stdin=b"abc123def456\n")
    assert r.stdout == b"abcdef\n"


async def test_tr_squeeze(vfs):
    r = await _run(vfs, ["tr", "-s", " "], stdin=b"a   b   c\n")
    assert r.exit_code == 0
    assert r.stdout == b"a b c\n"


async def test_tr_squeeze_with_translate(vfs):
    r = await _run(vfs, ["tr", "-s", "a-z", "A-Z"], stdin=b"hellllooo\n")
    assert r.stdout == b"HELO\n"


async def test_tr_complement_delete(vfs):
    r = await _run(vfs, ["tr", "-cd", "a-zA-Z\n"], stdin=b"hello, world!\n")
    assert r.stdout == b"helloworld\n"


async def test_tr_escapes(vfs):
    r = await _run(vfs, ["tr", "\\n", " "], stdin=b"a\nb\nc\n")
    assert r.stdout == b"a b c "


async def test_tr_missing_operand(vfs):
    r = await _run(vfs, ["tr"])
    assert r.exit_code == 1
    assert r.stderr.startswith(b"tr: missing operand")


async def test_tr_translate_pads_with_last_char(vfs):
    # SET2 shorter -> padded with last char
    r = await _run(vfs, ["tr", "abc", "x"], stdin=b"abc\n")
    assert r.stdout == b"xxx\n"


async def test_tr_set2_longer_than_set1_truncated(vfs):
    # SET2 longer is fine; only first len(set1) chars used.
    r = await _run(vfs, ["tr", "ab", "xyz"], stdin=b"ab\n")
    assert r.stdout == b"xy\n"


async def test_tr_complement_translate(vfs):
    # Replace everything except letters with '_'
    r = await _run(vfs, ["tr", "-c", "a-zA-Z", "_"], stdin=b"hello, world!")
    # 'hello, world!' has 5 chars, comma, space, 5 chars, ! = "hello__world_"
    assert r.stdout == b"hello__world_"
