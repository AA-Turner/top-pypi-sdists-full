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
    await fs._pipe_file(
        "/tmp/data.txt",
        b"alpha 1 100\nbeta 2 200\ngamma 3 300\ndelta 4 400\n",
    )
    await fs._pipe_file(
        "/tmp/passwd",
        b"root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\nuser:x:1000:1000:User:/home/user:/bin/bash\n",
    )
    await fs._pipe_file(
        "/tmp/numbers.txt",
        b"1\n5\n10\n3\n7\n",
    )
    await fs._pipe_file(
        "/tmp/empty.txt",
        b"",
    )
    return fs


async def _run(vfs, argv, stdin=b"", cwd="/tmp"):
    cmd = get("awk")
    assert cmd is not None
    env = ShellEnv(cwd=cwd)
    ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=vfs)
    return await cmd(ctx)


# ---------------------------------------------------------------------------
# Basic field printing
# ---------------------------------------------------------------------------


async def test_print_first_field(vfs):
    r = await _run(vfs, ["awk", "{print $1}", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha\nbeta\ngamma\ndelta\n"


async def test_print_dollar_zero(vfs):
    r = await _run(vfs, ["awk", "{print $0}", "numbers.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"1\n5\n10\n3\n7\n"


async def test_print_default_action(vfs):
    r = await _run(vfs, ["awk", "{print}", "numbers.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"1\n5\n10\n3\n7\n"


async def test_print_multiple_fields_uses_ofs(vfs):
    r = await _run(vfs, ["awk", "{print $1, $3}", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha 100\nbeta 200\ngamma 300\ndelta 400\n"


# ---------------------------------------------------------------------------
# BEGIN / END
# ---------------------------------------------------------------------------


async def test_begin_end_with_fs(vfs):
    r = await _run(
        vfs,
        ["awk", 'BEGIN { FS=":"; print "header" } { print $1, $3 }', "passwd"],
    )
    assert r.exit_code == 0
    assert r.stdout == b"header\nroot 0\nbin 1\nuser 1000\n"


async def test_begin_only_no_input(vfs):
    r = await _run(vfs, ["awk", 'BEGIN { print "hello" }'])
    assert r.exit_code == 0
    assert r.stdout == b"hello\n"


async def test_sum_with_end(vfs):
    r = await _run(
        vfs,
        ["awk", "BEGIN { sum = 0 } { sum += $1 } END { print sum }", "numbers.txt"],
    )
    assert r.exit_code == 0
    assert r.stdout == b"26\n"


# ---------------------------------------------------------------------------
# Pattern matching
# ---------------------------------------------------------------------------


async def test_regex_pattern(vfs):
    r = await _run(vfs, ["awk", "/beta/ { print }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"beta 2 200\n"


async def test_boolean_pattern_default_print(vfs):
    r = await _run(vfs, ["awk", "$1 > 5", "numbers.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"10\n7\n"


async def test_nr_pattern(vfs):
    r = await _run(vfs, ["awk", "NR == 3", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"gamma 3 300\n"


async def test_multi_rule_script(vfs):
    script = '/alpha/ { print "A" } /gamma/ { print "G" }'
    r = await _run(vfs, ["awk", script, "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"A\nG\n"


# ---------------------------------------------------------------------------
# CLI options
# ---------------------------------------------------------------------------


async def test_F_option(vfs):
    r = await _run(vfs, ["awk", "-F:", "{ print $1 }", "passwd"])
    assert r.exit_code == 0
    assert r.stdout == b"root\nbin\nuser\n"


async def test_F_option_separate_arg(vfs):
    r = await _run(vfs, ["awk", "-F", ":", "{ print $7 }", "passwd"])
    assert r.exit_code == 0
    assert r.stdout == b"/bin/bash\n/sbin/nologin\n/bin/bash\n"


async def test_v_option(vfs):
    r = await _run(vfs, ["awk", "-v", "x=10", "BEGIN { print x }"])
    assert r.exit_code == 0
    assert r.stdout == b"10\n"


async def test_v_option_inline(vfs):
    r = await _run(vfs, ["awk", "-vx=hello", 'BEGIN { print x }'])
    assert r.exit_code == 0
    assert r.stdout == b"hello\n"


# ---------------------------------------------------------------------------
# printf
# ---------------------------------------------------------------------------


async def test_printf_basic(vfs):
    r = await _run(vfs, ["awk", '{ printf "%d: %s\\n", NR, $0 }', "numbers.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"1: 1\n2: 5\n3: 10\n4: 3\n5: 7\n"


async def test_printf_padding(vfs):
    r = await _run(vfs, ["awk", '{ printf "%5d\\n", $1 }', "numbers.txt"])
    assert r.exit_code == 0
    # Each line padded to width 5.
    assert r.stdout == b"    1\n    5\n   10\n    3\n    7\n"


# ---------------------------------------------------------------------------
# Builtin functions
# ---------------------------------------------------------------------------


async def test_gsub(vfs):
    r = await _run(vfs, ["awk", "{ gsub(/a/, \"X\"); print }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"XlphX 1 100\nbetX 2 200\ngXmmX 3 300\ndeltX 4 400\n"


async def test_sub(vfs):
    r = await _run(vfs, ["awk", "{ sub(/a/, \"X\"); print }", "data.txt"])
    assert r.exit_code == 0
    # sub replaces first occurrence only.
    assert r.stdout == b"Xlpha 1 100\nbetX 2 200\ngXmma 3 300\ndeltX 4 400\n"


async def test_length_builtin(vfs):
    r = await _run(vfs, ["awk", "{ print length($0) }", "numbers.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"1\n1\n2\n1\n1\n"


async def test_substr_builtin(vfs):
    r = await _run(vfs, ["awk", "{ print substr($0, 1, 5) }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha\nbeta \ngamma\ndelta\n"


async def test_tolower_toupper(vfs):
    r = await _run(vfs, ["awk", "{ print tolower(\"ABC\"), toupper(\"def\") }"], stdin=b"x\n")
    assert r.exit_code == 0
    assert r.stdout == b"abc DEF\n"


async def test_index_builtin(vfs):
    r = await _run(vfs, ["awk", 'BEGIN { print index("hello", "ll") }'])
    assert r.exit_code == 0
    assert r.stdout == b"3\n"


async def test_split_builtin(vfs):
    r = await _run(
        vfs,
        ["awk", 'BEGIN { n = split("a,b,c", arr, ","); print n, arr[1], arr[3] }'],
    )
    assert r.exit_code == 0
    assert r.stdout == b"3 a c\n"


async def test_match_builtin(vfs):
    r = await _run(
        vfs,
        ["awk", 'BEGIN { match("hello world", /world/); print RSTART, RLENGTH }'],
    )
    assert r.exit_code == 0
    assert r.stdout == b"7 5\n"


async def test_sprintf_builtin(vfs):
    r = await _run(
        vfs,
        ["awk", 'BEGIN { s = sprintf("%05d", 42); print s }'],
    )
    assert r.exit_code == 0
    assert r.stdout == b"00042\n"


# ---------------------------------------------------------------------------
# Control flow
# ---------------------------------------------------------------------------


async def test_if_else(vfs):
    r = await _run(
        vfs,
        ["awk", "{ if ($1 > 5) print \"big\"; else print \"small\" }", "numbers.txt"],
    )
    assert r.exit_code == 0
    assert r.stdout == b"small\nsmall\nbig\nsmall\nbig\n"


async def test_next_skips_remaining_rules(vfs):
    script = '/alpha/ { print "skip"; next } { print $1 }'
    r = await _run(vfs, ["awk", script, "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"skip\nbeta\ngamma\ndelta\n"


async def test_exit_statement(vfs):
    r = await _run(vfs, ["awk", "NR == 2 { exit } { print }", "numbers.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"1\n"


# ---------------------------------------------------------------------------
# Regex matching operators
# ---------------------------------------------------------------------------


async def test_match_operator(vfs):
    r = await _run(vfs, ["awk", "$1 ~ /^b/ { print }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"beta 2 200\n"


async def test_not_match_operator(vfs):
    r = await _run(vfs, ["awk", "$1 !~ /^b/ { print $1 }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha\ngamma\ndelta\n"


# ---------------------------------------------------------------------------
# Stdin
# ---------------------------------------------------------------------------


async def test_stdin_input(vfs):
    r = await _run(vfs, ["awk", "{ print $2 }"], stdin=b"a 1\nb 2\nc 3\n")
    assert r.exit_code == 0
    assert r.stdout == b"1\n2\n3\n"


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


async def test_missing_file_error(vfs):
    r = await _run(vfs, ["awk", "{ print }", "missing.txt"])
    assert r.exit_code == 2
    assert r.stderr == b"awk: can't open file missing.txt\n source line number 0\n"


async def test_syntax_error(vfs):
    r = await _run(vfs, ["awk", "{ print $1 "])
    assert r.exit_code == 2
    assert r.stderr.startswith(b"awk: cmd. line:1:")
    assert b"syntax error" in r.stderr


# ---------------------------------------------------------------------------
# NF / NR
# ---------------------------------------------------------------------------


async def test_nf_variable(vfs):
    r = await _run(vfs, ["awk", "{ print NF }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"3\n3\n3\n3\n"


async def test_nr_variable(vfs):
    r = await _run(vfs, ["awk", "END { print NR }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"4\n"


async def test_filename_variable(vfs):
    r = await _run(vfs, ["awk", "{ print FILENAME }", "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"data.txt\ndata.txt\ndata.txt\ndata.txt\n"


# ---------------------------------------------------------------------------
# Empty input
# ---------------------------------------------------------------------------


async def test_empty_input(vfs):
    r = await _run(vfs, ["awk", "{ print }", "empty.txt"])
    assert r.exit_code == 0
    assert r.stdout == b""


async def test_begin_end_with_empty_input(vfs):
    r = await _run(vfs, ["awk", 'BEGIN { print "B" } END { print "E" }', "empty.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"B\nE\n"


# ---------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------


async def test_arithmetic_ops(vfs):
    r = await _run(
        vfs,
        ["awk", 'BEGIN { print 2+3, 10-4, 3*5, 10/4, 10%3 }'],
    )
    assert r.exit_code == 0
    assert r.stdout == b"5 6 15 2.5 1\n"


# ---------------------------------------------------------------------------
# Comparison operators
# ---------------------------------------------------------------------------


async def test_string_equality(vfs):
    r = await _run(vfs, ["awk", '$1 == "alpha" { print $0 }', "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"alpha 1 100\n"


async def test_string_inequality(vfs):
    r = await _run(vfs, ["awk", '$1 != "alpha" { print $1 }', "data.txt"])
    assert r.exit_code == 0
    assert r.stdout == b"beta\ngamma\ndelta\n"
