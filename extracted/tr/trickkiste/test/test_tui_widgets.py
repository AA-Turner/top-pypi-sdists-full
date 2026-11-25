"""Unit tests for trickkiste.tui_widgets and the TUI log of base_tui_app"""

import asyncio
import logging
import subprocess
from collections.abc import Iterator
from typing import Any

import pytest
from textual.app import App

from trickkiste import tui_widgets
from trickkiste.base_tui_app import TuiBaseApp
from trickkiste.tui_widgets import (
    SCANNER_DARK,
    SCANNER_TAIL,
    ConfirmScreen,
    LogAlert,
    alert_style,
    clean_line,
    clipped,
    desktop_clipboard,
    scanner,
    with_alerts,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("raw", "plain"),
    [
        ("plain", "plain"),
        ("a\tb", "a\tb"),
        ("\x1b]0;title\x07x", "x"),
        ("\x1b]8;;http://x\x1b\\link\x1b]8;;\x1b\\", "link"),
        ("50%\r100%", "50%100%"),
        (
            "".join(map(chr, range(32)))
            .replace("\t", "")
            .replace("\n", "")
            .replace("\x1b", ""),
            "",
        ),
        ("\x7fdel", "del"),
        ("stray \x1b esc", "stray  esc"),
    ],
)
def test_clean_line(raw: str, plain: str) -> None:
    assert clean_line(raw).plain == plain


def test_alert_style() -> None:
    assert alert_style(logging.DEBUG) == ""
    assert alert_style(logging.WARNING) != alert_style(logging.ERROR) != ""


def test_scanner_edge_widths() -> None:
    assert scanner(5, "").plain == ""
    assert [s.style for s in scanner(3, "x").spans] == [SCANNER_TAIL[0]]
    assert {s.style for s in scanner(-1, "abc").spans} == {SCANNER_DARK}


def test_clipped() -> None:
    assert clipped("a\nb", 5) == "a\nb"
    assert clipped("a\nb\nc", 0) == "…"
    assert all(
        len(line) <= tui_widgets.TIP_WIDTH
        for line in clipped("x " * 99, 99).splitlines()
    )


@pytest.fixture
def clipboard(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, ...]]:
    """Every argv `desktop_clipboard` runs, with only `xclip` installed"""
    calls: list[tuple[str, ...]] = []
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setattr(
        tui_widgets.shutil, "which", lambda cmd: cmd if cmd == "xclip" else None
    )

    def run(
        argv: tuple[str, ...], **_kwargs: Any
    ) -> subprocess.CompletedProcess[bytes]:
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(tui_widgets.subprocess, "run", run)
    return calls


def test_desktop_clipboard(
    clipboard: list[tuple[str, ...]], monkeypatch: pytest.MonkeyPatch
) -> None:
    assert desktop_clipboard("x")
    assert clipboard == [("xclip", "-selection", "clipboard")]
    monkeypatch.delenv("DISPLAY")
    assert not desktop_clipboard("x")
    assert len(clipboard) == 1


def test_desktop_clipboard_tool_fails(
    clipboard: list[tuple[str, ...]], monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken(*_args: Any, **_kwargs: Any) -> None:
        raise subprocess.TimeoutExpired("xclip", 2)

    monkeypatch.setattr(tui_widgets.subprocess, "run", broken)
    assert not desktop_clipboard("x")


@pytest.mark.parametrize(
    ("keys", "answer"),
    [
        (["y"], True),
        (["n"], False),
        (["escape"], False),
        (["enter"], True),
        (["tab", "enter"], False),
    ],
)
def test_confirm_screen(keys: list[str], answer: bool) -> None:
    answers: list[bool | None] = []

    async def scenario() -> None:
        app: App[None] = App()
        async with app.run_test() as pilot:
            app.push_screen(ConfirmScreen("sure?", title="t"), answers.append)
            await pilot.pause()
            await pilot.press(*keys)
            await pilot.pause()

    asyncio.run(scenario())
    assert answers == [answer]


@pytest.fixture
def root_logging() -> Iterator[None]:
    """`TuiBaseApp` replaces the root handlers, they come back afterwards"""
    root = logging.getLogger()
    saved = root.handlers[:], root.level, logging.getLogger("t").level
    yield
    root.handlers = saved[0]
    root.setLevel(saved[1])
    logging.getLogger("t").setLevel(saved[2])


class AlertApp(TuiBaseApp):
    """Logs through the alerting handler, keeps the alerts"""

    def __init__(self) -> None:
        super().__init__(logger_show_time=False, logger_show_name=False)
        self.alerts: list[int] = []

    async def initialize(self) -> None:
        with_alerts()
        self.set_log_levels(("t", logging.DEBUG))

    def on_log_alert(self, message: LogAlert) -> None:
        self.alerts.append(message.level)


@pytest.mark.usefixtures("root_logging")
def test_tui_log_escapes_once_and_alerts() -> None:
    async def scenario() -> tuple[list[str], list[int]]:
        app = AlertApp()
        async with app.run_test() as pilot:
            await pilot.pause()
            logging.getLogger("t").info("[red] %s", "[b]")
            logging.getLogger("t").warning("w")
            logging.getLogger("t").error(42)
            try:
                {}["[/]"]  # noqa: B018
            except KeyError:
                logging.getLogger("t").exception("tb")
            await pilot.pause()
            lines = [strip.text.rstrip() for strip in app._richlog.lines]  # noqa: SLF001
            return lines, app.alerts

    lines, alerts = asyncio.run(scenario())
    assert [line.split("│ ")[-1] for line in lines[:4]] == [
        "[red] [b]",
        "w",
        "42",
        "tb",
    ]
    assert lines[4] == "Traceback (most recent call last):"
    assert lines[-1] == "KeyError: '[/]'"
    assert alerts == [logging.WARNING, logging.ERROR, logging.ERROR]
