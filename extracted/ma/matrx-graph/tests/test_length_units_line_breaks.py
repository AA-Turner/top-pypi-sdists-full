"""Length units ``line_breaks`` and ``characters_collapsed``: "one line of at most N characters" as a check.

A one-line reason, title or label is a common contract (the Curator's opinion reason: no line break, at most
60 characters counted after runs of whitespace are squeezed to one space). ``lines`` cannot say it — a trailing
break still reads as one line — and ``characters`` counts doubled spaces the reader never sees.
"""

from __future__ import annotations

import pytest

from matrx_graph.checks import length_of


@pytest.mark.parametrize(("text", "breaks"), [
    ("one line", 0), ("two\nlines", 1), ("ends with a break\n", 1), ("crlf\r\nline", 1), ("", 0),
])
def test_line_breaks_counts_every_break_including_a_trailing_one(text, breaks):
    assert length_of(text, "line_breaks") == breaks


@pytest.mark.parametrize(("text", "n"), [
    ("a  b", 3), ("  padded  ", 6), ("tab\tand\nbreak", 13), ("", 0),
])
def test_characters_collapsed_counts_what_a_reader_sees(text, n):
    assert length_of(text, "characters_collapsed") == n


def test_the_old_units_are_unchanged():
    assert length_of("two words", "words") == 2
    assert length_of("a  b", "characters") == 4
