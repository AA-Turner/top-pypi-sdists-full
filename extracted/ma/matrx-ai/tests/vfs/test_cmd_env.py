from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    ws = "ws-env"
    await backend.ensure_workspace_root(ws)
    return MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv, vfs, env=None, stdin=b""):
    return CommandContext(argv=argv, stdin=stdin, env=env or ShellEnv(), vfs=vfs)


# ---------------------------------------------------------------- env --------


async def test_env_prints_all_vars(vfs: MatrxAsyncFS) -> None:
    cmd = get("env")
    assert cmd is not None
    env = ShellEnv(env={"FOO": "bar", "BAZ": "qux"})
    r = await cmd(make_ctx(["env"], vfs, env=env))
    assert r.exit_code == 0
    assert b"FOO=bar\n" in r.stdout
    assert b"BAZ=qux\n" in r.stdout


async def test_env_dash_i_clears_then_prints_empty(vfs: MatrxAsyncFS) -> None:
    cmd = get("env")
    assert cmd is not None
    env = ShellEnv(env={"FOO": "bar"})
    r = await cmd(make_ctx(["env", "-i"], vfs, env=env))
    assert r.exit_code == 0
    assert r.stdout == b""
    assert env.vars == {}


async def test_env_dash_u_unsets_var(vfs: MatrxAsyncFS) -> None:
    cmd = get("env")
    assert cmd is not None
    env = ShellEnv(env={"FOO": "bar", "BAZ": "qux"})
    r = await cmd(make_ctx(["env", "-u", "FOO"], vfs, env=env))
    assert r.exit_code == 0
    assert b"FOO=" not in r.stdout
    assert b"BAZ=qux\n" in r.stdout


async def test_env_assignments_set_vars_and_print(vfs: MatrxAsyncFS) -> None:
    cmd = get("env")
    assert cmd is not None
    env = ShellEnv(env={})
    r = await cmd(make_ctx(["env", "X=1", "Y=2"], vfs, env=env))
    assert r.exit_code == 0
    assert env.vars["X"] == "1"
    assert env.vars["Y"] == "2"
    assert "X" in env.exported


async def test_env_dispatches_to_command(vfs: MatrxAsyncFS) -> None:
    cmd = get("env")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["env", "GREETING=hi", "echo", "ok"], vfs, env=env))
    assert r.exit_code == 0
    assert r.stdout == b"ok\n"
    assert env.vars["GREETING"] == "hi"


async def test_env_null_separator(vfs: MatrxAsyncFS) -> None:
    cmd = get("env")
    assert cmd is not None
    env = ShellEnv(env={"A": "1", "B": "2"})
    r = await cmd(make_ctx(["env", "-0"], vfs, env=env))
    assert r.exit_code == 0
    assert b"\0" in r.stdout
    assert r.stdout.count(b"\0") >= 2


async def test_env_unknown_command_returns_127(vfs: MatrxAsyncFS) -> None:
    cmd = get("env")
    assert cmd is not None
    r = await cmd(make_ctx(["env", "nonsuch_xyz"], vfs))
    assert r.exit_code == 127
    assert b"No such file or directory" in r.stderr


# ------------------------------------------------------------- export --------


async def test_export_set_var(vfs: MatrxAsyncFS) -> None:
    cmd = get("export")
    assert cmd is not None
    env = ShellEnv(env={})
    r = await cmd(make_ctx(["export", "FOO=bar"], vfs, env=env))
    assert r.exit_code == 0
    assert env.vars["FOO"] == "bar"
    assert "FOO" in env.exported


async def test_export_mark_existing(vfs: MatrxAsyncFS) -> None:
    cmd = get("export")
    assert cmd is not None
    env = ShellEnv(env={})
    env.set("FOO", "bar")
    env.exported.discard("FOO")
    r = await cmd(make_ctx(["export", "FOO"], vfs, env=env))
    assert r.exit_code == 0
    assert "FOO" in env.exported


async def test_export_no_args_lists(vfs: MatrxAsyncFS) -> None:
    cmd = get("export")
    assert cmd is not None
    env = ShellEnv(env={})
    env.set("FOO", "bar", export=True)
    env.set("ZZZ", "end", export=True)
    r = await cmd(make_ctx(["export"], vfs, env=env))
    assert r.exit_code == 0
    assert b'declare -x FOO="bar"\n' in r.stdout
    assert b'declare -x ZZZ="end"\n' in r.stdout
    # Sorted: FOO before ZZZ.
    assert r.stdout.index(b"FOO") < r.stdout.index(b"ZZZ")


async def test_export_bad_identifier(vfs: MatrxAsyncFS) -> None:
    cmd = get("export")
    assert cmd is not None
    env = ShellEnv(env={})
    r = await cmd(make_ctx(["export", "1bad=value"], vfs, env=env))
    assert r.exit_code == 1
    assert b"not a valid identifier" in r.stderr


# -------------------------------------------------------------- unset --------


async def test_unset_removes_var(vfs: MatrxAsyncFS) -> None:
    cmd = get("unset")
    assert cmd is not None
    env = ShellEnv(env={"FOO": "bar"})
    r = await cmd(make_ctx(["unset", "FOO"], vfs, env=env))
    assert r.exit_code == 0
    assert "FOO" not in env.vars
    assert "FOO" not in env.exported


async def test_unset_dash_v_explicit(vfs: MatrxAsyncFS) -> None:
    cmd = get("unset")
    assert cmd is not None
    env = ShellEnv(env={"FOO": "bar"})
    r = await cmd(make_ctx(["unset", "-v", "FOO"], vfs, env=env))
    assert r.exit_code == 0
    assert "FOO" not in env.vars


async def test_unset_dash_f_silent(vfs: MatrxAsyncFS) -> None:
    cmd = get("unset")
    assert cmd is not None
    env = ShellEnv(env={"FOO": "bar"})
    r = await cmd(make_ctx(["unset", "-f", "FOO"], vfs, env=env))
    assert r.exit_code == 0
    # -f doesn't touch vars.
    assert env.vars["FOO"] == "bar"


async def test_unset_bad_identifier(vfs: MatrxAsyncFS) -> None:
    cmd = get("unset")
    assert cmd is not None
    r = await cmd(make_ctx(["unset", "1bad"], vfs))
    assert r.exit_code == 1
    assert b"not a valid identifier" in r.stderr
