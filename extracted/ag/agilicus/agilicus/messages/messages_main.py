import click

from ..input_helpers import EnumType
from ..output.table import output_entry

from agilicus.command_helpers import Command
from . import messages

cmd = Command()


@cmd.command(name="send-broadcast")
@click.option(
    "--user-org-id",
    multiple=True,
    type=(str, str),
    required=True,
    help="a user and org id",
)
@click.option("--expiry", type=click.DateTime(), required=True)
@click.option("--text", type=str, required=True)
@click.option("--title", type=str, required=True)
@click.option("--icon-url", type=str)
@click.option("--link", type=str)
@click.option("--campaign_id", type=str)
@click.option("--target", type=EnumType(messages.MessageTarget), required=True)
@click.option("--message-type", type=EnumType(messages.BroadcastType), required=True)
@click.option("--push-probability", type=float, default=None)
@click.pass_context
def cli_command_send_broadcast(ctx, **kwargs):
    """
    Sends a broadcast message to some number of users, identified by
    space-delimeted user and org-id pairs (e.g. `--user-org-id user1 org1
    --user-org-id user2 org2`). This message persists in the users' inboxes
    until it expires. A campaign ID can be used to uniquely tie together sets
    of messages sent over a period of time. The message-type helps to identify
    to client software how to interpret and display the message. Target chooses
    which client software will display the message.
    """
    output_entry(
        ctx, messages.send_broadcast_from_cli(ctx, **kwargs).sent_messages[0].to_dict()
    )


def add_commands(cli):
    cmd.add_to_cli(cli)
