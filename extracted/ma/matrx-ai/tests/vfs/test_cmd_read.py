from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    ws = "ws-read"
    await backend.ensure_workspace_root(ws)
    return MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv, vfs, env=None, stdin=b""):
    return CommandContext(argv=argv, stdin=stdin, env=env or ShellEnv(), vfs=vfs)


async def test_read_into_one_var(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "X"], vfs, env=env, stdin=b"hello\n"))
    assert r.exit_code == 0
    assert env.vars["X"] == "hello"


async def test_read_strips_trailing_newline(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "X"], vfs, env=env, stdin=b"line1\nline2\n"))
    assert r.exit_code == 0
    # Only first line, no \n.
    assert env.vars["X"] == "line1"


async def test_read_default_var_is_REPLY(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read"], vfs, env=env, stdin=b"hi\n"))
    assert r.exit_code == 0
    assert env.vars["REPLY"] == "hi"


async def test_read_into_multiple_vars(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "A", "B", "C"], vfs, env=env, stdin=b"one two three\n"))
    assert r.exit_code == 0
    assert env.vars["A"] == "one"
    assert env.vars["B"] == "two"
    assert env.vars["C"] == "three"


async def test_read_last_var_swallows_rest(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "A", "B"], vfs, env=env, stdin=b"one two three four\n"))
    assert r.exit_code == 0
    assert env.vars["A"] == "one"
    assert env.vars["B"] == "two three four"


async def test_read_empty_stdin_fails(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "X"], vfs, env=env, stdin=b""))
    assert r.exit_code == 1
    assert "X" not in env.vars


async def test_read_p_prompt_to_stderr(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "-p", "Name: ", "X"], vfs, env=env, stdin=b"alice\n"))
    assert r.exit_code == 0
    assert env.vars["X"] == "alice"
    assert r.stderr == b"Name: "


async def test_read_r_flag_accepted(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "-r", "X"], vfs, env=env, stdin=b"a\\b\n"))
    assert r.exit_code == 0
    # Default behavior already preserves backslashes; -r is a no-op.
    assert env.vars["X"] == "a\\b"


async def test_read_t_no_stdin(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "-t", "1", "X"], vfs, env=env, stdin=b""))
    assert r.exit_code == 142


async def test_read_t_invalid_timeout(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    r = await cmd(make_ctx(["read", "-t", "abc", "X"], vfs))
    assert r.exit_code == 1
    assert b"invalid timeout specification" in r.stderr


async def test_read_no_newline_takes_all(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["read", "X"], vfs, env=env, stdin=b"no_newline"))
    assert r.exit_code == 0
    assert env.vars["X"] == "no_newline"


async def test_read_unknown_option(vfs: MatrxAsyncFS) -> None:
    cmd = get("read")
    assert cmd is not None
    r = await cmd(make_ctx(["read", "-Z", "X"], vfs))
    assert r.exit_code == 2
    assert b"invalid option" in r.stderr
