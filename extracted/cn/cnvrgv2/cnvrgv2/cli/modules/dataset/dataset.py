import json
import os
import time
from datetime import datetime

import click
from prettytable import PrettyTable

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.cli.utils.helpers import print_generator_in_chunks
from cnvrgv2.config import Config
from cnvrgv2.config import CONFIG_FOLDER_NAME
from cnvrgv2.modules.dataset import Dataset
from cnvrgv2.modules.labels.utils import LabelKind


@click.group(name='dataset')
def dataset_group():
    pass


@dataset_group.command()
@click.option('-n', '--name', prompt=messages.DATASET_PROMPT_CLONE, help=messages.DATASET_HELP_CLONE)
@click.option('-o', '--override', is_flag=True, default=False, help=messages.DATASET_HELP_CLONE_OVERRIDE)
@click.option('-cl', '--cache_link', default=False, is_flag=True, required=False,
              help=messages.DATASET_HELP_CLONE_OVERRIDE)
@click.option('-c', '--commit', default=None, help=messages.DATASET_HELP_CLONE_COMMIT)
@click.option('-t', '--threads', default=40, type=int, help=messages.CLONE_NUMBER_OF_THREADS)
@click.option('-q', '--query', default=None, help=messages.QUERY_SLUG)
@prepare_command()
def clone(cnvrg, logger, name, override, cache_link, commit, threads, query):
    """
    Clones the given dataset to local folder
    """
    dataset = cnvrg.datasets.get(name)
    logger.info(messages.LOG_CLONING_DATASET.format(name))
    if os.path.exists(dataset.slug + '/' + CONFIG_FOLDER_NAME) and not override:
        logger.log_and_echo(messages.DATASET_CLONE_SKIP.format(name))
        return
    dataset.clone(progress_bar_enabled=True, override=override, commit=commit, use_cached=cache_link, threads=threads,
                  query_slug=query)
    success_message = messages.DATASET_CLONE_SUCCESS.format(name)
    logger.log_and_echo(success_message)


@dataset_group.command()
@click.option('-n', '--name', prompt=messages.DATASET_PROMPT_NAME, help=messages.DATASET_HELP_NAME)
@click.option('-f', '--files', prompt=messages.DATASET_PUT_PROMPT_FILES, help=messages.DATASET_PUT_HELP_FILES)
@click.option('-fc', '--force', is_flag=True, help=messages.DATA_UPLOAD_HELP_FORCE)
@click.option('-or', '--override', is_flag=True, help=messages.DATA_UPLOAD_HELP_OVERRIDE)
@click.option('-gd', '--git-diff', is_flag=True, help=messages.DATA_UPLOAD_HELP_GIT_DIFF)
@click.option('-d', '--dir', default="", help=messages.DATA_LOCATION_IN_STORAGE)
@click.option('-t', '--threads', default=40, type=int, help=messages.DATA_UPLOAD_HELP_THREADS)
@click.option('-c', '--chunks', default=1000, type=int, help=messages.DATA_UPLOAD_HELP_CHUNKS)
@prepare_command()
def put(cnvrg, logger, name, files, force, override, git_diff, threads, chunks, dir):
    """
    Uploads the given files to the given dataset
    """
    file_paths = files.split(",")
    dataset = cnvrg.datasets.get(name)
    dataset.put_files(
        paths=file_paths,
        progress_bar_enabled=True,
        git_diff=git_diff,
        force=force,
        override=override,
        threads=threads,
        chunks=chunks,
        dir_path=dir
    )
    logger.log_and_echo(messages.DATA_UPLOAD_SUCCESS)


@dataset_group.command()
@click.option('-g', '--git-diff', is_flag=True, help=messages.DATA_UPLOAD_HELP_GIT_DIFF)
@prepare_command()
def upload(dataset, logger, git_diff):
    """
    Uploads updated files from the current dataset folder
    """
    dataset.upload(progress_bar_enabled=True, git_diff=git_diff)
    logger.log_and_echo(messages.DATA_UPLOAD_SUCCESS)


@dataset_group.command()
@prepare_command()
def download(dataset, logger):
    """
    Downloads updated files to the current dataset folder
    """
    dataset.download(progress_bar_enabled=True)
    logger.log_and_echo(messages.DATA_DOWNLOAD_SUCCESS)


@dataset_group.command()
@click.option('-n', '--name', prompt=messages.DATASET_PROMPT_NAME, help=messages.DATASET_HELP_CLONE)
@click.option('-f', '--files', prompt=messages.DATASET_REMOVE_PROMPT_FILES, help=messages.DATASET_REMOVE_HELP_FILES)
@click.option('-m', '--message', help=messages.DATA_COMMIT_MESSAGE, default="")
@prepare_command()
def remove(cnvrg, logger, name, files, message):
    """
    Removes the given files remotely
    """
    file_paths = files.split(",")
    dataset = cnvrg.datasets.get(name)
    dataset.remove_files(paths=file_paths, message=message, progress_bar_enabled=True)
    logger.log_and_echo(messages.DATASET_REMOVE_SUCCESS)


@dataset_group.command()
@click.option('-n', '--name', prompt=messages.DATASET_PROMPT_DELETE, help=messages.DATASET_HELP_DELETE)
@prepare_command()
def delete(cnvrg, logger, name):
    """
    Deletes the dataset
    """
    click.confirm(messages.DATASET_DELETE_CONFIRM.format(name), default=False, abort=True)
    dataset = cnvrg.datasets.get(name)
    dataset.delete()
    success_message = messages.DATASET_DELETE_SUCCESS.format(name)
    logger.log_and_echo(success_message)


@dataset_group.command()
@click.option('-n', '--name', prompt=messages.DATASET_PROMPT_CREATE, help=messages.DATASET_HELP_CREATE)
@prepare_command()
def create(cnvrg, logger, name):
    """
    Creates a new dataset, and associates the current folder with the created project.
    It is recommended to create a new dataset in an empty folder.
    To create a dataset from a folder that contains content please refer to dataset link command.
    """
    if os.listdir():
        click.confirm(messages.DATASET_CREATE_FOLDER_NOT_EMPTY, default=False, abort=True)

    logger.log_and_echo(messages.DATASET_CREATING_MESSAGE)
    new_dataset = cnvrg.datasets.create(name)

    new_dataset.local_commit = new_dataset.last_commit

    logger.log_and_echo(messages.DATASET_CONFIGURING_FOLDER)
    new_dataset.save_config()
    logger.log_and_echo(messages.DATASET_CREATE_SUCCESS.format(name, new_dataset.slug))


@dataset_group.command(name='list-files')
@click.option('-n', '--name', prompt=messages.DATASET_HELP_LIST_FILES, help=messages.DATASET_HELP_LIST_FILES)
@click.option('-cs', '--chunk-size', default=20, help=messages.DATASET_LIST_FILES_HELP_CHUNK_SIZE)
@click.option('-l', '--limit', type=int, help=messages.DATASET_LIST_FILES_HELP_LIMIT)
@prepare_command()
def list_files_command(cnvrg, logger, name, chunk_size, limit):
    """
    List files within a dataset
    """
    dataset = cnvrg.datasets.get(name)
    files = dataset.list_files()
    logger.info(messages.LOG_LIST_FILES_DATASET.format(name))
    attributes_field_name = ["File Name", "File Size", "SHA1"]
    attributes = ["file_name", "file_size", "sha1"]
    print_generator_in_chunks(files, chunk_size, limit, attributes, attributes_field_name, line_numbers=True)


@dataset_group.command(name='list')
@prepare_command()
def list_command(cnvrg, logger):
    """
    list all datasets
    """
    datasets = cnvrg.datasets.list()
    domain = cnvrg._context.domain
    organization = cnvrg._context.organization
    table = PrettyTable()
    table.field_names = ["Dataset Title", "Dataset Link", "Public"]
    table.align["Dataset Title"] = "l"
    table.align["Dataset Link"] = "l"
    table.align["Public"] = "l"
    for dataset in datasets:
        url = "{0}/{1}/datasets/{2}".format(domain, organization, dataset.slug)
        table.add_row([dataset.title, url, dataset.is_public])
    click.echo(table)


@dataset_group.command(name='labels')
@click.option('-n', '--name', prompt=messages.DATASET_HELP_LABELS__NAME, help=messages.DATASET_HELP_LABELS__NAME)
@prepare_command()
def labels_command(cnvrg, logger, name):
    """
    List labels within a dataset
    """
    dataset = cnvrg.datasets.get(name)
    labels = dataset.labels.list()
    logger.info(messages.LOG_LIST_LABELS_DATASET.format(name))
    attributes_field_name = ["Name", "Color Name"]
    attributes = ["name", "color_name"]
    print_generator_in_chunks(labels, 20, 10, attributes, attributes_field_name, line_numbers=True)


@dataset_group.command(name='add-label')
@click.option('-n', '--name', prompt=messages.DATASET_HELP_LABELS__NAME, help=messages.DATASET_HELP_LABELS__NAME)
@click.option('-ln', '--label-name', prompt=messages.DATASET_HELP_LABELS__LABEL_NAME,
              help=messages.DATASET_HELP_LABELS__LABEL_NAME)
@prepare_command()
def add_label_command(cnvrg, logger, name, label_name):
    """
    Add label to dataset
    """
    dataset = cnvrg.datasets.get(name)
    label = cnvrg.labels.get(label_name, LabelKind.DATASET)
    dataset.labels.add(label)
    success_message = messages.DATASET_ADD_LABEL_SUCCESS.format(label_name, name)
    logger.log_and_echo(success_message)


@dataset_group.command(name='remove-label')
@click.option('-n', '--name', prompt=messages.DATASET_HELP_LABELS__NAME, help=messages.DATASET_HELP_LABELS__NAME)
@prepare_command()
def remove_label_command(cnvrg, logger, name):
    """
    Remove label from a dataset
    """
    dataset = cnvrg.datasets.get(name)
    dataset.labels.remove()
    success_message = messages.DATASET_REMOVE_LABEL_SUCCESS.format(name)
    logger.log_and_echo(success_message)


@dataset_group.command()
@click.option('-n', '--name', prompt=messages.DATASET_PROMPT_NAME, help=messages.DATASET_HELP_CACHE)
@click.option('-c', '--commit', prompt=messages.DATA_PROMPT_CACHE, default="latest", show_default=True,
              help=messages.DATASET_HELP_CACHE)
@click.option('-d', '--external-disk-title', prompt=messages.DATASET_PROMPT_DISK_NAME, help=messages.DATASET_HELP_CACHE)
@prepare_command()
def cache(cnvrg, logger, name, commit, external_disk_title):
    """
    Caches the current commit onto an external disk, for quick access
    """
    dataset = cnvrg.datasets.get(name)
    if commit.lower() == 'latest':
        commit = dataset.last_commit
    dataset_commit = dataset.get_commit(commit)
    dataset_commit.cache_commit(external_disk_title)
    logger.log_and_echo(messages.DATASET_CACHE_SUCCESS)


@dataset_group.command()
@click.option('-n', '--name', prompt=messages.DATASET_PROMPT_NAME, help=messages.DATASET_HELP_UNCACHE)
@click.option('-c', '--commit', prompt=messages.DATA_PROMPT_CACHE, default="latest", show_default=True,
              help=messages.DATASET_HELP_UNCACHE)
@click.option('-d', '--external-disk-title', prompt=messages.DATASET_PROMPT_DISK_NAME,
              help=messages.DATASET_HELP_UNCACHE)
@prepare_command()
def uncache(cnvrg, logger, name, commit, external_disk_title):
    """
    Removes the current cached commit from the external disk.
    """
    dataset = cnvrg.datasets.get(name)
    if commit.lower() == 'latest':
        commit = dataset.last_commit
    dataset_commit = dataset.get_commit(commit)
    dataset_commit.clear_cached_commit(external_disk_title)
    logger.log_and_echo(messages.DATASET_UNCACHE_SUCCESS)


@dataset_group.command()
@prepare_command()
def scan(logger):
    """
    Scan the current working directory and print the datasets found in it
    """
    logger.log_and_echo(messages.DATASET_SCAN_START)
    cwd = os.getcwd()
    try:
        datasets = []
        _, dirs, _ = next(os.walk(cwd))  # Direct children of cwd

        for curr_dir in dirs:
            os.chdir(os.path.join(cwd, curr_dir))
            config = Config()
            if config.local_config:
                datasets.append({
                    "dataset_slug": config.dataset_slug,
                    "local_commit": config.commit_sha1
                })

        if len(datasets) > 0:
            logger.log_and_echo(json.dumps(datasets))
        else:
            logger.log_and_echo(messages.DATASET_SCAN_NO_RESULTS)
    finally:
        os.chdir(cwd)


@dataset_group.command()
@click.option('-n', '--names', prompt=messages.DATASET_NAMES, help=messages.DATASET_NAMES_HELP)
@click.option('-t', '--time-out', help=messages.DATASET_VERIFY_TIMEOUT,
              required=False, default=None)
@prepare_command()
def verify(cnvrg, logger, names, time_out):
    """
    Scans datasets folders for given names and returns when all of them are successfully downloaded,
    returns status code 1 otherwise (in use for Agent)
    """
    datasets = names.split(",")
    start_time = datetime.now()
    all_ready = [False] * len(datasets)
    max_timeout = int(time_out) if time_out and time_out.isnumeric() else None

    while True:
        try:
            seconds_diff = (datetime.now() - start_time).total_seconds()
            if max_timeout:
                if seconds_diff >= max_timeout:
                    logger.log_and_echo(messages.DATASET_VERIFY_STATUS.format(all(all_ready)),
                                        error=False if all(all_ready) else True)
                    return
                else:
                    # For debugging purposes
                    logger.log_and_echo(str('%.1f' % (max_timeout - seconds_diff)) + " seconds until timeout")
            for i, dataset in enumerate(datasets):
                # For debugging purposes
                logger.log_and_echo("Verifying " + dataset)
                if Dataset(slug=dataset).verify():
                    all_ready[i] = True
            if all(all_ready):
                logger.log_and_echo(messages.DATASET_VERIFY_STATUS.format(True))
                return
            else:
                time.sleep(1)
        except FileNotFoundError:
            continue
    # return exit status 1 by passing error=True(in use for Agent)
    logger.log_and_echo(messages.DATASET_VERIFY_STATUS.format(False), error=True)
    return
