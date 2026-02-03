r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineAclUserOrGroup", "DataEngineAclUserOrGroupSchema"]
__pdoc__ = {
    "DataEngineAclUserOrGroupSchema.resource": False,
    "DataEngineAclUserOrGroupSchema.opts": False,
    "DataEngineAclUserOrGroup": False,
}

class DataEngineAclUserOrGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineAclUserOrGroup object"""

    allocation_time = ImpreciseDateTime(data_key="allocation_time", allow_none=True)
    r""" The time when the user or group is granted access to the workspace.

Example: 2025-06-04T19:00:00.000+0000 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the user or group.

Example: user1 """

    @property
    def resource(self):
        return DataEngineAclUserOrGroup

    gettable_fields = [
        "allocation_time",
        "name",
    ]
    """allocation_time,name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class DataEngineAclUserOrGroup(Resource):

    _schema = DataEngineAclUserOrGroupSchema
