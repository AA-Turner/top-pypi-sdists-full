from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    ws = "ws-ps"
    await backend.ensure_workspace_root(ws)
    return MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv, vfs, env=None):
    return CommandContext(argv=argv, stdin=b"", env=env or ShellEnv(), vfs=vfs)


# ------------------------------------------------------------- ps --------


async def test_ps_default_header_and_shell(vfs: MatrxAsyncFS) -> None:
    cmd = get("ps")
    assert cmd is not None
    r = await cmd(make_ctx(["ps"], vfs))
    assert r.exit_code == 0
    assert r.stdout.startswith(b"  PID TTY          TIME CMD\n")
    assert b"bash" in r.stdout


async def test_ps_e_lists_all(vfs: MatrxAsyncFS) -> None:
    cmd = get("ps")
    assert cmd is not None
    r = await cmd(make_ctx(["ps", "-e"], vfs))
    assert r.exit_code == 0
    # Should include PID 1 init.
    assert b"init" in r.stdout
    assert b"bash" in r.stdout


async def test_ps_aux_format(vfs: MatrxAsyncFS) -> None:
    cmd = get("ps")
    assert cmd is not None
    r = await cmd(make_ctx(["ps", "aux"], vfs))
    assert r.exit_code == 0
    assert r.stdout.startswith(b"USER")
    assert b"%CPU" in r.stdout


async def test_ps_ef_format(vfs: MatrxAsyncFS) -> None:
    cmd = get("ps")
    assert cmd is not None
    r = await cmd(make_ctx(["ps", "-ef"], vfs))
    assert r.exit_code == 0
    assert b"PPID" in r.stdout


async def test_ps_p_filters_pid(vfs: MatrxAsyncFS) -> None:
    cmd = get("ps")
    assert cmd is not None
    r = await cmd(make_ctx(["ps", "-p", "1"], vfs))
    assert r.exit_code == 0
    assert b"init" in r.stdout
    assert b"bash" not in r.stdout


async def test_ps_p_unknown_pid(vfs: MatrxAsyncFS) -> None:
    cmd = get("ps")
    assert cmd is not None
    r = await cmd(make_ctx(["ps", "-p", "9999"], vfs))
    assert r.exit_code == 1


# ----------------------------------------------------------- kill --------


async def test_kill_unknown_pid(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    r = await cmd(make_ctx(["kill", "9999"], vfs))
    assert r.exit_code == 1
    assert r.stderr == b"bash: kill: (9999) - No such process\n"


async def test_kill_pid_one_refused(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    r = await cmd(make_ctx(["kill", "1"], vfs))
    assert r.exit_code == 1
    assert r.stderr == b"bash: kill: (1) - Operation not permitted\n"


async def test_kill_shell_pid_succeeds(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    env = ShellEnv()
    env.pid = 1234
    r = await cmd(make_ctx(["kill", "1234"], vfs, env=env))
    assert r.exit_code == 0
    assert r.stderr == b""


async def test_kill_with_signal_dash_9(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    env = ShellEnv()
    env.pid = 1234
    r = await cmd(make_ctx(["kill", "-9", "1234"], vfs, env=env))
    assert r.exit_code == 0


async def test_kill_with_signal_name(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    env = ShellEnv()
    env.pid = 1234
    r = await cmd(make_ctx(["kill", "-TERM", "1234"], vfs, env=env))
    assert r.exit_code == 0


async def test_kill_l_lists_signals(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    r = await cmd(make_ctx(["kill", "-l"], vfs))
    assert r.exit_code == 0
    assert b"SIGHUP" in r.stdout
    assert b"SIGINT" in r.stdout
    assert b"SIGKILL" in r.stdout
    assert b"SIGTERM" in r.stdout


async def test_kill_l_translates_number(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    r = await cmd(make_ctx(["kill", "-l", "9"], vfs))
    assert r.exit_code == 0
    assert b"KILL\n" in r.stdout


async def test_kill_zero_unknown_pid(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    r = await cmd(make_ctx(["kill", "-0", "9999"], vfs))
    assert r.exit_code == 1


async def test_kill_no_args_usage(vfs: MatrxAsyncFS) -> None:
    cmd = get("kill")
    assert cmd is not None
    r = await cmd(make_ctx(["kill"], vfs))
    assert r.exit_code == 2
    assert b"usage" in r.stderr
