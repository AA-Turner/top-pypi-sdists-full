#!/usr/bin/env python3
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

"""Showcase for `base_tui_app` and `tui_widgets` - and my manual test for both

- colourful logging into a foldable log (`collapsible_log`) which unfolds on
  warnings and errors (`with_alerts`, `LogAlert`), drag the bar above it
- `HeatBar`s in a tree, a vertical `Splitter` between tree and right pane
- foreign process output with colours, carriage returns, OSC and control
  codes made harmless by `clean_line`
- `scanner` and `SPINNER`, the footer (`update_status_bar`), a `StatusBar`
  (hover the task count)

Keys: c copies the tree's current node, w / e log a warning / an error,
l folds the log, q asks (`ConfirmScreen`) before quitting
"""

import asyncio
import logging
import math
from contextlib import suppress
from typing import ClassVar

from rich.color import ANSI_COLOR_NAMES
from rich.style import Style
from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.widgets import Collapsible, Label, RichLog, Tree

from trickkiste import __version__
from trickkiste.base_tui_app import HeatBar, TuiBaseApp
from trickkiste.tui_widgets import (
    SPINNER,
    ConfirmScreen,
    LogAlert,
    Splitter,
    StatusBar,
    clean_line,
    collapsible_log,
    copy_text,
    scanner,
    with_alerts,
)

# what a child process might write: a window title (OSC), colours, progress
# via carriage return, erase sequences, a bell and other control codes
FOREIGN_SCRIPT = r"""
while true; do
  printf '\033]0;stolen title\007\033[32mgreen\033[0m, \033[1;31mbold red\033[0m\n'
  for p in 10 50 100; do printf "progress $p%%\r"; sleep 0.3; done; echo
  printf 'bell\007, erase\033[2K, \020DLE and \033[?25lcursor gone?\n'
  sleep 2
done
"""


def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("trickkiste.fancytui")


class ExampleTUI(TuiBaseApp):
    """A little example TUI"""

    CSS = """
    #main { height: 1fr; }
    #main > Tree { width: 50%; }
    #foreign { border: solid grey; }
    #scanner { padding: 0 1; }
    #footer { dock: none; }
    """
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("c", "copy", "copy node"),
        Binding("w", "alert(30)", "warn"),
        Binding("e", "alert(40)", "error"),
        Binding("l", "fold", "fold log"),
        Binding("q", "request_quit", "quit"),
    ]

    def __init__(self) -> None:
        """A little example __init__ function"""
        super().__init__(
            logger_show_funcname=True,
            logger_show_tid=True,
            logger_show_name=True,
        )
        self.tree_widget: Tree[None] = Tree("A Tree")
        self.foreign = RichLog(id="foreign")
        self.scanner_label = Label(id="scanner")
        self.log_split, self.log_box = collapsible_log(
            self._richlog,
            title="log (unfolds on warnings)",
            collapsed=True,
            box_id="log-box",
            split_id="log-split",
        )
        self.tick = 0

    async def initialize(self) -> None:
        """UI entry point"""
        with_alerts()
        self.set_log_levels(
            (log(), "DEBUG"), ("trickkiste", "INFO"), others_level="WARNING"
        )
        self.set_interval(0.1, self.animate_tick)
        self.produce()
        self.relay_foreign_output()

    def compose(self) -> ComposeResult:
        """Tree | right pane, the log below, footer and status bar"""
        with Horizontal(id="main"):
            yield self.tree_widget
            yield Splitter(self.tree_widget, vertical=True, before=True)
            with Vertical():
                yield self.scanner_label
                yield self.foreign
        yield self.log_split
        yield self.log_box
        yield self._footer_label
        yield StatusBar("fancytui", __version__)

    def animate_tick(self) -> None:
        """Moves the K.I.T.T. light and the footer's spinner"""
        self.tick += 1
        self.scanner_label.update(scanner(self.tick, " foreign output "))
        self.update_status_bar(
            f"{SPINNER[self.tick % len(SPINNER)]} c: copy  w/e: warn/error"
            "  l: fold log  q: quit"
        )

    def on_log_alert(self, _message: LogAlert) -> None:
        """A warning or an error unfolds the log"""
        self.log_box.collapsed = False

    def action_copy(self) -> None:
        """The tree's current node into the clipboard"""
        if (node := self.tree_widget.cursor_node) is not None:
            copy_text(self, Text.from_markup(str(node.label)).plain)

    def action_alert(self, level: int) -> None:
        """Logs something worth a red background"""
        log().log(level, "you asked for a %s", logging.getLevelName(level))

    def action_fold(self) -> None:
        """Folds or unfolds the log"""
        self.log_box.collapsed = not self.log_box.collapsed

    def action_request_quit(self) -> None:
        """Quits, but only on yes"""
        self.push_screen(
            ConfirmScreen(
                "Really quit?", title="fancytui", yes="quit", variant="error"
            ),
            lambda yes: self.exit() if yes else None,
        )

    @on(Tree.NodeSelected)
    def on_node_selected(self, event: Tree.NodeSelected[None]) -> None:
        """React on clicking a node (links handled differently)"""
        log().debug("clicked %s", event.node.label)

    @on(Collapsible.Expanded)
    def on_log_unfolded(self) -> None:
        """Keeps the newest lines in view"""
        self._richlog.scroll_end(animate=False)

    @work(exit_on_error=True)
    async def relay_foreign_output(self) -> None:
        """Runs a noisy child process, shows its output tamed"""
        process = await asyncio.create_subprocess_exec(
            "sh", "-c", FOREIGN_SCRIPT, stdout=asyncio.subprocess.PIPE
        )
        assert process.stdout
        try:
            while line := await process.stdout.readline():
                self.foreign.write(clean_line(line.decode(errors="replace")))
        finally:
            with suppress(ProcessLookupError):
                process.kill()  # it loops forever, the app doesn't

    @work(exit_on_error=True)
    async def produce(self) -> None:
        """Busy worker task continuously rebuilding the job tree"""
        log().info("first message from async worker")
        await asyncio.sleep(0.2)
        cpu_node = self.tree_widget.root.add("CPU")
        disk_node = self.tree_widget.root.add("DISK")
        mem_node = self.tree_widget.root.add("MEM")

        colors_node = self.tree_widget.root.add(
            "[bold spring_green1]Colors[/]", expand=False, allow_expand=True
        )
        for col in ANSI_COLOR_NAMES:
            colors_node.add(
                f"[{col}]{col}[/] [bold {col}]{col}[/]", allow_expand=False
            )

        self.tree_widget.root.expand()

        cpu_bar = HeatBar(
            min_color="cyan",
            max_color="bright_red",
            min_bar_value=0,
            max_bar_value=100,
            min_color_value=50,
            max_color_value=95,
        )
        cpu_bar.width = max(10, self.tree_widget.size.width - 25)
        cpu_bar.data = [
            (math.sin(4 * math.pi / 200 * i) + 1) / 2 * 110 for i in range(200)
        ]
        parts = [
            (s.text, s.style or Style) for s in self.console.render(cpu_bar)
        ]
        cpu_node.set_label(
            Text.from_markup(
                f"{float(cpu_bar.data[-1]):.1f} {max(cpu_bar.data[2:]):<5} "
            )
            + Text.assemble(*parts)  # type: ignore[arg-type]
        )

        disk_bar = HeatBar(
            # min_color="dodger_blue3",
            # max_color="bright_yellow",
            min_color="grey42",
            max_color="bright_white",
            # bg_color="grey11",
            min_bar_value=0,
            max_bar_value=10,
            min_color_value=8,
            max_color_value=12,
            inverted=True,
        )
        disk_bar.width = max(10, self.tree_widget.size.width - 25)
        disk_bar.data = [
            int((math.cos(2 * math.pi / 200 * i) + 1) / 2 * 15)
            for i in range(200)
        ]
        parts = [
            (s.text, s.style or Style) for s in self.console.render(disk_bar)
        ]
        disk_node.set_label(
            Text.from_markup(
                f"{float(disk_bar.data[-1]):>5.1f} {max(disk_bar.data[2:]):<5} "
            )
            + Text.assemble(*parts)  # type: ignore[arg-type]
        )

        while True:
            log().info("step..")
            mem_node.set_label("TBD")
            self.log_foo()
            await asyncio.sleep(15)

    @work(exit_on_error=True, thread=True)
    def log_foo(self) -> None:
        """Some function executed in a separate thread"""
        log().info("foo")


if __name__ == "__main__":
    ExampleTUI().execute()
