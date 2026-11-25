# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Any, Tuple

import click

from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.test_common import run_tests, update_test


@cli.group()
@click.pass_context
def test(ctx: click.Context) -> None:
    """Test commands."""


@test.command(
    name="update",
    help="Update the test expectations for a file or a test.",
)
@click.argument("pipe", type=str)
@click.pass_context
def test_update(ctx: click.Context, pipe: str) -> None:
    client: TinyB = ctx.ensure_object(dict)["client"]
    project: Project = ctx.ensure_object(dict)["project"]
    config: dict[str, Any] = ctx.ensure_object(dict)["config"]
    update_test(pipe, project, client, config=config)


@test.command(
    name="run",
    help="Run the test suite, a file, or a test",
)
@click.argument("name", nargs=-1)
@click.option(
    "--auto-fixtures/--no-auto-fixtures",
    "auto_fixtures",
    default=True,
    help=(
        "Auto-load fixture files whose name matches a datasource (default). "
        "Use --no-auto-fixtures to skip this step; --fixture entries still load."
    ),
)
@click.option(
    "--fixture",
    "fixtures",
    multiple=True,
    metavar="DATASOURCE=PATH",
    help=(
        "Load fixture PATH into DATASOURCE before running tests. May be repeated; "
        "entries are applied top-to-bottom and multiple entries per datasource are allowed. "
        "When combined with --auto-fixtures (the default), entries are appended after the "
        "auto-loaded fixtures for the same datasource."
    ),
)
@click.pass_context
def run_tests_command(
    ctx: click.Context,
    name: Tuple[str, ...],
    auto_fixtures: bool,
    fixtures: Tuple[str, ...],
) -> None:
    client: TinyB = ctx.ensure_object(dict)["client"]
    project: Project = ctx.ensure_object(dict)["project"]
    config: dict[str, Any] = ctx.ensure_object(dict)["config"]
    run_tests(name, project, client, config=config, fixtures=fixtures, auto_fixtures=auto_fixtures)
