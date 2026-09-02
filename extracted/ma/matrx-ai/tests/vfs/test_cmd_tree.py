from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-tree"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/proj", create_parents=False)
    await fs._mkdir("/proj/src", create_parents=False)
    await fs._mkdir("/empty", create_parents=False)
    await fs._pipe_file("/proj/README.md", b"# proj\n")
    await fs._pipe_file("/proj/src/main.py", b"x = 1\n")
    await fs._pipe_file("/proj/.hidden", b"secret\n")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_tree_basic(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "/proj"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert out.startswith("/proj\n")
    assert "├── README.md" in out or "└── README.md" in out
    assert "└── src" in out
    assert "└── main.py" in out
    # report — root is not counted; one subdir + two files
    assert "1 directory, 2 files\n" in out


async def test_tree_dotfiles_hidden_default(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "/proj"], vfs))
    assert result.exit_code == 0
    assert b".hidden" not in result.stdout


async def test_tree_a_shows_dotfiles(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "-a", "/proj"], vfs))
    assert result.exit_code == 0
    assert b".hidden" in result.stdout


async def test_tree_d_only_dirs(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "-d", "/proj"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "main.py" not in out
    assert "src" in out
    assert "1 directory\n" in out


async def test_tree_max_depth(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "-L", "1", "/proj"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "main.py" not in out
    assert "src" in out


async def test_tree_empty_dir(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "/empty"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert out.startswith("/empty\n")
    assert "0 directories, 0 files\n" in out


async def test_tree_missing_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "/no_such"], vfs))
    # GNU tree exits 0 even on missing.
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "/no_such [error opening dir]" in out
    assert "0 directories, 0 files\n" in out


async def test_tree_noreport(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "--noreport", "/proj"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "directories" not in out
    assert "files" not in out


async def test_tree_singular_units(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    # Make a fresh dir with exactly 1 file and 1 subdir-with-no-files.
    await vfs._mkdir("/single", create_parents=False)
    await vfs._mkdir("/single/dir", create_parents=False)
    await vfs._pipe_file("/single/file.txt", b"x")
    result = await cmd(make_ctx(["tree", "/single"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "1 directory, 1 file\n" in out


async def test_tree_full_paths(vfs: MatrxAsyncFS) -> None:
    cmd = get("tree")
    assert cmd is not None
    result = await cmd(make_ctx(["tree", "-f", "/proj"], vfs))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "/proj/README.md" in out
    assert "/proj/src/main.py" in out
