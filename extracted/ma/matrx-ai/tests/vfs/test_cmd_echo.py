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
    cmd = get("echo")
    assert cmd is not None
    env = ShellEnv()
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_echo_simple(vfs):
    r = await _run(vfs, ["echo", "hello", "world"])
    assert r.exit_code == 0
    assert r.stdout == b"hello world\n"


async def test_echo_no_args_just_newline(vfs):
    r = await _run(vfs, ["echo"])
    assert r.stdout == b"\n"


async def test_echo_n_no_trailing_newline(vfs):
    r = await _run(vfs, ["echo", "-n", "hello"])
    assert r.stdout == b"hello"


async def test_echo_e_interprets_escapes(vfs):
    r = await _run(vfs, ["echo", "-e", "a\\tb\\nc"])
    assert r.stdout == b"a\tb\nc\n"


async def test_echo_E_disables_escapes(vfs):
    r = await _run(vfs, ["echo", "-E", "a\\tb"])
    assert r.stdout == b"a\\tb\n"


async def test_echo_clustered_nE(vfs):
    r = await _run(vfs, ["echo", "-nE", "no\\tescape"])
    assert r.stdout == b"no\\tescape"


async def test_echo_e_backslash_c_terminates(vfs):
    r = await _run(vfs, ["echo", "-e", "abc\\cdef"])
    assert r.stdout == b"abc"


async def test_echo_e_octal(vfs):
    r = await _run(vfs, ["echo", "-e", "\\0101"])  # 0o101 = 'A'
    assert r.stdout == b"A\n"


async def test_echo_e_hex(vfs):
    r = await _run(vfs, ["echo", "-e", "\\x41"])
    assert r.stdout == b"A\n"


async def test_echo_e_all_escapes(vfs):
    r = await _run(vfs, ["echo", "-e", "\\a\\b\\f\\n\\r\\t\\v\\\\"])
    assert r.stdout == b"\x07\x08\x0c\n\r\t\x0b\\\n"


async def test_echo_unknown_flag_is_literal(vfs):
    # Bash builtin echo: an unknown -x is treated as a literal arg.
    r = await _run(vfs, ["echo", "-x", "hello"])
    assert r.stdout == b"-x hello\n"


async def test_echo_args_joined_by_single_space(vfs):
    r = await _run(vfs, ["echo", "a", "b", "c"])
    assert r.stdout == b"a b c\n"


async def test_echo_e_escape_then_E_in_cluster(vfs):
    # Last cluster wins: -eE => escapes off.
    r = await _run(vfs, ["echo", "-eE", "a\\tb"])
    assert r.stdout == b"a\\tb\n"


async def test_echo_E_then_e_in_cluster(vfs):
    # -Ee => escapes on (last wins).
    r = await _run(vfs, ["echo", "-Ee", "a\\tb"])
    assert r.stdout == b"a\tb\n"
