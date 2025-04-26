r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterPeerRemote", "ClusterPeerRemoteSchema"]
__pdoc__ = {
    "ClusterPeerRemoteSchema.resource": False,
    "ClusterPeerRemoteSchema.opts": False,
    "ClusterPeerRemote": False,
}


class ClusterPeerRemoteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterPeerRemote object"""

    ip_addresses = marshmallow_fields.List(marshmallow_fields.Str, data_key="ip_addresses", allow_none=True)
    r""" The IPv4 addresses, IPv6 addresses, or hostnames of the peers. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the remote cluster.

Example: cluster2 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" The serial number of the remote cluster.

Example: 4048820-60-9 """

    @property
    def resource(self):
        return ClusterPeerRemote

    gettable_fields = [
        "ip_addresses",
        "name",
        "serial_number",
    ]
    """ip_addresses,name,serial_number,"""

    patchable_fields = [
        "ip_addresses",
    ]
    """ip_addresses,"""

    postable_fields = [
        "ip_addresses",
    ]
    """ip_addresses,"""


class ClusterPeerRemote(Resource):

    _schema = ClusterPeerRemoteSchema
