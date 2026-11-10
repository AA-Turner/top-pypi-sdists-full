# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Test html_utils module.
"""

from __future__ import annotations

import pytest

from antsibull_docutils.html_utils import html_argument_escape, html_escape


@pytest.mark.parametrize(
    "text, escaped",
    [
        ("", ""),
        ("Te'st", "Te&#x27;st"),
        (
            '<a href="https://example.com/?foo=bar&baz=bam">Test</a>',
            '&lt;a href="https://example.com/?foo=bar&amp;baz=bam"&gt;Test&lt;/a&gt;',
        ),
    ],
)
def test_html_escape(text: str, escaped: str) -> None:
    result = html_escape(text)
    assert result == escaped


@pytest.mark.parametrize(
    "text, escaped",
    [
        ("", ""),
        ("Te'st", "Te&#x27;st"),
        (
            '<a href="https://example.com/?foo=bar&baz=bam">Test</a>',
            "&lt;a href=&quot;https://example.com/?foo=bar&amp;baz=bam&quot;&gt;Test&lt;/a&gt;",
        ),
    ],
)
def test_html_argument_escape(text: str, escaped: str) -> None:
    result = html_argument_escape(text)
    assert result == escaped
