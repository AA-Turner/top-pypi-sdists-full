r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEnginePolicyConditions", "DataEnginePolicyConditionsSchema"]
__pdoc__ = {
    "DataEnginePolicyConditionsSchema.resource": False,
    "DataEnginePolicyConditionsSchema.opts": False,
    "DataEnginePolicyConditions": False,
}

class DataEnginePolicyConditionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEnginePolicyConditions object"""

    condition = marshmallow_fields.Str(data_key="condition", allow_none=True)
    r""" Valid JSON string that defines the condition under which the data engine policy is applied.

Example: {'type': 'pdf'} """

    @property
    def resource(self):
        return DataEnginePolicyConditions

    gettable_fields = [
        "condition",
    ]
    """condition,"""

    patchable_fields = [
        "condition",
    ]
    """condition,"""

    postable_fields = [
        "condition",
    ]
    """condition,"""


class DataEnginePolicyConditions(Resource):

    _schema = DataEnginePolicyConditionsSchema
