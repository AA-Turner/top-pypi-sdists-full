import json
from texttable import Texttable

from nexuscli import exception
from nexuscli.cli import constants


def cmd_list(nexus_client):
    """Performs ``nexus3 repository list``"""
    repositories = nexus_client.repositories.raw_list()

    table = Texttable(max_width=constants.TTY_MAX_WIDTH)
    table.add_row(['Name', 'Format', 'Type', 'URL'])
    table.set_deco(Texttable.HEADER)
    for repo in repositories:
        table.add_row(
            [repo['name'], repo['format'], repo['type'], repo['url']])

    print(table.draw())
    return exception.CliReturnCode.SUCCESS.value


def cmd_create(ctx, repo_type=None, **kwargs):
    """Performs ``nexus3 repository create`` commands"""
    nexus_client = ctx.obj
    enable_health_check = kwargs.pop('health_check', False)

    r = nexus_client.repositories.new(repo_type, **kwargs)
    nexus_client.repositories.create(r)

    # only available for proxy repositories; relying on Click to not set this for hosted, group.
    if enable_health_check:
        nexus_client.repositories.set_health_check(r.name, True)

    return exception.CliReturnCode.SUCCESS.value


def cmd_delete(nexus_client, repository_name):
    """Performs ``nexus3 repository delete``"""
    nexus_client.repositories.delete(repository_name)
    return exception.CliReturnCode.SUCCESS.value


def cmd_show(nexus_client, repository_name):
    """Performs ``nexus3 repository show"""
    repo_name = repository_name
    try:
        configuration = nexus_client.repositories.get_raw_by_name(repo_name)
    except exception.NexusClientInvalidRepository:
        print(f'Repository not found: {repo_name}')
        return exception.CliReturnCode.REPOSITORY_NOT_FOUND.value

    print(json.dumps(configuration, indent=2))
    return exception.CliReturnCode.SUCCESS.value
