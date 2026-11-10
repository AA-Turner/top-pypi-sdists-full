# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Test md_utils module.
"""

from __future__ import annotations

import pytest

from antsibull_docutils.md_utils import md_escape


@pytest.mark.parametrize(
    "text, escaped",
    [
        ("", ""),
        ("This is a test, ok.", r"This is a test\, ok\."),
        (
            r"""!"#$%&'()*+,:;<=>?@[\]^_`{|}~.-""",
            r"""\!\"\#\$\%\&\'\(\)\*\+\,\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~\.\-""",
        ),
        ("* foo", r"\* foo"),
    ],
)
def test_md_escape(text: str, escaped: str) -> None:
    result = md_escape(text)
    print(result)
    print(escaped)
    assert result == escaped
