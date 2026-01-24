import json

from nexuscli.cli import util
from nexuscli.nexus_client import NexusClient


def cmd_activate(nexus_client: NexusClient, realm_id: str) -> None:
    """Performs `nexus3 security realm activate`"""
    nexus_client.security_realms.activate(realm_id)


def cmd_active(nexus_client: NexusClient) -> None:
    """Performs `nexus3 security realm active`"""
    active_realms = nexus_client.security_realms.active

    print(json.dumps(active_realms))


def cmd_available(nexus_client: NexusClient, **kwargs) -> None:
    """Performs `nexus3 security realm available`"""
    raw_realms = nexus_client.security_realms.list

    if kwargs.get('json'):
        print(json.dumps(raw_realms))
    else:
        util.print_as_table(raw_realms, ['id', 'name'])
