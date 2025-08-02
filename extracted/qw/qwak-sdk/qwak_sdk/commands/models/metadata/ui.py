import re

import click
from google.protobuf.json_format import MessageToDict
from tabulate import tabulate

from qwak_sdk.commands.models.metadata._logic import (
    list_models_metadata as _list_models_metadata,
)
from qwak_sdk.commands.ui_tools import output_as_json
from qwak_sdk.inner.tools.cli_tools import QwakCommand


def print_text_data(metadata):
    def dict_to_table(data, prefix=""):
        headers = []
        values = []
        for key, value in data.items():
            key = re.sub(r"(\w)([A-Z])", r"\1 \2", key).lower()
            if isinstance(value, dict):
                headers.append(key.title())
                values.append(dict_to_table(value, prefix=key + ": "))
            elif isinstance(value, list):
                headers.append(key.title())
                values.append(
                    "\n".join(
                        [
                            dict_to_table(item, prefix=key + ": ")
                            for item in value
                            if isinstance(item, dict)
                        ]
                    )
                )
            else:
                headers.append((prefix + key).title())
                values.append(value)
        return tabulate([values], headers=headers)

    for model_metadata in metadata.model_metadata:
        print(dict_to_table(MessageToDict(model_metadata)))
        print("")


@click.command("metadata", cls=QwakCommand)
@click.option("--project-id", metavar="NAME", required=True, help="Project id")
@click.option(
    "--format",
    default="text",
    show_default=True,
    type=click.Choice(["text", "json"], case_sensitive=True),
    metavar="FORMAT",
    required=False,
    help="The formatting style for command output (choose from text, json)",
)
def list_models_metadata(project_id, format, **kwargs):
    model_list_result = _list_models_metadata(project_id)
    if format == "json":
        output_as_json(model_list_result)
    elif format == "text":
        print_text_data(model_list_result)
