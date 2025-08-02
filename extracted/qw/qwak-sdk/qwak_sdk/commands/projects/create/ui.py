import re
from typing import Optional

import click
from click import Argument, Context

from qwak_sdk.commands.projects.create._logic import execute as execute_create
from qwak_sdk.commands.ui_tools import output_as_json
from qwak_sdk.inner.tools.cli_tools import QwakCommand


def validate_name(_: Context, argument: Argument, value: str) -> str:
    """
    Validate that `value` is a valid project name.
    A valid project name must:
    - Start with a lowercase letter,
    - Contain only lowercase letters or hyphens,
    - End with a lowercase letter,
    - Not be empty.
    :param _: Unused parameter for click's callback signature.
    :param argument: Argument provided.
    :param value: The project name to validate.
    :raise click.BadParameter: If the validation fails.
    :return: The validated project name.
    """
    # Validate that `value`:
    # - starts with a lowercase letter,
    # - contains only lowercase letters or hyphens,
    # - ends with a lowercase letter,
    # - and is not empty.
    if not re.fullmatch(r"[a-z](?:[a-z-]*[a-z])?", value):
        raise click.BadParameter(
            f"{argument.name} must be lower-cased, "
            "start and end with a letter, and only contain letters or hyphens (-)."
        )
    return value


@click.command("create", cls=QwakCommand)
@click.argument(
    "name", metavar="name", type=click.STRING, required=True, callback=validate_name
)
@click.option(
    "--description",
    metavar="DESCRIPTION",
    required=False,
    help="Project description",
)
@click.option(
    "--format",
    default="text",
    show_default=True,
    type=click.Choice(["text", "json"], case_sensitive=True),
    metavar="FORMAT",
    required=False,
    help="The formatting style for commands output (choose from text, json)",
)
@click.option(
    "--jfrog-project-key",
    metavar="ID",
    required=False,
    help="An existing jfrog project key",
)
def create_project(
    name,
    description,
    format,
    jfrog_project_key: Optional[str] = None,
    *args,
    **kwargs,
):
    response = execute_create(name, description, jfrog_project_key=jfrog_project_key)
    if format == "json":
        output_as_json(response)
    else:
        print(f"Project created\nproject id : {response.project.project_id}")
