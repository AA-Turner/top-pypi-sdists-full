r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsDomainDiscoveredServer", "CifsDomainDiscoveredServerSchema"]
__pdoc__ = {
    "CifsDomainDiscoveredServerSchema.resource": False,
    "CifsDomainDiscoveredServerSchema.opts": False,
    "CifsDomainDiscoveredServer": False,
}


class CifsDomainDiscoveredServerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsDomainDiscoveredServer object"""

    domain = marshmallow_fields.Str(data_key="domain", allow_none=True)
    r""" Fully Qualified Domain Name.


Example: test.com """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the cifs_domain_discovered_server. """

    preference = marshmallow_fields.Str(data_key="preference", allow_none=True)
    r""" Server Preference


Valid choices:

* unknown
* preferred
* favored
* adequate """

    server_ip = marshmallow_fields.Str(data_key="server_ip", allow_none=True)
    r""" Server IP address """

    server_name = marshmallow_fields.Str(data_key="server_name", allow_none=True)
    r""" Server Name """

    server_type = marshmallow_fields.Str(data_key="server_type", allow_none=True)
    r""" Server Type


Valid choices:

* unknown
* kerberos
* ms_ldap
* ms_dc
* ldap """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Server status


Valid choices:

* ok
* unavailable
* slow
* expired
* undetermined
* unreachable """

    @property
    def resource(self):
        return CifsDomainDiscoveredServer

    gettable_fields = [
        "domain",
        "node.links",
        "node.name",
        "node.uuid",
        "preference",
        "server_ip",
        "server_name",
        "server_type",
        "state",
    ]
    """domain,node.links,node.name,node.uuid,preference,server_ip,server_name,server_type,state,"""

    patchable_fields = [
        "domain",
        "node.name",
        "node.uuid",
        "preference",
        "server_ip",
        "server_name",
        "server_type",
        "state",
    ]
    """domain,node.name,node.uuid,preference,server_ip,server_name,server_type,state,"""

    postable_fields = [
        "domain",
        "node.name",
        "node.uuid",
        "preference",
        "server_ip",
        "server_name",
        "server_type",
        "state",
    ]
    """domain,node.name,node.uuid,preference,server_ip,server_name,server_type,state,"""


class CifsDomainDiscoveredServer(Resource):

    _schema = CifsDomainDiscoveredServerSchema
