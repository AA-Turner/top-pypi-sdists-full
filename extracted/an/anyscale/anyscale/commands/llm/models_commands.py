from typing import Optional

import click

from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand
from anyscale.controllers.llm.models_controller import ModelsController
from anyscale.util import validate_non_negative_arg


@click.group("model", help="Finetuned models stored on your Anyscale cloud.")
def models_cli():
    pass


@models_cli.command(
    name="get",
    short_help="Retrieves information for a model in your Anyscale cloud.",
    cls=AnyscaleCommand,
    is_alpha=True,
    example=command_examples.LLM_MODELS_GET_EXAMPLE,
)
@click.option(
    "--model-id",
    required=False,
    type=str,
    default=None,
    help="ID for the model of interest",
)
@click.option(
    "--job-id",
    required=False,
    type=str,
    default=None,
    help="ID for the Anyscale job corresponding to the fine-tuning run",
)
def get_model(model_id: Optional[str], job_id: Optional[str]) -> None:
    """
    Gets the model card for the given model ID or corresponding job ID.

    Example usage:

        anyscale llm model get --model-id my-model-id

        anyscale llm model get --job-id job_123
    """
    ModelsController().get_model(model_id=model_id, job_id=job_id)


@models_cli.command(
    name="delete",
    short_help="Delete a fine-tuned model in your Anyscale cloud.",
    cls=AnyscaleCommand,
    is_alpha=True,
    example=command_examples.LLM_MODELS_DELETE_EXAMPLE,
)
@click.argument("model_id", required=True)
def delete_model(model_id: str) -> None:
    """
    Deletes the model for the given model ID. Requires owner permission for the corresponding Anyscale project.

    MODEL_ID = ID for the model of interest

    Example usage:

        anyscale llm model delete my-model-id
    """
    ModelsController().delete_model(model_id)


@models_cli.command(
    name="list",
    short_help="Lists fine-tuned models available to the user.",
    cls=AnyscaleCommand,
    is_alpha=True,
    example=command_examples.LLM_MODELS_LIST_EXAMPLE,
)
@click.option(
    "--cloud-id",
    required=False,
    type=str,
    help="Cloud ID to filter by. If not specified, all models from all visible clouds (filtered optionally by `project_id`) are listed.",
)
@click.option(
    "--project-id",
    required=False,
    type=str,
    help="Project ID to filter by. If not specified, all the models from all visible projects (filtered optionally by `cloud_id`) are listed.",
)
@click.option(
    "--max-items",
    required=False,
    type=int,
    default=20,
    help="Maximum number of items to show in the list. By default, the 20 most recently created models are fetched.",
    callback=validate_non_negative_arg,
)
def list_models(cloud_id: Optional[str], project_id: Optional[str], max_items: int):
    """
    Lists fine-tuned models available to the user.

    By default, all models in all visible clouds under all visible projects to the user are listed. This is optionally filtered by `project_id` and/or `cloud_id`.

    Example usage:

        anyscale llm model list

        anyscale llm model list --max-items 50

        anyscale llm model list --cloud-id cld_123

        anyscale llm model list --project-id prj_123

        anyscale llm model list --cloud-id cld_123 --project-id prj_123


    NOTE:
    If you are running this from within an Anyscale workspace, and neither `cloud_id` nor `project_id` are provided, the cloud and project of the workspace will be used.
    """
    controller = ModelsController()
    controller.list_models(
        cloud_id=cloud_id, project_id=project_id, max_items=max_items
    )
