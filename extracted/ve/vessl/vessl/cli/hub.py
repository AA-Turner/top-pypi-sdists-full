import click

from vessl.cli._base import VesslGroup
from vessl.hub import list_hub_model_tasks
from vessl.util.echo import print_info
from vessl.util.prompt import prompt_choices


@click.command(name="hub", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command(
    name="list",
    login_required=False,
)
@click.option(
    "--type",
    "-t",
    "_type",
    help="Filter by hub type. service or run.",
    default=None,
    )
def list_hub_templates(_type: str):
    
    tasks = list_hub_model_tasks(_type=_type)

    if not _type == "service":
        print_info("Run Tasks:")
        for task in tasks:
            if task.hub_type == "run":
                print_info(f"\t{task.key} ")
        print("\n")

    if not _type == "run":
        print_info("Service Tasks:")
        for task in tasks:
            if task.hub_type == "service":
                print_info(f"\t{task.key} ")


@cli.vessl_command(name="open")
@click.argument("key", type=str, default=None, required=False)
def open_task(key: str):
    if key is None:
        tasks = list_hub_model_tasks()
        selected = prompt_choices(
            "Select a task to open",
            [f"({task.hub_type})\t{task.key}" for task in tasks],
        )
        key = selected.split("\t")[1] 
    click.launch(f"https://app.vessl.ai/hub/{key}")
