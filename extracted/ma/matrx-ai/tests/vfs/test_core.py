from __future__ import annotations

import errno

import pytest
import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.core import MatrxAsyncFS


@pytest_asyncio.fixture
async def fs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    instance = MatrxAsyncFS(backend, workspace_id="ws-test")
    await instance._ensure_root()
    return instance


# ---------------------------------------------------------------------------
# Read / write
# ---------------------------------------------------------------------------


async def test_pipe_and_cat_root_file(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/hello.txt", b"hi there")
    data = await fs._cat_file("/hello.txt")
    assert data == b"hi there"


async def test_cat_file_with_range(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/x", b"abcdefgh")
    assert await fs._cat_file("/x", start=2, end=5) == b"cde"


async def test_pipe_overwrites(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/x", b"first")
    await fs._pipe_file("/x", b"second-longer")
    assert await fs._cat_file("/x") == b"second-longer"
    info = await fs._info("/x")
    assert info["size"] == len(b"second-longer")


# ---------------------------------------------------------------------------
# Nested directories
# ---------------------------------------------------------------------------


async def test_makedirs_and_nested_write(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/a/b/c")
    await fs._pipe_file("/a/b/c/note.md", b"hello")
    listing = await fs._ls("/a/b/c", detail=False)
    assert "/a/b/c/note.md" in listing
    assert await fs._cat_file("/a/b/c/note.md") == b"hello"


async def test_makedirs_exist_ok(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/a/b")
    await fs._makedirs("/a/b", exist_ok=True)
    with pytest.raises(FileExistsError) as exc:
        await fs._makedirs("/a/b", exist_ok=False)
    assert exc.value.errno == errno.EEXIST


async def test_ls_detail_shape(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    await fs._pipe_file("/d/f", b"x")
    listing = await fs._ls("/d", detail=True)
    assert len(listing) == 1
    e = listing[0]
    for key in (
        "name",
        "size",
        "type",
        "mode",
        "uid",
        "gid",
        "mtime",
        "ctime",
        "atime",
        "symlink_target",
    ):
        assert key in e
    assert e["type"] == "file"
    assert e["name"] == "/d/f"
    assert e["size"] == 1


# ---------------------------------------------------------------------------
# Errno-correct exceptions
# ---------------------------------------------------------------------------


async def test_ls_missing_raises_enoent(fs: MatrxAsyncFS) -> None:
    with pytest.raises(FileNotFoundError) as exc:
        await fs._ls("/nope")
    assert exc.value.errno == errno.ENOENT  # 2


async def test_ls_on_file_raises_enotdir(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/file", b"x")
    with pytest.raises(NotADirectoryError) as exc:
        await fs._ls("/file")
    assert exc.value.errno == errno.ENOTDIR  # 20


async def test_cat_dir_raises_eisdir(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    with pytest.raises(IsADirectoryError) as exc:
        await fs._cat_file("/d")
    assert exc.value.errno == errno.EISDIR  # 21


async def test_mkdir_existing_raises_eexist(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    with pytest.raises(FileExistsError) as exc:
        await fs._mkdir("/d")
    assert exc.value.errno == errno.EEXIST  # 17


async def test_mkdir_no_parent_raises_enoent(fs: MatrxAsyncFS) -> None:
    with pytest.raises(FileNotFoundError) as exc:
        await fs._mkdir("/missing/child", create_parents=False)
    assert exc.value.errno == errno.ENOENT


async def test_rmdir_nonempty_raises_enotempty(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    await fs._pipe_file("/d/f", b"x")
    with pytest.raises(OSError) as exc:
        await fs._rmdir("/d")
    assert exc.value.errno == errno.ENOTEMPTY  # 39


async def test_rm_dir_without_recursive_raises_eisdir(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    with pytest.raises(IsADirectoryError) as exc:
        await fs._rm("/d", recursive=False)
    assert exc.value.errno == errno.EISDIR


# ---------------------------------------------------------------------------
# Removal
# ---------------------------------------------------------------------------


async def test_rm_recursive_removes_tree(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/a/b/c")
    await fs._pipe_file("/a/b/c/leaf", b"x")
    await fs._pipe_file("/a/top", b"y")
    await fs._rm("/a", recursive=True)
    assert not await fs._exists("/a")
    assert not await fs._exists("/a/b/c/leaf")


async def test_rm_file(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/x", b"x")
    await fs._rm_file("/x")
    assert not await fs._exists("/x")


async def test_rmdir_empty(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/empty")
    await fs._rmdir("/empty")
    assert not await fs._exists("/empty")


# ---------------------------------------------------------------------------
# Copy / move
# ---------------------------------------------------------------------------


async def test_cp_file(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/src", b"contents")
    await fs._cp_file("/src", "/dst")
    assert await fs._cat_file("/dst") == b"contents"
    assert await fs._cat_file("/src") == b"contents"


async def test_mv_rename_in_same_dir(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/a", b"x")
    await fs._mv("/a", "/b")
    assert not await fs._exists("/a")
    assert await fs._cat_file("/b") == b"x"


async def test_mv_across_dirs(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d1")
    await fs._makedirs("/d2")
    await fs._pipe_file("/d1/f", b"y")
    await fs._mv("/d1/f", "/d2/f")
    assert not await fs._exists("/d1/f")
    assert await fs._cat_file("/d2/f") == b"y"


async def test_mv_overwrite_file(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/a", b"new")
    await fs._pipe_file("/b", b"old")
    await fs._mv("/a", "/b")
    assert await fs._cat_file("/b") == b"new"
    assert not await fs._exists("/a")


# ---------------------------------------------------------------------------
# Glob / walk / find
# ---------------------------------------------------------------------------


async def test_glob_recursive(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/src/pkg")
    await fs._pipe_file("/src/main.py", b"")
    await fs._pipe_file("/src/pkg/util.py", b"")
    await fs._pipe_file("/src/pkg/data.txt", b"")
    matches = await fs._glob("/src/**/*.py")
    assert "/src/main.py" in matches
    assert "/src/pkg/util.py" in matches
    assert "/src/pkg/data.txt" not in matches


async def test_glob_no_magic_returns_existing(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/a", b"x")
    assert await fs._glob("/a") == ["/a"]
    assert await fs._glob("/missing") == []


async def test_walk_topdown(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/a/b")
    await fs._pipe_file("/a/f1", b"")
    await fs._pipe_file("/a/b/f2", b"")
    seen: list[tuple[str, list[str], list[str]]] = []
    async for tup in fs._walk("/a", topdown=True):
        seen.append((tup[0], sorted(tup[1]), sorted(tup[2])))
    assert seen[0][0] == "/a"
    # /a should appear before /a/b in topdown order
    paths = [t[0] for t in seen]
    assert paths.index("/a") < paths.index("/a/b")
    a_root = next(t for t in seen if t[0] == "/a")
    assert "b" in a_root[1]
    assert "f1" in a_root[2]


async def test_find_files(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/a/b")
    await fs._pipe_file("/a/x", b"")
    await fs._pipe_file("/a/b/y", b"")
    found = await fs._find("/a")
    assert sorted(found) == ["/a/b/y", "/a/x"]


async def test_du_total(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    await fs._pipe_file("/d/a", b"abc")
    await fs._pipe_file("/d/b", b"de")
    total = await fs._du("/d", total=True)
    assert total == 5


# ---------------------------------------------------------------------------
# Symlinks
# ---------------------------------------------------------------------------


async def test_symlink_creates_link(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/target", b"data")
    await fs._symlink("/target", "/link")
    info = await fs._info("/link")
    assert info["type"] == "link"
    assert info["symlink_target"] == "/target"


async def test_ls_shows_symlink(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    await fs._pipe_file("/d/real", b"x")
    await fs._symlink("/d/real", "/d/alias")
    listing = await fs._ls("/d", detail=True)
    types = {basename_of(e["name"]): e["type"] for e in listing}
    assert types["alias"] == "link"
    assert types["real"] == "file"


def basename_of(p: str) -> str:
    return p.rsplit("/", 1)[-1]


# ---------------------------------------------------------------------------
# touch
# ---------------------------------------------------------------------------


async def test_touch_creates_empty(fs: MatrxAsyncFS) -> None:
    await fs._touch("/new")
    assert await fs._exists("/new")
    assert await fs._cat_file("/new") == b""


async def test_touch_truncates(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/x", b"hello")
    await fs._touch("/x", truncate=True)
    assert await fs._cat_file("/x") == b""


async def test_touch_no_truncate_preserves(fs: MatrxAsyncFS) -> None:
    await fs._pipe_file("/x", b"hello")
    await fs._touch("/x", truncate=False)
    assert await fs._cat_file("/x") == b"hello"


# ---------------------------------------------------------------------------
# Predicates
# ---------------------------------------------------------------------------


async def test_isdir_isfile(fs: MatrxAsyncFS) -> None:
    await fs._makedirs("/d")
    await fs._pipe_file("/f", b"x")
    assert await fs._isdir("/d")
    assert not await fs._isfile("/d")
    assert await fs._isfile("/f")
    assert not await fs._isdir("/f")
    assert await fs._isdir("/")
    assert not await fs._isdir("/missing")


# ---------------------------------------------------------------------------
# Workspace isolation
# ---------------------------------------------------------------------------


async def test_workspace_isolation() -> None:
    backend = MemoryBackend()
    fs1 = MatrxAsyncFS(backend, workspace_id="ws-1")
    fs2 = MatrxAsyncFS(backend, workspace_id="ws-2")
    await fs1._ensure_root()
    await fs2._ensure_root()
    await fs1._pipe_file("/shared.txt", b"ws1")
    await fs2._pipe_file("/shared.txt", b"ws2")
    assert await fs1._cat_file("/shared.txt") == b"ws1"
    assert await fs2._cat_file("/shared.txt") == b"ws2"
    assert "/shared.txt" in await fs1._ls("/", detail=False)
    assert "/shared.txt" in await fs2._ls("/", detail=False)


# ---------------------------------------------------------------------------
# Error: ensure os.strerror messages are wired through
# ---------------------------------------------------------------------------


async def test_strerror_present(fs: MatrxAsyncFS) -> None:
    import os

    with pytest.raises(FileNotFoundError) as exc:
        await fs._ls("/no")
    assert os.strerror(errno.ENOENT) in str(exc.value)
