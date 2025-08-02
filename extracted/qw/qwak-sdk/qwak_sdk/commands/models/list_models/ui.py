import click
from _qwak_proto.qwak.models.models_pb2 import DeploymentModelStatus

from qwak_sdk.commands.models.list_models._logic import list_models as _list_models
from qwak_sdk.commands.ui_tools import output_as_json, output_as_table
from qwak_sdk.inner.tools.cli_tools import QwakCommand


def parse_model(model):
    return [
        model.model_id,
        model.uuid,
        model.display_name,
        model.model_description,
        model.project_id,
        model.created_by,
        model.created_at,
        model.last_modified_by,
        model.last_modified_at,
        model.model_status,
        "\n".join(
            [f"{branch.branch_name} {branch.branch_id}" for branch in model.branches]
        ),
        DeploymentModelStatus.DESCRIPTOR.values_by_number[
            model.deployment_model_status
        ].name,
    ]


@click.command("list-models", cls=QwakCommand)
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
def list_models(project_id, format, **kwargs):
    model_list_result = _list_models(project_id)
    columns = [
        "Model id",
        "Model UUID",
        "Model Name",
        "Model Description",
        "Project ID",
        "Created By",
        "Created At",
        "Last Modified At",
        "Last Modified By",
        "Model Status",
        "Branches",
        "Deployment Status",
    ]
    if format == "json":
        output_as_json(model_list_result)
    elif format == "text":
        output_as_table(model_list_result.models, parse_model, headers=columns)
