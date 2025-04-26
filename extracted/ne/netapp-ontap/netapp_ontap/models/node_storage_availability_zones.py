r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NodeStorageAvailabilityZones", "NodeStorageAvailabilityZonesSchema"]
__pdoc__ = {
    "NodeStorageAvailabilityZonesSchema.resource": False,
    "NodeStorageAvailabilityZonesSchema.opts": False,
    "NodeStorageAvailabilityZones": False,
}


class NodeStorageAvailabilityZonesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NodeStorageAvailabilityZones object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the node_storage_availability_zones. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the storage availability zone.

Example: storage_availability_zone_1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the storage availability zone.

Example: 9b3ff559-3333-11ef-b420-005056ae6060 """

    @property
    def resource(self):
        return NodeStorageAvailabilityZones

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class NodeStorageAvailabilityZones(Resource):

    _schema = NodeStorageAvailabilityZonesSchema
