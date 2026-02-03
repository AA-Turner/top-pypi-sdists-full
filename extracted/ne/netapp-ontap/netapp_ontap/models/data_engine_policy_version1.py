r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEnginePolicyVersion1", "DataEnginePolicyVersion1Schema"]
__pdoc__ = {
    "DataEnginePolicyVersion1Schema.resource": False,
    "DataEnginePolicyVersion1Schema.opts": False,
    "DataEnginePolicyVersion1": False,
}

class DataEnginePolicyVersion1Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEnginePolicyVersion1 object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the version.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DataEnginePolicyVersion1

    gettable_fields = [
        "uuid",
    ]
    """uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class DataEnginePolicyVersion1(Resource):

    _schema = DataEnginePolicyVersion1Schema
