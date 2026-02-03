r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineEventAttributes", "DataEngineEventAttributesSchema"]
__pdoc__ = {
    "DataEngineEventAttributesSchema.resource": False,
    "DataEngineEventAttributesSchema.opts": False,
    "DataEngineEventAttributes": False,
}

class DataEngineEventAttributesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEventAttributes object"""

    key = marshmallow_fields.Str(data_key="key", allow_none=True)
    r""" The key of the attribute.

Example: attribute_key_1 """

    value = marshmallow_fields.Str(data_key="value", allow_none=True)
    r""" The value of the attribute.

Example: attribute_value_1 """

    @property
    def resource(self):
        return DataEngineEventAttributes

    gettable_fields = [
        "key",
        "value",
    ]
    """key,value,"""

    patchable_fields = [
        "key",
        "value",
    ]
    """key,value,"""

    postable_fields = [
        "key",
        "value",
    ]
    """key,value,"""


class DataEngineEventAttributes(Resource):

    _schema = DataEngineEventAttributesSchema
