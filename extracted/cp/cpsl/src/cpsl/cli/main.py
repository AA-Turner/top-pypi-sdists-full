import os

os.environ.setdefault("GRPC_VERBOSITY", "ERROR")

import click

from .create import create
from .login import login
from .app import app
from .channel import channel
from .deploy import deploy
from .secret import secret
from .serve import serve
from .fs import fs


@click.group()
def cli():
    """Capsule CLI — create and manage capsule apps."""
    pass


cli.add_command(create)
cli.add_command(login)
cli.add_command(app)
cli.add_command(channel)
cli.add_command(deploy)
cli.add_command(secret)
cli.add_command(serve)
cli.add_command(fs)


def start():
    cli()
