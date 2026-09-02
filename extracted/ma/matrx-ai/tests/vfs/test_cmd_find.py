from __future__ import annotations

import time
from datetime import UTC, datetime, timedelta

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext
from matrx_ai.tools.vfs.commands.find import cmd_find  # noqa: F401  ensures registration
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    ws = "ws-find"
    await backend.ensure_workspace_root(ws)
    fs = MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)
    # Tree:
    #   /a.py
    #   /b.md
    #   /sub/c.py
    #   /sub/deep/d.py
    await fs._pipe_file("/a.py", b"hello")
    await fs._pipe_file("/b.md", b"# README")
    await fs._mkdir("/sub")
    await fs._pipe_file("/sub/c.py", b"x" * 50)
    await fs._mkdir("/sub/deep")
    await fs._pipe_file("/sub/deep/d.py", b"y" * 5000)
    return fs


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


def _lines(out: bytes) -> list[str]:
    return out.decode().splitlines()


# ---------------------------------------------------------------------------
# Default behavior + prefix preservation
# ---------------------------------------------------------------------------


async def test_find_dot_lists_all_with_dot_prefix(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", "."], vfs, cwd="/"))
    assert res.exit_code == 0
    assert res.stderr == b""
    lines = _lines(res.stdout)
    assert lines == [
        ".",
        "./a.py",
        "./b.md",
        "./sub",
        "./sub/c.py",
        "./sub/deep",
        "./sub/deep/d.py",
    ]


async def test_find_absolute_path_uses_absolute_prefix(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", "/sub"], vfs))
    assert res.exit_code == 0
    lines = _lines(res.stdout)
    assert lines == ["/sub", "/sub/c.py", "/sub/deep", "/sub/deep/d.py"]


async def test_find_no_path_defaults_to_dot(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find"], vfs, cwd="/"))
    assert res.exit_code == 0
    lines = _lines(res.stdout)
    assert lines[0] == "."
    assert all(line.startswith(".") for line in lines)


async def test_find_siblings_sorted_lexicographically(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/zebra.txt", b"")
    await vfs._pipe_file("/alpha.txt", b"")
    res = await cmd_find(make_ctx(["find", ".", "-maxdepth", "1", "-type", "f"], vfs, cwd="/"))
    files = _lines(res.stdout)
    # Alphabetic order
    assert files == ["./a.py", "./alpha.txt", "./b.md", "./zebra.txt"]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


async def test_find_name_glob(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-name", "*.py"], vfs, cwd="/"))
    assert res.exit_code == 0
    assert _lines(res.stdout) == ["./a.py", "./sub/c.py", "./sub/deep/d.py"]


async def test_find_iname_case_insensitive(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/UPPER.PY", b"")
    res = await cmd_find(make_ctx(["find", ".", "-iname", "*.py"], vfs, cwd="/"))
    lines = _lines(res.stdout)
    assert "./UPPER.PY" in lines
    assert "./a.py" in lines


async def test_find_path_glob(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-path", "./sub/*"], vfs, cwd="/"))
    lines = _lines(res.stdout)
    assert lines == ["./sub/c.py", "./sub/deep", "./sub/deep/d.py"]


async def test_find_type_f(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-type", "f"], vfs, cwd="/"))
    assert _lines(res.stdout) == [
        "./a.py",
        "./b.md",
        "./sub/c.py",
        "./sub/deep/d.py",
    ]


async def test_find_type_d(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-type", "d"], vfs, cwd="/"))
    assert _lines(res.stdout) == [".", "./sub", "./sub/deep"]


async def test_find_maxdepth(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-maxdepth", "1"], vfs, cwd="/"))
    lines = _lines(res.stdout)
    assert lines == [".", "./a.py", "./b.md", "./sub"]


async def test_find_mindepth(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-mindepth", "2"], vfs, cwd="/"))
    lines = _lines(res.stdout)
    # depth 0 = ".", depth 1 = top-level entries, depth 2+ = nested
    assert "." not in lines
    assert "./a.py" not in lines
    assert "./sub/c.py" in lines
    assert "./sub/deep/d.py" in lines


async def test_find_mtime_within_one_day(vfs: MatrxAsyncFS) -> None:
    # By default, freshly created files have mtime ~now.
    res = await cmd_find(make_ctx(["find", ".", "-mtime", "-1", "-type", "f"], vfs, cwd="/"))
    assert res.exit_code == 0
    files = _lines(res.stdout)
    assert "./a.py" in files


async def test_find_mtime_plus_30_days_ago(vfs: MatrxAsyncFS) -> None:
    # Make /a.py 60 days old
    inode = await vfs._resolve("/a.py")
    old_dt = datetime.now(UTC) - timedelta(days=60)
    await vfs.backend.update_inode(inode.id, mtime=old_dt)
    res = await cmd_find(make_ctx(["find", ".", "-mtime", "+30", "-type", "f"], vfs, cwd="/"))
    files = _lines(res.stdout)
    assert files == ["./a.py"]


async def test_find_size_plus_1k(vfs: MatrxAsyncFS) -> None:
    # /sub/deep/d.py is 5000 bytes (~5K), the rest are smaller.
    res = await cmd_find(make_ctx(["find", ".", "-size", "+1k", "-type", "f"], vfs, cwd="/"))
    files = _lines(res.stdout)
    assert files == ["./sub/deep/d.py"]


async def test_find_size_in_bytes(vfs: MatrxAsyncFS) -> None:
    # /a.py is 5 bytes.
    res = await cmd_find(make_ctx(["find", ".", "-size", "5c", "-type", "f"], vfs, cwd="/"))
    assert _lines(res.stdout) == ["./a.py"]


async def test_find_empty(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/empty.txt", b"")
    await vfs._mkdir("/emptydir")
    res = await cmd_find(make_ctx(["find", ".", "-empty"], vfs, cwd="/"))
    lines = _lines(res.stdout)
    assert "./empty.txt" in lines
    assert "./emptydir" in lines
    # /sub has children
    assert "./sub" not in lines


async def test_find_or(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(
        make_ctx(["find", ".", "-name", "*.py", "-or", "-name", "*.md"], vfs, cwd="/")
    )
    files = _lines(res.stdout)
    assert files == ["./a.py", "./b.md", "./sub/c.py", "./sub/deep/d.py"]


async def test_find_implicit_and(vfs: MatrxAsyncFS) -> None:
    # All .py files have non-zero size in fixture.
    res = await cmd_find(
        make_ctx(["find", ".", "-name", "*.py", "-and", "-size", "+0"], vfs, cwd="/")
    )
    assert _lines(res.stdout) == ["./a.py", "./sub/c.py", "./sub/deep/d.py"]


async def test_find_not(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(
        make_ctx(["find", ".", "-type", "f", "-not", "-name", "*.py"], vfs, cwd="/")
    )
    assert _lines(res.stdout) == ["./b.md"]


async def test_find_grouping(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(
        make_ctx(
            [
                "find",
                ".",
                "(",
                "-name",
                "*.py",
                "-or",
                "-name",
                "*.md",
                ")",
                "-type",
                "f",
            ],
            vfs,
            cwd="/",
        )
    )
    assert _lines(res.stdout) == [
        "./a.py",
        "./b.md",
        "./sub/c.py",
        "./sub/deep/d.py",
    ]


async def test_find_regex(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-regex", r"\./sub/.*\.py"], vfs, cwd="/"))
    assert _lines(res.stdout) == ["./sub/c.py", "./sub/deep/d.py"]


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


async def test_find_missing_path(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", "/missing"], vfs))
    assert res.exit_code == 1
    assert res.stderr == b"find: '/missing': No such file or directory\n"
    assert res.stdout == b""


async def test_find_missing_path_continues_others(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", "/missing", "/sub"], vfs))
    assert res.exit_code == 1
    assert b"'/missing'" in res.stderr
    assert b"/sub" in res.stdout


async def test_find_missing_arg_to_name(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-name"], vfs, cwd="/"))
    assert res.exit_code == 1
    assert res.stderr == b"find: missing argument to '-name'\n"


async def test_find_unknown_predicate(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-foo"], vfs, cwd="/"))
    assert res.exit_code == 1
    assert res.stderr == b"find: unknown predicate '-foo'\n"


async def test_find_path_after_expr_is_error(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-name", "*.py", "extra"], vfs, cwd="/"))
    assert res.exit_code == 1
    assert b"paths must precede expression" in res.stderr


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


async def test_find_print0(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-name", "*.py", "-print0"], vfs, cwd="/"))
    chunks = res.stdout.split(b"\x00")
    # Last split is empty if data ends with \0; here we don't have trailing \0
    # so 3 NUL-separated paths means 3 chunks total.
    paths = [c for c in chunks if c]
    assert paths == [b"./a.py", b"./sub/c.py", b"./sub/deep/d.py"]


async def test_find_delete(vfs: MatrxAsyncFS) -> None:
    # Delete all .py files; the rest of the tree should remain.
    res = await cmd_find(
        make_ctx(["find", ".", "-name", "*.py", "-type", "f", "-delete"], vfs, cwd="/")
    )
    assert res.exit_code == 0
    # /a.py, /sub/c.py, /sub/deep/d.py gone; /b.md remains
    assert not await vfs._exists("/a.py")
    assert not await vfs._exists("/sub/c.py")
    assert not await vfs._exists("/sub/deep/d.py")
    assert await vfs._exists("/b.md")
    assert await vfs._exists("/sub")
    assert await vfs._exists("/sub/deep")


async def test_find_prune_skips_subtree(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(
        make_ctx(
            ["find", ".", "-name", "sub", "-prune", "-or", "-print"],
            vfs,
            cwd="/",
        )
    )
    lines = _lines(res.stdout)
    # Root + top-level files emitted; nothing under /sub
    assert "./a.py" in lines
    assert "./b.md" in lines
    assert "./sub/c.py" not in lines
    assert "./sub/deep" not in lines
    # ./sub itself is NOT printed because the AND short-circuits and -or skips
    # the right side when left is true.
    assert "./sub" not in lines


async def test_find_quit_stops_immediately(vfs: MatrxAsyncFS) -> None:
    # -quit after the first match terminates traversal.
    res = await cmd_find(
        make_ctx(
            ["find", ".", "-name", "a.py", "-print", "-quit"],
            vfs,
            cwd="/",
        )
    )
    lines = _lines(res.stdout)
    assert lines == ["./a.py"]


async def test_find_ls_action(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(make_ctx(["find", ".", "-name", "a.py", "-ls"], vfs, cwd="/"))
    assert res.exit_code == 0
    line = res.stdout.decode().rstrip("\n")
    assert "./a.py" in line
    assert "-rw-r--r--" in line


async def test_find_exec_dispatches_registered(vfs: MatrxAsyncFS) -> None:
    # Ensure the cat command is registered, then -exec cat {} \; on a small file.
    from matrx_ai.tools.vfs.commands import cat as _cat_module  # noqa: F401

    res = await cmd_find(
        make_ctx(
            ["find", ".", "-name", "a.py", "-exec", "cat", "{}", ";"],
            vfs,
            cwd="/",
        )
    )
    assert res.exit_code == 0
    assert res.stdout == b"hello"


async def test_find_exec_unknown_command(vfs: MatrxAsyncFS) -> None:
    res = await cmd_find(
        make_ctx(
            ["find", ".", "-name", "a.py", "-exec", "nonexistent", "{}", ";"],
            vfs,
            cwd="/",
        )
    )
    assert res.exit_code == 1
    assert b"find: 'nonexistent': No such file or directory\n" in res.stderr


# ---------------------------------------------------------------------------
# Sanity: time hasn't moved
# ---------------------------------------------------------------------------


def test_time_imports_resolve() -> None:
    assert callable(time.time)
