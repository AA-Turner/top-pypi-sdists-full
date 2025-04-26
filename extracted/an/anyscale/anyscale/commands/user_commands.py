import click

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand
from anyscale.user.models import AdminCreateUser, AdminCreateUsers


log = BlockLogger()  # CLI Logger


@click.group("user", help="Manage users.")
def user_cli() -> None:
    pass


@user_cli.command(
    name="batch-create",
    cls=AnyscaleCommand,
    example=command_examples.USER_BATCH_CREATE_EXAMPLE,
)
@click.option(
    "--users-file",
    "-f",
    required=True,
    type=str,
    help="Path to a YAML file that contains the information for user accounts to be created.",
)
def admin_batch_create(users_file: str,) -> None:
    """
    Batch create, as an admin, users without email verification.
    """
    log.info("Creating users...")

    create_users = AdminCreateUsers.from_yaml(users_file)

    try:
        created_users = anyscale.user.admin_batch_create(
            admin_create_users=[
                AdminCreateUser(**create_user)
                for create_user in create_users.create_users
            ]
        )
    except ValueError as e:
        log.error(f"Error creating users: {e}")
        return

    log.info(f"{len(created_users)} users created.")
