from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, load_all
from matrx_ai.tools.vfs.commands.registry import get
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv

load_all()


@pytest.fixture
async def vfs():
    backend = MemoryBackend()
    ws = "ws-test"
    await backend.ensure_workspace_root(ws)
    fs = MatrxAsyncFS(backend=backend, workspace_id=ws, asynchronous=True)
    await fs._mkdir("/work")
    await fs._pipe_file("/work/a.txt", b"hello world\nfoo bar\nhello there\n")
    await fs._pipe_file("/work/lines.txt", b"line1\nline2\nline3\nline4\nline5\n")
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/work"):
    cmd = get("sed")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


async def test_sed_substitute_first(vfs):
    r = await _run(vfs, ["sed", "s/hello/HI/", "a.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"HI world\nfoo bar\nHI there\n"


async def test_sed_substitute_global(vfs):
    r = await _run(vfs, ["sed", "s/o/0/g"], stdin=b"foo bar boom\n")
    assert r.stdout == b"f00 bar b00m\n"


async def test_sed_alternate_delimiter(vfs):
    r = await _run(vfs, ["sed", "s|hello|HI|g", "a.txt"])
    assert r.stdout == b"HI world\nfoo bar\nHI there\n"


async def test_sed_backreference(vfs):
    r = await _run(vfs, ["sed", "-E", "s/(hello) (world)/\\2 \\1/"], stdin=b"hello world\n")
    assert r.stdout == b"world hello\n"


async def test_sed_quiet_mode_with_p(vfs):
    r = await _run(vfs, ["sed", "-n", "/hello/p", "a.txt"])
    assert r.stdout == b"hello world\nhello there\n"


async def test_sed_delete_address(vfs):
    r = await _run(vfs, ["sed", "/foo/d", "a.txt"])
    assert r.stdout == b"hello world\nhello there\n"


async def test_sed_quit_at_address(vfs):
    r = await _run(vfs, ["sed", "2q", "lines.txt"])
    assert r.stdout == b"line1\nline2\n"


async def test_sed_print_line_numbers(vfs):
    r = await _run(vfs, ["sed", "=", "lines.txt"])
    assert r.stdout == (b"1\nline1\n2\nline2\n3\nline3\n4\nline4\n5\nline5\n")


async def test_sed_address_range_delete(vfs):
    r = await _run(vfs, ["sed", "2,4d", "lines.txt"])
    assert r.stdout == b"line1\nline5\n"


async def test_sed_in_place(vfs):
    r = await _run(vfs, ["sed", "-i", "s/hello/HI/g", "a.txt"])
    assert r.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"HI world\nfoo bar\nHI there\n"


async def test_sed_in_place_with_backup_suffix(vfs):
    r = await _run(vfs, ["sed", "-i.bak", "s/hello/HI/g", "a.txt"])
    assert r.exit_code == 0
    data = await vfs._cat_file("/work/a.txt")
    assert data == b"HI world\nfoo bar\nHI there\n"
    backup = await vfs._cat_file("/work/a.txt.bak")
    assert backup == b"hello world\nfoo bar\nhello there\n"


async def test_sed_multiple_e(vfs):
    r = await _run(
        vfs, ["sed", "-e", "s/hello/HI/", "-e", "s/world/EARTH/"], stdin=b"hello world\n"
    )
    assert r.stdout == b"HI EARTH\n"


async def test_sed_command_separator_semicolon(vfs):
    r = await _run(vfs, ["sed", "s/a/A/;s/b/B/"], stdin=b"abc\n")
    assert r.stdout == b"ABc\n"


async def test_sed_missing_file(vfs):
    r = await _run(vfs, ["sed", "s/x/y/", "missing.txt"])
    assert r.exit_code == 2
    assert r.stderr == b"sed: can't read missing.txt: No such file or directory\n"


async def test_sed_unterminated_substitute(vfs):
    r = await _run(vfs, ["sed", "s/foo"], stdin=b"foo\n")
    assert r.exit_code == 1
    assert b"unterminated" in r.stderr


async def test_sed_step_address(vfs):
    # 1~2 = line 1, then every 2nd
    r = await _run(vfs, ["sed", "-n", "1~2p", "lines.txt"])
    assert r.stdout == b"line1\nline3\nline5\n"


async def test_sed_last_line_address(vfs):
    r = await _run(vfs, ["sed", "$d", "lines.txt"])
    assert r.stdout == b"line1\nline2\nline3\nline4\n"


async def test_sed_substitute_nth_match(vfs):
    r = await _run(vfs, ["sed", "s/o/0/2"], stdin=b"foo bar\n")
    # Replace 2nd occurrence of 'o' only.
    assert r.stdout == b"fo0 bar\n"
