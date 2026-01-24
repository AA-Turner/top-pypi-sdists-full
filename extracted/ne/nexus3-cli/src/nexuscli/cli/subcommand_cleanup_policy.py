import json
from texttable import Texttable

from nexuscli import exception
from nexuscli.nexus_client import NexusClient
from nexuscli.api import cleanup_policy
from nexuscli.cli import constants


def cmd_list(nexus_client: NexusClient) -> None:
    """Performs ``nexus3 cleanup_policy list``"""
    if len(nexus_client.cleanup_policies.list) == 0:
        return exception.CliReturnCode.POLICY_NOT_FOUND.value

    table = Texttable(max_width=constants.TTY_MAX_WIDTH)
    table.add_row(
        ['Name', 'Format', 'Downloaded', 'Updated', 'Regex'])
    table.set_deco(Texttable.HEADER)
    for policy in nexus_client.cleanup_policies.list:
        p = policy.configuration
        table.add_row([
            p['name'], p['format'],
            p['criteria'].get('lastDownloaded', 'null'),
            p['criteria'].get('lastBlobUpdated', 'null'),
            p['criteria'].get('regex', 'null')],
        )

    print(table.draw())
    return exception.CliReturnCode.SUCCESS.value


def cmd_create(nexus_client: NexusClient, **kwargs) -> None:
    """Performs ``nexus3 cleanup_policy create``"""
    policy = cleanup_policy.CleanupPolicy(None, **kwargs)
    nexus_client.cleanup_policies.create_or_update(policy)

    return exception.CliReturnCode.SUCCESS.value


def cmd_show(nexus_client: NexusClient, policy_name: str) -> None:
    """Performs ``nexus3 cleanup-policy show"""
    try:
        policy = nexus_client.cleanup_policies.get_by_name(policy_name)
    except exception.NexusClientInvalidRepository:
        print(f'Cleanup policy not found: {policy_name}')
        return exception.CliReturnCode.NOT_FOUND.value

    print(json.dumps(policy.configuration, indent=2))
    return exception.CliReturnCode.SUCCESS.value
