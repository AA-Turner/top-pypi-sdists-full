r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitConsistencyGroup", "StorageUnitConsistencyGroupSchema"]
__pdoc__ = {
    "StorageUnitConsistencyGroupSchema.resource": False,
    "StorageUnitConsistencyGroupSchema.opts": False,
    "StorageUnitConsistencyGroup": False,
}


class StorageUnitConsistencyGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitConsistencyGroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the storage_unit_consistency_group. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the consistency group.


Example: cg1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the consistency group.


Example: 4abc2317-4332-9d37-93a0-20bd29c22df0 """

    @property
    def resource(self):
        return StorageUnitConsistencyGroup

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class StorageUnitConsistencyGroup(Resource):

    _schema = StorageUnitConsistencyGroupSchema
