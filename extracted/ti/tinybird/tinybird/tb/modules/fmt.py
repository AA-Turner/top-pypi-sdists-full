import difflib
import sys
from pathlib import Path
from typing import List, Optional

import click
from click import Context

from tinybird.datafile.common import is_file_a_datasource, peek
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.datafile.diff import color_diff
from tinybird.tb.modules.datafile.format_connection import format_connection
from tinybird.tb.modules.datafile.format_datasource import format_datasource
from tinybird.tb.modules.datafile.format_pipe import format_pipe
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.command()
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, required=True)
@click.option(
    "--line-length",
    is_flag=False,
    default=100,
    help="A number indicating the maximum characters per line in the node SQL, lines will be splitted based on the SQL syntax and the number of characters passed as a parameter",
)
@click.option("--dry-run", is_flag=True, default=False, help="Don't ask to override the local file")
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation to overwrite the local file")
@click.option(
    "--diff",
    is_flag=True,
    default=False,
    help="Formats local file, prints the diff and exits 1 if different, 0 if equal",
)
@click.option("--no-color", is_flag=True, default=False, help="Don't colorize diff")
@click.pass_context
def fmt(
    ctx: Context, filenames: List[str], line_length: int, dry_run: bool, yes: bool, diff: bool, no_color: bool
) -> Optional[str]:
    """
    Formats a .datasource, .pipe, or .connection file

    This command removes comments starting with # from the file, use DESCRIPTION instead.

    The format command tries to parse the datafile so syntax errors might rise.
    """

    result = ""
    failed = []
    for filename in filenames:
        if not diff:
            click.echo(filename)
        extensions = Path(filename).suffixes
        if is_file_a_datasource(filename):
            result = format_datasource(filename, skip_eval=True, ignore_secrets=True)
        elif ".pipe" in extensions:
            result = format_pipe(filename, line_length, skip_eval=True, ignore_secrets=True)
        elif ".connection" in extensions:
            result = format_connection(filename, skip_eval=True, ignore_secrets=True)
        else:
            click.echo("Unsupported file type. Supported files types are: .datasource, .pipe, and .connection")
            return None

        if diff:
            result = result.rstrip("\n")
            lines_fmt = [f"{line}\n" for line in result.split("\n")]
            with open(filename, "r") as file:
                lines_file = file.readlines()
            diff_result = difflib.unified_diff(
                lines_file, lines_fmt, fromfile=f"{Path(filename).name} local", tofile="fmt datafile"
            )
            if not no_color:
                diff_result = color_diff(diff_result)
            not_empty, diff_lines = peek(diff_result)
            if not_empty:
                sys.stdout.writelines(diff_lines)
                failed.append(filename)
                click.echo("")
        else:
            click.echo(result)
            if dry_run:
                return None

            if yes or click.confirm(FeedbackManager.prompt_override_local_file(name=filename)):
                with open(f"{filename}", "w") as file:
                    file.write(result)

                click.echo(FeedbackManager.success_generated_local_file(file=filename))

    if failed:
        click.echo(FeedbackManager.error_failed_to_format_files(number=len(failed)))
        for f in failed:
            click.echo(f"tb fmt {f} --yes")
        sys.exit(1)
    return result
