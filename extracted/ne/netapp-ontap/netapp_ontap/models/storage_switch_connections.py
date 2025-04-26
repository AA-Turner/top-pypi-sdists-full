r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchConnections", "StorageSwitchConnectionsSchema"]
__pdoc__ = {
    "StorageSwitchConnectionsSchema.resource": False,
    "StorageSwitchConnectionsSchema.opts": False,
    "StorageSwitchConnections": False,
}


class StorageSwitchConnectionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchConnections object"""

    peer_port = marshmallow_fields.Nested("netapp_ontap.models.storage_switch_connections_peer_port.StorageSwitchConnectionsPeerPortSchema", unknown=EXCLUDE, data_key="peer_port", allow_none=True)
    r""" The peer_port field of the storage_switch_connections. """

    source_port = marshmallow_fields.Nested("netapp_ontap.models.storage_switch_connections_source_port.StorageSwitchConnectionsSourcePortSchema", unknown=EXCLUDE, data_key="source_port", allow_none=True)
    r""" The source_port field of the storage_switch_connections. """

    @property
    def resource(self):
        return StorageSwitchConnections

    gettable_fields = [
        "peer_port",
        "source_port",
    ]
    """peer_port,source_port,"""

    patchable_fields = [
        "peer_port",
        "source_port",
    ]
    """peer_port,source_port,"""

    postable_fields = [
        "peer_port",
        "source_port",
    ]
    """peer_port,source_port,"""


class StorageSwitchConnections(Resource):

    _schema = StorageSwitchConnectionsSchema
