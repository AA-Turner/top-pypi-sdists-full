r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitMapsHostGroup", "StorageUnitMapsHostGroupSchema"]
__pdoc__ = {
    "StorageUnitMapsHostGroupSchema.resource": False,
    "StorageUnitMapsHostGroupSchema.opts": False,
    "StorageUnitMapsHostGroup": False,
}


class StorageUnitMapsHostGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitMapsHostGroup object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the mapped host group.


Example: host_group1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the mapped host group.


Example: 19f8d194-4d24-b1df-f3f7-e7aa68bc53db """

    @property
    def resource(self):
        return StorageUnitMapsHostGroup

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class StorageUnitMapsHostGroup(Resource):

    _schema = StorageUnitMapsHostGroupSchema
