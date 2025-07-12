import os
import sys

from rich.console import Console
from rich.text import Text


"""
A drop-in wrapper around `print` and Rich's spinner that's primarily used to filter rich output
(i.e. emojis) from CLI output.
"""

REINITIALIZE_RICH_CONSOLE = os.environ.get("TECTON_REINITIALIZE_RICH_CONSOLE") == "true"
SPINNER_TYPE = "point"

_stdout_console = Console()
_stderr_console = Console(file=sys.stderr)


def _get_or_create_console(file):
    """Get the appropriate console instance based on the file."""
    if file == sys.stderr:
        return _stderr_console
    return _stdout_console


def get_console(file=None):
    """Get a console instance, reinitializing if needed."""
    if REINITIALIZE_RICH_CONSOLE:
        console = Console()
        if file is not None:
            console.file = file
        return console
    return _get_or_create_console(file)


def safe_print(*objects, **kwargs):
    """Use to print text to the console."""
    file = kwargs.pop("file", sys.stdout)
    ansi = kwargs.pop("ansi", False)
    plain = kwargs.pop("plain", False)

    if file not in (sys.stderr, sys.stdout):
        msg = f"Invalid file: {file}"
        raise ValueError(msg)

    # Use standard print for plain output (useful for JSON)
    if plain:
        print(*objects, file=file, **kwargs)
        return

    print_console = get_console(file)

    if ansi:
        objects = [Text.from_ansi(obj) for obj in objects]

    print_console.print(*objects, **kwargs)


def rich_print(text, file=None):
    """Use to print Rich Objects to the console."""
    get_console(file).print(text)
