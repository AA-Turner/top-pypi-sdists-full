"""Misc utils needed by the probe."""
import datetime
import logging
import os
from pathlib import Path
from typing import Tuple

import click
from click_aliases import ClickAliasedGroup
from click_default_group import DefaultGroup
from click_help_colors import HelpColorsGroup
from dateutil.parser import parse
from rich.logging import RichHandler

database = "task.db"


log = logging.getLogger("rich")

debug = log.debug

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)


class AliasedGroup(DefaultGroup, HelpColorsGroup, ClickAliasedGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_headers_color = "green"
        self.help_options_color = "blue"


def info(msg: str):
    """Print info message."""
    # check if debug level is DEBUG (Num value = 10)
    # https://docs.python.org/3/library/logging.html#logging-levels
    if log.getEffectiveLevel() == 10:
        debug(msg)
    else:
        click.secho(f"[i] {msg}", fg='blue')


def error(msg: str):
    """Print error message."""
    if log.getEffectiveLevel() == 10:
        debug(msg)
    else:
        click.secho(f"[e] {msg}", fg='red', bold=True)


def warning(msg: str):
    """Print warning message."""
    if log.getEffectiveLevel() == 10:
        debug(msg)
    else:
        click.secho(f"[w] {msg}", fg='yellow')


def format_current_time() -> str:
    date = str(datetime.datetime.now())
    return date.split(".")[0]


def does_db_exist() -> Tuple[bool, bool]:
    """Check if database exists."""
    global database
    prod_path = f"{os.getenv('HOME')}/.task.db"

    if Path("task.db").exists():
        db = True
        is_prod = False
    elif Path(prod_path).exists():
        db, is_prod = True, True
        database = prod_path
    else:
        db, is_prod = False, False
    return db, is_prod


def prettify_header(header) -> tuple:
    """Pretty header."""
    new_header = list()
    for data in header:
        new_header.append(f"\x1b[4m{data}\x1b[0m")
    return new_header


def parse_due(due: str = None) -> datetime.date:
    if due is None:
        return None

    now = datetime.datetime.now()
    when = due.lower()
    due_date = None

    # check if it's a date format
    try:
        due_date = parse(when)
    except ValueError:
        pass

    if when == "tomorrow":
        due_date = now + datetime.timedelta(days=1)
    elif when.find("day") != -1:
        number = int(when.split()[0])
        due_date = now + datetime.timedelta(days=number)
    elif when.find("month") != 1:
        number = int(when.split()[0])
        due_date = now + datetime.timedelta(days=(number * 31))
    elif when.find("year") != 1:
        number = int(when.split()[0])
        due_date = now + datetime.timedelta(days=(number * 365))
    else:
        pass
    return due_date
