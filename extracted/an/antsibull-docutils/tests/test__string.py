# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project

"""
Test _string module.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from antsibull_docutils._string import (
    ASCIIStringProcessor,
    UnicodeStringProcessor,
    has_unicode_string_processor,
)

TEST_ASCII_STRING_PROCESSOR_GET_COLUMN_COUNT_DATA: list[tuple[str, int]] = [
    ("", 0),
    ("foo", 3),
    ("foo bar", 7),
    ("      ", 6),
]


@pytest.mark.parametrize(
    "text, expected_columns",
    TEST_ASCII_STRING_PROCESSOR_GET_COLUMN_COUNT_DATA,
)
def test_ASCIIStringProcessor_get_column_count(
    text: str,
    expected_columns: int,
) -> None:
    proc = ASCIIStringProcessor()
    columns = proc.get_column_count(text=text)
    assert columns == expected_columns


TEST_ASCII_STRING_PROCESSOR_SPLIT_DATA: list[
    tuple[str, int, int, bool, bool, list[int], str, int, str, int, str]
] = [
    (
        "",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "",
        0,
        "",
    ),
    (
        "  ",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "  ",
        2,
        "",
    ),
    (
        "  foobarbazbam  baz",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "  ",
        2,
        "foobarbazbam  baz",
    ),
    (
        "foobarbazbam  ",
        10,
        20,
        False,
        True,
        [],
        "foobarbazbam",
        12,
        "  ",
        2,
        "",
    ),
    (
        "foobarbazbam  baz",
        10,
        20,
        False,
        True,
        [],
        "foobarbazbam  baz",
        17,
        "",
        0,
        "",
    ),
    (
        "foobarbazbam  bambazfoobar",
        10,
        20,
        False,
        True,
        [],
        "foobarbazbam",
        12,
        "  ",
        2,
        "bambazfoobar",
    ),
    (
        "Hello foo!",
        10,
        20,
        False,
        False,
        [],
        "Hello foo!",
        10,
        "",
        0,
        "",
    ),
    (
        "Hello foo!  ",
        10,
        20,
        False,
        False,
        [],
        "Hello foo!",
        10,
        "  ",
        2,
        "",
    ),
    (
        "Hello  foo!",
        10,
        20,
        False,
        False,
        [],
        "Hello",
        5,
        "  ",
        2,
        "foo!",
    ),
    (
        "       foo!",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "       ",
        7,
        "foo!",
    ),
    (
        "Hello world!",
        10,
        20,
        False,
        False,
        [],
        "Hello",
        5,
        " ",
        1,
        "world!",
    ),
    (
        "Helloworld!",
        10,
        10,
        False,
        False,
        [],
        "Helloworld",
        10,
        "",
        0,
        "!",
    ),
    (
        "Helloworld!",
        10,
        20,
        False,
        True,
        [],
        "Helloworld!",
        11,
        "",
        0,
        "",
    ),
    (
        "Helloworld!  ",
        10,
        20,
        False,
        True,
        [],
        "Helloworld!",
        11,
        "  ",
        2,
        "",
    ),
    (
        "Hello wor",
        10,
        20,
        False,
        False,
        [],
        "Hello wor",
        9,
        "",
        0,
        "",
    ),
    (
        "Hello wor",
        10,
        20,
        True,
        False,
        [],
        "Hello",
        5,
        " ",
        1,
        "wor",
    ),
]


@pytest.mark.parametrize(
    "text, remaining_columns, total_columns, keep_nonseparable_end, expected_newline,"
    " expected_removed_codepoints, expected_text, expected_text_columns, expected_space,"
    " expected_space_columns, expected_remainder",
    TEST_ASCII_STRING_PROCESSOR_SPLIT_DATA,
)
def test_ASCIIStringProcessor_split(
    text: str,
    remaining_columns: int,
    total_columns: int,
    keep_nonseparable_end: bool,
    expected_newline: bool,
    expected_removed_codepoints: list[str],
    expected_text: str,
    expected_text_columns: int,
    expected_space: str,
    expected_space_columns: int,
    expected_remainder: str,
) -> None:
    proc = ASCIIStringProcessor()
    newline, removed_codepoints, text, text_columns, space, space_columns, remainder = (
        proc.split(
            text=text,
            remaining_columns=remaining_columns,
            total_columns=total_columns,
            keep_nonseparable_end=keep_nonseparable_end,
        )
    )
    print(
        newline,
        removed_codepoints,
        repr(text),
        text_columns,
        repr(space),
        space_columns,
        repr(remainder),
    )
    assert newline == expected_newline
    assert removed_codepoints == expected_removed_codepoints
    assert text == expected_text
    assert text_columns == expected_text_columns
    assert space == expected_space
    assert space_columns == expected_space_columns
    assert remainder == expected_remainder


TEST_UNICODE_STRING_PROCESSOR_GET_COLUMN_COUNT_DATA: list[tuple[str, int]] = [
    ("", 0),
    ("foo", 3),
    ("foo bar", 7),
    ("      ", 6),
    # The following use grapheme cluster examples from
    # https://www.unicode.org/reports/tr29/#Grapheme_Cluster_Boundaries
    # The column counts are not what we would expect from looking at the result,
    # so a better implementation that improves on this is definitely welcome...
    (
        "நி",  # Tamil ni grapheme (two codeopints)
        2,
    ),
    (
        "กำ",  # Thai kam grapheme (two codepoints)
        2,
    ),
    (
        "षि",  # Devanagari ssi grapheme (two codepoints)
        2,
    ),
    (
        "क्षि",  # Devanagari kshi grapheme (four codepoints)
        3,
    ),
    (
        "क्षि",  # Devanagari kshi grapheme (four codepoints)
        3,
    ),
]


@pytest.mark.parametrize(
    "text, expected_columns",
    TEST_UNICODE_STRING_PROCESSOR_GET_COLUMN_COUNT_DATA,
)
def test_UnicodeStringProcessor_get_column_count(
    text: str,
    expected_columns: int,
) -> None:
    proc = UnicodeStringProcessor()
    columns = proc.get_column_count(text=text)
    assert columns == expected_columns


TEST_UNICODE_STRING_PROCESSOR_SPLIT_DATA: list[
    tuple[str, int, int, bool, bool, list[int], str, int, str, int, str]
] = [
    (
        "",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "",
        0,
        "",
    ),
    (
        "  ",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "  ",
        2,
        "",
    ),
    (
        "  foobarbazbam  baz",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "  ",
        2,
        "foobarbazbam  baz",
    ),
    (
        "foobarbazbam  ",
        10,
        20,
        False,
        True,
        [],
        "foobarbazbam",
        12,
        "  ",
        2,
        "",
    ),
    (
        "foobarbazbam  baz",
        10,
        20,
        False,
        True,
        [],
        "foobarbazbam  baz",
        17,
        "",
        0,
        "",
    ),
    (
        "foobarbazbam  bambazfoobar",
        10,
        20,
        False,
        True,
        [],
        "foobarbazbam",
        12,
        "  ",
        2,
        "bambazfoobar",
    ),
    (
        "Hello foo!",
        10,
        20,
        False,
        False,
        [],
        "Hello foo!",
        10,
        "",
        0,
        "",
    ),
    (
        "Hello foo!  ",
        10,
        20,
        False,
        False,
        [],
        "Hello foo!",
        10,
        "  ",
        2,
        "",
    ),
    (
        "Hello  foo!",
        10,
        20,
        False,
        False,
        [],
        "Hello",
        5,
        "  ",
        2,
        "foo!",
    ),
    (
        "       foo!",
        10,
        20,
        False,
        False,
        [],
        "",
        0,
        "       ",
        7,
        "foo!",
    ),
    (
        "Hello world!",
        10,
        20,
        False,
        False,
        [],
        "Hello",
        5,
        " ",
        1,
        "world!",
    ),
    (
        "Helloworld!",
        10,
        10,
        False,
        False,
        [],
        "Helloworld",
        10,
        "",
        0,
        "!",
    ),
    (
        "Helloworld!",
        10,
        20,
        False,
        True,
        [],
        "Helloworld!",
        11,
        "",
        0,
        "",
    ),
    (
        "Helloworld!  ",
        10,
        20,
        False,
        True,
        [],
        "Helloworld!",
        11,
        "  ",
        2,
        "",
    ),
    (
        "Hello-world!  ",
        10,
        20,
        False,
        False,
        [],
        "Hello-",
        6,
        "",
        0,
        "world!  ",
    ),
    (
        "Hello\u00adworld!  ",
        10,
        20,
        False,
        False,
        [5],
        "Hello-",
        6,
        "",
        0,
        "world!  ",
    ),
    (
        "\u00adx\u00ad",
        1,
        1,
        False,
        False,
        [0, 2],
        "x",
        1,
        "",
        0,
        "",
    ),
    (
        "\u00adx\u00adx",
        1,
        1,
        False,
        False,
        [0, 2],
        "x",
        1,
        "",
        0,
        "x",
    ),
    (
        "\u00adx\u00adx",
        1,
        2,
        False,
        True,
        [0, 2],
        "xx",
        2,
        "",
        0,
        "",
    ),
    # The following use grapheme cluster examples from
    # https://www.unicode.org/reports/tr29/#Grapheme_Cluster_Boundaries
    (
        "நிx",  # Tamil ni grapheme (two codeopints)
        1,
        2,
        False,
        True,
        [],
        "நி",
        2,
        "",
        0,
        "x",
    ),
    (
        "กำx",  # Thai kam grapheme (two codepoints)
        1,
        2,
        False,
        True,
        [],
        "กำ",
        2,
        "",
        0,
        "x",
    ),
    (
        "षिx",  # Devanagari ssi grapheme (two codepoints)
        1,
        2,
        False,
        True,
        [],
        "षि",
        2,
        "",
        0,
        "x",
    ),
    (
        "क्षिx",  # Devanagari kshi grapheme (four codepoints)
        2,
        3,
        False,
        True,
        [],
        "क्षि",
        3,
        "",
        0,
        "x",
    ),
    (
        "क्षिx",  # Devanagari kshi grapheme (four codepoints)
        1,
        2,
        False,
        True,
        [],
        "क्षि",
        3,
        "",
        0,
        "x",
    ),
    (
        "Hello wor",
        10,
        20,
        False,
        False,
        [],
        "Hello wor",
        9,
        "",
        0,
        "",
    ),
    (
        "Hello wor",
        10,
        20,
        True,
        False,
        [],
        "Hello",
        5,
        " ",
        1,
        "wor",
    ),
    (
        "Hello wo-r",
        10,
        20,
        True,
        False,
        [],
        "Hello wo-",
        9,
        "",
        0,
        "r",
    ),
    (
        "Hello wo\u00adr",
        10,
        20,
        True,
        False,
        [],
        "Hello",
        5,
        " ",
        1,
        "wo\u00adr",
    ),
    (
        "Foobarbazbam",
        10,
        10,
        False,
        False,
        [],
        "Foobarbazb",
        10,
        "",
        0,
        "am",
    ),
    (
        "Foobarbazbam",
        10,
        10,
        True,
        False,
        [],
        "",
        0,
        "",
        0,
        "Foobarbazbam",
    ),
]


@pytest.mark.parametrize(
    "text, remaining_columns, total_columns, keep_nonseparable_end, expected_newline,"
    " expected_removed_codepoints, expected_text, expected_text_columns, expected_space,"
    " expected_space_columns, expected_remainder",
    TEST_UNICODE_STRING_PROCESSOR_SPLIT_DATA,
)
def test_UnicodeStringProcessor_split(
    text: str,
    remaining_columns: int,
    total_columns: int,
    keep_nonseparable_end: bool,
    expected_newline: bool,
    expected_removed_codepoints: list[int],
    expected_text: str,
    expected_text_columns: int,
    expected_space: str,
    expected_space_columns: int,
    expected_remainder: str,
) -> None:
    proc = UnicodeStringProcessor()
    newline, removed_codepoints, text, text_columns, space, space_columns, remainder = (
        proc.split(
            text=text,
            remaining_columns=remaining_columns,
            total_columns=total_columns,
            keep_nonseparable_end=keep_nonseparable_end,
        )
    )
    print(
        newline,
        removed_codepoints,
        repr(text),
        text_columns,
        repr(space),
        space_columns,
        repr(remainder),
    )
    assert newline == expected_newline
    assert removed_codepoints == expected_removed_codepoints
    assert text == expected_text
    assert text_columns == expected_text_columns
    assert space == expected_space
    assert space_columns == expected_space_columns
    assert remainder == expected_remainder


def test_has_unicode_string_processor() -> None:
    with patch("antsibull_docutils._string._HAS_ITER_GRAPHEMES", False):
        with patch("antsibull_docutils._string._HAS_GRAPHEME", False):
            assert has_unicode_string_processor() is False
            with pytest.raises(
                RuntimeError, match="^Unicode string processing requires"
            ):
                UnicodeStringProcessor()
