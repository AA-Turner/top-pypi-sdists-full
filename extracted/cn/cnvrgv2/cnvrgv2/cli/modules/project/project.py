import os

import click
from prettytable import PrettyTable

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.cli.utils.helpers import print_generator_in_chunks
from cnvrgv2.config import Config, CONFIG_FOLDER_NAME
from cnvrgv2.config import error_messages
from cnvrgv2.utils.storage_utils import cnvrgignore_exists, create_cnvrgignore
from cnvrgv2.modules.labels.utils import LabelKind


@click.group(name='project')
def project_group():
    pass


@project_group.command()
@click.option('-n', '--name', prompt=messages.PROJECT_PROMPT_CREATE, help=messages.PROJECT_HELP_CREATE)
@prepare_command()
def create(cnvrg, logger, name):
    """
    Creates a new project, and associates the current folder with the created project.
    It is recommended to create a new project in an empty folder.
    To create a project from a folder that contains content please refer to project link command.
    """
    if os.listdir():
        click.confirm(messages.PROJECT_CREATE_FOLDER_NOT_EMPTY, default=False, abort=True)

    logger.log_and_echo(messages.PROJECT_CREATING_PROJECT.format(name))
    new_project = cnvrg.projects.create(name)

    new_project.local_commit = new_project.commit

    logger.log_and_echo(messages.PROJECT_CONFIGURING_FOLDER)
    new_project.save_config()

    logger.log_and_echo(messages.PROJECT_CREATE_SUCCESS.format(new_project.title))


@project_group.command()
@click.option('-n', '--name', prompt=messages.PROJECT_PROMPT_CLONE, help=messages.PROJECT_PROMPT_CLONE)
@click.option('-o', '--override', is_flag=True, default=False, help=messages.PROJECT_HELP_CLONE_OVERRIDE)
@click.option('-c', '--commit', prompt=messages.DATA_PROMPT_COMMIT, default="latest",
              help=messages.PROJECT_HELP_CLONE_COMMIT)
@click.option('-d', '--current_dir', help=messages.PROJECT_HELP_CURRENT_DIR, is_flag=True, default=False)
@prepare_command()
def clone(cnvrg, logger, name, override, commit, current_dir):
    """
    Clones the given project to local folder
    """
    project = cnvrg.projects.get(name)
    logger.info(messages.LOG_CLONING_PROJECT.format(name))
    config_path = project.slug + '/' + CONFIG_FOLDER_NAME
    if current_dir:
        config_path = CONFIG_FOLDER_NAME
    if os.path.exists(config_path) and not override:
        logger.log_and_echo(messages.PROJECT_CLONE_SKIP.format(name))
        return
    project.clone(progress_bar_enabled=True, override=override, commit=commit, current_dir=current_dir)
    success_message = messages.PROJECT_CLONE_SUCCESS.format(name)
    logger.log_and_echo(success_message)


@project_group.command(name='list-files')
@click.option('-n', '--name', prompt=messages.PROJECT_HELP_LIST_FILES, help=messages.PROJECT_HELP_LIST_FILES)
@click.option('-cs', '--chunk-size', default=20, help=messages.DATASET_LIST_FILES_HELP_CHUNK_SIZE)
@click.option('-l', '--limit', type=int, help=messages.DATASET_LIST_FILES_HELP_LIMIT)
@prepare_command()
def list_files(cnvrg, logger, name, chunk_size, limit):
    """
    List files within a project
    """
    project = cnvrg.projects.get(name)
    files = project.list_files()
    logger.info(messages.LOG_LIST_FILES_PROJECT.format(name))
    attributes_field_name = ["File Name", "File Size", "SHA1"]
    attributes = ["file_name", "file_size", "sha1"]
    print_generator_in_chunks(files, chunk_size, limit, attributes, attributes_field_name, line_numbers=True)


@project_group.command(name='list')
@prepare_command()
def list_command(cnvrg, logger):
    """
    list projects title
    """
    projects = cnvrg.projects.list()
    domain = cnvrg._context.domain
    organization = cnvrg._context.organization
    table = PrettyTable()
    table.field_names = ["Project Title", "Project Link", "Public"]
    table.align["Project Title"] = "l"
    table.align["Project Link"] = "l"
    table.align["Public"] = "l"
    for project in projects:
        url = "{0}/{1}/projects/{2}".format(domain, organization, project.slug)
        table.add_row([project.title, url, project.public])
    click.echo(table)


@project_group.command(name='labels')
@click.option('-n', '--name', prompt=messages.PROJECT_HELP_LABELS__NAME, help=messages.PROJECT_HELP_LABELS__NAME)
@prepare_command()
def labels_command(cnvrg, logger, name):
    """
    List labels within a project
    """
    project = cnvrg.projects.get(name)
    labels = project.labels.list()
    logger.info(messages.LOG_LIST_LABELS_PROJECT.format(name))
    attributes_field_name = ["Name", "Color Name"]
    attributes = ["name", "color_name"]
    print_generator_in_chunks(labels, 20, 10, attributes, attributes_field_name, line_numbers=True)


@project_group.command(name='add-label')
@click.option('-n', '--name', prompt=messages.PROJECT_HELP_LABELS__NAME, help=messages.PROJECT_HELP_LABELS__NAME)
@click.option('-ln', '--label-name', prompt=messages.PROJECT_HELP_LABELS__LABEL_NAME,
              help=messages.PROJECT_HELP_LABELS__LABEL_NAME)
@prepare_command()
def add_label_command(cnvrg, logger, name, label_name):
    """
    Add label to project
    """
    project = cnvrg.projects.get(name)
    label = cnvrg.labels.get(label_name, LabelKind.PROJECT)
    project.labels.add(label)
    success_message = messages.PROJECT_ADD_LABEL_SUCCESS.format(label_name, name)
    logger.log_and_echo(success_message)


@project_group.command(name='remove-label')
@click.option('-n', '--name', prompt=messages.PROJECT_HELP_LABELS__NAME, help=messages.PROJECT_HELP_LABELS__NAME)
@prepare_command()
def remove_label_command(cnvrg, logger, name):
    """
    Remove label from a project
    """
    project = cnvrg.projects.get(name)
    project.labels.remove()
    success_message = messages.PROJECT_REMOVE_LABEL_SUCCESS.format(name)
    logger.log_and_echo(success_message)


@project_group.command()
@click.option('-n', '--name', prompt=messages.PROJECT_PROMPT_DELETE, help=messages.PROJECT_HELP_DELETE)
@prepare_command()
def delete(cnvrg, logger, name):
    """
    Deletes the current project
    """
    click.confirm(messages.PROJECT_DELETE_CONFIRM.format(name), default=False, abort=True)
    cnvrg.projects.delete([name])
    success_message = messages.PROJECT_DELETE_SUCCESS.format(name)
    logger.log_and_echo(success_message)


@project_group.command()
@click.option('-g', '--git-diff', is_flag=True, help=messages.DATA_UPLOAD_HELP_GIT_DIFF)
@prepare_command()
def upload(project, logger, git_diff):
    """
    Uploads updated files from the current project folder
    """
    project.upload(progress_bar_enabled=True, git_diff=git_diff)
    logger.log_and_echo(messages.DATA_UPLOAD_SUCCESS)


@project_group.command()
@prepare_command()
def download(project, logger):
    """
    Downloads updated files to the current project folder
    """
    project.download(progress_bar_enabled=True)
    logger.log_and_echo(messages.DATA_DOWNLOAD_SUCCESS)


@project_group.command()
@click.option('-n', '--name', prompt=messages.PROJECT_LINK_PROMPT_NAME, help=messages.PROJECT_LINK_HELP_NAME)
@prepare_command()
def link(cnvrg, logger, name):
    """
    Links the current directory with a new project.
    This command will create a new project and upload the current folder content to the newly created project.
    """
    curr_dir_project_name = Config().data_owner_slug
    if curr_dir_project_name:
        error_message = error_messages.DIRECTORY_ALREADY_LINKED.format(curr_dir_project_name)
        logger.log_and_echo(error_message, error=True)

    logger.log_and_echo(messages.PROJECT_CREATE_NEW.format(name))
    new_project = cnvrg.projects.create(name=name)
    new_project.local_commit = new_project.commit

    logger.log_and_echo(messages.PROJECT_CONFIGURING_FOLDER)
    new_project.save_config()

    logger.log_and_echo(messages.PROJECT_UPLOAD)
    new_project.upload(progress_bar_enabled=True)

    success_message = messages.PROJECT_LINK_SUCCESS.format(new_project.title)
    logger.log_and_echo(success_message)


@project_group.command()
@click.option('-n', '--name', prompt=messages.PROJECT_LINK_GIT_PROMPT_NAME, help=messages.PROJECT_LINK_GIT_HELP_NAME)
@click.option('-s', '--soft', is_flag=True, help=messages.SOFT_LINK_GIT_PROJECT)
@prepare_command()
def link_git(cnvrg, logger, name, soft):
    """
     Links the current directory, which is expected to be a git directory, with an existing cnvrg project
     that is configured to be a git project.
    """
    git_proj = cnvrg.projects.get(name)
    if not git_proj:
        project_not_exist_error = error_messages.PROJECT_NOT_EXIST.format(name)
        logger.log_and_echo(project_not_exist_error, error=True)

    if not git_proj.git:
        error_message = error_messages.NOT_A_GIT_PROJECT.format(git_proj.title)
        logger.log_and_echo(error_message, error=True)

    if soft and os.path.exists(CONFIG_FOLDER_NAME):
        logger.log_and_echo(messages.PROJECT_GIT_LINK_SKIP.format(git_proj.title))
        return

    logger.log_and_echo(messages.PROJECT_CONFIGURING_FOLDER)
    git_proj.local_commit = git_proj.commit
    git_proj.save_config()

    if not cnvrgignore_exists(os.getcwd()):
        create_cnvrgignore(os.getcwd())

    output_folder = os.environ.get('CNVRG_OUTPUT_DIR')
    if output_folder and not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    success_message = messages.PROJECT_LINK_SUCCESS.format(git_proj.title)
    logger.log_and_echo(success_message)


@project_group.command()
@click.option('-j', '--job-slug', default=None, help=messages.PROJECT_JOB_SLUG_HELP_NAME)
@click.option('-g', '--git-diff', is_flag=True, default=None, help=messages.DATA_UPLOAD_HELP_GIT_DIFF)
@click.option('-m', '--message', default="", help=messages.DATA_COMMIT_MESSAGE)
@click.option('-o', '--output-dir', default=None, help=messages.SYNC_OUTPUT_DIR)
@click.option('-d', '--debug-mode', is_flag=True, default=False, help=messages.DEBUG_MODE_HELP)
@prepare_command()
def sync(project, logger, message, job_slug=None, git_diff=None, output_dir=None, debug_mode=None):
    """
    Sync local project to remote
    """
    logger.log_and_echo('Syncing Project')

    # store the last commit before syncing
    start_commit = project.last_commit
    commit_sha1, changes = project.sync_from_cli_in_job_context(job_slug=job_slug, git_diff=git_diff,
                                                                progress_bar_enabled=True, message=message,
                                                                output_dir=output_dir, debug_mode=debug_mode)
    # if the last commit is the same as the start commit before syncing, the project is up to date
    if changes is True:
        logger.log_and_echo(messages.PROJECT_SYNC_SUCCESS.format(project.slug, commit_sha1))
    elif changes is False:
        logger.log_and_echo(messages.PROJECT_IS_UP_TO_DATE.format(project.slug))
    elif changes is None:
        if commit_sha1 is None or commit_sha1 == start_commit:
            logger.log_and_echo(messages.PROJECT_IS_UP_TO_DATE.format(project.slug))
        else:
            logger.log_and_echo(messages.PROJECT_SYNC_SUCCESS.format(project.slug, commit_sha1))


@project_group.command()
@click.option('-n', '--name', prompt=messages.PROJECT_PROMPT_NAME, help=messages.PROJECT_HELP_NAME)
@click.option('-f', '--files', prompt=messages.DATASET_PUT_PROMPT_FILES, help=messages.DATASET_PUT_HELP_FILES)
@click.option('-fc', '--force', is_flag=True, help=messages.DATA_UPLOAD_HELP_FORCE)
@click.option('-or', '--override', is_flag=True, help=messages.DATA_UPLOAD_HELP_OVERRIDE)
@click.option('-gd', '--git-diff', is_flag=True, help=messages.DATA_UPLOAD_HELP_GIT_DIFF)
@click.option('-d', '--dir', default="", help=messages.DATA_LOCATION_IN_STORAGE)
@prepare_command()
def put(cnvrg, logger, name, files, force, override, git_diff, dir):
    """
    Uploads the given files to the given project
    """
    file_paths = files.split(",")
    project = cnvrg.projects.get(name)
    sha1 = project.put_files(
        paths=file_paths,
        progress_bar_enabled=True,
        git_diff=git_diff,
        force=force,
        override=override,
        dir_path=dir
    )
    logger.log_and_echo("\n" + messages.FILES_UPLOAD_SUCCESS)
    logger.log_and_echo(messages.COMMIT_SHA1_MESSAGE.format(sha1))


@project_group.command()
@click.option('-n', '--name', prompt=messages.PROJECT_PROMPT_NAME, help=messages.PROJECT_HELP_DELETE)
@click.option('-f', '--files', prompt=messages.DATASET_REMOVE_PROMPT_FILES, help=messages.DATASET_REMOVE_HELP_FILES)
@click.option('-m', '--message', help=messages.DATA_COMMIT_MESSAGE, default="")
@prepare_command()
def rm(cnvrg, logger, name, files, message):
    """
    Removes the given files remotely
    """
    file_paths = files.split(",")
    project = cnvrg.projects.get(name)
    removed_files_count = project.remove_files(paths=file_paths, message=message, progress_bar_enabled=True)
    str_count = str(removed_files_count)
    pluralize = "File{}".format('s'[:removed_files_count ^ 1])  # Pluralizes the word (File/Files)
    logger.log_and_echo("{} {} removed.".format(str_count, pluralize))
