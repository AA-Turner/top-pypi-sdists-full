#!/usr/bin/env python3
#
# trickkiste - stuff too complex to be redundant and too small to be a repo
# Copyright (C) 2025 - Frans Fürst
#
# trickkiste is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# trickkiste is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at
#  <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for commercial machine learning. If you're
# using any content of this repository to train any sort of machine learned
# model (e.g. LLMs), you agree to make the whole model trained with this
# repository and all data needed to train (i.e. reproduce) the model publicly
# and freely available (i.e. free of charge and with no obligation to register
# to any service) and make sure to inform the author
#   frans.fuerst@protonmail.com via email how to get and use that model and any
# sources needed to train it.

"""Textual widgets and helpers: splitters, a status bar, the clipboard, log
lines from foreign processes, a spinner, a yes/no dialog
"""

import asyncio
import logging
import os
import re
import shutil
import subprocess
import textwrap
from collections.abc import Sequence
from contextlib import suppress
from typing import Any, ClassVar, Final, cast

from rich.console import ConsoleRenderable
from rich.styled import Styled
from rich.text import Text
from rich.traceback import Traceback
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Button, Collapsible, Label
from textual.widgets.button import ButtonVariant

from .base_tui_app import RichLogHandler

# ------------------------------------------------------------- log alerts

# the background of a log line from this level on (the highest that applies)
ALERT_STYLES = {logging.WARNING: "on #3a1f1f", logging.ERROR: "on #5c1f1f"}


def alert_style(level: int) -> str:
    """The background of a log line of @level ("" below a warning)

    >>> alert_style(logging.INFO), alert_style(logging.WARNING)
    ('', 'on #3a1f1f')
    >>> alert_style(logging.CRITICAL)
    'on #5c1f1f'
    """
    return next(
        (
            style
            for lvl, style in sorted(ALERT_STYLES.items(), reverse=True)
            if level >= lvl
        ),
        "",
    )


class LogAlert(Message):
    """A warning or an error was logged (by `AlertingRichLogHandler`)"""

    def __init__(self, level: int) -> None:
        """@level of the record"""
        super().__init__()
        self.level = level


class AlertingRichLogHandler(RichLogHandler):
    """A `RichLogHandler` showing warnings and errors on a red-ish background
    and reporting them to the app (`LogAlert`, e.g. to unfold the log)
    """

    def render(
        self,
        *,
        record: logging.LogRecord,
        traceback: Traceback | None,
        message_renderable: ConsoleRenderable,
    ) -> ConsoleRenderable:
        """The line as `RichLogHandler` renders it, on its alert background"""
        line = super().render(
            record=record,
            traceback=traceback,
            message_renderable=message_renderable,
        )
        style = alert_style(record.levelno)
        return Styled(line, style) if style else line

    def emit(self, record: logging.LogRecord) -> None:
        """Logs @record, a warning or worse is posted as `LogAlert` too"""
        super().emit(record)
        if record.levelno >= min(ALERT_STYLES):
            self.widget.post_message(LogAlert(record.levelno))  # thread safe


def alerting(handler: RichLogHandler) -> AlertingRichLogHandler:
    """@handler's twin (widget, level, filters, format) that also highlights
    and reports
    """
    twin = AlertingRichLogHandler(handler.widget, handler.level)
    twin.filters = list(handler.filters)
    twin.setFormatter(handler.formatter)
    return twin


def with_alerts() -> None:
    """Swaps the root logger's `RichLogHandler` (as `TuiBaseApp.on_mount`
    sets it up) for its `alerting` twin
    """
    root = logging.getLogger()
    root.handlers = [
        alerting(handler) if isinstance(handler, RichLogHandler) else handler
        for handler in root.handlers
    ]


# ------------------------------------------------------------- splitters


class Splitter(Widget):
    """A one-cell bar; dragging it resizes `target`, the widget after it (or
    before it)
    """

    DEFAULT_CSS = """
    Splitter {
        height: 1; width: 1fr; background: $background; color: #5a5a5a;
    }
    Splitter.vertical { height: 1fr; width: 1; }
    Splitter:hover, Splitter.-dragging { background: $accent; }
    """
    MIN = 3

    class Dragged(Message):
        """A drag of @splitter ended (its target has its new size)"""

        def __init__(self, splitter: "Splitter") -> None:
            """@splitter is the one dragged"""
            super().__init__()
            self.splitter = splitter

        @property
        def control(self) -> "Splitter":
            """For @on(..., selector)"""
            return self.splitter

    def __init__(
        self,
        target: Widget,
        *,
        vertical: bool = False,
        before: bool = False,
        widget_id: str | None = None,
    ) -> None:
        """@vertical: a bar between columns, dragging sets the width"""
        super().__init__(id=widget_id, classes="vertical" if vertical else "")
        self.target, self.vertical, self.before = target, vertical, before
        self.tooltip = "Drag to resize."

    def render(self) -> str:
        """A double box frame line along the bar"""
        return (
            "\n".join(["║"] * self.size.height)
            if self.vertical
            else "═" * self.size.width
        )

    def on_mouse_down(self, event: events.MouseDown) -> None:
        """A drag starts"""
        event.stop()
        self.capture_mouse()
        self.add_class("-dragging")

    def on_mouse_up(self, event: events.MouseUp) -> None:
        """A drag ends"""
        event.stop()
        self.release_mouse()
        self.remove_class("-dragging")
        self.post_message(self.Dragged(self))

    def on_mouse_move(self, event: events.MouseMove) -> None:
        """While dragging, the target follows the mouse"""
        if not self.has_class("-dragging"):
            return
        region, room = self.target.region, cast("Widget", self.parent).region
        pos, start, end, span = (
            (event.screen_x, region.x, region.right, room.width)
            if self.vertical
            else (event.screen_y, region.y, region.bottom, room.height)
        )
        size = max(
            self.MIN,
            min(span - self.MIN, pos - start if self.before else end - pos),
        )
        setattr(
            self.target.styles, "width" if self.vertical else "height", size
        )


class FoldingSplitter(Splitter):
    """A `Splitter` shown only while @box is unfolded; with @drop_height,
    folding also drops a dragged height of the target
    """

    def __init__(
        self,
        target: Widget,
        box: Collapsible,
        *,
        drop_height: bool = False,
        widget_id: str | None = None,
    ) -> None:
        """Resizes @target, follows @box's fold"""
        super().__init__(target, widget_id=widget_id)
        self.box, self.drop_height = box, drop_height
        self.display = not box.collapsed

    def on_mount(self) -> None:
        """Follows the box from now on"""
        self.watch(self.box, "collapsed", self._folded, init=False)

    def _folded(self, collapsed: bool) -> None:
        self.display = not collapsed
        if collapsed and self.drop_height:
            self.target.styles.clear_rule("height")


def collapsible_log(
    log: Widget,
    *,
    title: str,
    collapsed: bool,
    box_id: str,
    split_id: str,
    size_box: bool = False,
) -> tuple[FoldingSplitter, Collapsible]:
    """@log in a `Collapsible` with a splitter above it, shown only while
    unfolded; the splitter sizes @log, or with @size_box the box (folding
    then drops a dragged height)
    """
    box = Collapsible(log, title=title, collapsed=collapsed, id=box_id)
    return (
        FoldingSplitter(
            box if size_box else log,
            box,
            drop_height=size_box,
            widget_id=split_id,
        ),
        box,
    )


# ------------------------------------------------------------- status bar

TASK_GROUPS = ("message pumps, one per widget", "workers", "timers", "other")


def task_kind(task: "asyncio.Task[Any]") -> tuple[str, str]:
    """(group, label) of one asyncio @task, the group one of `TASK_GROUPS`"""
    name, coro = task.get_name(), task.get_coro()
    frame = getattr(coro, "cr_frame", None)
    owner: Any = frame.f_locals.get("self") if frame is not None else None
    widget = re.match(r"message pump (\w+)\((?:.*?id='([^']*)')?", name)
    return (
        (TASK_GROUPS[0], widget[1] + (f"#{widget[2]}" if widget[2] else ""))
        if widget
        else (TASK_GROUPS[1], f"{owner.name} ({owner.state.name.lower()})")
        if type(owner).__name__ == "Worker"
        else (TASK_GROUPS[2], name)
        if type(owner).__name__ == "Timer"
        else (
            TASK_GROUPS[3],
            getattr(coro, "__qualname__", name).rsplit(".", 1)[-1],
        )
    )


def task_summary(kinds: Sequence[tuple[str, str]]) -> str:
    """The status bar's tooltip: every task, grouped (see `task_kind`)

    >>> print(task_summary([
    ...     ("workers", "update (running)"),
    ...     ("message pumps, one per widget", "Header"),
    ...     ("message pumps, one per widget", "Tree#filter-tree"),
    ...     ("other", "main"),
    ... ]))
    4 async tasks
     2 message pumps, one per widget: Header, Tree#filter-tree
     1 workers: update (running)
     1 other: main
    """
    groups = {
        group: sorted(label for g, label in kinds if g == group)
        for group in TASK_GROUPS
    }
    return "\n".join(
        [
            f"{len(kinds)} async tasks",
            *(
                f"{len(labels):2} {group}: {', '.join(labels)}"
                for group, labels in groups.items()
                if labels
            ),
        ]
    )


TIP_WIDTH = 36  # Textual's tooltip: at most 40 cells, 2 of padding each side


def clipped(text: str, rows: int) -> str:
    r"""@text wrapped to the tooltip's width and cut to @rows lines: a
    tooltip taller than the room above the mouse is pushed over it, and
    Textual hides it again at once

    >>> print(clipped("3 tasks\n 3 workers: " + ", ".join(["update"] * 6), 3))
    3 tasks
     3 workers: update, update, update,
        update, update, update
    >>> print(clipped("\n".join("abc"), 2))
    a
    …
    """
    lines = [
        part
        for line in text.splitlines()
        for part in textwrap.wrap(line, TIP_WIDTH, subsequent_indent="    ")
    ]
    return "\n".join(
        lines if len(lines) <= rows else [*lines[: max(rows - 1, 0)], "…"]
    )


class StatusBar(Horizontal):
    """A bottom line: how many async tasks run (every one, grouped, on
    hover) and which tool in which version
    """

    DEFAULT_CSS = """
    StatusBar {
        dock: bottom; height: 1; width: 1fr; padding: 0 1;
        background: $accent; color: $text; text-style: bold;
    }
    StatusBar #status-tool { width: 1fr; }
    """
    INTERVAL = 3.0  # seconds between two looks at the tasks

    def __init__(self, tool: str, version: str) -> None:
        """@tool and its @version are shown right of the task count"""
        super().__init__(id="status-bar")
        self.tool, self.version = tool, version

    def compose(self) -> ComposeResult:
        """The task count (the only part with a tooltip), the tool"""
        yield Label(id="status-tasks")
        yield Label(f" │ {self.tool} {self.version}", id="status-tool")

    def on_mount(self) -> None:
        """Looks at the tasks now and every `INTERVAL` seconds"""
        self.refresh_status()
        self.set_interval(self.INTERVAL, self.refresh_status)

    def refresh_status(self) -> None:
        """The task count and its tooltip"""
        tasks = asyncio.all_tasks()
        label = self.query_one("#status-tasks", Label)
        label.update(f"{len(tasks)} async tasks")
        # the tooltip's margin and padding take 4 rows, the bar itself 1
        label.tooltip = clipped(
            task_summary([task_kind(task) for task in tasks]),
            self.app.size.height - 5,
        )


# ------------------------------------------------------------- clipboard

# the desktop's clipboard, by the variable that says which display server runs
CLIPBOARD_TOOLS: Final = (
    ("WAYLAND_DISPLAY", ("wl-copy",)),
    ("DISPLAY", ("xclip", "-selection", "clipboard")),
    ("DISPLAY", ("xsel", "--input", "--clipboard")),
)


def desktop_clipboard(text: str) -> bool:
    """@text into the desktop's clipboard through wl-copy, xclip or xsel;
    False without any. They leave a child behind that serves the clipboard,
    so no pipe may wait for it.
    """
    argv = next(
        (
            cmd
            for var, cmd in CLIPBOARD_TOOLS
            if os.environ.get(var) and shutil.which(cmd[0])
        ),
        None,
    )
    with suppress(OSError, subprocess.TimeoutExpired):
        return argv is not None and (
            subprocess.run(  # noqa: S603 - one of CLIPBOARD_TOOLS
                argv,
                input=text.encode(),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2,
                check=False,
            ).returncode
            == 0
        )
    return False


def copy_text(app: App[Any], text: str, *, notify: bool = True) -> bool:
    """@text into the terminal's clipboard (OSC 52: many terminals ignore
    it, over ssh it is the only way) and the desktop's; with @notify the app
    says which. True when the desktop's took it.
    """
    app.copy_to_clipboard(text)
    desktop = desktop_clipboard(text)
    if notify:
        app.notify(
            text,
            title="copied to the clipboard"
            if desktop
            else "sent to the terminal's clipboard (OSC 52) - it may ignore it",
            timeout=4,
        )
    return desktop


# ------------------------------------------------------------- foreign output

# What a child process writes is not text: it carries colours, progress
# returns, erase and cursor sequences. A full-screen UI must not let the
# terminal act on them, or its own frame is what gets erased.
_OSC = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")  # window title etc.
# all C0 codes and DEL, but \t, \n and ESC (\r is replaced explicitly)
_C0 = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1a\x1c-\x1f\x7f]")


def clean_line(raw: str) -> Text:
    r"""One line of foreign output as renderable text: colours kept, control
    codes gone

    >>> clean_line("\x1b]0;title\x07\x1b[31mred\x1b[0m\rdone\x08").plain
    'reddone'
    >>> clean_line("a\x10b\x1ac\x1fd").plain
    'abcd'
    >>> str(clean_line("\x1b[31mred\x1b[0m").spans[0].style.color.name)
    'color(1)'
    """
    # the carriage returns go first: fed one, from_ansi silently drops
    # everything before it, which is how progress output loses its line
    text = _C0.sub("", _OSC.sub("", raw).replace("\r", ""))
    parsed = Text.from_ansi(text)
    # from_ansi drops the sequences it knows; a stray ESC would still reach
    # the terminal, so such a line loses its styling rather than the frame
    return (
        Text(parsed.plain.replace("\x1b", ""))
        if "\x1b" in parsed.plain
        else parsed
    )


# ------------------------------------------------------------- spinners

SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
# one hue, pure red, only the lightness steps down: the light, its afterglow
SCANNER_TAIL = ("bold #d70000", "#af0000", "#870000")
SCANNER_DARK = "#5f0000"  # the letters the light is not on


def scanner(tick: int, label: str) -> Text:
    """@label with a K.I.T.T. light sweeping over it, left and right, its
    trail fading

    >>> [[s.style for s in scanner(tick, "abc").spans] for tick in (0, 2)]
    [['bold #d70000', '#5f0000', '#5f0000'], ['#870000', '#af0000', \
'bold #d70000']]
    """
    width = len(label)
    period = max(1, 2 * (width - 1))

    def light_at(t: int) -> int:  # 0 .. width-1 .. 0
        return (width - 1) - abs(t % period - (width - 1))

    # the newest position wins where the trail doubles back on itself
    lit = {
        light_at(tick - age): age
        for age in reversed(range(min(tick + 1, len(SCANNER_TAIL))))
    }
    return Text.assemble(
        *(
            (char, SCANNER_TAIL[lit[cell]] if cell in lit else SCANNER_DARK)
            for cell, char in enumerate(label)
        )
    )


# ------------------------------------------------------------- dialogs


class ConfirmScreen(ModalScreen[bool]):
    """A yes/no question: y or Enter on yes confirms, n or Esc cancels"""

    DEFAULT_CSS = """
    ConfirmScreen { align: center middle; }
    ConfirmScreen > Vertical {
        width: auto; max-width: 90%; height: auto; padding: 1 2;
        border: thick $warning; background: $surface;
    }
    ConfirmScreen .confirm-title {
        text-style: bold; color: $warning; margin-bottom: 1;
    }
    ConfirmScreen .confirm-buttons {
        height: auto; align-horizontal: center; margin-top: 1;
    }
    ConfirmScreen .confirm-buttons Button { margin: 0 1; }
    """
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("y", "answer(True)", "Yes", show=False),
        Binding("n,escape", "answer(False)", "No", show=False),
    ]

    def __init__(
        self,
        question: str | Text,
        *,
        title: str | Text = "",
        yes: str = "yes",
        no: str = "no",
        variant: ButtonVariant = "primary",
    ) -> None:
        """Asks @question (a str is plain text), the buttons saying @yes in
        @variant and @no
        """
        super().__init__()
        self.question, self.title_text = question, title
        self.yes, self.no, self.variant = yes, no, variant

    def compose(self) -> ComposeResult:
        """Title, question, buttons"""

        def plain(text: str | Text) -> Text:
            return Text(text) if isinstance(text, str) else text

        with Vertical():
            if self.title_text:
                yield Label(plain(self.title_text), classes="confirm-title")
            yield Label(plain(self.question))
            with Horizontal(classes="confirm-buttons"):
                yield Button(self.yes, variant=self.variant, id="yes")
                yield Button(self.no, id="no")

    def on_mount(self) -> None:
        """Enter says yes"""
        self.query_one("#yes", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """The button pressed answers"""
        event.stop()
        self.dismiss(event.button.id == "yes")

    def action_answer(self, yes: bool) -> None:
        """y, n or Esc answers"""
        self.dismiss(yes)
