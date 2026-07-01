"""
custom mcli spinners
"""
import contextlib
import os

import rich
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from mcli.utils.utils_logging import console, err_console

# pylint: disable-next=protected-access,
rich._spinners.SPINNERS["doge"] = {  # pyright: ignore
    "interval": 80,
    "frames": [
        "      🐕",
        "     🐕 ",
        "    🐕  ",
        "   🐕   ",
        "  🐕    ",
        " 🐕     ",
        "🐕      ",
        "        ",
        "        ",
    ]
}


def get_spinner_style() -> str:
    if os.environ.get('DOGEMODE', None) == 'ON':
        return "doge"

    return "dots"  # default


def progress() -> Progress:
    spinner = get_spinner_style()
    return Progress(
        SpinnerColumn(spinner_name=spinner),
        TextColumn('[progress.description]{task.description}'),
        TimeElapsedColumn(),
        console=err_console,
        transient=True,
    )


@contextlib.contextmanager
def console_status(text: str):
    with console.status(text, spinner=get_spinner_style()) as s:
        yield s
