from __future__ import annotations

import io
import tarfile

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext
from matrx_ai.tools.vfs.commands.tar import cmd_tar
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-test"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/work")
    await fs._mkdir("/work/src")
    await fs._pipe_file("/work/src/a.txt", b"hello\n")
    await fs._pipe_file("/work/src/b.txt", b"world\n")
    await fs._mkdir("/work/src/sub")
    await fs._pipe_file("/work/src/sub/c.txt", b"deep\n")
    return fs


def _ctx(
    vfs: MatrxAsyncFS, argv: list[str], stdin: bytes = b"", cwd: str = "/work"
) -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


async def test_create_and_extract_roundtrip(vfs: MatrxAsyncFS) -> None:
    res = await cmd_tar(_ctx(vfs, ["tar", "-cf", "out.tar", "src"]))
    assert res.exit_code == 0
    assert await vfs._exists("/work/out.tar")

    # Extract into a fresh dir.
    await vfs._mkdir("/work/extract")
    res2 = await cmd_tar(
        _ctx(vfs, ["tar", "-xf", "out.tar", "-C", "extract"])
    )
    assert res2.exit_code == 0
    assert await vfs._exists("/work/extract/src/a.txt")
    data = await vfs._cat_file("/work/extract/src/a.txt")
    assert data == b"hello\n"
    assert await vfs._exists("/work/extract/src/sub/c.txt")


async def test_create_with_gzip(vfs: MatrxAsyncFS) -> None:
    res = await cmd_tar(_ctx(vfs, ["tar", "-czf", "out.tgz", "src"]))
    assert res.exit_code == 0
    archive = await vfs._cat_file("/work/out.tgz")
    # Gzip magic bytes
    assert archive[:2] == b"\x1f\x8b"


async def test_extract_gzip(vfs: MatrxAsyncFS) -> None:
    await cmd_tar(_ctx(vfs, ["tar", "-czf", "out.tgz", "src"]))
    await vfs._mkdir("/work/out2")
    res = await cmd_tar(
        _ctx(vfs, ["tar", "-xzf", "out.tgz", "-C", "out2"])
    )
    assert res.exit_code == 0
    assert await vfs._exists("/work/out2/src/a.txt")


async def test_list(vfs: MatrxAsyncFS) -> None:
    await cmd_tar(_ctx(vfs, ["tar", "-cf", "out.tar", "src"]))
    res = await cmd_tar(_ctx(vfs, ["tar", "-tf", "out.tar"]))
    assert res.exit_code == 0
    out = res.stdout.decode()
    assert "src/a.txt" in out
    assert "src/b.txt" in out
    assert "src/sub/c.txt" in out


async def test_list_verbose(vfs: MatrxAsyncFS) -> None:
    await cmd_tar(_ctx(vfs, ["tar", "-cf", "out.tar", "src"]))
    res = await cmd_tar(_ctx(vfs, ["tar", "-tvf", "out.tar"]))
    assert res.exit_code == 0
    out = res.stdout.decode()
    # Format includes permission bits like -rw-r--r--
    assert "rw-" in out
    assert "src/a.txt" in out


async def test_list_gzip(vfs: MatrxAsyncFS) -> None:
    await cmd_tar(_ctx(vfs, ["tar", "-czf", "out.tgz", "src"]))
    res = await cmd_tar(_ctx(vfs, ["tar", "-tzf", "out.tgz"]))
    assert res.exit_code == 0
    assert b"src/a.txt" in res.stdout


async def test_missing_source(vfs: MatrxAsyncFS) -> None:
    res = await cmd_tar(_ctx(vfs, ["tar", "-cf", "out.tar", "nope"]))
    assert res.exit_code == 2
    assert b"Cannot stat" in res.stderr


async def test_bad_archive(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/junk.tar", b"not a tar archive")
    res = await cmd_tar(_ctx(vfs, ["tar", "-tf", "junk.tar"]))
    assert res.exit_code == 2
    assert b"does not look like a tar archive" in res.stderr


async def test_chdir_C_for_create(vfs: MatrxAsyncFS) -> None:
    res = await cmd_tar(
        _ctx(vfs, ["tar", "-cf", "out.tar", "-C", "src", "a.txt"])
    )
    assert res.exit_code == 0
    res2 = await cmd_tar(_ctx(vfs, ["tar", "-tf", "out.tar"]))
    assert b"a.txt" in res2.stdout


async def test_strip_components(vfs: MatrxAsyncFS) -> None:
    await cmd_tar(_ctx(vfs, ["tar", "-cf", "out.tar", "src"]))
    await vfs._mkdir("/work/strip")
    res = await cmd_tar(
        _ctx(
            vfs,
            ["tar", "-xf", "out.tar", "-C", "strip", "--strip-components=1"],
        )
    )
    assert res.exit_code == 0
    assert await vfs._exists("/work/strip/a.txt")


async def test_extract_from_external_tar(vfs: MatrxAsyncFS) -> None:
    # Build a tar using stdlib outside the vfs.
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        info = tarfile.TarInfo(name="external.txt")
        data = b"external content\n"
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    await vfs._pipe_file("/work/external.tar", buf.getvalue())

    await vfs._mkdir("/work/ex")
    res = await cmd_tar(_ctx(vfs, ["tar", "-xf", "external.tar", "-C", "ex"]))
    assert res.exit_code == 0
    data = await vfs._cat_file("/work/ex/external.txt")
    assert data == b"external content\n"


async def test_no_operation(vfs: MatrxAsyncFS) -> None:
    res = await cmd_tar(_ctx(vfs, ["tar", "-f", "x.tar"]))
    assert res.exit_code == 2
