r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsLunsCloneSource", "ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsLunsCloneSource": False,
}


class ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsLunsCloneSource object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the clone source LUN.
<personalities supports=unified>A LUN is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
LUN names are paths of the form "/vol/\<volume>[/\<qtree>]/\<namespace>" where the qtree name is optional.<br/>
Valid in POST and PATCH.</personalities>
<personalities supports=asar2>This property is not supported. Cloning is supported through the /api/storage/storage-units endpoint. See the [`POST /api/storage/storage-units`](#/SAN/storage_unit_create) to learn more about cloning LUNs.</personalities>


Example: /vol/volume1/lun1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the clone source LUN.
<personalities supports=unified>Valid in POST and PATCH.</personalities>
<personalities supports=asar2>This property is not supported. Cloning is supported through the /api/storage/storage-units endpoint. See the [`POST /api/storage/storage-units`](#/SAN/storage_unit_create) to learn more about cloning LUNs.</personalities>


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsLunsCloneSource

    gettable_fields = [
    ]
    """"""

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


class ConsistencyGroupConsistencyGroupsLunsCloneSource(Resource):

    _schema = ConsistencyGroupConsistencyGroupsLunsCloneSourceSchema
