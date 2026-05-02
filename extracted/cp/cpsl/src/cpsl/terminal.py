"""Rich-based terminal output for the Capsule CLI and SDK.

Modeled on beta9's terminal module: spinners, progress bars, phased headers.
"""

from __future__ import annotations

import sys
import threading
from contextlib import contextmanager
from io import BytesIO
from os import PathLike
from typing import Any, Generator, Literal, Optional, Sequence, Tuple, Union

import rich.status
from rich.console import Console
from rich.markup import escape
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    ProgressColumn,
    Task,
    TextColumn,
    TimeRemainingColumn,
)
from rich.progress import open as _progress_open
from rich.text import Text

_console = Console()
_err_console = Console(stderr=True)
_current_status = None
_status_lock = threading.Lock()
_status_count = 0


class SpinnerHandle:
    def __init__(self, status: rich.status.Status):
        self._status = status

    def update(
        self,
        text: Optional[str] = None,
        *,
        spinner: Optional[str] = None,
        spinner_style: Optional[str] = None,
        speed: Optional[float] = None,
    ) -> None:
        kwargs: dict[str, Any] = {}
        if text is not None:
            kwargs["status"] = Text(text)
        if spinner is not None:
            kwargs["spinner"] = spinner
        if spinner_style is not None:
            kwargs["spinner_style"] = spinner_style
        if speed is not None:
            kwargs["speed"] = speed
        self._status.update(**kwargs)
        if self._status._live is not None:
            self._status._live.refresh()


def header(text: str, subtext: str = "") -> None:
    _console.print()
    _console.print(f"[bold #4CCACC]=> {text}[/bold #4CCACC]", subtext)


def info(text: str, markup: bool = True) -> None:
    _console.print(text, markup=markup)


def detail(text: str, dim: bool = True, **kwargs) -> None:
    style = "dim" if dim else ""
    _console.print(Text(text, style=style), **kwargs)


def success(text: str) -> None:
    _console.print("[#4CCACC]✓[/#4CCACC]", Text(text))


def url(href: str) -> None:
    _console.print(f"  [bold #4CCACC][link={href}]{href}[/link][/bold #4CCACC]")


def status_ok(text: str) -> None:
    _console.print("  [#4CCACC]\u2713[/#4CCACC]", Text(text))


def status_fail(text: str) -> None:
    _console.print("  [bold yellow]\u2717[/bold yellow]", Text(text, style="yellow"))


def warn(text: str) -> None:
    _err_console.print(Text(text, style="bold yellow"))


def error(text: str, exit: bool = True) -> None:
    _err_console.print(Text(text, style="bold red"))
    if exit:
        sys.exit(1)


@contextmanager
def progress(task_name: str) -> Generator[SpinnerHandle, None, None]:
    """Show a dots spinner while work is in progress. Thread-safe, refcounted."""
    global _current_status, _status_count

    with _status_lock:
        if _current_status is None:
            _current_status = _console.status(Text(task_name), spinner="dots", spinner_style="white")
            _current_status.start()
        _status_count += 1

    try:
        yield SpinnerHandle(_current_status)
    finally:
        with _status_lock:
            _status_count -= 1
            if _status_count == 0:
                _current_status.stop()
                _current_status = None


def progress_open(file: Union[str, PathLike, bytes], mode: str, **kwargs: Any) -> BytesIO:
    """Open a file with a Rich progress bar for reading (e.g. uploads)."""
    options = dict(
        complete_style="green",
        finished_style="slate_blue1",
        refresh_per_second=30,
        **kwargs,
    )
    if "description" in options and options["description"]:
        options["description"] = escape(f"[{options['description']}]")
    return _progress_open(file, mode, **options)  # type: ignore


def humanize_memory(m: float, base: Literal[2, 10] = 2) -> str:
    factor = 1024 if base == 2 else 1000
    units = (
        ["B", "KiB", "MiB", "GiB", "TiB"]
        if base == 2
        else ["B", "KB", "MB", "GB", "TB"]
    )
    index = 0
    while m >= factor and index < len(units) - 1:
        m /= factor
        index += 1
    return f"{m:.2f} {units[index]}"


def pluralize(seq: Sequence) -> Tuple[int, str]:
    n = len(seq)
    return n, "s" if n != 1 else ""


class AverageTransferSpeedColumn(ProgressColumn):
    def render(self, task: Task) -> Text:
        task.fields.setdefault("average_mib_s", 0.0)
        if not task.started or task.elapsed == 0:
            return Text("?", style="progress.data.speed")
        if task.completed == task.total:
            return Text(f"{task.fields['average_mib_s']:.2f} MiB/s", style="progress.data.speed")
        average_bps = task.completed / (task.elapsed or 1)
        task.fields["average_mib_s"] = average_bps / (1024**2)
        return Text(f"{task.fields['average_mib_s']:.2f} MiB/s", style="progress.data.speed")


def styled_progress() -> Progress:
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="slate_blue1"),
        DownloadColumn(binary_units=True),
        AverageTransferSpeedColumn(),
        TimeRemainingColumn(elapsed_when_finished=True),
        auto_refresh=True,
        refresh_per_second=30,
    )
