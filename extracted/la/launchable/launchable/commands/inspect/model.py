import json
import sys
from http import HTTPStatus

import click
from requests import Response
from tabulate import tabulate

from ...utils.launchable_client import LaunchableClient


@click.command()
@click.option(
    '--json',
    'is_json_format',
    help='display JSON format',
    is_flag=True
)
@click.pass_context
def model(context: click.core.Context, is_json_format: bool):
    client = LaunchableClient(app=context.obj)
    try:
        res: Response = client.request("get", "model-metadata")

        if res.status_code == HTTPStatus.NOT_FOUND:
            click.echo(click.style(
                "Model metadata currently not available for this workspace.", 'yellow'), err=True)
            sys.exit()

        res.raise_for_status()

        if is_json_format:
            display_as_json(res)
        else:
            display_as_table(res)

    except Exception as e:
        client.print_exception_and_recover(e, "Warning: failed to inspect model")


def display_as_json(res: Response):
    res_json = res.json()
    click.echo(json.dumps(res_json, indent=2))


def display_as_table(res: Response):
    headers = ["Metadata", "Value"]
    res_json = res.json()
    rows = [["Training Cutoff Test Session ID", res_json['training_cutoff_test_session_id']]]
    click.echo(tabulate(rows, headers, tablefmt="github"))
