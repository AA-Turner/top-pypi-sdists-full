"""Test lexers module"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import pygments.lexers
import pytest
from pygments import __version__ as pygments_version
from pygments.lexers import BashLexer
from pygments.token import Token

import ipython_pygments_lexers as lexers

pyg214 = tuple(int(x) for x in pygments_version.split(".")[:2]) >= (2, 14)

TOKEN_WS = Token.Text.Whitespace if pyg214 else Token.Text

EXPECTED_LEXER_NAMES = [
    cls.name for cls in [lexers.IPythonConsoleLexer, lexers.IPython3Lexer]
]


@pytest.mark.parametrize("expected_lexer", EXPECTED_LEXER_NAMES)
def test_pygments_entry_points(expected_lexer: str):
    """Check whether the ``entry_points`` for ``pygments.lexers`` are correct."""
    all_pygments_lexer_names = {l[0] for l in pygments.lexers.get_all_lexers()}
    assert expected_lexer in all_pygments_lexer_names


def test_plain_python():
    lexer = lexers.IPythonLexer()
    fragment_2 = "x != y\n"
    tokens_2 = [
        (Token.Name, "x"),
        (Token.Text, " "),
        (Token.Operator, "!="),
        (Token.Text, " "),
        (Token.Name, "y"),
        (Token.Text, "\n"),
    ]
    assert tokens_2[:-1] == list(lexer.get_tokens(fragment_2))[:-1]


def test_shell_commands():
    lexer = lexers.IPythonLexer()
    bash_lexer = BashLexer()
    fragment = "!echo $HOME\n"
    bash_tokens = [
        (Token.Operator, "!"),
    ]
    bash_tokens.extend(bash_lexer.get_tokens(fragment[1:]))
    ipylex_token = list(lexer.get_tokens(fragment))
    assert bash_tokens[:-1] == ipylex_token[:-1]

    fragment_2 = "!" + fragment
    tokens_2 = [
        (Token.Operator, "!!"),
    ] + bash_tokens[1:]
    assert tokens_2[:-1] == list(lexer.get_tokens(fragment_2))[:-1]

    fragment_2 = "\t %%!\n" + fragment[1:]
    tokens_2 = [
        (Token.Text, "\t "),
        (Token.Operator, "%%!"),
        (Token.Text, "\n"),
    ] + bash_tokens[1:]
    assert tokens_2 == list(lexer.get_tokens(fragment_2))

    fragment_2 = "x = " + fragment
    tokens_2 = [
        (Token.Name, "x"),
        (Token.Text, " "),
        (Token.Operator, "="),
        (Token.Text, " "),
    ] + bash_tokens
    assert tokens_2[:-1] == list(lexer.get_tokens(fragment_2))[:-1]

    fragment_2 = "x, = " + fragment
    tokens_2 = [
        (Token.Name, "x"),
        (Token.Punctuation, ","),
        (Token.Text, " "),
        (Token.Operator, "="),
        (Token.Text, " "),
    ] + bash_tokens
    assert tokens_2[:-1] == list(lexer.get_tokens(fragment_2))[:-1]

    fragment_2 = "x, = %sx " + fragment[1:]
    tokens_2 = [
        (Token.Name, "x"),
        (Token.Punctuation, ","),
        (Token.Text, " "),
        (Token.Operator, "="),
        (Token.Text, " "),
        (Token.Operator, "%"),
        (Token.Keyword, "sx"),
        (TOKEN_WS, " "),
    ] + bash_tokens[1:]
    assert tokens_2[:-1] == list(lexer.get_tokens(fragment_2))[:-1]


def test_magics():
    lexer = lexers.IPythonLexer()
    fragment_2 = "f = %R function () {}\n"
    tokens_2 = [
        (Token.Name, "f"),
        (Token.Text, " "),
        (Token.Operator, "="),
        (Token.Text, " "),
        (Token.Operator, "%"),
        (Token.Keyword, "R"),
        (Token.Text, " function () {}\n"),
    ]
    assert tokens_2 == list(lexer.get_tokens(fragment_2))

    fragment_2 = "%system?\n"
    tokens_2 = [
        (Token.Operator, "%"),
        (Token.Keyword, "system"),
        (Token.Operator, "?"),
        (Token.Text, "\n"),
    ]
    assert tokens_2[:-1] == list(lexer.get_tokens(fragment_2))[:-1]


def test_help():
    lexer = lexers.IPythonLexer()
    fragment_2 = " ?math.sin\n"
    tokens_2 = [
        (Token.Text, " "),
        (Token.Operator, "?"),
        (Token.Text, "math.sin"),
        (Token.Text, "\n"),
    ]
    assert tokens_2[:-1] == list(lexer.get_tokens(fragment_2))[:-1]

    fragment = " *int*?\n"
    tokens = [
        (Token.Text, " *int*"),
        (Token.Operator, "?"),
        (Token.Text, "\n"),
    ]
    assert tokens == list(lexer.get_tokens(fragment))


def test_cell_magics():
    lexer = lexers.IPythonLexer()
    fragment = "%%writefile -a foo.py\nif a == b:\n    pass"
    tokens = [
        (Token.Operator, "%%writefile"),
        (Token.Text, " -a foo.py\n"),
        (Token.Keyword, "if"),
        (Token.Text, " "),
        (Token.Name, "a"),
        (Token.Text, " "),
        (Token.Operator, "=="),
        (Token.Text, " "),
        (Token.Name, "b"),
        (Token.Punctuation, ":"),
        (TOKEN_WS, "\n"),
        (Token.Text, "    "),
        (Token.Keyword, "pass"),
        (TOKEN_WS, "\n"),
    ]
    assert tokens == list(lexer.get_tokens(fragment))

    fragment = "%%timeit\nmath.sin(0)"
    tokens = [
        (Token.Operator, "%%timeit"),
        (Token.Text, "\n"),
        (Token.Name, "math"),
        (Token.Operator, "."),
        (Token.Name, "sin"),
        (Token.Punctuation, "("),
        (Token.Literal.Number.Integer, "0"),
        (Token.Punctuation, ")"),
        (TOKEN_WS, "\n"),
    ]
    assert tokens == list(lexer.get_tokens(fragment))

    fragment = "%%HTML\n<div>foo</div>"
    tokens = [
        (Token.Operator, "%%HTML"),
        (Token.Text, "\n"),
        (Token.Punctuation, "<"),
        (Token.Name.Tag, "div"),
        (Token.Punctuation, ">"),
        (Token.Text, "foo"),
        (Token.Punctuation, "<"),
        (Token.Punctuation, "/"),
        (Token.Name.Tag, "div"),
        (Token.Punctuation, ">"),
        (Token.Text, "\n"),
    ]
    assert tokens == list(lexer.get_tokens(fragment))

    fragment_2 = "\t%%xyz\n$foo\n"
    tokens_2 = [
        (Token.Text, "\t"),
        (Token.Operator, "%%"),
        (Token.Keyword, "xyz"),
        (Token.Text, "\n$foo\n"),
    ]
    assert tokens_2 == list(lexer.get_tokens(fragment_2))
