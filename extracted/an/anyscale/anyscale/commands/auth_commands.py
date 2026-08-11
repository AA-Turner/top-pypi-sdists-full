import click

from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import OutputFormat
from anyscale.controllers.auth_controller import AuthController


@click.group(
    "auth",
    short_help="Show the authenticated user and manage credentials",
    help="""Show the authenticated user and manage the Anyscale
authentication credentials""",
)
def auth_cli() -> None:
    pass


# Replaced by anyscale login
@auth_cli.command(
    name="set", help="Set up credentials and save it to a file", hidden=True
)
def auth_set() -> None:
    auth_controller = AuthController()
    auth_controller.set()


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Show the currently authenticated user and organization.",
            command="anyscale auth show",
            output_raw=(
                "Identifying the user\n"
                "Successfully authenticated as:\n"
                "  user name:                    Some One\n"
                "  user email:                   someone@myorg.com\n"
                "  user id:                      usr_we8x7d7u8hq8mj2488ed9x47n6\n"
                "  organization name:            myorg\n"
                "  organization id:              org_7c1Kalm9WcX2bNIjW53GUT\n"
                "  organization role:            collaborator\n"
            ),
        ),
    ],
)
@auth_cli.command(
    name="show",
    short_help="Show the authenticated user.",
    help="Show the information of the authenticated user using credentials",
)
def auth_show() -> None:
    auth_controller = AuthController()
    auth_controller.show()


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Restrict the credentials file permissions to the owner.",
            command="anyscale auth fix",
            output_raw=(
                "Successfully fixed the permissions of ~/.anyscale/credentials.json\n"
            ),
        ),
    ],
)
@auth_cli.command(
    name="fix",
    short_help="Fix credentials file permissions.",
    help="Fix the permission of the existing credentials file",
)
def auth_fix() -> None:
    auth_controller = AuthController()
    auth_controller.fix()


# Replaced by anyscale logout
@auth_cli.command(
    name="remove", help="Remove the current credentials file", hidden=True
)
def auth_remove() -> None:
    auth_controller = AuthController()
    auth_controller.remove()
