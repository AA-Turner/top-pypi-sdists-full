import sys

import click

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


@click.group("user", cls=TectonGroup)
def user():
    """Manage users."""


@user.command("invite", help="Invite users to Tecton cluster")
@click.option("-u", "--user", default=None, help="User email")
@click.option("-f", "--file", default=None, help="File containing user emails, newline-separated", type=click.File("r"))
def invite(user, file):
    _process_user_action(user, file, _invite_user)


@user.command("delete", help="Delete users from Tecton cluster")
@click.option("-u", "--user", default=None, help="User email")
@click.option("-f", "--file", default=None, help="File containing user emails, newline-separated", type=click.File("r"))
def delete(user, file):
    _process_user_action(user, file, _delete_user)


def _process_user_action(user, file, handler):
    if file is not None:
        if user:
            msg = "Please use exactly one of --user or --file"
            raise click.BadArgumentUsage(msg)

        for u in [line.strip() for line in file.readlines() if len(line.strip()) > 0]:
            handler(u)
    elif user is not None:
        handler(user)
    else:
        msg = "Please submit one of --user or --file."
        raise click.BadArgumentUsage(msg)


def _invite_user(user_email: str) -> None:
    try:
        request = metadata_service_pb2.CreateClusterUserRequest(login_email=user_email)
        metadata_service.instance().CreateClusterUser(request)
    except Exception as e:
        printer.safe_print(f"Failed to invite [{user_email}]: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print(f"Successfully invited [{user_email}]")


def _delete_user(user_email: str) -> None:
    try:
        get_user_request = metadata_service_pb2.GetUserRequest(email=user_email)
        response = metadata_service.instance().GetUser(get_user_request)
        okta_id = response.user.okta_id

        delete_request = metadata_service_pb2.DeleteClusterUserRequest(okta_id=okta_id)
        metadata_service.instance().DeleteClusterUser(delete_request)
    except Exception as e:
        printer.safe_print(f"Failed to delete [{user_email}]: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print(f"Successfully deleted [{user_email}]")
