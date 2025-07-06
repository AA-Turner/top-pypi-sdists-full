import click
from cnvrgv2.modules.workflows import NotebookType
from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command


@click.group(name='workspace')
def workspace_group():
    pass


@workspace_group.command()
@click.option('-t', '--title', default=None, help=messages.WORKSPACE_HELP_TITLE)
@click.option('-tm', '--templates', default=None, help=messages.WORKSPACE_HELP_TEMPLATES)
@click.option('-c', '--commit', default=None, help=messages.WORKSPACE_HELP_COMMIT)
@click.option('-nt', '--notebook_type', default=NotebookType.JUPYTER_LAB, help=messages.WORKSPACE_HELP_NOTEBOOK_TYPE)
@click.option('-d', '--datasets', default=None, help=messages.WORKSPACE_HELP_DATASETS)
@click.option('-ds', '--datasources', default=[], help=messages.WORKSPACE_HELP_DATASOURCE)
@click.option('-v', '--volume', default=None, help=messages.WORKSPACE_HELP_VOLUME)
@click.option('-i', '--image', default=None, help=messages.WORKSPACE_HELP_IMAGE)
@click.option('-gb', '--git-branch', default=None, help=messages.WORKSPACE_HELP_GIT_BRANCH)
@click.option('-gc', '--git-commit', default=None, help=messages.WORKSPACE_HELP_GIT_COMMIT)
@click.option('-lf', '--local_folders', default=None, help=messages.WORKSPACE_HELP_LOCAL_FOLDERS)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def create(cnvrg, project, logger, title, commit, templates, notebook_type, datasets, datasources, volume,
           image, git_branch, git_commit, local_folders, project_slug):
    """
      Create a workspace
    """
    dataset_objects = None
    volume_object = None
    kwargs = {}
    templates_list = templates.split(",") if templates else None

    if datasets:
        dataset_names = datasets.split(",")
        dataset_objects = [cnvrg.datasets.get(ds_name) for ds_name in dataset_names]

    if volume:
        volume_object = project.volumes.get(volume)

    if image:
        image_name, image_tag = image.split(":")
        kwargs["image"] = cnvrg.images.get(name=image_name, tag=image_tag)

    if git_branch:
        kwargs["git_branch"] = git_branch

    if git_commit:
        kwargs["git_commit"] = git_commit

    workspace = project.workspaces.create(
        title=title,
        templates=templates_list,
        notebook_type=notebook_type,
        datasets=dataset_objects,
        volume=volume_object,
        commit=commit,
        local_folders=local_folders,
        datasource_slugs=datasources,
        **kwargs
    )

    success_message = messages.WORKSPACE_CREATE_SUCCESS.format(workspace.title, workspace.full_href)
    logger.log_and_echo(success_message)


@workspace_group.command()
@click.option('-s', '--slug', default=None, help=messages.WORKSPACE_SLUG)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def start(workspace, logger, slug, project_slug):
    """
      starts the current workspace
    """
    if workspace is None:
        logger.log_and_echo(messages.WORKSPACE_DOES_NOT_EXIST, error=True)

    workspace.start()
    logger.log_and_echo('Workflow {} started!'.format(slug))


@workspace_group.command()
@click.option('-s', '--slug', default=None, help=messages.WORKSPACE_SLUG)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def sync_remote(workspace, logger, slug, project_slug):
    """
      sync the current workspace
    """
    if workspace is None:
        logger.log_and_echo(messages.WORKSPACE_DOES_NOT_EXIST, error=True)

    workspace.sync_remote()
    logger.log_and_echo('Workflow {} sync has been sent'.format(slug))


@workspace_group.command()
@click.option('-s', '--slug', default=None, help=messages.WORKSPACE_SLUG)
@click.option('-sy', '--sync', default=True, help=messages.WORKSPACE_HELP_SYNC_REMOTE)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def stop(workspace, logger, slug, sync, project_slug):
    """
      stop the current workspace
    """
    if workspace is None:
        logger.log_and_echo(messages.WORKSPACE_DOES_NOT_EXIST, error=True)

    workspace.stop(sync=sync)
    logger.log_and_echo('Workspace {} stopped!'.format(slug))


@workspace_group.command()
@click.option('-s', '--slug', default=None, help=messages.WORKSPACE_SLUG)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def start_tensorboard(workspace, logger, slug, project_slug):
    """
      starts tensorboard associated with the current workspace
    """
    if workspace is None:
        logger.log_and_echo(messages.WORKSPACE_DOES_NOT_EXIST, error=True)

    workspace.start_tensorboard()
    logger.log_and_echo('tensorboard started!')


@workspace_group.command()
@click.option('-s', '--slug', default=None, help=messages.WORKSPACE_SLUG)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def stop_tensorboard(workspace, logger, slug, project_slug):
    """
      stops tensorboard associated with the current workspace
    """
    if workspace is None:
        logger.log_and_echo(messages.WORKSPACE_DOES_NOT_EXIST, error=True)

    workspace.stop_tensorboard()
    logger.log_and_echo('tensorboard session stopped')
