from typing import Optional
import asyncclick as click


from ..__init__ import __version__
from ..commands import commands

from ..commands.global_options import (
    DAP_API_URL_DEFAULT,
    GlobalOptions,
    dap_tracking_valid_values,
    pass_global_options,
)
from ..log import setup_logging, log_system_info
from ..tracking import executing_in_cli_mode
from .. import ui


class CustomGroup(click.Group):
    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        super().format_help(ctx, formatter)

        formatter.write("\n")

        url1 = "https://developerdocs.instructure.com/services/dap/dap-cli-readme/dap-cli-reference"
        url2 = "https://developerdocs.instructure.com/services/dap/query-api"
        self._write_text_with_non_wrapped_parts(
            formatter,
            f"For more information and examples, check the reference at {url1} "
            f"and the OpenAPI specification for DAP API at {url2}.",
            non_wrapped_parts=[url1, url2],
        )

    def list_commands(self, ctx: click.Context) -> list[str]:
        # This overrides the default alphabetical ordering of commands with the order in which they were added
        return list(self.commands.keys())

    def _write_text_with_non_wrapped_parts(
        self,
        formatter: click.HelpFormatter,
        text: str,
        non_wrapped_parts: list[str] = [],
    ) -> None:
        """
        Writes text into the formatter, replacing non-wrapped parts with placeholders
        to prevent them from being wrapped by the formatter. Then it replaces the placeholders
        back with the original parts after the text has been written to the formatter.
        """

        placeholders: dict[str, str] = {}

        for i in range(len(non_wrapped_parts)):
            part = non_wrapped_parts[i]
            placeholder = part.replace("-", "_").replace(" ", "_")
            placeholders[part] = placeholder

        for part, placeholder in placeholders.items():
            text = text.replace(part, placeholder)

        formatter.write_text(text)

        for part, placeholder in placeholders.items():
            formatter.buffer = [
                line.replace(placeholder, part) for line in formatter.buffer
            ]


@click.group(
    help="Invokes the DAP API to fetch table snapshots and incremental updates. "
         "You can opt out of analytics tracking at any time by using the DAP CLI (Data Access Platform Command Line Interface). "
         "Please refer to the documentation for instructions on how to disable analytics through the CLI.",
    cls=CustomGroup,
    context_settings={
        "obj": GlobalOptions,
        "help_option_names": ["--help", "-h"],
        "max_content_width": 150,
    },
    commands={
        "snapshot": commands.snapshot,
        "incremental": commands.incremental,
        "list": commands.list,
        "schema": commands.schema,
        "initdb": commands.initdb,
        "syncdb": commands.syncdb,
        "dropdb": commands.dropdb,
    },
    epilog="Try 'dap COMMAND --help' to get more information about a specific command.",
)
@pass_global_options
@click.option(
    "--base-url",
    type=click.STRING,
    default=DAP_API_URL_DEFAULT,
    show_default=True,
    metavar="URL",
    help="Base URL of the DAP API. May be set via environment variable DAP_API_URL.",
    envvar="DAP_API_URL",
)
@click.option(
    "--client-id",
    type=click.STRING,
    metavar="CLIENTID",
    help="OAuth client ID obtained from the Identity Service. May be set via environment variable DAP_CLIENT_ID.",
    envvar="DAP_CLIENT_ID",
)
@click.option(
    "--client-secret",
    type=click.STRING,
    metavar="CLIENTSECRET",
    help="OAuth client secret obtained from the Identity Service. May be set via environment variable DAP_CLIENT_SECRET.",
    envvar="DAP_CLIENT_SECRET",
)
@click.option(
    "--loglevel",
    type=click.Choice(["debug", "info", "warning", "error"]),
    default="info",
    show_default=True,
    help="Sets log verbosity.",
)
@click.option(
    "--logfile",
    type=click.Path(exists=False, writable=True),
    default=None,
    metavar="LOGFILE",
    help="Sets the path of the file to save logs to.",
)
@click.option(
    "--logformat",
    type=click.Choice(["plain", "json"]),
    default="plain",
    show_default=True,
    help="Sets the log format.",
)
@click.option(
    "--no-log-to-console",
    is_flag=True,
    default=False,
    help="Disable logging to console stderr in case of non-interactive mode.",
)
@click.option(
    "--no-tracking",
    is_flag=True,
    default=None,
    help="Disable DAP analytics tracking. May be set via environment variable DAP_TRACKING "
    f"using values {dap_tracking_valid_values()}.",
)
@click.option(
    "--non-interactive",
    is_flag=True,
    default=False,
    help="Run in non-interactive mode for usage in scripts.",
)
@click.option(
    "--console-theme",
    type=commands.EnumType(ui.ConsoleTheme),
    default=ui.ConsoleTheme.DARK,
    show_default=True,
    help="Sets the theme for the interactive console. May be set via environment variable DAP_CONSOLE_THEME.",
    envvar="DAP_CONSOLE_THEME",
)
@click.version_option(__version__, prog_name="dap", message="%(prog)s %(version)s")
async def dap(
    global_options: GlobalOptions,
    base_url: str,
    client_id: str,
    client_secret: str,
    loglevel: str,
    logfile: str,
    logformat: str,
    no_log_to_console: bool,
    no_tracking: Optional[bool],
    non_interactive: bool,
    console_theme: ui.ConsoleTheme,
) -> None:
    global_options.base_url = base_url
    global_options.client_id = client_id
    global_options.client_secret = client_secret
    global_options.loglevel = loglevel
    global_options.logfile = logfile
    global_options.logformat = logformat
    global_options.log_to_console = not no_log_to_console
    global_options.tracking = not no_tracking if no_tracking is not None else None
    global_options.interactive = not non_interactive
    global_options.console_theme = console_theme

    executing_in_cli_mode()
    ui.set_interactive_mode(global_options.interactive)
    ui.set_console_theme(global_options.console_theme)

    setup_logging(global_options)
    log_system_info()
