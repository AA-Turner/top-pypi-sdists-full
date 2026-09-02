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
    await fs._mkdir("/tmp", create_parents=False)
    await fs._pipe_file("/tmp/a.txt", b"alpha\nbeta\n")
    await fs._pipe_file("/tmp/b.txt", b"gamma\ndelta\n")
    await fs._pipe_file("/tmp/empty.txt", b"")
    await fs._pipe_file("/tmp/no_newline.txt", b"no_nl")
    await fs._pipe_file("/tmp/blank.txt", b"x\n\n\n\ny\n\n\nz\n")
    await fs._pipe_file("/tmp/tabs.txt", b"a\tb\tc\n")
    return fs


def _ctx(vfs, argv, stdin=b"", cwd="/tmp"):
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


async def _run(vfs, argv, stdin=b"", cwd="/tmp"):
    cmd = get("cat")
    assert cmd is not None
    return await cmd(_ctx(vfs, argv, stdin, cwd))


async def test_cat_no_args_copies_stdin(vfs):
    r = await _run(vfs, ["cat"], stdin=b"hello\nworld\n")
    assert r.exit_code == 0
    assert r.stdout == b"hello\nworld\n"
    assert r.stderr == b""


async def test_cat_single_file(vfs):
    r = await _run(vfs, ["cat", "a.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha\nbeta\n"


async def test_cat_multi_file_concat(vfs):
    r = await _run(vfs, ["cat", "a.txt", "b.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha\nbeta\ngamma\ndelta\n"


async def test_cat_byte_fidelity_no_trailing_newline(vfs):
    r = await _run(vfs, ["cat", "no_newline.txt"])
    assert r.stdout == b"no_nl"


async def test_cat_dash_reads_stdin(vfs):
    r = await _run(vfs, ["cat", "a.txt", "-", "b.txt"], stdin=b"MIDDLE\n")
    assert r.stdout == b"alpha\nbeta\nMIDDLE\ngamma\ndelta\n"


async def test_cat_missing_continues_with_exit_1(vfs):
    r = await _run(vfs, ["cat", "a.txt", "missing.txt", "b.txt"])
    assert r.exit_code == 1
    assert r.stdout == b"alpha\nbeta\ngamma\ndelta\n"
    assert r.stderr == b"cat: missing.txt: No such file or directory\n"


async def test_cat_directory_error(vfs):
    r = await _run(vfs, ["cat", "/tmp"])
    assert r.exit_code == 1
    assert r.stderr == b"cat: /tmp: Is a directory\n"


async def test_cat_n_continuous_numbering_across_files(vfs):
    r = await _run(vfs, ["cat", "-n", "a.txt", "b.txt"])
    assert r.exit_code == 0
    assert r.stdout == (
        b"     1\talpha\n"
        b"     2\tbeta\n"
        b"     3\tgamma\n"
        b"     4\tdelta\n"
    )


async def test_cat_b_only_numbers_nonblank(vfs):
    r = await _run(vfs, ["cat", "-b", "blank.txt"])
    assert r.exit_code == 0
    # Blank lines get no number; nonblank lines get numbered starting at 1.
    assert r.stdout == (
        b"     1\tx\n"
        b"\n"
        b"\n"
        b"\n"
        b"     2\ty\n"
        b"\n"
        b"\n"
        b"     3\tz\n"
    )


async def test_cat_show_ends(vfs):
    r = await _run(vfs, ["cat", "-E", "a.txt"])
    assert r.stdout == b"alpha$\nbeta$\n"


async def test_cat_show_tabs(vfs):
    r = await _run(vfs, ["cat", "-T", "tabs.txt"])
    assert r.stdout == b"a^Ib^Ic\n"


async def test_cat_a_equivalent_to_vet(vfs):
    r = await _run(vfs, ["cat", "-A", "tabs.txt"])
    assert r.stdout == b"a^Ib^Ic$\n"


async def test_cat_squeeze(vfs):
    r = await _run(vfs, ["cat", "-s", "blank.txt"])
    # Runs of empty lines collapsed to single empty line.
    assert r.stdout == b"x\n\ny\n\nz\n"


async def test_cat_clustered_flags(vfs):
    r = await _run(vfs, ["cat", "-nE", "a.txt"])
    assert r.stdout == b"     1\talpha$\n     2\tbeta$\n"


async def test_cat_long_form(vfs):
    r = await _run(vfs, ["cat", "--number", "a.txt"])
    assert r.stdout == b"     1\talpha\n     2\tbeta\n"


async def test_cat_unknown_option(vfs):
    r = await _run(vfs, ["cat", "-Z"])
    assert r.exit_code == 1
    assert b"cat: invalid option -- 'Z'" in r.stderr


async def test_cat_double_dash_separator(vfs):
    # `--` followed by a path that begins with `-` should be treated as a path.
    await vfs._pipe_file("/tmp/-weird", b"weirdo\n")
    r = await _run(vfs, ["cat", "--", "-weird"])
    assert r.exit_code == 0
    assert r.stdout == b"weirdo\n"
