from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-file"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/d", create_parents=False)
    await fs._pipe_file("/empty.txt", b"")
    await fs._pipe_file("/text.txt", b"hello world\n")
    await fs._pipe_file("/script.py", b"print('hi')\n")
    await fs._pipe_file("/shellsh.sh", b"#!/bin/bash\necho hi\n")
    await fs._pipe_file("/data.bin", b"abc\x00def\xff\xfe")
    await fs._pipe_file("/cfg.json", b'{"k": 1}\n')
    await fs._pipe_file("/binary_no_ext", b"abc\x00\xff\xfe")
    await fs._symlink("text.txt", "/link.txt")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_file_empty(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/empty.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/empty.txt: empty\n"


async def test_file_directory(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/d"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/d: directory\n"


async def test_file_text(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/text.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/text.txt: ASCII text\n"


async def test_file_python(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/script.py"], vfs))
    assert result.exit_code == 0
    assert b"Python script" in result.stdout


async def test_file_shell(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/shellsh.sh"], vfs))
    assert result.exit_code == 0
    assert b"shell script" in result.stdout.lower()


async def test_file_binary(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/binary_no_ext"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/binary_no_ext: data\n"


async def test_file_json(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/cfg.json"], vfs))
    assert result.exit_code == 0
    assert b"JSON" in result.stdout


async def test_file_symlink(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/link.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/link.txt: symbolic link to text.txt\n"


async def test_file_missing_exits_zero(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/nope.txt"], vfs))
    assert result.exit_code == 0
    # GNU file uses backtick + apostrophe quirk.
    assert (
        result.stdout
        == b"/nope.txt: cannot open `/nope.txt' (No such file or directory)\n"
    )


async def test_file_multiple(vfs: MatrxAsyncFS) -> None:
    cmd = get("file")
    assert cmd is not None
    result = await cmd(make_ctx(["file", "/empty.txt", "/text.txt"], vfs))
    assert result.exit_code == 0
    assert result.stdout == b"/empty.txt: empty\n/text.txt: ASCII text\n"
