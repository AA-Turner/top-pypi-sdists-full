from typing import Optional

import click

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand, LegacyAnyscaleCommand, NotRequiredIf
from anyscale.controllers.project_controller import ProjectController
from anyscale.project.models import (
    CreateProjectCollaborator,
    CreateProjectCollaborators,
)
from anyscale.project_utils import validate_project_name
from anyscale.util import validate_non_negative_arg


log = BlockLogger()


@click.group(
    "project",
    short_help="Manage projects on Anyscale.",
    help="Manages projects on Anyscale. A project can be used to organize a collection of jobs.",
)
def project_cli() -> None:
    pass


@project_cli.command(
    name="list",
    short_help="List projects for which you have access.",
    help="List projects for which you have access. By default, only projects created by you are listed.",
    cls=LegacyAnyscaleCommand,
    is_limited_support=True,
    legacy_prefix="anyscale project",
)
@click.option(
    "--name", "-n", help="List information for a particular project.", type=str
)
@click.option("--json", help="Format output as JSON.", is_flag=True)
@click.option(
    "--any-creator",
    "-a",
    help="[Deprecated] List projects created by any user.",
    is_flag=True,
    default=None,
    hidden=True,
)
@click.option("--created-by-me", help="List projects created by me only.", is_flag=True)
@click.option(
    "--max-items",
    required=False,
    default=20,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(  # noqa: A001
    name: str,
    json: bool,
    created_by_me: bool,
    any_creator: Optional[bool],
    max_items: int,
) -> None:
    if any_creator is not None:
        log.warning(
            "`--any-creator` and `-a` flags have been deprecated. "
            "`anyscale project list` now shows projects created by any user by default. "
            "If you would like to show projects created by you only, you can pass the --created-by-me flag"
        )
    project_controller = ProjectController()
    project_controller.list(name, json, created_by_me, max_items)


def _validate_project_name(ctx, param, value) -> str:  # noqa: ARG001
    if value and not validate_project_name(value):
        raise click.BadParameter(
            '"{}" contains spaces. Please enter a project name without spaces'.format(
                value
            )
        )

    return value


def _default_project_name() -> str:
    import os

    cur_dir = os.getcwd()
    return os.path.basename(cur_dir)


@click.command(
    name="init",
    help=(
        "[DEPRECATED] Create a new project or attach this directory to an existing project."
    ),
    hidden=True,
)
@click.option(
    "--project-id",
    help="Project id for an existing project you wish to attach to.",
    required=False,
    prompt=False,
)
@click.option(
    "--name",
    help="Project name.",
    cls=NotRequiredIf,
    not_required_if="project_id",
    callback=_validate_project_name,
    prompt=True,
    default=_default_project_name(),
)
@click.option(
    "--config",
    help="[DEPRECATED] Path to autoscaler yaml. Created by default.",
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--requirements",
    help="[DEPRECATED] Path to requirements.txt. Created by default.",
    required=False,
)
def anyscale_init(
    project_id: Optional[str],
    name: Optional[str],
    config: Optional[str],
    requirements: Optional[str],
) -> None:
    log.warning(
        "`anyscale init` has been deprecated. Please use `anyscale project init` "
        "to create or attach to a project from this directory."
    )
    if (project_id and name) or not (project_id or name):
        raise click.BadArgumentUsage(
            "Only one of project_id and name must be provided."
        )

    project_controller = ProjectController()
    project_controller.init(project_id, name, config, requirements)


@project_cli.command(
    name="init",
    help="[DEPRECATED] Create a new project or attach this directory to an existing project.",
    hidden=True,
)
@click.option(
    "--project-id",
    "--id",
    help="Project id for an existing project you wish to attach to.",
    required=False,
    prompt=False,
)
@click.option(
    "--name",
    "-n",
    help="Project name.",
    cls=NotRequiredIf,
    not_required_if="project_id",
    callback=_validate_project_name,
    prompt=True,
    default=_default_project_name(),
)
def init(project_id: Optional[str], name: Optional[str],) -> None:
    log.warning(
        "`anyscale project init` has been deprecated and will be removed in "
        "April 2022. Please use `anyscale project create` to create a new project "
        "and specify a project id or name for the other Anyscale CLI commands."
    )
    if (project_id and name) or not (project_id or name):
        raise click.BadArgumentUsage(
            "Only one of --project-id and --name must be provided."
        )

    project_controller = ProjectController()
    project_controller.init(project_id, name, None, None)


@project_cli.command(
    name="create",
    help="Create a new project.",
    cls=LegacyAnyscaleCommand,
    is_limited_support=True,
    legacy_prefix="anyscale project",
)
@click.option(
    "--name",
    "-n",
    help="Project name.",
    callback=_validate_project_name,
    prompt=True,
    default=_default_project_name(),
)
@click.option(
    "--parent-cloud-id",
    required=False,
    default=None,
    help=(
        "Cloud id that this project is associated with. This argument "
        "is only relevant if cloud isolation is enabled."
    ),
)
def create(name: str, parent_cloud_id: str) -> None:
    project_controller = ProjectController()
    project_controller.create(name, parent_cloud_id)


@project_cli.command(
    name="add-collaborators",
    help="Add collaborators to the project.",
    cls=AnyscaleCommand,
    example=command_examples.PROJECT_ADD_COLLABORATORS_EXAMPLE,
)
@click.option(
    "--cloud",
    "-c",
    help="Name of the cloud that the project belongs to.",
    required=True,
)
@click.option(
    "--project",
    "-p",
    help="Name of the project to add collaborators to.",
    required=True,
)
@click.option(
    "--users-file",
    help="Path to a YAML file containing a list of users to add to the project.",
    required=True,
)
def add_collaborators(cloud: str, project: str, users_file: str,) -> None:
    collaborators = CreateProjectCollaborators.from_yaml(users_file)

    try:
        anyscale.project.add_collaborators(
            cloud=cloud,
            project=project,
            collaborators=[
                CreateProjectCollaborator(**collaborator)
                for collaborator in collaborators.collaborators
            ],
        )
    except ValueError as e:
        log.error(f"Error adding collaborators to project: {e}")
        return

    log.info(
        f"Successfully added {len(collaborators.collaborators)} collaborators to project {project}."
    )
