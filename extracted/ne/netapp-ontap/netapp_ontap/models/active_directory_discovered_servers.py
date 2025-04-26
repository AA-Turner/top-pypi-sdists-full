r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ActiveDirectoryDiscoveredServers", "ActiveDirectoryDiscoveredServersSchema"]
__pdoc__ = {
    "ActiveDirectoryDiscoveredServersSchema.resource": False,
    "ActiveDirectoryDiscoveredServersSchema.opts": False,
    "ActiveDirectoryDiscoveredServers": False,
}


class ActiveDirectoryDiscoveredServersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ActiveDirectoryDiscoveredServers object"""

    domain = marshmallow_fields.Str(data_key="domain", allow_none=True)
    r""" The Active Directory domain that the discovered server is a member of.

Example: server1.com """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the active_directory_discovered_servers. """

    preference = marshmallow_fields.Str(data_key="preference", allow_none=True)
    r""" The preference level of the server that was discovered.

Valid choices:

* unknown
* preferred
* favored
* adequate """

    server = marshmallow_fields.Nested("netapp_ontap.models.active_directory_discovered_server.ActiveDirectoryDiscoveredServerSchema", unknown=EXCLUDE, data_key="server", allow_none=True)
    r""" The server field of the active_directory_discovered_servers. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The status of the connection to the server that was discovered.

Valid choices:

* ok
* unavailable
* slow
* expired
* undetermined
* unreachable """

    @property
    def resource(self):
        return ActiveDirectoryDiscoveredServers

    gettable_fields = [
        "domain",
        "node.links",
        "node.name",
        "node.uuid",
        "preference",
        "server.ip",
        "server.name",
        "server.type",
        "state",
    ]
    """domain,node.links,node.name,node.uuid,preference,server.ip,server.name,server.type,state,"""

    patchable_fields = [
        "domain",
        "node.name",
        "node.uuid",
        "preference",
        "server.ip",
        "server.name",
        "server.type",
        "state",
    ]
    """domain,node.name,node.uuid,preference,server.ip,server.name,server.type,state,"""

    postable_fields = [
        "domain",
        "node.name",
        "node.uuid",
        "preference",
        "server.ip",
        "server.name",
        "server.type",
        "state",
    ]
    """domain,node.name,node.uuid,preference,server.ip,server.name,server.type,state,"""


class ActiveDirectoryDiscoveredServers(Resource):

    _schema = ActiveDirectoryDiscoveredServersSchema
