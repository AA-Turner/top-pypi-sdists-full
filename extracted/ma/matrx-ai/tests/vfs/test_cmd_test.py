from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    ws = "ws-test-cmd"
    await backend.ensure_workspace_root(ws)
    fs = MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)
    await fs._mkdir("/d", create_parents=False)
    await fs._pipe_file("/f.txt", b"hello")
    await fs._pipe_file("/empty", b"")
    await fs._pipe_file("/exec.sh", b"#!/bin/sh\n")
    # Mark exec.sh as executable.
    inode = await fs._resolve("/exec.sh")
    await fs.backend.update_inode(inode.id, mode=0o755)
    # Create a symlink.
    await fs._symlink("/f.txt", "/sym")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv, vfs):
    return CommandContext(argv=argv, stdin=b"", env=ShellEnv(), vfs=vfs)


# ---------------------------------------------------------- file tests --


async def test_test_e_existing_file_true(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-e", "/f.txt"], vfs))
    assert r.exit_code == 0


async def test_test_e_missing_false(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-e", "/missing"], vfs))
    assert r.exit_code == 1


async def test_test_f_regular_file(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-f", "/f.txt"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-f", "/d"], vfs))
    assert r.exit_code == 1


async def test_test_d_directory(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-d", "/d"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-d", "/f.txt"], vfs))
    assert r.exit_code == 1


async def test_test_L_symlink(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-L", "/sym"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-L", "/f.txt"], vfs))
    assert r.exit_code == 1


async def test_test_x_executable(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-x", "/exec.sh"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-x", "/f.txt"], vfs))
    assert r.exit_code == 1


async def test_test_s_size(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-s", "/f.txt"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-s", "/empty"], vfs))
    assert r.exit_code == 1


# -------------------------------------------------------- string tests --


async def test_test_z_empty(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-z", ""], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-z", "x"], vfs))
    assert r.exit_code == 1


async def test_test_n_nonempty(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-n", "x"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-n", ""], vfs))
    assert r.exit_code == 1


async def test_test_string_eq(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "abc", "=", "abc"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "abc", "=", "xyz"], vfs))
    assert r.exit_code == 1


async def test_test_string_ne(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "abc", "!=", "xyz"], vfs))
    assert r.exit_code == 0


async def test_test_string_lt_gt(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "a", "<", "b"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "b", ">", "a"], vfs))
    assert r.exit_code == 0


# -------------------------------------------------------- numeric tests --


async def test_test_numeric_eq(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "5", "-eq", "5"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "5", "-eq", "6"], vfs))
    assert r.exit_code == 1


async def test_test_numeric_lt_gt(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "3", "-lt", "10"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "10", "-gt", "3"], vfs))
    assert r.exit_code == 0


async def test_test_numeric_le_ge_ne(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "5", "-le", "5"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "5", "-ge", "5"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "5", "-ne", "6"], vfs))
    assert r.exit_code == 0


async def test_test_numeric_non_int_errors(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "abc", "-eq", "5"], vfs))
    assert r.exit_code == 2
    assert b"integer expression expected" in r.stderr


# ----------------------------------------------------------- logical --


async def test_test_negation(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "!", "-e", "/missing"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "!", "-e", "/f.txt"], vfs))
    assert r.exit_code == 1


async def test_test_a_and(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-e", "/f.txt", "-a", "-e", "/d"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-e", "/f.txt", "-a", "-e", "/missing"], vfs))
    assert r.exit_code == 1


async def test_test_o_or(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(make_ctx(["test", "-e", "/missing", "-o", "-e", "/f.txt"], vfs))
    assert r.exit_code == 0
    r = await cmd(make_ctx(["test", "-e", "/missing", "-o", "-e", "/missing2"], vfs))
    assert r.exit_code == 1


async def test_test_paren_grouping(vfs: MatrxAsyncFS) -> None:
    cmd = get("test")
    assert cmd is not None
    r = await cmd(
        make_ctx(
            ["test", "(", "-e", "/missing", "-o", "-e", "/f.txt", ")", "-a", "-e", "/d"],
            vfs,
        )
    )
    assert r.exit_code == 0


# ----------------------------------------------------------- [ alias --


async def test_lbracket_requires_close(vfs: MatrxAsyncFS) -> None:
    cmd = get("[")
    assert cmd is not None
    r = await cmd(make_ctx(["[", "-e", "/f.txt"], vfs))
    assert r.exit_code == 2
    assert b"missing ']'" in r.stderr


async def test_lbracket_with_close(vfs: MatrxAsyncFS) -> None:
    cmd = get("[")
    assert cmd is not None
    r = await cmd(make_ctx(["[", "-e", "/f.txt", "]"], vfs))
    assert r.exit_code == 0


async def test_lbracket_string_eq(vfs: MatrxAsyncFS) -> None:
    cmd = get("[")
    assert cmd is not None
    r = await cmd(make_ctx(["[", "abc", "=", "abc", "]"], vfs))
    assert r.exit_code == 0
