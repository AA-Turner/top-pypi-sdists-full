from __future__ import annotations

import pytest_asyncio

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import CommandContext
from matrx_ai.tools.vfs.commands.grep import cmd_grep
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest_asyncio.fixture
async def vfs() -> MatrxAsyncFS:
    backend = MemoryBackend()
    workspace_id = "ws-test"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/work")
    await fs._pipe_file(
        "/work/a.txt",
        b"alpha line\nbeta line\nGAMMA line\nalpha again\n",
    )
    await fs._pipe_file(
        "/work/b.txt",
        b"foo\nbar\nbaz\n",
    )
    await fs._pipe_file("/work/empty.txt", b"")
    await fs._mkdir("/work/sub")
    await fs._pipe_file("/work/sub/c.txt", b"alpha sub\nzeta line\n")
    await fs._pipe_file("/work/sub/d.py", b"def alpha():\n    pass\n")
    await fs._mkdir("/work/sub/node_modules")
    await fs._pipe_file(
        "/work/sub/node_modules/skip.txt",
        b"alpha junk\n",
    )
    await fs._pipe_file("/work/binary.bin", b"alpha\x00binary\nmore\n")
    return fs


def _ctx(vfs: MatrxAsyncFS, argv: list[str], stdin: bytes = b"", cwd: str = "/work"):
    env = ShellEnv(cwd=cwd)
    return CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)


# ---------------------------------------------------------------------------
# Single-file basic match
# ---------------------------------------------------------------------------


async def test_single_file_match_emits_line(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "beta", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"beta line\n"


async def test_single_file_no_match(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "zzz", "a.txt"]))
    assert res.exit_code == 1
    assert res.stdout == b""


async def test_empty_file_no_output(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "x", "empty.txt"]))
    assert res.exit_code == 1
    assert res.stdout == b""


async def test_empty_pattern_matches_every_line(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"foo\nbar\nbaz\n"


# ---------------------------------------------------------------------------
# Filename prefix
# ---------------------------------------------------------------------------


async def test_multiple_files_prefix(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "alpha", "a.txt", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"a.txt:alpha line\na.txt:alpha again\n"


async def test_force_filename_with_H(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-H", "beta", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"a.txt:beta line\n"


async def test_suppress_filename_with_h(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-h", "alpha", "a.txt", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"alpha line\nalpha again\n"


# ---------------------------------------------------------------------------
# -n line numbers
# ---------------------------------------------------------------------------


async def test_lineno_single_file(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-n", "alpha", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"1:alpha line\n4:alpha again\n"


async def test_lineno_multiple_files(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-n", "alpha", "a.txt", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"a.txt:1:alpha line\na.txt:4:alpha again\n"


# ---------------------------------------------------------------------------
# -r recursive
# ---------------------------------------------------------------------------


async def test_recursive_with_lineno(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-rn", "alpha", "/work"]))
    assert res.exit_code == 0
    out = res.stdout.decode()
    assert "/work/a.txt:1:alpha line" in out
    assert "/work/a.txt:4:alpha again" in out
    assert "/work/sub/c.txt:1:alpha sub" in out
    assert "/work/sub/d.py:1:def alpha():" in out


async def test_recursive_default_path_dot(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-rn", "beta"]))
    assert res.exit_code == 0
    assert b"beta line" in res.stdout


# ---------------------------------------------------------------------------
# -l / -L
# ---------------------------------------------------------------------------


async def test_files_with_matches(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-l", "alpha", "a.txt", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"a.txt\n"


async def test_files_without_match(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-L", "alpha", "a.txt", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"b.txt\n"


# ---------------------------------------------------------------------------
# -c count
# ---------------------------------------------------------------------------


async def test_count_single_file(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-c", "alpha", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"2\n"


async def test_count_multiple_files_zero_for_no_match(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-c", "alpha", "a.txt", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"a.txt:2\nb.txt:0\n"


# ---------------------------------------------------------------------------
# -v invert
# ---------------------------------------------------------------------------


async def test_invert_match(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-v", "alpha", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"beta line\nGAMMA line\n"


# ---------------------------------------------------------------------------
# -i / -w / -x
# ---------------------------------------------------------------------------


async def test_ignore_case(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-i", "gamma", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"GAMMA line\n"


async def test_word_regexp(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/words.txt", b"foo\nfoobar\nfoo bar\n")
    res = await cmd_grep(_ctx(vfs, ["grep", "-w", "foo", "words.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"foo\nfoo bar\n"


async def test_line_regexp(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-x", "foo", "b.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"foo\n"


# ---------------------------------------------------------------------------
# -F fixed strings
# ---------------------------------------------------------------------------


async def test_fixed_strings(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/dot.txt", b"a.b\naxb\n")
    res = await cmd_grep(_ctx(vfs, ["grep", "-F", "a.b", "dot.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"a.b\n"


# ---------------------------------------------------------------------------
# Context: -A / -B / -C / -m
# ---------------------------------------------------------------------------


async def test_after_context(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/ctx.txt", b"l1\nl2\nMATCH\nl4\nl5\nl6\nMATCH\nl8\n")
    res = await cmd_grep(_ctx(vfs, ["grep", "-A2", "MATCH", "ctx.txt"]))
    assert res.exit_code == 0
    expected = b"MATCH\nl4\nl5\n--\nMATCH\nl8\n"
    assert res.stdout == expected


async def test_before_context(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/ctx.txt", b"l1\nl2\nMATCH\nl4\nl5\nl6\nMATCH\nl8\n")
    res = await cmd_grep(_ctx(vfs, ["grep", "-B2", "MATCH", "ctx.txt"]))
    assert res.exit_code == 0
    # Group 1 = lines 1..3, Group 2 = lines 5..7. Non-adjacent, so '--' separator.
    expected = b"l1\nl2\nMATCH\n--\nl5\nl6\nMATCH\n"
    assert res.stdout == expected


async def test_around_context(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/ctx.txt", b"l1\nl2\nMATCH\nl4\nl5\n")
    res = await cmd_grep(_ctx(vfs, ["grep", "-C1", "MATCH", "ctx.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"l2\nMATCH\nl4\n"


async def test_max_count(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-m", "1", "alpha", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"alpha line\n"


# ---------------------------------------------------------------------------
# --include / --exclude-dir
# ---------------------------------------------------------------------------


async def test_include_glob(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(
        _ctx(vfs, ["grep", "--include=*.py", "-r", "alpha", "/work"])
    )
    assert res.exit_code == 0
    assert res.stdout == b"/work/sub/d.py:def alpha():\n"


async def test_exclude_dir(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(
        _ctx(vfs, ["grep", "--exclude-dir=node_modules", "-r", "alpha", "/work"])
    )
    assert res.exit_code == 0
    out = res.stdout.decode()
    assert "node_modules" not in out
    assert "/work/a.txt:alpha line" in out


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


async def test_missing_file_emits_error_exit_2(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "x", "/missing"]))
    assert res.exit_code == 2
    assert res.stderr == b"grep: /missing: No such file or directory\n"


async def test_directory_without_recursive(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "alpha", "/work"]))
    assert res.exit_code == 2
    assert res.stderr == b"grep: /work: Is a directory\n"


async def test_no_pattern_usage_error(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep"]))
    assert res.exit_code == 2
    assert b"Usage: grep" in res.stderr


async def test_bad_regex_exit_2(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "[unclosed", "a.txt"]))
    assert res.exit_code == 2
    assert res.stderr.startswith(b"grep:")


# ---------------------------------------------------------------------------
# Quiet
# ---------------------------------------------------------------------------


async def test_quiet_match(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-q", "alpha", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b""
    assert res.stderr == b""


async def test_quiet_no_match(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-q", "zzz", "a.txt"]))
    assert res.exit_code == 1
    assert res.stdout == b""


# ---------------------------------------------------------------------------
# Binary detection
# ---------------------------------------------------------------------------


async def test_binary_default_match(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "alpha", "binary.bin"]))
    assert res.exit_code == 0
    assert res.stdout == b"Binary file binary.bin matches\n"


async def test_binary_skip_with_capital_I(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-I", "alpha", "binary.bin"]))
    assert res.exit_code == 1
    assert res.stdout == b""


async def test_binary_text_flag_emits_content(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-a", "alpha", "binary.bin"]))
    assert res.exit_code == 0
    assert b"alpha" in res.stdout


# ---------------------------------------------------------------------------
# Aliases
# ---------------------------------------------------------------------------


async def test_egrep_alias_uses_extended(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["egrep", "alpha|beta", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"alpha line\nbeta line\nalpha again\n"


async def test_fgrep_alias_treats_as_literal(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/dot.txt", b"a.b\naxb\n")
    res = await cmd_grep(_ctx(vfs, ["fgrep", "a.b", "dot.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"a.b\n"


async def test_rgrep_alias_recurses(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["rgrep", "alpha", "/work"]))
    assert res.exit_code == 0
    assert b"/work/a.txt:" in res.stdout


# ---------------------------------------------------------------------------
# Multiple -e patterns
# ---------------------------------------------------------------------------


async def test_multiple_e_patterns(vfs: MatrxAsyncFS) -> None:
    res = await cmd_grep(_ctx(vfs, ["grep", "-e", "alpha", "-e", "beta", "a.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"alpha line\nbeta line\nalpha again\n"


# ---------------------------------------------------------------------------
# -o only-matching
# ---------------------------------------------------------------------------


async def test_only_matching(vfs: MatrxAsyncFS) -> None:
    await vfs._pipe_file("/work/om.txt", b"alpha bravo alpha\nzeta\n")
    res = await cmd_grep(_ctx(vfs, ["grep", "-o", "alpha", "om.txt"]))
    assert res.exit_code == 0
    assert res.stdout == b"alpha\nalpha\n"
