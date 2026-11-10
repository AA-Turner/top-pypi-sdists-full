# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project

"""
Contexts for plain text formatting.
"""

from __future__ import annotations

import abc
import typing as t

from ._collector import Collector as _Collector
from ._collector import State as _State
from ._string import StringProcessor as _StringProcessor
from ._utils import ContextBase as _ContextBase


class Context(_ContextBase["Context"]):  # pylint: disable=too-many-instance-attributes
    """
    Base context class for text conversion.
    """

    def __init__(
        self,
        *,
        remaining_width: int,
        state: _State,
        string_proc: _StringProcessor,
        has_top: bool = False,
        ignore_newlines: bool = True,
    ) -> None:
        self.remaining_width = remaining_width
        self.top_state = state.clone()
        self.state = state.clone()
        self.string_proc = string_proc
        self._has_top = has_top
        self._top = _Collector(
            width=self.remaining_width,
            state=self.top_state,
            string_proc=self.string_proc,
            ignore_newlines=ignore_newlines,
        )
        self._main = _Collector(
            width=self.remaining_width,
            state=self.state,
            string_proc=self.string_proc,
            ignore_newlines=ignore_newlines,
        )
        self._result_top: list[str] | None = None
        self._result_main: list[str] | None = None

    @property
    def top(self) -> _Collector:
        """
        Get hold of top collector.
        """
        if not self._has_top:
            raise ValueError("Context has no top part")
        return self._top

    @property
    def main(self) -> _Collector:
        """
        Get hold of main collector.
        """
        return self._main

    def append(
        self,
        context: Context,
    ) -> None:
        """
        Append another context to this context.
        """
        # pylint: disable-next=protected-access
        if context._result_top is None or context._result_main is None:
            raise ValueError("Context is not closed!")
        if context._has_top:  # pylint: disable=protected-access
            if not self._has_top:
                raise ValueError("Context has no top part")
            self._top.add_raw_lines(
                context._result_top  # pylint: disable=protected-access
            )
        self._main.add_raw_lines(
            context._result_main  # pylint: disable=protected-access
        )

    def close(self) -> None:
        """
        Close the context.

        Should be called before using its value / content, for example by
        passing it to ``append()`` or calling ``get_text()``.
        """
        if self._result_main is not None or self._result_top is not None:
            raise ValueError("Context is already closed!")
        self._result_top = self._top.close()
        self._result_main = self._main.close()

    def get_lines(self) -> list[str]:
        """
        Return the content of the context as a list of lines.
        """
        if self._result_main is None or self._result_top is None:
            raise ValueError("Context is not closed!")
        return self._result_top + self._result_main

    def get_text(self) -> str:
        """
        Return the content of the context as a string.
        """
        return "\n".join(self.get_lines())


def _indent(lines: list[str], *, first_indent: str, next_indent: str) -> None:
    while lines and lines[0] == "":
        del lines[0]
    while lines and lines[-1] == "":
        del lines[-1]
    for i, line in enumerate(lines):
        if i == 0:
            lines[i] = f"{first_indent}{line}".rstrip(" ")
        else:
            lines[i] = f"{next_indent}{line}".rstrip(" ")


class IndentContext(Context):
    """
    Context for things to be indented.
    """

    def __init__(
        self,
        *,
        first_indent: str,
        next_indent: str | None = None,
        remaining_width: int,
        state: _State,
        string_proc: _StringProcessor,
        at_least_one_line: bool = False,
        ignore_newlines: bool = True,
    ):
        indent_columns = string_proc.get_column_count(text=first_indent)
        super().__init__(
            remaining_width=remaining_width - indent_columns,
            state=state,
            string_proc=string_proc,
            ignore_newlines=ignore_newlines,
        )
        self.first_indent = first_indent
        self.next_indent = " " * indent_columns if next_indent is None else next_indent
        self.at_least_one_line = at_least_one_line

    def close(self) -> None:
        super().close()
        assert self._result_main is not None
        _indent(
            self._result_main,
            first_indent=self.first_indent,
            next_indent=self.next_indent,
        )
        if self.at_least_one_line and not self._result_main:
            self._result_main.append(self.first_indent.rstrip())


class Enumerator(metaclass=abc.ABCMeta):
    """
    Abstract enumerator for producing indents.
    """

    @abc.abstractmethod
    def get_maximal_length(self) -> int:
        """
        Return the maximum indentation length.
        """

    @abc.abstractmethod
    def get_next_first_indent(self) -> str:
        """
        Generates a new first indent.
        Must be called exactly as many times as defined.
        """


class ConstEnumerator(Enumerator):
    """
    Enumerator with the same indent per item.
    """

    def __init__(self, *, prefix: str, string_proc: _StringProcessor) -> None:
        self.prefix = prefix
        self.string_proc = string_proc

    def get_maximal_length(self) -> int:
        """
        Return the maximum indentation length.
        """
        return self.string_proc.get_column_count(text=self.prefix)

    def get_next_first_indent(self) -> str:
        """
        Generates a new first indent.
        Must be called exactly as many times as defined.
        """
        return self.prefix


def arabic(index: int) -> str:
    """
    Formats a list indent with an arabic number.
    """
    return f"{index + 1}. "


class VariableEnumerator(Enumerator):
    """
    Enumerator with a different indent per item.
    """

    def __init__(
        self,
        *,
        generator: t.Callable[[int], str],
        count: int,
        string_proc: _StringProcessor,
    ) -> None:
        self.index = 0
        self.prefixes = [generator(i) for i in range(count)]
        self.max_length = (
            max(string_proc.get_column_count(text=elt) for elt in self.prefixes)
            if self.prefixes
            else 0
        )

    def get_maximal_length(self) -> int:
        """
        Return the maximum indentation length.
        """
        return self.max_length

    def get_next_first_indent(self) -> str:
        """
        Generates a new first indent.
        Must be called exactly as many times as defined.
        """
        index = self.index
        self.index += 1
        return self.prefixes[index]


class ListContext(Context):
    """
    Context for lists (enumeration, bullet list).
    """

    def __init__(
        self,
        *,
        enumerator: Enumerator,
        remaining_width: int,
        state: _State,
        string_proc: _StringProcessor,
    ):
        max_length = enumerator.get_maximal_length()
        super().__init__(
            remaining_width=remaining_width - max_length,
            state=state,
            string_proc=string_proc,
        )
        self.enumerator = enumerator
        self.max_length = max_length

    def get_next_item_indents(self) -> tuple[str, str]:
        """
        Retrieve the ``(first_indent, next_indent)`` pair for the next list item.
        """
        first_indent = self.enumerator.get_next_first_indent()
        indent_length = self.string_proc.get_column_count(text=first_indent)
        if indent_length > self.max_length:
            raise RuntimeError(  # pragma: no cover
                f"Expected a maximum indent column count of {self.max_length},"
                f" but got {first_indent!r} of column count {indent_length}"
            )
        return (
            first_indent + " " * (self.max_length - indent_length),
            " " * self.max_length,
        )
