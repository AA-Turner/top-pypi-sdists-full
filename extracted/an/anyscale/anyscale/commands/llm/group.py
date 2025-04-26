import click

from anyscale.commands.llm.dataset_commands import dataset_cli
from anyscale.commands.llm.models_commands import models_cli


@click.group(
    "llm", help="Interact with Anyscale's LLM APIs.",
)
def llm_cli():
    pass


llm_cli.add_command(dataset_cli)
llm_cli.add_command(models_cli)
