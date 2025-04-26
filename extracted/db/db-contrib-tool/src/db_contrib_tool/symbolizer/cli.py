"""CLI for symbolize."""

import sys
from typing import List, Optional

import click
import inject

from db_contrib_tool.symbolizer.mongosymb import (
    InputFormat,
    OutputFormat,
    PathResolver,
    SymbolizerOrchestrator,
    SymbolizerParameters,
)
from db_contrib_tool.usage_analytics import CommandWithUsageTracking

INPUT_FORMATS = ("classic", "thin")
DEFAULT_INPUT_FORMAT = "classic"
OUTPUT_FORMATS = ("classic", "json")
DEFAULT_OUTPUT_FORMAT = "classic"


@click.command(cls=CommandWithUsageTracking)
@click.option("--symbolizer-path", type=click.Path(), help="Path to llvm-symbolizer executable.")
@click.option(
    "--dsym-hint", multiple=True, help="`-dsym-hint` flag values to pass to llvm-symbolizer."
)
@click.option(
    "--input-format",
    type=click.Choice(INPUT_FORMATS, case_sensitive=False),
    default=DEFAULT_INPUT_FORMAT,
    help="Input mongo log format type.",
)
@click.option(
    "--output-format",
    type=click.Choice(OUTPUT_FORMATS, case_sensitive=False),
    default=DEFAULT_OUTPUT_FORMAT,
    help="`json` shows some extra information.",
)
@click.option("--live", is_flag=True, help="Enter live mode.")
@click.option("--host", help="URL of web service running the API to get debug symbol URL.")
# caching mechanism is currently not fully developed and needs more advanced cleaning techniques,
# we add an option to enable it after completing the implementation.
@click.option(
    "--cache-dir",
    type=click.Path(),
    help="Full path to a directory to store cache/files.",
    hidden=True,
)
@click.option(
    "--total-seconds-for-retries", default=0, help="Timeout for getting data from web service."
)
@click.option("--client-secret", help="Secret key for Okta Oauth.")
@click.option("--client-id", help="Client id for Okta Oauth.")
def symbolize(
    symbolizer_path: Optional[str],
    dsym_hint: List[str],
    input_format: str,
    output_format: str,
    live: bool,
    host: Optional[str],
    cache_dir: Optional[str],
    total_seconds_for_retries: int,
    client_secret: Optional[str],
    client_id: Optional[str],
) -> None:  # noqa: D413, D406
    """
    Symbolize MongoDB stack traces.

    To use as a script, paste the JSON object on the line after ----- BEGIN BACKTRACE ----- into the
    standard input of this script.

    Sample usage:

    db-contrib-tool symbolize --symbolizer-path=/path/to/llvm-symbolizer < /file/with/stacktrace

    or more simply:

    db-contrib-tool symbolize < file/with/stackraces

    You can also pass --output-format=json, to get rich json output. It shows some extra information,
    but emits json instead of plain text.

    Notes:

        - To symbolize stacktraces from Evergreen tasks, please ensure the
    `generate_buildid_to_debug_symbols_mapping` task is run on the build variant that generates
    the stacktrace to symbolize.

        - In a non-GUI environment, please forward local port 8989 to enable the OAuth flow from the
    local browser. The command may look something like:

            `ssh -L 8989:localhost:8989 user@virtual-host.amazonaws.com`.
    """
    symbolizer_params = SymbolizerParameters(
        symbolizer_path=symbolizer_path,
        dsym_hint=dsym_hint,
        input_format=InputFormat.CLASSIC if input_format == "classic" else InputFormat.THIN,
        output_format=OutputFormat.CLASSIC if output_format == "classic" else OutputFormat.JSON,
        live=live,
        host=host,
        cache_dir=cache_dir,
        total_seconds_for_retries=total_seconds_for_retries,
        client_secret=client_secret,
        client_id=client_id,
    )

    dbg_path_resolver = PathResolver(
        host=symbolizer_params.host,
        cache_dir=symbolizer_params.cache_dir,
        client_secret=symbolizer_params.client_secret,
        client_id=symbolizer_params.client_id,
    )

    def dependencies(binder: inject.Binder) -> None:
        """Define dependencies for execution."""
        binder.bind(PathResolver, dbg_path_resolver)

    inject.configure(dependencies)
    symbolize_orchestrator = inject.instance(SymbolizerOrchestrator)

    success = symbolize_orchestrator.execute(symbolizer_params)
    if not success:
        sys.exit(1)
