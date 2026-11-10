# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project

"""
Test _collector module.
"""

from __future__ import annotations

import typing as t

import pytest

from antsibull_docutils._collector import (
    ANSIState,
    Collector,
    EmptyState,
    Formatting,
    State,
)
from antsibull_docutils._string import ASCIIStringProcessor, UnicodeStringProcessor

if t.TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Sequence

    InputElt = (
        str
        | None
        | tuple[Formatting, t.Literal["push", "pop", "clear"]]
        | tuple[t.Literal["new-par", "new-line", "new-line-force"]]
    )


def process_input(  # noqa: C901
    input: Sequence[InputElt],
    state: State,
    collector: Collector,
) -> None:
    for part in input:
        if part is None:
            collector.new_par()
        elif isinstance(part, str):
            collector.append(text=part)
        elif len(part) == 1:
            if part[0] == "new-par":
                collector.new_par()
            if part[0] == "new-line":
                collector.new_line()
            if part[0] == "new-line-force":
                collector.new_line(force=True)
        else:
            formatting, op = part
            if op == "push":
                state.push_formatting(formatting)
            if op == "pop":
                state.pop_formatting(formatting)
            if op == "clear":
                state.clear_formatting(formatting)
            collector.update_state()


TEST_ASCII_EMPTYSTATE_COLLECTOR_DATA: list[
    tuple[list[InputElt], int, bool, list[str]]
] = [
    (
        [],
        1,
        False,
        [],
    ),
    (
        ["Hello world! This is a text."],
        10,
        False,
        ["Hello", "world!", "This is a", "text."],
    ),
    (
        [
            "Hello world! This ",
            (Formatting.ITALICS, "push"),
            "is",
            (Formatting.ITALICS, "pop"),
            " a ",
            (Formatting.BOLD, "clear"),
            "text",
            (Formatting.BOLD, "push"),
            ".",
        ],
        10,
        False,
        ["Hello", "world!", "This is a", "text."],
    ),
    (
        ["Hello world! This is a text. bazbamfoo Foobarbazbam"],
        10,
        False,
        ["Hello", "world!", "This is a", "text.", "bazbamfoo", "Foobarbazb", "am"],
    ),
    (
        [
            "Hello world!",
            " ",
            "This",
            " is ",
            "a text.",
            None,
            "bazbamfoo",
            " ",
            "Foobarbazbam",
        ],
        10,
        False,
        ["Hello", "world!", "This is a", "text.", "", "bazbamfoo", "Foobarbazb", "am"],
    ),
    (
        [
            "Hello wor",
            "ld!",
        ],
        10,
        False,
        ["Hello", "world!"],
    ),
    (
        [
            ("new-line",),
            ("new-line",),
            ("new-par",),
            ("new-line",),
            "x",
        ],
        10,
        False,
        ["x"],
    ),
    (
        [
            ("new-line",),
            "a",
            ("new-line",),
            "b",
            ("new-par",),
            "c",
            ("new-line",),
            ("new-par",),
            ("new-line",),
            ("new-par",),
            "d",
            ("new-line",),
            ("new-line-force",),
            "e",
            ("new-line-force",),
            ("new-par",),
            "f",
            ("new-line-force",),
            ("new-line-force",),
            ("new-line-force",),
            "g",
        ],
        10,
        False,
        ["a", "b", "", "c", "", "d", "", "e", "", "f", "", "", "g"],
    ),
    (
        ["xyz ", (Formatting.ITALICS, "push"), " ", "x-y-z"],
        10,
        True,
        ["xyz  x-y-z"],
    ),
]


@pytest.mark.parametrize(
    "input, width, ignore_newlines, expected_lines",
    TEST_ASCII_EMPTYSTATE_COLLECTOR_DATA,
)
def test_ASCIIEmptyState_Collector(
    input: list[InputElt],
    width: int,
    ignore_newlines: bool,
    expected_lines: list[str],
) -> None:
    string_proc = ASCIIStringProcessor()
    state = EmptyState()
    assert state.clone() is state
    collector = Collector(
        width=width,
        state=state,
        string_proc=string_proc,
        ignore_newlines=ignore_newlines,
    )
    process_input(input, state, collector)
    lines = collector.close()
    for line in lines:
        print(line)
    assert lines == expected_lines


TEST_ASCII_ANSISTATE_COLLECTOR_DATA: list[
    tuple[list[InputElt], int, bool, list[str]]
] = [
    (
        [
            "Hello world! This ",
            (Formatting.ITALICS, "push"),
            "is",
            (Formatting.ITALICS, "pop"),
            " a ",
            (Formatting.BOLD, "push"),
            "text",
            (Formatting.BOLD, "pop"),
            ".",
        ],
        10,
        False,
        ["Hello", "world!", "This \033[0;3mis\033[0m a", "\033[0;1mtext\033[0m."],
    ),
    (
        [
            "Hello world! This ",
            (Formatting.ITALICS, "push"),
            "is",
            (Formatting.BOLD, "push"),
            " a ",
            (Formatting.BOLD, "push"),
            "text",
            (Formatting.BOLD, "pop"),
            ".",
            (Formatting.BOLD, "pop"),
            ".",
            (Formatting.ITALICS, "pop"),
            ".",
        ],
        10,
        False,
        [
            "Hello",
            "world!",
            "This \033[0;3mis\033[0;1;3m a\033[0m",
            "\033[0;1;3mtext.\033[0;3m.\033[0m.",
        ],
    ),
    (
        [
            "   ",
            (Formatting.ITALICS, "push"),
            "foo!",
            (Formatting.ITALICS, "pop"),
            " ",
            (Formatting.BOLD, "push"),
            "bar",
            (Formatting.BOLD, "pop"),
            " ",
        ],
        20,
        False,
        ["   \033[0;3mfoo!\033[0m \033[0;1mbar\033[0m"],
    ),
    (
        [
            (Formatting.ITALICS, "push"),
            (Formatting.ITALICS, "push"),
            (Formatting.ITALICS, "clear"),
            "x",
        ],
        1,
        False,
        ["x"],
    ),
    (
        [
            "foo  ",
            "  ",
            "bar",
        ],
        10,
        False,
        ["foo    bar"],
    ),
    (
        ["foo\nbar baz\n\nbam!"],
        10,
        False,
        ["foo", "bar baz", "", "bam!"],
    ),
    (
        ["foo\nbar baz\n\nbam!"],
        10,
        True,
        ["foo bar", "baz bam!"],
    ),
    (
        ["xyz ", (Formatting.ITALICS, "push"), " ", "x-y-z"],
        10,
        True,
        ["xyz \x1b[0;3m x-y-z\x1b[0m"],
    ),
]


@pytest.mark.parametrize(
    "input, width, ignore_newlines, expected_lines",
    TEST_ASCII_ANSISTATE_COLLECTOR_DATA,
)
def test_ASCII_ANSIState_Collector(
    input: list[InputElt],
    width: int,
    ignore_newlines: bool,
    expected_lines: list[str],
) -> None:
    string_proc = ASCIIStringProcessor()
    state = ANSIState()
    assert state.clone() is not state
    collector = Collector(
        width=width,
        state=state,
        string_proc=string_proc,
        ignore_newlines=ignore_newlines,
    )
    process_input(input, state, collector)
    lines = collector.close()
    for line in lines:
        print(line)
    assert lines == expected_lines


TEST_UNICODE_ANSISTATE_COLLECTOR_DATA: list[
    tuple[list[InputElt], int, bool, list[str]]
] = [
    (
        ["x\u00ady\u00adz ", (Formatting.ITALICS, "push"), " ", "x-y-z"],
        10,
        True,
        ["xyz \x1b[0;3m x-y-z\x1b[0m"],
    ),
    (
        ["x\u00ady\u00adz ", (Formatting.ITALICS, "push"), " ", "xyz"],
        6,
        True,
        ["xyz", "\x1b[0;3mxyz\x1b[0m"],
    ),
    (
        ["\n", (Formatting.ITALICS, "push"), "\n"],
        6,
        True,
        [],
    ),
    (
        ["\n", (Formatting.ITALICS, "push"), ("new-par",), "\n"],
        6,
        True,
        [],
    ),
    (
        [
            "load_vars - load variable files without stripping trailing whitespace. This"
            " could accidentally modify content of YAML files which end with a block scalar (",
            "https://github.com/ansible-collections/community.sops/issues/309",
            ", ",
            "https://github.com/ansible-collections/community.sops/pull/310",
            ").",
        ],
        180,
        True,
        [
            "load_vars - load variable files without stripping trailing whitespace. "
            "This could accidentally modify content of YAML files which end with a "
            "block scalar",
            "(https://github.com/ansible-collections/community.sops/issues/309, "
            "https://github.com/ansible-collections/community.sops/pull/310).",
        ],
    ),
]


@pytest.mark.parametrize(
    "input, width, ignore_newlines, expected_lines",
    TEST_UNICODE_ANSISTATE_COLLECTOR_DATA,
)
def test_Unicode_ANSIState_Collector(
    input: list[InputElt],
    width: int,
    ignore_newlines: bool,
    expected_lines: list[str],
) -> None:
    string_proc = UnicodeStringProcessor()
    state = ANSIState()
    assert state.clone() is not state
    collector = Collector(
        width=width,
        state=state,
        string_proc=string_proc,
        ignore_newlines=ignore_newlines,
    )
    process_input(input, state, collector)
    lines = collector.close()
    for line in lines:
        print(line)
    assert lines == expected_lines
