from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.shell.lexer import ShellSyntaxError, tokenize


def kinds(toks):
    return [t.kind for t in toks if t.kind != "EOF"]


def values(toks):
    return [t.value for t in toks if t.kind != "EOF"]


def test_simple_command():
    toks = tokenize("ls -la /tmp")
    assert kinds(toks) == ["WORD", "WORD", "WORD"]
    assert values(toks) == ["ls", "-la", "/tmp"]


def test_pipe_operator():
    toks = tokenize("ls | grep foo")
    assert kinds(toks) == ["WORD", "OPERATOR", "WORD", "WORD"]
    assert values(toks) == ["ls", "|", "grep", "foo"]


def test_andor_operators():
    toks = tokenize("a && b || c")
    assert values(toks) == ["a", "&&", "b", "||", "c"]


def test_redirect_operators():
    toks = tokenize("cmd > out 2>err >> app")
    assert values(toks) == ["cmd", ">", "out", "2>", "err", ">>", "app"]


def test_amp_redirect():
    toks = tokenize("cmd &> all &>> app")
    assert values(toks) == ["cmd", "&>", "all", "&>>", "app"]


def test_single_quoted():
    toks = tokenize("echo 'hello world'")
    assert values(toks) == ["echo", "'hello world'"]
    # quoted_segments preserved
    segs = toks[1].quoted_segments
    assert segs is not None
    assert segs == [("sq", "hello world")]


def test_double_quoted():
    toks = tokenize('echo "hi $USER"')
    assert values(toks) == ["echo", '"hi $USER"']
    segs = toks[1].quoted_segments
    assert segs is not None
    assert segs[0][0] == "dq"


def test_assign_prefix():
    toks = tokenize("FOO=bar cmd")
    assert toks[0].kind == "ASSIGN_PREFIX"
    assert toks[0].value == "FOO=bar"
    assert toks[1].kind == "WORD"


def test_assign_with_quotes():
    toks = tokenize('FOO="hello world" cmd')
    assert toks[0].kind == "ASSIGN_PREFIX"


def test_command_substitution_dollar_paren():
    toks = tokenize("echo $(date)")
    assert values(toks) == ["echo", "$(date)"]


def test_nested_command_substitution():
    toks = tokenize("echo $(echo $(date))")
    assert values(toks) == ["echo", "$(echo $(date))"]


def test_backtick_substitution():
    toks = tokenize("echo `date`")
    assert values(toks) == ["echo", "`date`"]


def test_arith_expansion():
    toks = tokenize("echo $((1+2))")
    assert values(toks) == ["echo", "$((1+2))"]


def test_brace_var():
    toks = tokenize('echo "${VAR:-default}"')
    assert toks[1].kind == "WORD"
    # ensure the brace var stayed inside dq segment intact
    segs = toks[1].quoted_segments
    assert segs is not None
    seg = segs[0]
    assert "${VAR:-default}" in seg[1]


def test_comment_stripped():
    toks = tokenize("ls # this is a comment\nls -la")
    assert kinds(toks) == ["WORD", "NEWLINE", "WORD", "WORD"]


def test_line_continuation():
    toks = tokenize("echo \\\nhello")
    assert values(toks) == ["echo", "hello"]


def test_subshell_parens():
    toks = tokenize("(a; b) | c")
    assert values(toks) == ["(", "a", ";", "b", ")", "|", "c"]


def test_heredoc_operator():
    toks = tokenize("cat <<EOF")
    # heredoc preprocess hasn't run here — tokenize sees the raw operators.
    assert "<<" in [t.value for t in toks]


def test_here_string():
    toks = tokenize("cat <<<word")
    assert values(toks) == ["cat", "<<<", "word"]


def test_unmatched_quote_raises():
    with pytest.raises(ShellSyntaxError):
        tokenize("echo 'unterminated")


def test_unmatched_dquote_raises():
    with pytest.raises(ShellSyntaxError):
        tokenize('echo "unterminated')


def test_escape_outside_quotes():
    toks = tokenize(r"echo a\ b")
    assert toks[1].kind == "WORD"
    # The escape preserves space within the word, no boundary.
    assert toks[1].value == r"a\ b"


def test_numeric_fd_redirect():
    toks = tokenize("cmd 3> file")
    assert toks[1].kind == "OPERATOR"
    assert toks[1].value == "3>"


def test_ansi_c_quoting_segment():
    toks = tokenize(r"echo $'hi\n'")
    assert toks[1].kind == "WORD"
    # ANSI-C segment should be preserved verbatim within the word value
    assert "$'hi\\n'" in toks[1].value


def test_semicolon_separator():
    toks = tokenize("a; b; c")
    assert values(toks) == ["a", ";", "b", ";", "c"]


def test_background_amp():
    toks = tokenize("a &")
    assert values(toks) == ["a", "&"]
