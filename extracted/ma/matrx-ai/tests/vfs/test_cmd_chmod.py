from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-chmod"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/d", create_parents=False)
    await fs._mkdir("/d/sub", create_parents=False)
    await fs._pipe_file("/d/a.txt", b"abc")
    await fs._pipe_file("/d/sub/b.txt", b"def")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_chmod_octal(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "755", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["mode"] & 0o777 == 0o755


async def test_chmod_symbolic_add_x(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "u+x", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["mode"] & 0o100  # user execute set


async def test_chmod_symbolic_remove_r(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    # First set known state, then remove.
    await cmd(make_ctx(["chmod", "644", "/d/a.txt"], vfs))
    result = await cmd(make_ctx(["chmod", "a-r", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["mode"] & 0o444 == 0


async def test_chmod_symbolic_equals(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "u=rw,g=r,o=r", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    info = await vfs._info("/d/a.txt")
    assert info["mode"] & 0o777 == 0o644


async def test_chmod_recursive(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "-R", "700", "/d"], vfs))
    assert result.exit_code == 0
    assert (await vfs._info("/d"))["mode"] & 0o777 == 0o700
    assert (await vfs._info("/d/a.txt"))["mode"] & 0o777 == 0o700
    assert (await vfs._info("/d/sub"))["mode"] & 0o777 == 0o700
    assert (await vfs._info("/d/sub/b.txt"))["mode"] & 0o777 == 0o700


async def test_chmod_verbose(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "-v", "777", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "mode of '/d/a.txt' changed from" in out
    assert "0777" in out


async def test_chmod_missing(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "755", "/no_such"], vfs))
    assert result.exit_code == 1
    assert (
        result.stderr
        == b"chmod: cannot access '/no_such': No such file or directory\n"
    )


async def test_chmod_invalid_mode(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "qq", "/d/a.txt"], vfs))
    assert result.exit_code == 1
    assert b"invalid mode: 'qq'" in result.stderr


async def test_chmod_no_stdout_default(vfs: MatrxAsyncFS) -> None:
    cmd = get("chmod")
    assert cmd is not None
    result = await cmd(make_ctx(["chmod", "644", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b""
