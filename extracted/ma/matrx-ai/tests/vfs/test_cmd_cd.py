from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-cd"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/home", create_parents=False)
    await fs._mkdir("/home/user", create_parents=False)
    await fs._mkdir("/home/user/projects", create_parents=False)
    await fs._mkdir("/tmp", create_parents=False)
    await fs._pipe_file("/home/user/notes.txt", b"some content")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_cd_to_existing_dir(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", "/home/user"], vfs, cwd="/")
    result = await cmd(ctx)
    assert result.exit_code == 0
    assert result.stdout == b""
    assert result.stderr == b""
    assert ctx.env.cwd == "/home/user"


async def test_cd_to_file_not_a_directory(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", "/home/user/notes.txt"], vfs, cwd="/")
    result = await cmd(ctx)
    assert result.exit_code == 1
    assert result.stderr == b"bash: cd: /home/user/notes.txt: Not a directory\n"
    assert ctx.env.cwd == "/"


async def test_cd_missing_dir(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", "/not/here"], vfs, cwd="/")
    result = await cmd(ctx)
    assert result.exit_code == 1
    assert result.stderr == b"bash: cd: /not/here: No such file or directory\n"
    assert ctx.env.cwd == "/"


async def test_cd_dash_swaps_with_oldpwd(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", "-"], vfs, cwd="/home/user")
    ctx.env.set("OLDPWD", "/tmp")
    result = await cmd(ctx)
    assert result.exit_code == 0
    assert result.stdout == b"/tmp\n"
    assert ctx.env.cwd == "/tmp"
    assert ctx.env.get("OLDPWD") == "/home/user"


async def test_cd_dash_unset_oldpwd(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", "-"], vfs, cwd="/home/user")
    ctx.env.unset("OLDPWD")
    result = await cmd(ctx)
    assert result.exit_code == 1
    assert result.stderr == b"bash: cd: OLDPWD not set\n"
    assert ctx.env.cwd == "/home/user"


async def test_cd_no_arg_goes_home(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd"], vfs, cwd="/tmp")
    result = await cmd(ctx)
    assert result.exit_code == 0
    assert result.stdout == b""
    assert ctx.env.cwd == "/home/user"


async def test_cd_relative_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", "projects"], vfs, cwd="/home/user")
    result = await cmd(ctx)
    assert result.exit_code == 0
    assert ctx.env.cwd == "/home/user/projects"


async def test_cd_dotdot(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", ".."], vfs, cwd="/home/user")
    result = await cmd(ctx)
    assert result.exit_code == 0
    assert ctx.env.cwd == "/home"


async def test_cd_updates_pwd_and_oldpwd(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    ctx = make_ctx(["cd", "/tmp"], vfs, cwd="/home/user")
    result = await cmd(ctx)
    assert result.exit_code == 0
    assert ctx.env.vars["PWD"] == "/tmp"
    assert ctx.env.vars["OLDPWD"] == "/home/user"


async def test_cd_tilde_expansion(vfs: MatrxAsyncFS) -> None:
    cmd = get("cd")
    assert cmd is not None
    # If a literal `~` arrives, expand to $HOME.
    ctx = make_ctx(["cd", "~"], vfs, cwd="/tmp")
    result = await cmd(ctx)
    assert result.exit_code == 0
    assert ctx.env.cwd == "/home/user"
