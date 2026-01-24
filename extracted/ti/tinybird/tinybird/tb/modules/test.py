# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Any, Tuple

import click

from tinybird.tb.client import TinyB
from tinybird.tb.modules.agent import run_agent
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.test_common import run_tests, update_test


@cli.group()
@click.pass_context
def test(ctx: click.Context) -> None:
    """Test commands."""


@test.command(
    name="create",
    help="Create a test for an existing pipe",
)
@click.argument("name_or_filename", type=str)
@click.option("--prompt", type=str, default="", help="Prompt to be used to create the test")
@click.pass_context
def test_create(ctx: click.Context, name_or_filename: str, prompt: str) -> None:
    """
    Create a test for an existing pipe
    """
    project: Project = ctx.ensure_object(dict)["project"]
    config: dict[str, Any] = ctx.ensure_object(dict)["config"]
    prompt = (
        f"""Create tests for the following pipe: {name_or_filename}. Extra context: {prompt or "No extra context."}"""
    )
    run_agent(config, project, True, prompt=prompt, feature="tb_test_create")


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
@click.pass_context
def run_tests_command(ctx: click.Context, name: Tuple[str, ...]) -> None:
    client: TinyB = ctx.ensure_object(dict)["client"]
    project: Project = ctx.ensure_object(dict)["project"]
    config: dict[str, Any] = ctx.ensure_object(dict)["config"]
    run_tests(name, project, client, config=config)
