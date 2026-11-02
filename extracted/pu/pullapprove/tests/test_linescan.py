"""Unit tests for the string-literal-aware line scanners.

These exercise the tokenizers directly (rather than through hunk classification)
so the tricky string-awareness cases are easy to read and extend.
"""

from __future__ import annotations

import pytest
from pullapprove.trust.comments import strip_inline_comment
from pullapprove.trust.linescan import (
    collapse_ws,
    collapse_ws_outside_strings,
    consume_string,
)


def test_collapse_ws():
    assert collapse_ws("  a   b\tc  ") == "a b c"


@pytest.mark.parametrize(
    ("text", "start", "expected"),
    [
        pytest.param('"abc" x', 0, 5, id="plain-string"),
        pytest.param('"a\\"b" x', 0, 6, id="escaped-quote-inside"),
        # An escaped backslash right before the close quote must not hide the close:
        # `"a\\"` is a terminated string (value `a\`), so the close is at index 8.
        pytest.param('x = "a\\\\" + y', 4, 9, id="escaped-backslash-before-close"),
        # Unterminated: return the end of the text rather than overshoot.
        pytest.param('"abc', 0, 4, id="unterminated"),
    ],
)
def test_consume_string(text, start, expected):
    assert consume_string(text, start) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param("  a   b\tc  ", "a b c", id="outside-strings-collapsed"),
        # Whitespace inside a string literal is preserved.
        pytest.param('x = "a  b"', 'x = "a  b"', id="string-interior-preserved"),
        pytest.param("x = 'a  b'", "x = 'a  b'", id="single-quote-interior"),
        pytest.param("x = `a  b`", "x = `a  b`", id="backtick-interior"),
        # ...but whitespace between literals still collapses.
        pytest.param('f("a  b" ,  "c")', 'f("a  b" , "c")', id="between-strings"),
    ],
)
def test_collapse_ws_outside_strings(text, expected):
    assert collapse_ws_outside_strings(text) == expected


@pytest.mark.parametrize(
    ("line", "prefixes", "expected"),
    [
        pytest.param("x = 1  # note", ("#",), "x = 1", id="strips-trailing-comment"),
        pytest.param("code  // note", ("//",), "code", id="slash-comment"),
        pytest.param("x = 1", ("#",), "x = 1", id="no-comment-unchanged"),
        # The prefix appears inside a string -> NOT a comment.
        pytest.param('x = "a # b"', ("#",), 'x = "a # b"', id="hash-in-string-ignored"),
        pytest.param(
            'x = "a # b"  # real', ("#",), 'x = "a # b"', id="hash-in-string-then-real"
        ),
        # Escaped quote doesn't end the string early.
        pytest.param('x = "a\\"# b"', ("#",), 'x = "a\\"# b"', id="escaped-quote"),
        # A prefix glued to a preceding token (no space) isn't a comment — it's
        # part of a value, e.g. a YAML URL fragment.
        pytest.param(
            "url: https://x/#frag",
            ("#",),
            "url: https://x/#frag",
            id="hash-glued-to-value",
        ),
    ],
)
def test_strip_inline_comment(line, prefixes, expected):
    assert strip_inline_comment(line, prefixes) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        # A `//` inside a backtick template literal is not a comment.
        pytest.param("const u = `http://x`", "const u = `http://x`", id="template-url"),
        pytest.param("const u = `a` // real", "const u = `a`", id="template-then-real"),
    ],
)
def test_strip_inline_comment_backtick(line, expected):
    assert strip_inline_comment(line, ("//",), "\"'`") == expected
