from __future__ import annotations
import atexit
import gc
import logging
import os
import signal
import sys
from importlib import metadata

import typer
from dotenv import load_dotenv

from mcp_cli.console import restore_terminal
from mcp_cli.commands import server_app, tool_app


DOTENV_PATH = os.getenv("MCP_CLI_DOTENV_PATH", None)
load_dotenv(DOTENV_PATH)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
LOG_LEVEL_MAP = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}

# Get log level from environment variable, default to WARNING
log_level_name = os.getenv('LOG_LEVEL', 'WARNING').upper()
log_level = LOG_LEVEL_MAP.get(log_level_name, logging.WARNING)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
    level=log_level
)

# Ensure terminal restoration on exit
atexit.register(restore_terminal)

# ---------------------------------------------------------------------------
# Version handling
# ---------------------------------------------------------------------------
def _get_version() -> str:
    """Get the version of mcp-cli from package metadata."""
    try:
        return metadata.version("devin-mcp-cli")
    except metadata.PackageNotFoundError:
        return "unknown"


def _version_callback(value: bool):
    """Callback for version option."""
    if value:
        typer.echo(_get_version())
        raise typer.Exit()


# ---------------------------------------------------------------------------
# Typer application
# ---------------------------------------------------------------------------
app = typer.Typer()


# ---------------------------------------------------------------------------
# Main callback for global options
# ---------------------------------------------------------------------------
@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show the version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """MCP CLI - A command-line interface for MCP servers."""
    pass


# ---------------------------------------------------------------------------
# Server commands
# ---------------------------------------------------------------------------
app.add_typer(server_app, name="server")

# ---------------------------------------------------------------------------
# Tool commands
# ---------------------------------------------------------------------------
app.add_typer(tool_app, name="tool")

# ---------------------------------------------------------------------------
# Signal‐handler for clean shutdown
# ---------------------------------------------------------------------------
def _signal_handler(sig, _frame):
    logging.debug("Received signal %s, restoring terminal", sig)
    restore_terminal()
    sys.exit(0)


def _setup_signal_handlers() -> None:
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _signal_handler)


# ---------------------------------------------------------------------------
# Main entry‐point
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    _setup_signal_handlers()
    try:
        app()
    finally:
        restore_terminal()
        gc.collect()
