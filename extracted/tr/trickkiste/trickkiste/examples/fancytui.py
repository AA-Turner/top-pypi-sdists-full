#!/usr/bin/env python3

"""Too lazy for a real test - I'm using this example to check if colorful logging works"""

import asyncio
import logging
import math

from rich.color import ANSI_COLOR_NAMES
from rich.style import Style
from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.widgets import Tree

from trickkiste.base_tui_app import HeatBar, TuiBaseApp


def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("trickkiste.fancytui")


class ExampleTUI(TuiBaseApp):
    """A little example TUI"""

    def __init__(self) -> None:
        super().__init__(logger_show_funcname=True, logger_show_tid=True, logger_show_name=True)
        self.tree_widget: Tree[None] = Tree("A Tree")

    async def initialize(self) -> None:
        """UI entry point"""
        self.set_log_levels((log(), "DEBUG"), ("trickkiste", "INFO"), others_level="WARNING")
        self.produce()

    def compose(self) -> ComposeResult:
        """Set up the UI"""
        yield self.tree_widget
        yield from super().compose()

    @on(Tree.NodeSelected)
    def on_node_selected(self, event: Tree.NodeSelected[None]) -> None:
        """React on clicking a node (links handled differently)"""
        log().debug("clicked %s", event.node.label)

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
            colors_node.add(f"[{col}]{col}[/] [bold {col}]{col}[/]", allow_expand=False)

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
        cpu_bar.data = [(math.sin(4 * math.pi / 200 * i) + 1) / 2 * 110 for i in range(200)]
        parts = [(s.text, s.style or Style) for s in self.console.render(cpu_bar)]
        cpu_node.set_label(
            Text.from_markup(f"{float(cpu_bar.data[-1]):.1f} {max(cpu_bar.data[2:]):<5} ")
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
        disk_bar.data = [int((math.cos(2 * math.pi / 200 * i) + 1) / 2 * 15) for i in range(200)]
        parts = [(s.text, s.style or Style) for s in self.console.render(disk_bar)]
        disk_node.set_label(
            Text.from_markup(f"{float(disk_bar.data[-1]):>5.1f} {max(disk_bar.data[2:]):<5} ")
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
