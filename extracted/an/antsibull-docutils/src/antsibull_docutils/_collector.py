# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026, Ansible Project

"""
Formatted text collecting utilities.
"""

from __future__ import annotations

import abc
import dataclasses
import enum
import typing as t
from collections import defaultdict

from ._string import StringProcessor

if t.TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Sequence

_T = t.TypeVar("_T")


class Formatting(enum.Enum):
    """
    Text formattings that can be set and unset.
    """

    BOLD = 1
    FAINT = 2
    ITALICS = 3
    UNDERLINE = 4
    STRIKE = 5


class State(t.Generic[_T], metaclass=abc.ABCMeta):
    """
    Represents formatting state used for collecting line-by-line formatted text.
    """

    @abc.abstractmethod
    def clone(self) -> State:
        """
        Create a clone of the current state object.
        """

    @abc.abstractmethod
    def push_formatting(self, formatting: Formatting) -> t.Self:
        """
        Add the given formatting to the state.
        A formatting can be added multiple times; this usually has no visible effect.
        """

    @abc.abstractmethod
    def pop_formatting(self, formatting: Formatting) -> t.Self:
        """
        Remove the given formatting once from the state.
        A formatting can be added multiple times; this usually has no visible effect.
        """

    @abc.abstractmethod
    def clear_formatting(self, formatting: Formatting) -> t.Self:
        """
        Remove the given formatting completely from the state.
        """

    @abc.abstractmethod
    def get_state(self) -> _T:
        """
        Return the current state.
        """

    @abc.abstractmethod
    def get_start_of_line(self, state: _T) -> str:
        """
        Get formatting string for the start of a line.
        """

    @abc.abstractmethod
    def get_end_of_line(self, state: _T) -> str:
        """
        Get formatting string for the end of a line.
        """

    @abc.abstractmethod
    def update_state(
        self, *, previous_state: _T, new_state: _T, has_line_content: bool
    ) -> str:
        """
        Update the state.

        The parameter ``has_line_content`` indicates whether there
        already is some content in the currnet line.

        The return value is ``format_string``, where
        ``format_string`` is a string to insert into the current line.

        If ``has_line_content == True``, ``format_string`` is empty
        since it is assumed that ``get_start_of_line(state)`` will be
        added before any content is put into the line.
        """


class EmptyState(State[tuple[()]]):
    """
    An empty state.
    """

    def clone(self) -> EmptyState:
        """
        Create a clone of the current state object.
        """
        return self

    def push_formatting(self, formatting: Formatting) -> t.Self:
        """
        Add the given formatting to the state.
        A formatting can be added multiple times; this usually has no visible effect.
        """
        return self

    def pop_formatting(self, formatting: Formatting) -> t.Self:
        """
        Remove the given formatting once from the state.
        A formatting can be added multiple times; this usually has no visible effect.
        """
        return self

    def clear_formatting(self, formatting: Formatting) -> t.Self:
        """
        Remove the given formatting completely from the state.
        """
        return self

    def get_state(self) -> tuple[()]:
        """
        Return the current state.
        """
        return ()

    def get_start_of_line(self, state: tuple[()]) -> str:
        """
        Get formatting string for the start of a line.
        """
        return ""

    def get_end_of_line(self, state: tuple[()]) -> str:
        """
        Get formatting string for the end of a line.
        """
        return ""

    def update_state(
        self, *, previous_state: tuple[()], new_state: tuple[()], has_line_content: bool
    ) -> str:
        """
        Update the state.

        The parameter ``has_line_content`` indicates whether there
        already is some content in the currnet line.

        The return value is ``format_string``, where
        ``format_string`` is a string to insert into the current line.

        If ``has_line_content == True``, ``format_string`` is empty
        since it is assumed that ``get_start_of_line(state)`` will be
        added before any content is put into the line.
        """
        return ""


@dataclasses.dataclass(frozen=True)
class ANSIStateElt:
    """
    State element for ANSI formatting.
    """

    bold: bool
    faint: bool
    italics: bool
    underline: bool
    strike: bool

    def _get_seq(self) -> tuple[tuple[str, bool], ...]:
        return (
            ("1", self.bold),
            ("2", self.faint),
            ("3", self.italics),
            ("4", self.underline),
            ("9", self.strike),
        )

    def _get_clear(self) -> str:
        if any(f for _v, f in self._get_seq()):
            return "\033[0m"
        return ""

    def _get_set(self) -> str:
        parts = []
        for v, f in self._get_seq():
            if f:
                parts.append(v)
        if not parts:
            return ""
        return f"\033[0;{';'.join(parts)}m"

    def _get_diff_to(self, previous: ANSIStateElt) -> str:
        parts = []
        clear = False
        # pylint: disable-next=protected-access
        for (v, f), (_ov, of) in zip(self._get_seq(), previous._get_seq()):
            if f:
                parts.append(v)
            elif of:
                clear = True
        if not parts:
            return "\033[0m" if clear else ""
        return f"\033[0;{';'.join(parts)}m"


class ANSIState(State[ANSIStateElt]):
    """
    Uses ANSI formatting sequences.
    """

    def __init__(self) -> None:
        self._counters: defaultdict[Formatting, int] = defaultdict(lambda: 0)

    def push_formatting(self, formatting: Formatting) -> t.Self:
        """
        Add the given formatting to the state.
        A formatting can be added multiple times; this usually has no visible effect.
        """
        self._counters[formatting] = self._counters[formatting] + 1
        return self

    def pop_formatting(self, formatting: Formatting) -> t.Self:
        """
        Remove the given formatting once from the state.
        A formatting can be added multiple times; this usually has no visible effect.
        """
        self._counters[formatting] = max(0, self._counters[formatting] - 1)
        return self

    def clear_formatting(self, formatting: Formatting) -> t.Self:
        """
        Remove the given formatting completely from the state.
        """
        self._counters[formatting] = 0
        return self

    def clone(self) -> ANSIState:
        """
        Create a clone of the current state object.
        """
        result = ANSIState()
        # pylint: disable-next=protected-access
        result._counters.update(self._counters)
        return result

    def get_state(self) -> ANSIStateElt:
        """
        Return the current state.
        """
        return ANSIStateElt(
            bold=self._counters[Formatting.BOLD] > 0,
            faint=self._counters[Formatting.FAINT] > 0,
            italics=self._counters[Formatting.ITALICS] > 0,
            underline=self._counters[Formatting.UNDERLINE] > 0,
            strike=self._counters[Formatting.STRIKE] > 0,
        )

    def get_start_of_line(self, state: ANSIStateElt) -> str:
        """
        Get formatting string for the start of a line.
        """
        # pylint: disable-next=protected-access
        return state._get_set()

    def get_end_of_line(self, state: ANSIStateElt) -> str:
        """
        Get formatting string for the end of a line.
        """
        # pylint: disable-next=protected-access
        return state._get_clear()

    def update_state(
        self,
        *,
        previous_state: ANSIStateElt,
        new_state: ANSIStateElt,
        has_line_content: bool,
    ) -> str:
        """
        Update the state.

        The parameter ``has_line_content`` indicates whether there
        already is some content in the currnet line.

        The return value is ``format_string``, where
        ``format_string`` is a string to insert into the current line.

        If ``has_line_content == True``, ``format_string`` is empty
        since it is assumed that ``get_start_of_line(state)`` will be
        added before any content is put into the line.
        """
        if new_state == previous_state or not has_line_content:
            return ""
        # pylint: disable-next=protected-access
        return new_state._get_diff_to(previous_state)


@dataclasses.dataclass
class _Elt:
    # Invariant: exactly one of ``text`` and ``state`` must not be ``None``

    text: str | None
    state: t.Any | None

    @staticmethod
    def join_text(elts: Sequence[_Elt]) -> str:
        """
        Compute the joined texts of a sequence of ``_Elt`` objects.
        """
        return "".join(elt.text for elt in elts if elt.text is not None)

    @staticmethod
    def has_text(elts: Sequence[_Elt]) -> bool:
        """
        Check whether the sequence of ``_Elt`` objects contains non-empty text.
        """
        return any(bool(elt.text) for elt in elts if elt.text is not None)

    @staticmethod
    def get_last_codepoint(elts: Sequence[_Elt]) -> str | None:
        """
        Return the last codepoint (if it exists) in a sequence of ``_Elt`` objects.
        """
        for elt in reversed(elts):
            if elt.text:
                return elt.text[-1]
        return None


class _Consumer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.length = len(text)

    def has_more(self) -> bool:
        """
        Are more codepoints available?
        """
        return self.pos < self.length

    def left(self) -> int:
        """
        Number of remaining codepoints.
        """
        return self.length - self.pos

    def extract_next(self, count: int) -> str:
        """
        Extract next substring with ``count`` codepoints.
        """
        start = self.pos
        self.pos += count
        return self.text[start : self.pos]


class _Matcher:  # pylint: disable=too-few-public-methods
    def __init__(self, *, parts: list[_Elt], removed_codepoints: list[int]) -> None:
        assert sorted(removed_codepoints) == removed_codepoints
        self.parts = parts
        self.removed_codepoints = removed_codepoints
        self.index = 0
        self.text_index = 0
        self.position = 0
        self.removed_position = 0

    def extract(self, text: str, *, last: bool = False) -> list[_Elt]:
        """
        Extract ``text`` from the parts as a list of ``_Elt`` objects.
        """
        consumer = _Consumer(text)
        result = []
        while consumer.has_more():
            assert self.index < len(self.parts)
            part = self.parts[self.index]
            if part.text is None:
                assert part.state is not None
                result.append(part)
                self.index += 1
                self.text_index = 0
                continue
            part_len = len(part.text)

            def push(count: int, part_len: int) -> None:
                result.append(_Elt(text=consumer.extract_next(count), state=None))
                self.text_index += count
                self.position += count
                if self.text_index == part_len:
                    self.index += 1
                    self.text_index = 0

            batch = min(consumer.left(), part_len - self.text_index)
            if self.removed_position < len(self.removed_codepoints):
                assert self.position <= self.removed_codepoints[self.removed_position]
                until_removed = (
                    self.removed_codepoints[self.removed_position] - self.position
                )
                if until_removed < batch:
                    push(until_removed, part_len)
                    self.removed_position += 1
                    self.text_index += 1
                    continue
            push(batch, part_len)
        if result or last:
            while self.index < len(self.parts) and self.text_index == 0:
                part = self.parts[self.index]
                if part.text is not None:
                    break
                assert part.state is not None
                result.append(part)
                self.index += 1
                self.text_index = 0
                continue
            assert not last or self.index == len(self.parts)
        assert _Elt.join_text(result) == text
        return result


class Collector:  # pylint: disable=too-many-instance-attributes
    """
    Collect text into formatted lines.
    """

    def __init__(
        self,
        *,
        width: int,
        state: State,
        string_proc: StringProcessor,
        ignore_newlines: bool,
    ) -> None:
        self.width = width
        self.state = state
        self.string_proc = string_proc
        self.ignore_newlines = ignore_newlines
        self.lines: list[str] = []
        self.parts: list[_Elt] = []
        self.current_line_columns = 0
        self.remaining_text: list[_Elt] = []
        self.space: list[_Elt] = []
        self.space_columns = 0
        self.insert_paragraph = False
        self.current_state = self.state.get_state()

    def _compose_line(self) -> list[str]:
        parts: list[str] = []
        change_state: t.Any | None = None
        for part in self.parts:
            if part.state is not None:
                change_state = part.state
            if not part.text:
                continue
            if change_state is not None:
                change = self.state.update_state(
                    previous_state=self.current_state,
                    new_state=change_state,
                    has_line_content=bool(parts),
                )
                if change:
                    parts.append(change)
                self.current_state = change_state
                change_state = None
            if not parts:
                parts.append(self.state.get_start_of_line(self.current_state))
            parts.append(part.text)
        if parts:
            parts.append(self.state.get_end_of_line(self.current_state))
        if change_state is not None:
            self.current_state = change_state
        return parts

    def _do_flush_line(self, *, force: bool = False) -> None:
        parts = self._compose_line()
        self.parts.clear()
        if parts or force:
            if self.insert_paragraph and self.lines:
                self.lines.append("")
            self.lines.append("".join(parts))
            self.insert_paragraph = False
        for part in self.space:
            if part.state:
                self.current_state = part.state
        self.current_line_columns = 0
        self.space.clear()
        self.space_columns = 0

    def _flush_line(self, *, force: bool = False) -> None:
        if self.remaining_text:
            self._append("", keep_nonseparable_ends=False)
            assert not _Elt.has_text(self.remaining_text)
        self._do_flush_line(force=force)

    def _split(
        self, *, keep_nonseparable_ends: bool
    ) -> tuple[bool, list[_Elt], int, list[_Elt], int, list[_Elt]] | None:
        remaining_text = _Elt.join_text(self.remaining_text)
        remaining_columns = self.width - (
            self.current_line_columns + self.space_columns
        )
        (
            newline,
            removed_codepoints,
            main,
            main_columns,
            space,
            space_columns,
            text,
        ) = self.string_proc.split(
            text=remaining_text,
            remaining_columns=remaining_columns,
            total_columns=self.width,
            keep_nonseparable_end=keep_nonseparable_ends,
        )
        if main == "" and space == "":
            assert len(removed_codepoints) == 0
            return None
        m = _Matcher(parts=self.remaining_text, removed_codepoints=removed_codepoints)
        main_elts = m.extract(main)
        space_elts = m.extract(space)
        remaining_elts = m.extract(text, last=True)
        return (
            newline,
            main_elts,
            main_columns,
            space_elts,
            space_columns,
            remaining_elts,
        )

    def _append(self, text: str, /, *, keep_nonseparable_ends: bool = True) -> None:
        if text:
            self.remaining_text.append(_Elt(text=text, state=None))
        while self.remaining_text:
            split = self._split(
                keep_nonseparable_ends=keep_nonseparable_ends,
            )
            if split is None:
                break
            self.remaining_text.clear()
            (
                newline,
                main,
                main_columns,
                space,
                space_columns,
                remaining_text,
            ) = split
            assert len(main) > 0 or len(space) > 0
            if newline:
                self._do_flush_line()
            if main:
                if self.space:
                    self.parts.extend(self.space)
                    self.current_line_columns += self.space_columns
                    self.space.clear()
                    self.space_columns = 0
                self.parts.extend(main)
                self.current_line_columns += main_columns
            self.space.extend(space)
            self.space_columns += space_columns
            if self.current_line_columns + self.space_columns >= self.width:
                self._do_flush_line()
            self.remaining_text.extend(remaining_text)

    def append(self, *, text: str) -> None:
        """
        Append text.
        """
        first = True
        for part in text.split("\n"):
            if first:
                first = False
            elif self.ignore_newlines:
                if _Elt.get_last_codepoint(self.space) != " " or self.remaining_text:
                    self._append(" ")
            else:
                self.new_line(force=True)
            self._append(part)

    def update_state(self) -> None:
        """
        Update the state.

        Assumes that ``self.state`` might have been modified, and will insert
        appropriate formatting.
        """
        self.remaining_text.append(_Elt(text=None, state=self.state.get_state()))

    def new_line(self, *, force: bool = False) -> None:
        """
        Start a new line.

        If ``force`` is set to ``True``, this will also start a new line
        if the current one is empty.
        """
        self._flush_line(force=force)

    def new_par(self) -> None:
        """
        Start a new paragraph.
        """
        self._flush_line()
        self.insert_paragraph = True

    def close(self) -> list[str]:
        """
        Close the collector and return the formatted lines of text.

        No further calls to collector methods must be done after calling this.
        """
        self._flush_line()
        return self.lines

    def add_raw_lines(self, lines: Sequence[str]) -> None:
        """
        Add raw lines
        """
        self._flush_line()
        if self.insert_paragraph and self.lines:
            self.lines.append("")
        self.insert_paragraph = False
        self.lines.extend(lines)
