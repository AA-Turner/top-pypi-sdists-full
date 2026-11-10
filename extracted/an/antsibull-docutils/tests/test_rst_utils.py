# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Test rst_utils module.
"""

from __future__ import annotations

import pytest

from antsibull_docutils.rst_utils import column_width, rst_escape


@pytest.mark.parametrize(
    "text, escape_ending_whitespace, escaped",
    [
        ("", False, ""),
        (" ", False, " "),
        (" ", True, r"\  \ "),
        (r"\<>_*`", False, r"\\\<\>\_\*\`"),
    ],
)
def test_rst_escape(text: str, escape_ending_whitespace: bool, escaped: str) -> None:
    result = rst_escape(text, escape_ending_whitespace=escape_ending_whitespace)
    assert result == escaped


@pytest.mark.parametrize(
    "text, width",
    [
        ("", 0),
        ("a", 1),
        ("A", 1),
        ("A test", 6),
        ("学校", 4),
    ],
)
def test_column_width(text: str, width: int) -> None:
    result = column_width(text)
    assert result == width
