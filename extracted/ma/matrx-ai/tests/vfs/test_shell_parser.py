from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.shell.ast import (
    AndOrList,
    CmdSubPart,
    CommandList,
    LiteralPart,
    Pipeline,
    Redirect,
    SimpleCommand,
    Subshell,
    VarPart,
)
from matrx_ai.tools.vfs.shell.parser import ShellParseError, parse


def _first_simple(cl: CommandList) -> SimpleCommand:
    return cl.items[0].pipelines[0].commands[0]  # type: ignore[return-value]


def _word_to_text(w) -> str:
    bits: list[str] = []
    for p in w.parts:
        if isinstance(p, LiteralPart):
            bits.append(p.text)
        elif isinstance(p, VarPart):
            bits.append(f"${p.name}")
        else:
            bits.append(f"<{type(p).__name__}>")
    return "".join(bits)


def test_simple_ls():
    cl = parse("ls -la")
    assert isinstance(cl, CommandList)
    cmd = _first_simple(cl)
    assert isinstance(cmd, SimpleCommand)
    assert [_word_to_text(w) for w in cmd.argv] == ["ls", "-la"]


def test_pipeline():
    cl = parse("ls -la | grep foo")
    pipe = cl.items[0].pipelines[0]
    assert isinstance(pipe, Pipeline)
    assert len(pipe.commands) == 2


def test_andor():
    cl = parse("cmd1 && cmd2 || cmd3")
    andor = cl.items[0]
    assert isinstance(andor, AndOrList)
    assert len(andor.pipelines) == 3
    assert andor.operators == ["&&", "||"]


def test_redirect_stdout_and_stderr():
    cl = parse("cmd > out 2> err")
    cmd = _first_simple(cl)
    assert len(cmd.redirects) == 2
    ops = [r.op for r in cmd.redirects]
    assert ops == [">", "2>"]
    assert cmd.redirects[0].fd == 1
    assert cmd.redirects[1].fd == 2


def test_heredoc_collected():
    cl = parse("cat <<EOF\nhello\nworld\nEOF\n")
    cmd = _first_simple(cl)
    assert len(cmd.redirects) == 1
    r = cmd.redirects[0]
    assert isinstance(r, Redirect)
    assert r.op == "<<"
    assert r.heredoc_body == "hello\nworld\n"
    assert r.heredoc_quoted is False


def test_heredoc_quoted_terminator():
    cl = parse("cat <<'EOF'\n$VAR not expanded\nEOF\n")
    cmd = _first_simple(cl)
    r = cmd.redirects[0]
    assert r.heredoc_quoted is True
    assert r.heredoc_body == "$VAR not expanded\n"


def test_heredoc_dash_strips_tabs():
    cl = parse("cat <<-EOF\n\thello\n\tEOF\n")
    cmd = _first_simple(cl)
    r = cmd.redirects[0]
    assert r.op == "<<-"
    assert r.heredoc_body == "hello\n"


def test_subshell():
    cl = parse("(a; b) | c")
    pipe = cl.items[0].pipelines[0]
    assert isinstance(pipe.commands[0], Subshell)
    assert isinstance(pipe.commands[1], SimpleCommand)


def test_assignment_prefix():
    cl = parse("VAR=value cmd")
    cmd = _first_simple(cl)
    assert cmd.assignments == [("VAR", cmd.assignments[0][1])]
    assert cmd.assignments[0][0] == "VAR"


def test_assignment_only():
    cl = parse("FOO=bar")
    cmd = _first_simple(cl)
    assert cmd.argv == []
    assert cmd.assignments[0][0] == "FOO"


def test_command_sub_in_argv():
    cl = parse("echo $(date)")
    cmd = _first_simple(cl)
    assert any(isinstance(p, CmdSubPart) for p in cmd.argv[1].parts)


def test_separator_semicolon():
    cl = parse("a; b; c")
    assert len(cl.items) == 3
    assert cl.separators[:2] == [";", ";"]


def test_background_amp():
    cl = parse("a & b")
    assert cl.separators[0] == "&"


def test_negated_pipeline():
    cl = parse("! true")
    pipe = cl.items[0].pipelines[0]
    assert pipe.negated is True


def test_parse_error_on_dangling_pipe():
    with pytest.raises(ShellParseError):
        parse("foo |")


def test_redirect_to_var_target():
    cl = parse("cmd > $OUT")
    cmd = _first_simple(cl)
    assert cmd.redirects[0].op == ">"
    target = cmd.redirects[0].target
    assert target is not None
    assert any(isinstance(p, VarPart) for p in target.parts)


def test_here_string():
    cl = parse("cat <<<word")
    cmd = _first_simple(cl)
    assert cmd.redirects[0].op == "<<<"
