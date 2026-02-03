r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEnginePolicyActions", "DataEnginePolicyActionsSchema"]
__pdoc__ = {
    "DataEnginePolicyActionsSchema.resource": False,
    "DataEnginePolicyActionsSchema.opts": False,
    "DataEnginePolicyActions": False,
}

class DataEnginePolicyActionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEnginePolicyActions object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether the action is enabled.

Example: true """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the name of the action to be performed by the data engine policy.

Example: classify_email """

    @property
    def resource(self):
        return DataEnginePolicyActions

    gettable_fields = [
        "enabled",
        "name",
    ]
    """enabled,name,"""

    patchable_fields = [
        "enabled",
        "name",
    ]
    """enabled,name,"""

    postable_fields = [
        "enabled",
        "name",
    ]
    """enabled,name,"""


class DataEnginePolicyActions(Resource):

    _schema = DataEnginePolicyActionsSchema
