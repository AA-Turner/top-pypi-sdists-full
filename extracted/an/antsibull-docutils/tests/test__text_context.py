# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Test _text_context module.
"""

from __future__ import annotations

import pytest

from antsibull_docutils._collector import EmptyState
from antsibull_docutils._string import ASCIIStringProcessor
from antsibull_docutils._text_context import (
    Context,
    _indent,
)


def test_context() -> None:
    context = Context(
        has_top=False,
        remaining_width=80,
        state=EmptyState(),
        string_proc=ASCIIStringProcessor(),
    )
    with pytest.raises(ValueError) as exc:
        context.top.append(text="test")
    assert str(exc.value) == "Context has no top part"

    subcontext = Context(
        has_top=True,
        remaining_width=70,
        state=EmptyState(),
        string_proc=ASCIIStringProcessor(),
    )
    with pytest.raises(ValueError) as exc:
        context.append(subcontext)
    assert str(exc.value) == "Context is not closed!"

    with pytest.raises(ValueError) as exc:
        subcontext.get_lines()
    assert str(exc.value) == "Context is not closed!"

    subcontext.close()

    with pytest.raises(ValueError) as exc:
        context.append(subcontext)
    assert str(exc.value) == "Context has no top part"

    with pytest.raises(ValueError) as exc:
        subcontext.close()
    assert str(exc.value) == "Context is already closed!"

    context2 = Context(
        has_top=True,
        remaining_width=80,
        state=EmptyState(),
        string_proc=ASCIIStringProcessor(),
    )
    context2.append(subcontext)


def test__indent() -> None:
    lines = ["", "", "a", " b", "", "  c", ""]
    _indent(lines, first_indent="X ", next_indent="Y ")
    assert lines == ["X a", "Y  b", "Y", "Y   c"]
