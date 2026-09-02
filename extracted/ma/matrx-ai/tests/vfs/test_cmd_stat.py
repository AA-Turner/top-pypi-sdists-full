from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-stat"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/d", create_parents=False)
    await fs._pipe_file("/d/a.txt", b"abc\n")
    await fs._pipe_file("/d/empty", b"")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_stat_default(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "  File: /d/a.txt" in out
    assert "Size: 4" in out
    assert "regular file" in out


async def test_stat_directory_label(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "/d"], vfs))
    assert result.exit_code == 0
    assert b"directory" in result.stdout


async def test_stat_empty_file_label(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "/d/empty"], vfs))
    assert result.exit_code == 0
    assert b"regular empty file" in result.stdout


async def test_stat_format_string_size(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "-c", "%s", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"4\n"


async def test_stat_format_string_name(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "-c", "%n", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    # GNU stat emits the path as given on the command line.
    assert result.stdout == b"/d/a.txt\n"


async def test_stat_format_string_combined(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "-c", "%n %s %a", "/d/a.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/d/a.txt 4 644\n"


async def test_stat_missing(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "/missing"], vfs))
    assert result.exit_code == 1
    assert result.stderr == b"stat: cannot statx '/missing': No such file or directory\n"


async def test_stat_multiple_paths(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "/d/a.txt", "/d/empty"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "  File: /d/a.txt" in out
    assert "  File: /d/empty" in out
    # Blank line separation
    assert "\n\n  File: /d/empty" in out


async def test_stat_filesystem_flag(vfs: MatrxAsyncFS) -> None:
    cmd = get("stat")
    assert cmd is not None
    result = await cmd(make_ctx(["stat", "-f", "/d"], vfs))
    assert result.exit_code == 0
    assert b'File: "/d"' in result.stdout
