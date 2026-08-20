import re
import shlex
import typing as t
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from dreadnode.agents.tools import tool

_ANSI_ESCAPES = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _plain(text: str) -> str:
    # Newer typer/rich render help with ANSI styling even when stdout is not
    # a terminal; this tool returns text for agents, so keep it plain.
    return _ANSI_ESCAPES.sub("", text)


def _normalize_tokens(command: str | None) -> list[str]:
    if not command or not command.strip():
        return []

    tokens = shlex.split(command)
    if tokens and tokens[0] in {"dreadnode", "dn"}:
        tokens = tokens[1:]
    return tokens


@tool
def dreadnode_cli(
    command: t.Annotated[
        str | None,
        "Optional command path such as 'capability improve' or 'runtime list'. "
        "The tool always returns help text and never executes the command itself.",
    ] = None,
) -> str:
    """
    Render exact `dreadnode` CLI help for a command path.

    Use this when you need the current shipped syntax for `dn` or `dreadnode`
    commands. This tool is help-only: it appends `--help` when needed and does
    not run mutating CLI actions.
    """
    from dreadnode.app.cli.main import cli

    tokens = _normalize_tokens(command)
    if "--help" not in tokens and "-h" not in tokens:
        tokens.append("--help")

    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            cli(tokens)
        except SystemExit as exc:
            if exc.code not in (0, None):
                error_output = (
                    _plain(stderr.getvalue()).strip() or _plain(stdout.getvalue()).strip()
                )
                if error_output:
                    raise RuntimeError(error_output) from exc
                raise RuntimeError(f"dreadnode CLI help failed with exit code {exc.code}") from exc

    output = _plain(stdout.getvalue()).strip()
    if output:
        return output

    error_output = _plain(stderr.getvalue()).strip()
    if error_output:
        return error_output

    resolved = " ".join(tokens[:-1]).strip()
    if resolved:
        return f"No help output available for `dreadnode {resolved}`."
    return "No help output available for `dreadnode`."
