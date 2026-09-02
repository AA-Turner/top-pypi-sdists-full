from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext, get, load_all
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-ls"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    # /tmp empty
    await fs._mkdir("/tmp", create_parents=False)
    # /home/user/* basic files
    await fs._mkdir("/home", create_parents=False)
    await fs._mkdir("/home/user", create_parents=False)
    await fs._pipe_file("/home/user/a.txt", b"abc\n")
    await fs._pipe_file("/home/user/b.txt", b"x" * 100)
    await fs._pipe_file("/home/user/.hidden", b"secret\n")
    await fs._mkdir("/home/user/projects", create_parents=False)
    await fs._pipe_file("/home/user/projects/main.py", b"print('hi')\n")
    await fs._symlink("a.txt", "/home/user/link_to_a")
    return fs


@pytest_asyncio.fixture(autouse=True)
def _load_commands():
    load_all()
    yield


def make_ctx(argv: list[str], vfs: MatrxAsyncFS, cwd: str = "/") -> CommandContext:
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=b"", env=env, vfs=vfs)


async def test_ls_empty_dir(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "/tmp"], vfs, cwd="/"))
    assert result.exit_code == 0
    assert result.stdout == b""
    assert result.stderr == b""


async def test_ls_single_file(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "/home/user/a.txt"], vfs, cwd="/"))
    assert result.exit_code == 0
    assert result.stdout == b"/home/user/a.txt\n"


async def test_ls_hides_dotfiles(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    assert b".hidden" not in result.stdout
    assert b"a.txt" in result.stdout


async def test_ls_a_shows_dotfiles_and_dots(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-a", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    lines = out.splitlines()
    assert lines[0] == "."
    assert lines[1] == ".."
    assert ".hidden" in lines


async def test_ls_capital_a_shows_dotfiles_no_dots(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-A", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    lines = out.splitlines()
    assert "." not in lines
    assert ".." not in lines
    assert ".hidden" in lines


async def test_ls_l_byte_exact_against_mimicry(vfs: MatrxAsyncFS) -> None:
    from matrx_ai.tools.vfs.commands.ls import _info_to_view
    from matrx_ai.tools.vfs.mimicry import LsOpts, format_ls_l

    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-l", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0

    raw = await vfs._ls("/home/user", detail=True)
    entries = [_info_to_view(info) for info in raw]
    visible = [e for e in entries if not e["name"].startswith(".")]
    expected = format_ls_l(visible, LsOpts())
    assert result.stdout == expected.encode()


async def test_ls_lh_uses_human_sizes(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    # Make a 1500-byte file so format_size_human emits "1.5K".
    await vfs._pipe_file("/home/user/big.bin", b"x" * 1500)
    result = await cmd(make_ctx(["ls", "-lh", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    assert b"1.5K" in result.stdout


async def test_ls_one_per_line(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-1", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    lines = out.splitlines()
    assert "a.txt" in lines
    assert "b.txt" in lines
    assert "projects" in lines


async def test_ls_F_classify(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-F", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "projects/" in out.splitlines()
    assert "link_to_a@" in out.splitlines()


async def test_ls_R_recursive(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-R", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "/home/user:" in out
    assert "/home/user/projects:" in out
    assert "main.py" in out


async def test_ls_t_sorts_by_mtime(vfs: MatrxAsyncFS) -> None:
    import asyncio

    cmd = get("ls")
    assert cmd is not None
    # Create files with slight delay so mtimes differ.
    await vfs._mkdir("/sortdir", create_parents=False)
    await vfs._pipe_file("/sortdir/oldest", b"1")
    await asyncio.sleep(0.01)
    await vfs._pipe_file("/sortdir/middle", b"2")
    await asyncio.sleep(0.01)
    await vfs._pipe_file("/sortdir/newest", b"3")

    result = await cmd(make_ctx(["ls", "-t", "/sortdir"], vfs, cwd="/"))
    assert result.exit_code == 0
    lines = result.stdout.decode().splitlines()
    # newest first under -t
    assert lines == ["newest", "middle", "oldest"]


async def test_ls_r_reverses(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-r", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    lines = result.stdout.decode().splitlines()
    # Forward sort of /home/user (excluding dotfiles): a.txt b.txt link_to_a projects
    # Reversed:
    assert lines == sorted(
        ["a.txt", "b.txt", "link_to_a", "projects"],
        reverse=True,
    )


async def test_ls_missing_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "/missing"], vfs, cwd="/"))
    assert result.exit_code == 2
    assert result.stderr == b"ls: cannot access '/missing': No such file or directory\n"


async def test_ls_mixed_paths_partial_failure(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "/tmp", "/missing", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 2
    assert b"ls: cannot access '/missing'" in result.stderr
    assert b"a.txt" in result.stdout


async def test_ls_la_equals_al(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    la = await cmd(make_ctx(["ls", "-la", "/home/user"], vfs, cwd="/"))
    al = await cmd(make_ctx(["ls", "-al", "/home/user"], vfs, cwd="/"))
    assert la.stdout == al.stdout
    assert la.exit_code == al.exit_code == 0


async def test_ls_multiple_dirs_section_headers(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "/tmp", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "/tmp:\n" in out
    assert "/home/user:\n" in out
    # Sections separated by a blank line.
    assert "\n\n" in out


async def test_ls_l_symlink_arrow(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-l", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "link_to_a -> a.txt" in out


async def test_ls_unknown_flag(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "--foo"], vfs, cwd="/"))
    assert result.exit_code == 2
    assert result.stderr == (
        b"ls: unrecognized option '--foo'\nTry 'ls --help' for more information.\n"
    )


async def test_ls_no_args_uses_cwd(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls"], vfs, cwd="/home/user"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "a.txt" in out


async def test_ls_d_lists_dir_itself(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-d", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    assert result.stdout == b"/home/user\n"


async def test_ls_S_sort_by_size(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    await vfs._mkdir("/sized", create_parents=False)
    await vfs._pipe_file("/sized/small", b"x")
    await vfs._pipe_file("/sized/med", b"x" * 50)
    await vfs._pipe_file("/sized/big", b"x" * 500)
    result = await cmd(make_ctx(["ls", "-S", "/sized"], vfs, cwd="/"))
    assert result.exit_code == 0
    lines = result.stdout.decode().splitlines()
    assert lines == ["big", "med", "small"]


async def test_ls_inode_does_not_crash(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    # -i is parsed but a no-op in the simple case (no inode column added). The
    # important contract: don't error out.
    result = await cmd(make_ctx(["ls", "-i", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0


async def test_ls_l_single_file_no_total(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "-l", "/home/user/a.txt"], vfs, cwd="/"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert not out.startswith("total")
    assert "/home/user/a.txt" in out


async def test_ls_default_sort_ascii(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "/home/user"], vfs, cwd="/"))
    assert result.exit_code == 0
    lines = result.stdout.decode().splitlines()
    assert lines == sorted(lines)


async def test_ls_relative_path(vfs: MatrxAsyncFS) -> None:
    cmd = get("ls")
    assert cmd is not None
    result = await cmd(make_ctx(["ls", "user"], vfs, cwd="/home"))
    assert result.exit_code == 0
    out = result.stdout.decode()
    assert "a.txt" in out
