"""Unit tests for trickkiste.logging_helper"""

import io
import logging
from argparse import ArgumentParser
from collections.abc import Iterator

import pytest
from rich.console import Console

from trickkiste.logging_helper import (
    FluidRichHandler,
    apply_common_logging_cli_args,
    logger_levelname_filter,
    markup_escape_filter,
    set_log_levels,
    setup_logging_handler,
)

pytestmark = pytest.mark.unit


class ListHandler(logging.Handler):
    """Keeps the formatted lines"""

    def __init__(self) -> None:
        super().__init__()
        self.lines: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.lines.append(self.format(record))


@pytest.fixture
def handler() -> Iterator[ListHandler]:
    """A `ListHandler` set up like the console one, root logging restored"""
    root = logging.getLogger()
    saved = root.handlers[:], root.level
    root.handlers = []
    setup_logging_handler(
        list_handler := ListHandler(),
        show_level=True,
        show_time=False,
        show_name=False,
        show_callstack=False,
        show_funcname=False,
        show_tid=False,
        show_linenumber=False,
    )
    root.setLevel(logging.DEBUG)
    yield list_handler
    root.handlers, _ = saved
    root.setLevel(saved[1])


def test_non_str_message_is_logged(handler: ListHandler) -> None:
    logging.getLogger("t").warning(42)
    logging.getLogger("t").warning({"a": "[b]"})
    assert [line.split("│ ")[-1] for line in handler.lines] == [
        "[bold white]42[/]",
        "[bold white]{'a': '[b]'}[/]",
    ]


def test_custom_level_is_logged(handler: ListHandler) -> None:
    logging.addLevelName(25, "NOTICE")
    logging.getLogger("t").log(25, "hi")
    assert handler.lines == ["NOTICE │ [bold white]hi[/]"]


def test_markup_is_escaped(handler: ListHandler) -> None:
    logging.getLogger("t").warning("[red] %s", "[blue]")
    assert handler.lines == ["[yellow]WW[/] │ [bold white]\\[red] \\[blue][/]"]


def test_filters_leave_unknown_records_intact() -> None:
    record = logging.LogRecord("n", 27, "p", 1, 42, None, None)
    assert markup_escape_filter(record)
    assert logger_levelname_filter(record)
    assert (record.msg, record.shortlevelname) == (42, "Level 27")


@pytest.mark.parametrize("level", ["WARN", "WARNING", "all_debug", "info"])
def test_cli_log_level(level: str) -> None:
    parser = apply_common_logging_cli_args(ArgumentParser())
    assert parser.parse_args(["-l", level]).log_level == level.upper()
    assert parser.parse_args([]).log_level == "WARNING"


@pytest.fixture
def restore_levels() -> Iterator[None]:
    names = (None, "trickkiste", "foo", "bar")
    saved = {name: logging.getLogger(name).level for name in names}
    yield
    for name, level in saved.items():
        logging.getLogger(name).setLevel(level)


@pytest.mark.usefixtures("restore_levels")
def test_set_log_levels() -> None:
    set_log_levels("DEBUG")
    assert logging.getLogger("trickkiste").level == logging.DEBUG
    assert logging.getLogger().level == logging.WARNING

    set_log_levels(("foo", "INFO"), (logging.getLogger("bar"), logging.ERROR))
    assert logging.getLogger("foo").level == logging.INFO
    assert logging.getLogger("bar").level == logging.ERROR

    set_log_levels("ERROR", ("foo", "ALL_DEBUG"))
    assert logging.getLogger().level == logging.DEBUG
    assert logging.getLogger("foo").level == logging.DEBUG

    with pytest.raises(TypeError, match="unsupported"):
        set_log_levels()


def test_fluid_handler_prints_tracebacks_plain() -> None:
    root = logging.getLogger()
    saved = root.handlers[:], root.level
    root.handlers = []
    console = Console(file=io.StringIO(), width=200, color_system=None)
    setup_logging_handler(
        FluidRichHandler(console),
        show_level=False,
        show_time=False,
        show_name=False,
        show_callstack=False,
        show_funcname=False,
        show_tid=False,
        show_linenumber=False,
    )
    root.setLevel(logging.DEBUG)
    try:
        try:
            {}["[/]"]  # noqa: B018
        except KeyError:
            logging.getLogger("t").exception("lookup [failed]")
        logging.getLogger("t").warning("stack", stack_info=True)
    finally:
        root.handlers, _ = saved
        root.setLevel(saved[1])
    output = console.file.getvalue()  # type: ignore[attr-defined]
    assert output.startswith("lookup [failed]\nTraceback")
    assert "KeyError: '[/]'" in output
    assert "\nstack\nStack (most recent call last):" in output
