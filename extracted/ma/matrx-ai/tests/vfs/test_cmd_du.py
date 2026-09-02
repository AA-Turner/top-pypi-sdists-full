from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-du"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/data", create_parents=False)
    await fs._mkdir("/data/sub", create_parents=False)
    await fs._pipe_file("/data/a.txt", b"x" * 2048)
    await fs._pipe_file("/data/sub/b.txt", b"y" * 4096)
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_du_basic_directory(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "/data"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    # Root /data must be the last line.
    lines = out.splitlines()
    assert lines[-1].endswith("\t/data")
    # Subdirectory listed.
    assert any(line.endswith("\t/data/sub") for line in lines)


async def test_du_summarize(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "-s", "/data"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    lines = out.splitlines()
    assert len(lines) == 1
    assert lines[0].endswith("\t/data")


async def test_du_human(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "-sh", "/data"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    # 6144 total bytes -> "6.0K"
    assert out.endswith("\t/data\n")
    assert "K" in out


async def test_du_a_includes_files(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "-a", "/data"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "/data/a.txt" in out
    assert "/data/sub/b.txt" in out


async def test_du_max_depth(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "--max-depth=0", "/data"], vfs))
    assert result.exit_code == 0
    lines = result.stdout.decode().splitlines()
    assert len(lines) == 1
    assert lines[0].endswith("\t/data")


async def test_du_total_flag(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "-c", "/data"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert out.rstrip("\n").splitlines()[-1].endswith("\ttotal")


async def test_du_missing(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "/nope"], vfs))
    assert result.exit_code == 1
    assert (
        result.stderr
        == b"du: cannot access '/nope': No such file or directory\n"
    )


async def test_du_block_size_default_is_1k(vfs: MatrxAsyncFS) -> None:
    cmd = get("du")
    assert cmd is not None
    result = await cmd(make_ctx(["du", "-s", "/data"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    # 6144 bytes / 1024 = 6 blocks
    size_str = out.split("\t")[0]
    assert size_str == "6"
