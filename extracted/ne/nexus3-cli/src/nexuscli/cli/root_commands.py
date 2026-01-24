"""Handles base/root commands (as opposed to subcommands)"""
import inflect
import sys

from nexuscli import exception, nexus_config, nexus_util
from nexuscli.nexus_client import NexusClient


PLURAL = inflect.engine().plural


def cmd_login(**kwargs):
    """Performs ``nexus3 login``"""
    config = nexus_config.NexusConfig(**kwargs)

    # make sure configuration works before saving
    try:
        NexusClient(config=config)
    except exception.NexusClientInvalidCredentials:
        # the regular message tells the user to try to login, which is what
        # they just did now, so override the msg
        raise exception.NexusClientInvalidCredentials('Invalid credentials')

    sys.stderr.write('\nLogin successful.\n')
    sys.stderr.write(f'Configuration saved to {config.dump()}, {config.dump_env()}\n')

    return exception.CliReturnCode.SUCCESS.value


def cmd_list(nexus_client, full_path):
    """Performs ``nexus3 list``"""
    # TODO: refactor the path handling
    repository_name, path_fragments = nexus_util.pop_repository(full_path)
    repository_path = nexus_util.REMOTE_PATH_SEPARATOR.join(path_fragments)
    repository = nexus_client.repositories.get_by_name(repository_name)

    artefact_list = repository.list(repository_path)
    for artefact in iter(artefact_list):
        print(artefact)
    return exception.CliReturnCode.SUCCESS.value


def _cmd_up_down_errors(count, action):
    """Print and exit with error if upload/download/delete didn't succeed"""
    if count == 0:
        # FIXME: inflex the action verb to past participle
        sys.stderr.write(f'WARNING: no files were {action}\'ed.')
        sys.exit(exception.CliReturnCode.NO_FILES.value)

    if count == -1:
        sys.stderr.write(f'ERROR during {action} operation.')
        sys.exit(exception.CliReturnCode.API_ERROR.value)


def cmd_upload(nexus_client, src=None, dst=None, flatten=None, recurse=None):
    """Performs ``nexus3 upload``"""
    sys.stderr.write(f'Uploading {src} to {dst}\n')

    # TODO: refactor the path handling
    repository_name, path_fragments = nexus_util.pop_repository(dst)
    dst_path = nexus_util.REMOTE_PATH_SEPARATOR.join(path_fragments)
    repository = nexus_client.repositories.get_by_name(repository_name)

    upload_count = repository.upload(src, dst_path, flatten=flatten, recurse=recurse)

    _cmd_up_down_errors(upload_count, 'upload')

    file = PLURAL('file', upload_count)
    sys.stderr.write(f'Uploaded {upload_count} {file} to {dst_path}\n')
    return exception.CliReturnCode.SUCCESS.value


def cmd_download(nexus_client, src=None, dst=None, flatten=None, cache=None):
    """Performs ``nexus3 download``"""
    sys.stderr.write(f'Downloading {src} to {dst}\n')

    # TODO: refactor the path handling
    repository_name, path_fragments = nexus_util.pop_repository(src)
    src_path = nexus_util.REMOTE_PATH_SEPARATOR.join(path_fragments)
    repository = nexus_client.repositories.get_by_name(repository_name)

    download_count = repository.download(src_path, dst, flatten=flatten, nocache=not cache)

    _cmd_up_down_errors(download_count, 'download')

    file_word = PLURAL('file', download_count)
    sys.stderr.write(
        f'Downloaded {download_count} {file_word} to {dst}\n')
    return exception.CliReturnCode.SUCCESS.value


def cmd_delete(nexus_client, repository_path):
    """Performs ``nexus3 delete``"""
    # TODO: refactor the path handling
    repository_name, path_fragments = nexus_util.pop_repository(repository_path)
    delete_path = nexus_util.REMOTE_PATH_SEPARATOR.join(path_fragments)
    repository = nexus_client.repositories.get_by_name(repository_name)

    delete_count = repository.delete(delete_path)

    _cmd_up_down_errors(delete_count, 'delete')

    file_word = PLURAL('file', delete_count)
    sys.stderr.write(f'Deleted {delete_count} {file_word}\n')
    return exception.CliReturnCode.SUCCESS.value
