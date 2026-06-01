# mypy: disable-error-code="unused-ignore"
import asyncio
import inspect
import re
from collections.abc import Iterable
from contextlib import contextmanager
from functools import wraps

import click
import typer.rich_utils
from rich.align import Align
from rich.console import Console, group
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.spinner import SPINNERS
from rich.text import Text
from typer.core import MarkupMode
from typer.rich_utils import MARKUP_MODE_MARKDOWN, STYLE_HELPTEXT_FIRST_LINE

from arraylake.types import UserInfo

try:
    # typer <=0.12.5
    # remove type ignores here and in pyproject.toml after we require typer>=0.13
    from typer.rich_utils import _make_rich_rext as _make_rich_text  # type: ignore
except ImportError:
    from typer.rich_utils import _make_rich_text  # type: ignore

rich_console = Console()
error_console = Console(stderr=True, style="red")


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


# temporary workaround for typer#447
# https://github.com/tiangolo/typer/issues/447
@group()
def _get_custom_help_text(
    *,
    obj: click.Command | click.Group,
    markup_mode: MarkupMode,
) -> Iterable[Markdown | Text]:
    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help or "")

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line = help_text.split("\n\n")[0]
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_MARKDOWN and not first_line.startswith("\b"):
        first_line = first_line.replace("\n", " ")
    yield _make_rich_text(
        text=first_line.strip(),
        style=STYLE_HELPTEXT_FIRST_LINE,
        markup_mode=markup_mode,
    )

    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]
    if remaining_paragraphs:
        remaining_lines = inspect.cleandoc("\n\n".join(remaining_paragraphs).replace("<br/>", "\\"))
        yield _make_rich_text(
            text=remaining_lines,
            style="cyan",
            markup_mode=markup_mode,
        )


typer.rich_utils._get_help_text = _get_custom_help_text

LOGO_ART_WORDMARK = r"""
                                     _           _
                                    | |         | |
   __ _   ___   ___   __ _   _   _  | |   __ _  | | __  ___
  / _` | / __) / __) / _` | | | | | | |  / _` | | |/ / / _ \
 | (_| | | |   | |  | (_| | | |/  | | | | (_| | |   < |  __/
  \__,_| |_|   |_|   \__,_|  \__/ | \__] \__,_| |_|\_\ \___/
                             [___/
"""

LOGO_ART = r"""
⠀⢠⣴⣶⣶⣶⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣿⣯⣤⣶⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢻⣿⣿⣿⣿⣿⣿⣭⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⢿⣿⣿⠟⣿⣦⠙⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠉⠙⠀⠈⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⠿⠿⠿⣾⣿⠀⢀⣾⠿⠿⠇⣰⡿⠿⠇⣀⣶⠿⠿⠿⣦⣿⠀⢸⣿⠀⠀⢠⣾⠿⢿⡆⠀⣿⡇⠀⠀⣠⣾⠿⠿⢷⣾⣿⠀⢸⣿⠀⣀⣾⠟⠁⣠⣶⠿⠻⢿⣦⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⢸⣿⠀⢸⣿⠀⠀⠀⣿⡇⠀⠀⣿⡏⠀⠀⠀⠘⣿⠀⢸⣿⠀⠀⣼⡏⠀⢸⡇⠀⣿⡇⠀⠀⣿⠁⠀⠀⠀⢹⣿⠀⢸⣿⣾⣿⡅⠀⠀⣿⣧⣤⣤⣤⣼⣧
⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⣀⠀⣀⣾⣿⠀⢸⣿⠀⠀⠀⣿⡇⠀⠀⢿⣷⣀⠀⣀⣼⣿⠀⢸⣿⣀⣸⡟⠀⠀⢸⡇⠀⣿⣇⠀⠀⢿⣦⡀⢀⣠⣾⣿⠀⢸⣿⠁⠙⢿⣦⠀⢿⣧⡀⠀⢀⣤⡄
⠛⠛⠛⠛⠛⠛⠛⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠛⠙⠛⠀⠘⠛⠀⠀⠀⠛⠃⠀⠀⠀⠙⠛⠛⠛⠉⠛⠀⠈⠛⠛⠛⠁⠀⠀⢸⡇⠀⠈⠛⠛⠀⠈⠛⠛⠛⠋⠙⠛⠀⠘⠛⠀⠀⠈⠛⠓⠀⠙⠛⠛⠛⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣤⣤⣴⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

SYMBOL_ART = r"""
⠀⠀⢀⣤⣶⣾⣿⣿⣿⣶⡤⠀⠀⠀
⢀⣴⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⣀⡄
⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⡿⠷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣅⡀⠀
⠸⣿⣿⣿⣿⣿⣿⣿⣿⡝⠻⢿⣿⡟
⠀⠙⢿⣿⣿⣿⠏⠹⣿⣷⡀⠀⠀⠀
⠀⠀⠀⠈⠙⠋⠀⠀⠙⠛⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
"""

EARTHMOVER_VIOLET = "#A653FF"
EARTHMOVER_GREEN = "#B7e400"

EARTHMOVER_LINK = f"[bold {EARTHMOVER_GREEN}][link=https://earthmover.io]earthmover.io[/link][/bold {EARTHMOVER_GREEN}]"


def print_logo():
    large = rich_console.width >= 80
    art = LOGO_ART if large else SYMBOL_ART
    subtitle = "The cloud platform for scientific data teams" if large else "arraylake" if rich_console.width >= 24 else None

    panel = Panel(
        Align.center(f"\n[bold {EARTHMOVER_VIOLET}]{art if rich_console.width >= 24 else 'arraylake'}[/bold {EARTHMOVER_VIOLET}]\n"),
        border_style=EARTHMOVER_VIOLET,
        title=EARTHMOVER_LINK,
        title_align="left" if large else "center",
        subtitle=subtitle,
    )
    rich_console.print(Align.center(Padding(panel, (1, 0, 1, 0))))


def print_logo_mini():
    rich_console.rule(
        f"[{EARTHMOVER_VIOLET}] [bold]Arraylake[/bold] | [/{EARTHMOVER_VIOLET}]{EARTHMOVER_LINK}", style=EARTHMOVER_VIOLET, align="left"
    )


def _parse_exception(e: Exception):
    # extract the HTTP error message and turn it into something more user-friendly
    ex = str(e)
    match = re.search(r"\"detail\":\"(.*)\"", ex)
    if match:
        return match.group(1)
    return ex


def print_user_details(user: UserInfo):
    rich_console.print(
        Panel(
            f"Name: [dim]{user.first_name} {user.family_name}[/dim]\nEmail: [dim]{user.email}[/dim]\nId: [dim]{user.id}[/dim]",
            title="[bold]User Details[/bold]",
        )
    )


@contextmanager
def simple_progress(description: str, total: int = 0, quiet: bool = False):
    exit_msg: str | None = None
    if quiet:
        yield
    else:
        if total > 0:
            p = Progress(
                SpinnerColumn(finished_text="[bold green]✓[/bold green]"),
                TextColumn("[progress.description]{task.description}"),
                TaskProgressColumn(),
                BarColumn(),
                MofNCompleteColumn(),
                TimeRemainingColumn(),
                TimeElapsedColumn(),
                console=rich_console,
            )
        else:
            p = Progress(
                SpinnerColumn(finished_text="[bold green]✓[/bold green]"),
                TextColumn("[progress.description]{task.description}"),
                console=rich_console,
            )

        with p as progress:
            task = progress.add_task(description, total=total)
            try:
                yield progress, task
            except Exception as e:
                progress.update(
                    task,
                    advance=0,
                    description=description + "[red bold]failed[/red bold]",
                )
                exit_msg = _parse_exception(e)
            else:
                progress.update(
                    task,
                    advance=1,
                    description=description + "[green bold]succeeded[/green bold]",
                )
    if exit_msg:
        error_console.print(exit_msg)
        exit(1)


# Create a function to generate frames with both the heart and wave moving gradually
def generate_frames(num_frames, width=15):
    frames = []

    # Base wave pattern without the heart
    base_wave = "ﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩـ"  # Wave pattern

    total_length = len(base_wave)

    # Generate frames by shifting the heart's position and modifying wave
    for i in range(num_frames):
        # Move the heart gradually across the base pattern
        heart_position = i % total_length

        # Shift the wave symbols left to simulate movement
        wave_shift = i % total_length  # Shift the wave symbols
        wave = base_wave[wave_shift:] + base_wave[:wave_shift]  # Rotate the wave

        # Insert the heart at the current position
        frame = wave[:heart_position] + "♡" + wave[heart_position + 1 :]  # noqa
        frames.append(frame)

    # Optional: Add reversed frames for smooth back-and-forth effect
    # frames += frames[::-1]

    return frames


frames = generate_frames(25)


# Custom EKG heartbeat spinner
ekg_spinner = {
    "interval": 120,
    "frames": frames,
}

SPINNERS["ekg"] = ekg_spinner


@contextmanager
def ekg_progress(description: str, total: int = 0):
    p = Progress(
        SpinnerColumn(spinner_name="ekg"),
        TextColumn("[progress.description]{task.description}"),
        console=rich_console,
    )

    exit_msg: str | None = None

    with p as progress:
        task = progress.add_task(description, total=total)
        try:
            yield progress, task
        except Exception as e:
            progress.update(
                task,
                advance=0,
                description=description + "[red bold]failed[/red bold]",
            )
            exit_msg = str(e)
        else:
            progress.update(
                task,
                advance=1,
                description=description + "[green bold]succeeded[/green bold]",
            )

    if exit_msg:
        error_console.print(exit_msg)
        exit(1)
