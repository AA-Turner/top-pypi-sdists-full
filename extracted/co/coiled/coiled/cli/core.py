import click

from ..compatibility import COILED_VERSION
from .batch import batch_group
from .cluster import better_logs, cluster
from .config import config
from .curl import curl
from .diagnostics import diagnostics
from .env import env
from .hello import hello
from .login import login
from .notebook import notebook_group
from .package_sync import package_sync
from .prefect import prefect
from .run import run
from .setup import setup

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(COILED_VERSION, message="%(version)s")
def cli():
    """Coiled command line tool"""
    pass


cli.add_command(login)
cli.add_command(env)
cli.add_command(diagnostics)
cli.add_command(setup)
cli.add_command(cluster)
cli.add_command(notebook_group)
cli.add_command(package_sync)
cli.add_command(prefect)
cli.add_command(curl)
cli.add_command(config)
cli.add_command(run)
cli.add_command(batch_group)
cli.add_command(better_logs, "logs")
cli.add_command(hello)
cli.add_command(hello, "quickstart")
