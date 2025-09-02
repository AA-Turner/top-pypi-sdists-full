#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import logging
import time
import webbrowser
from importlib import metadata
from typing import Annotated

import requests
import typer
from requests import Response
from rich.panel import Panel
from typer import Exit, Option, Typer

from pendingai import Environment, config
from pendingai.cli import auth, generator, retro
from pendingai.cli.console import Console
from pendingai.cli.context import PendingAiContext
from pendingai.client import PendingAiClient
from pendingai.utils.logger import Logger

logger: logging.Logger = Logger().get_logger()

cout = Console()
cerr = Console(stderr=True)


app = Typer(
    name="pendingai",
    help=(
        "Pending AI Command-Line Interface.\n\nCheminformatics services "
        "offered by this CLI are accessible through an API integration "
        "with the Pending AI platform. An authenticated session is required "
        "for use; see <pendingai auth>. Documentation is available with "
        "<pendingai docs>."
    ),
    epilog=(
        "For support, issues, or feature requests, please email support@pending.ai."
    ),
    no_args_is_help=True,
    add_completion=False,
    pretty_exceptions_show_locals=False,
    rich_markup_mode=None,
    context_settings={"max_content_width": config.CONSOLE_WIDTH},
)
app.add_typer(auth.app)
app.add_typer(retro.app)
app.add_typer(generator.app)


def version_callback(render_version: bool):
    if render_version:
        try:
            version: str = metadata.version("pendingai")
        except metadata.PackageNotFoundError:
            cerr.print("[red bold]Unable to find package: 'pendingai'.[/]")
            raise Exit(1)
        cout.print(f"[reset]pendingai/{version}[/]")
        raise Exit


def version_update_callback(render_version_update: bool = False):
    # hook to check the latest package version available on pypi, output
    # warning if the latest version is not in use and command to update
    # https://discuss.python.org/t/api-to-get-latest-version-of-a-pypi-package/10197/4
    try:
        response: Response = requests.get("https://pypi.org/pypi/pendingai/json")
        response.raise_for_status()
        pypi_version: str = response.json()["info"]["version"]
        inst_version: str = metadata.version("pendingai")
        pypi: list[int] = [int(x) for x in pypi_version.split(".")[:3]]
        inst: list[int] = [int(x) for x in inst_version.split(".")[:3]]
        message: str = (
            "A new release of 'pendingai' can be installed: "
            f"[red]{inst_version}[/] -> [green]{pypi_version}[/]\n"
            "To update, run: [green]pip install --upgrade pendingai[/]"
        )
        for pypi_int, inst_int in zip(pypi, inst):
            if pypi_int > inst_int:
                cout.print(Panel(message, expand=False))
                return
            elif inst_int > pypi_int:
                return

    except Exception:
        pass


def _enable_console_logging(log_to_console: bool = False) -> None:
    if log_to_console:
        Logger().enable_console_logging()


@app.callback()
def callback(
    ctx: PendingAiContext,
    render_version: Annotated[
        bool,
        Option(
            "--version",
            is_eager=True,
            callback=version_callback,
            help="Show the application version and exit.",
        ),
    ] = False,
    render_version_update: Annotated[
        bool,
        Option(
            is_eager=True,
            hidden=True,
            callback=version_update_callback,
        ),
    ] = True,
    environment: Annotated[
        Environment,
        typer.Option(
            "--env",
            "-e",
            hidden=True,
            show_default=False,
            envvar="PENDINGAI_ENVIRONMENT",
            help="Selectable runtime deployment server.",
        ),
    ] = Environment.DEFAULT,
    log_to_console: Annotated[
        bool,
        typer.Option(
            "--log-to-console",
            hidden=True,
            show_default=False,
            help="Enable printing logs to the console in addition to the log file.",
            callback=_enable_console_logging,
        ),
    ] = False,
    verbose: Annotated[
        int,
        Option("-v", count=True, hidden=True),
    ] = 0,
) -> None:
    # setup app verbosity and pendingai client for app context
    logger.setLevel(40 - min(verbose, 3) * 10)
    client: PendingAiClient = PendingAiClient(environment=environment.value)
    ctx.obj = {"client": client}


@app.command("docs", help="Open documentation in a web browser.")
def _docs() -> bool:
    redirect_url: str = "https://docs.pending.ai/"
    cout.print(f"[warn]! Redirecting to [link]{redirect_url}[/] in your browser...")
    time.sleep(1)
    return webbrowser.open_new_tab(redirect_url)


if __name__ == "__main__":
    app()
