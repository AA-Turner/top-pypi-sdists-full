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


async def _run(vfs, argv, stdin=b""):
    cmd = get("printf")
    assert cmd is not None
    env = ShellEnv()
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_printf_basic_string(vfs):
    r = await _run(vfs, ["printf", "hello\\n"])
    assert r.exit_code == 0
    assert r.stdout == b"hello\n"


async def test_printf_no_args_usage_error(vfs):
    r = await _run(vfs, ["printf"])
    assert r.exit_code == 2
    assert b"printf: usage:" in r.stderr


async def test_printf_s_substitution(vfs):
    r = await _run(vfs, ["printf", "%s\n", "world"])
    assert r.stdout == b"world\n"


async def test_printf_format_reuse(vfs):
    r = await _run(vfs, ["printf", "%s\n", "a", "b", "c"])
    assert r.stdout == b"a\nb\nc\n"


async def test_printf_d_integer(vfs):
    r = await _run(vfs, ["printf", "%d\n", "42"])
    assert r.stdout == b"42\n"


async def test_printf_x_hex(vfs):
    r = await _run(vfs, ["printf", "%x\n", "255"])
    assert r.stdout == b"ff\n"


async def test_printf_X_upper_hex(vfs):
    r = await _run(vfs, ["printf", "%X\n", "255"])
    assert r.stdout == b"FF\n"


async def test_printf_width_5d(vfs):
    r = await _run(vfs, ["printf", "%5d\n", "7"])
    assert r.stdout == b"    7\n"


async def test_printf_zero_padded(vfs):
    r = await _run(vfs, ["printf", "%05d\n", "42"])
    assert r.stdout == b"00042\n"


async def test_printf_left_align(vfs):
    r = await _run(vfs, ["printf", "[%-5s]\n", "hi"])
    assert r.stdout == b"[hi   ]\n"


async def test_printf_precision_string(vfs):
    r = await _run(vfs, ["printf", "%.3s\n", "abcdef"])
    assert r.stdout == b"abc\n"


async def test_printf_invalid_number(vfs):
    r = await _run(vfs, ["printf", "%d\n", "abc"])
    assert r.exit_code == 1
    assert b"printf: abc: invalid number" in r.stderr
    # 0 is substituted.
    assert r.stdout == b"0\n"


async def test_printf_b_interprets_escapes(vfs):
    r = await _run(vfs, ["printf", "%b\n", "a\\tb"])
    assert r.stdout == b"a\tb\n"


async def test_printf_percent_percent(vfs):
    r = await _run(vfs, ["printf", "100%%\n"])
    assert r.stdout == b"100%\n"


async def test_printf_format_octal_escape(vfs):
    # printf format string \101 -> 'A'.
    r = await _run(vfs, ["printf", "\\101\\n"])
    assert r.stdout == b"A\n"


async def test_printf_format_hex_escape(vfs):
    r = await _run(vfs, ["printf", "\\x41\\x42\\n"])
    assert r.stdout == b"AB\n"


async def test_printf_no_automatic_newline(vfs):
    r = await _run(vfs, ["printf", "%s", "foo"])
    assert r.stdout == b"foo"


async def test_printf_multiple_specs_one_pass(vfs):
    r = await _run(vfs, ["printf", "%s=%d\n", "x", "5"])
    assert r.stdout == b"x=5\n"


async def test_printf_q_quotes_safely(vfs):
    r = await _run(vfs, ["printf", "%q\n", "hello world"])
    # Spaces force quoting.
    out = r.stdout
    assert out == b"'hello world'\n"
