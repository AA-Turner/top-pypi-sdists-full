import click

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.cli.utils.helpers import build_grid_url, callback_log, parse_parameters_from_file
from cnvrgv2.cli.utils.helpers import print_generator_in_chunks
from cnvrgv2.cli.utils.options import PythonLiteralOption
from cnvrgv2.modules.workflows.workflow_utils import WorkflowStatuses, WorkflowUtils


@click.group(name='experiment')
def experiment_group():
    pass


@experiment_group.command()
@click.option('-t', '--title', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-tm', '--templates', default=None, help=messages.EXPERIMENT_HELP_TEMPLATES)
@click.option('-l/-nl', '--local/--no-local', default=False, help=messages.EXPERIMENT_HELP_LOCAL)
@click.option('-c', '--command', prompt=messages.EXPERIMENT_PROMPT_COMMAND, help=messages.EXPERIMENT_HELP_COMMAND)
@click.option('-d', '--datasets', cls=PythonLiteralOption, default=[], help=messages.EXPERIMENT_HELP_DATASETS)
@click.option('-ds', '--datasources', cls=PythonLiteralOption, default=[], help=messages.EXPERIMENT_HELP_DATASOURCES)
@click.option('-v', '--volume', default=None, help=messages.EXPERIMENT_HELP_VOLUME)
@click.option('-sb/-nsb', '--sync-before/--no-sync-before', default=True, help=messages.EXPERIMENT_HELP_SYNC_BEFORE)
@click.option('-sa/-nsa', '--sync-after/--no-sync-after', default=True, help=messages.EXPERIMENT_HELP_SYNC_AFTER)
@click.option('-i', '--image', default=None, help=messages.EXPERIMENT_HELP_IMAGE)
@click.option('-gb', '--git-branch', default=None, help=messages.EXPERIMENT_HELP_GIT_BRANCH)
@click.option('-gc', '--git-commit', default=None, help=messages.EXPERIMENT_HELP_GIT_COMMIT)
@click.option('-od', '--output_dir', default=None, help=messages.EXPERIMENT_HELP_OUTPUT_DIR)
@click.option('-g', '--grid', default=None, help=messages.EXPERIMENT_HELP_GRID)
@click.option('-lf', '--local_folders', default=None, help=messages.EXPERIMENT_HELP_LOCAL_FOLDERS)
@click.option('-log', '--log', default=False, help=messages.EXPERIMENT_HELP_LOG)
@click.option('-w', '--wait', default=False, help=messages.EXPERIMENT_HELP_LOG)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def run(
        cnvrg,
        logger,
        project,
        title,
        templates,
        local,
        command,
        datasets,
        volume,
        sync_before,
        sync_after,
        output_dir,
        image,
        git_branch,
        git_commit,
        grid,
        local_folders,
        log,
        wait,
        project_slug,
        datasources
):
    """
      run an experiment
    """
    dataset_objects = []
    volume_object = None
    kwargs = {}
    templates_list = templates.split(",") if templates else None

    for dataset in datasets:
        if dataset.get("commit") and dataset.get("query"):
            logger.log_and_echo(messages.EXPERIMENT_DATASET_QUERY_ERROR_MESSAGE.format(dataset.get("slug")),
                                error=True)
            return
        ds = cnvrg.datasets.get(dataset.get("slug"))
        if dataset.get("commit"):
            ds.local_commit = dataset.get("commit")
        if dataset.get("query"):
            ds.query = dataset.get("query")
        dataset_objects.append(ds)

    if volume:
        volume_object = project.volumes.get(volume)

    if image:
        image_name, image_tag = image.split(":")
        kwargs["image"] = cnvrg.images.get(name=image_name, tag=image_tag)

    if git_branch:
        kwargs["git_branch"] = git_branch

    if git_commit:
        kwargs["git_commit"] = git_commit

    if output_dir:
        kwargs["output_dir"] = output_dir

    if local_folders:
        kwargs["local_folders"] = local_folders

    if grid:
        parsed_parameters = parse_parameters_from_file(grid)
        kwargs["parameters"] = parsed_parameters
        grid_slug = project.experiments.create_grid(
            title=title,
            templates=templates_list,
            command=command,
            datasets=dataset_objects,
            volume=volume_object,
            sync_before=sync_before,
            **kwargs
        )
        grid_url = build_grid_url(cnvrg, project, grid_slug)
        success_message = messages.EXPERIMENT_GRID_CREATE_SUCCESS.format(grid_slug, grid_url)
        logger.log_and_echo(success_message)
    else:
        experiment = project.experiments.create(
            title=title,
            templates=templates_list,
            local=local,
            command=command,
            datasets=dataset_objects,
            volume=volume_object,
            sync_before=sync_before,
            sync_after=sync_after,
            **kwargs
        )
        success_message = messages.EXPERIMENT_CREATE_SUCCESS.format(experiment.title, experiment.full_href)
        logger.log_and_echo(success_message)

        if log or wait:
            WorkflowUtils.wait_for_statuses(experiment, WorkflowStatuses.FINAL_STATES,
                                            callback=callback_log(experiment, log))


@experiment_group.command()
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-c', '--commit', prompt=messages.EXPERIMENT_PROMPT_COMMIT, default='latest', required=False,
              help=messages.EXPERIMENT_HELP_COMMIT)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def merge_to_master(logger, project, experiment, slug, commit, project_slug):
    # TODO: Slug is not necessary as a parameter (it is as an option, since prepare command uses it).
    #  Change prepare command to send only required arguments

    if project.git:
        logger.log_and_echo(messages.EXPERIMENT_GIT_ERROR_MESSAGE, error=True)
        return
    commit_param = None if commit == 'latest' else commit
    if experiment is None:
        logger.log_and_echo(messages.EXPERIMENT_DOES_NOT_EXIST, error=True)
    sha1 = experiment.merge_to_master(commit_param)
    logger.log_and_echo(messages.EXPERIMENT_MERGE_SUCCESS)
    logger.log_and_echo(messages.COMMIT_SHA1_MESSAGE.format(sha1))


@experiment_group.command()
@click.option('-k', '--key', help='')
@click.option('-v', '--value', help='')
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def log_param(experiment, logger, slug, key, value, project_slug):
    """
      logging a parameter of an experiment
    """
    if experiment is None:
        logger.log_and_echo(messages.EXPERIMENT_DOES_NOT_EXIST, error=True)
    experiment.log_param(key=key, value=value)
    logger.log_and_echo('{0}: {1} was logged'.format(key, value))


@experiment_group.command()
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-f', '--files', prompt=messages.DATASET_PUT_PROMPT_FILES, help=messages.DATASET_PUT_HELP_FILES)
@click.option('-g', '--git-diff', is_flag=True, default=None, help=messages.DATA_UPLOAD_HELP_GIT_DIFF)
@click.option('-d', '--work-dir', required=False, help=messages.EXPERIMENT_HELP_COMMIT)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def log_artifacts(cnvrg, logger, experiment, slug, files, git_diff, work_dir, project_slug):
    file_paths = files.split(",")
    if experiment is None:
        logger.log_and_echo(messages.EXPERIMENT_DOES_NOT_EXIST, error=True)
    experiment.log_artifacts(paths=file_paths, git_diff=git_diff, work_dir=work_dir)
    logger.log_and_echo(messages.EXPERIMENT_LOG_ARTIFACTS_SUCCESS)


@experiment_group.command()
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-f', '--files', prompt=messages.DATASET_PUT_PROMPT_FILES, help=messages.DATASET_PUT_HELP_FILES)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def log_images(cnvrg, logger, experiment, slug, files, project_slug):
    file_paths = files.split(",")
    if experiment is None:
        logger.log_and_echo(messages.EXPERIMENT_DOES_NOT_EXIST, error=True)
    experiment.log_images(file_paths=file_paths)
    logger.log_and_echo(messages.EXPERIMENT_LOG_IMAGES_SUCCESS)


@experiment_group.command()
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def start_tensorboard(experiment, logger, slug, project_slug):
    """
      start a tensorboard session for current experiment
    """
    if experiment is None:
        logger.log_and_echo(messages.EXPERIMENT_DOES_NOT_EXIST, error=True)
    experiment.start_tensorboard()
    logger.log_and_echo('tensorboard started!')


@experiment_group.command()
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def stop_tensorboard(experiment, logger, slug, project_slug):
    """
      stop a tensorboard session for current experiment
    """
    if experiment is None:
        logger.log_and_echo(messages.EXPERIMENT_DOES_NOT_EXIST, error=True)
    experiment.stop_tensorboard()
    logger.log_and_echo('tensorboard session stopped')


@experiment_group.command()
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-c', '--commit', prompt=messages.EXPERIMENT_ARTIFACTS_PROMPT_COMMIT, default='latest', required=False,
              help=messages.EXPERIMENT_ARTIFACTS_HELP_COMMIT)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def pull_artifacts(experiment, logger, slug, commit, project_slug):
    """
      pull artifacts
      default is experiment's last commit
    """
    if experiment is None:
        logger.log_and_echo(messages.EXPERIMENT_DOES_NOT_EXIST, error=True)
    commit_param = None if commit == 'latest' else commit
    experiment.pull_artifacts(commit_sha1=commit_param)
    logger.log_and_echo(messages.EXPERIMENT_PULL_ARTIFACTS_SUCCESS)


@experiment_group.command()
@click.option('-s', '--slug', default=None, help=messages.EXPERIMENT_HELP_TITLE)
@click.option('-d', '--delete_artifacts', default=False, help=messages.EXPERIMENT_DELETE_ARTIFACTS, required=False)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def delete(experiment, logger, slug, delete_artifacts, project_slug):
    """
      delete experiment by slug
    """
    if delete_artifacts:
        user_answer = click.confirm(messages.EXPERIMENT_DELETE_ARTIFACTS_PROMPT, abort=False)
        if not user_answer:
            logger.log_and_echo(messages.EXPERIMENT_DELETE_ARTIFACTS_ABORTED, error=True)
            return

    experiment.delete(delete_artifacts=delete_artifacts)
    logger.log_and_echo(messages.EXPERIMENT_DELETE_SUCCESS)


@experiment_group.command()
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@click.option('-cs', '--chunk-size', default=20, type=int, help='Number of experiments to display at a time')
@click.option('-l', '--limit', type=int, help='Maximum number of experiments to display')
@prepare_command()
def list(cnvrg, project_slug, chunk_size, limit):
    project = cnvrg.projects.get(project_slug)
    experiments = project.experiments.list()
    attributes_field_name = [
        "Experiment Name",
        "Created By",
        "Experiment Slug",
        "Experiment Command",
        "Image Used",
        "Experiment Status",
        "Compute"
    ]
    attributes = ["title", "username", "slug", "input", "image_name", "status", "compute_name"]
    print_generator_in_chunks(experiments, chunk_size, limit, attributes, attributes_field_name, line_numbers=True)
