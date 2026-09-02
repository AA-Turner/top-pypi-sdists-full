from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    ws = "ws-set"
    await backend.ensure_workspace_root(ws)
    return MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv, vfs, env=None, stdin=b""):
    return CommandContext(argv=argv, stdin=stdin, env=env or ShellEnv(), vfs=vfs)


# ------------------------------------------------------- set (no args) --


async def test_set_no_args_prints_vars(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv(env={"FOO": "bar"})
    r = await cmd(make_ctx(["set"], vfs, env=env))
    assert r.exit_code == 0
    assert b"FOO='bar'\n" in r.stdout


async def test_set_no_args_quotes_with_special(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv(env={"X": "a 'b' c"})
    r = await cmd(make_ctx(["set"], vfs, env=env))
    assert r.exit_code == 0
    assert b"X='a '\\''b'\\'' c'\n" in r.stdout


# ----------------------------------------------------- short flag opts --


async def test_set_e_enables_errexit(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["set", "-e"], vfs, env=env))
    assert r.exit_code == 0
    assert env.shell_opts["errexit"] is True


async def test_set_plus_e_disables_errexit(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    env.shell_opts["errexit"] = True
    r = await cmd(make_ctx(["set", "+e"], vfs, env=env))
    assert r.exit_code == 0
    assert env.shell_opts["errexit"] is False


async def test_set_x_enables_xtrace(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["set", "-x"], vfs, env=env))
    assert r.exit_code == 0
    assert env.shell_opts["xtrace"] is True


async def test_set_u_enables_nounset(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["set", "-u"], vfs, env=env))
    assert r.exit_code == 0
    assert env.shell_opts["nounset"] is True


# --------------------------------------------------------- set -o NAME --


async def test_set_o_pipefail(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["set", "-o", "pipefail"], vfs, env=env))
    assert r.exit_code == 0
    assert env.shell_opts["pipefail"] is True


async def test_set_plus_o_pipefail_disables(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    env.shell_opts["pipefail"] = True
    r = await cmd(make_ctx(["set", "+o", "pipefail"], vfs, env=env))
    assert r.exit_code == 0
    assert env.shell_opts["pipefail"] is False


async def test_set_o_print_lists(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    env.shell_opts["errexit"] = True
    r = await cmd(make_ctx(["set", "-o"], vfs, env=env))
    assert r.exit_code == 0
    assert b"errexit\ton\n" in r.stdout
    assert b"pipefail\toff\n" in r.stdout


async def test_set_o_invalid_name(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    r = await cmd(make_ctx(["set", "-o", "notreal"], vfs))
    assert r.exit_code == 2
    assert b"invalid option name" in r.stderr


# -------------------------------------------------- positional params --


async def test_set_dashdash_clears_positional(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv(positional=["a", "b"])
    r = await cmd(make_ctx(["set", "--"], vfs, env=env))
    assert r.exit_code == 0
    assert env.positional == []


async def test_set_dashdash_assigns_positional(vfs: MatrxAsyncFS) -> None:
    cmd = get("set")
    assert cmd is not None
    env = ShellEnv()
    r = await cmd(make_ctx(["set", "--", "a", "b", "c"], vfs, env=env))
    assert r.exit_code == 0
    assert env.positional == ["a", "b", "c"]


# ---------------------------------------------------- true / false / : --


async def test_true_returns_zero(vfs: MatrxAsyncFS) -> None:
    cmd = get("true")
    assert cmd is not None
    r = await cmd(make_ctx(["true"], vfs))
    assert r.exit_code == 0
    assert r.stdout == b""


async def test_false_returns_one(vfs: MatrxAsyncFS) -> None:
    cmd = get("false")
    assert cmd is not None
    r = await cmd(make_ctx(["false"], vfs))
    assert r.exit_code == 1
    assert r.stdout == b""


async def test_colon_returns_zero(vfs: MatrxAsyncFS) -> None:
    cmd = get(":")
    assert cmd is not None
    r = await cmd(make_ctx([":"], vfs))
    assert r.exit_code == 0


# --------------------------------------------------------- exit ----


async def test_exit_default_uses_last_exit(vfs: MatrxAsyncFS) -> None:
    cmd = get("exit")
    assert cmd is not None
    env = ShellEnv()
    env.last_exit = 7
    r = await cmd(make_ctx(["exit"], vfs, env=env))
    assert r.exit_code == 7
    assert r.extra.get("exit_shell") is True


async def test_exit_with_code(vfs: MatrxAsyncFS) -> None:
    cmd = get("exit")
    assert cmd is not None
    r = await cmd(make_ctx(["exit", "42"], vfs))
    assert r.exit_code == 42


async def test_exit_non_numeric(vfs: MatrxAsyncFS) -> None:
    cmd = get("exit")
    assert cmd is not None
    r = await cmd(make_ctx(["exit", "abc"], vfs))
    assert r.exit_code == 2
    assert b"numeric argument required" in r.stderr


async def test_exit_masks_to_byte(vfs: MatrxAsyncFS) -> None:
    cmd = get("exit")
    assert cmd is not None
    r = await cmd(make_ctx(["exit", "256"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["exit", "257"], vfs))
    assert r.exit_code == 1
