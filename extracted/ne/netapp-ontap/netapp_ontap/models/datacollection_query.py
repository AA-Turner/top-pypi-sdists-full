r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DatacollectionQuery", "DatacollectionQuerySchema"]
__pdoc__ = {
    "DatacollectionQuerySchema.resource": False,
    "DatacollectionQuerySchema.opts": False,
    "DatacollectionQuery": False,
}

class DatacollectionQuerySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DatacollectionQuery object"""

    expression = marshmallow_fields.Str(data_key="expression", allow_none=True)
    r""" The query expression for the selector.

Example: {'type': 'pdf'} """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the query.

Example: 123e4567-e89b-12d3-a456-426614174000 """

    @property
    def resource(self):
        return DatacollectionQuery

    gettable_fields = [
        "expression",
        "uuid",
    ]
    """expression,uuid,"""

    patchable_fields = [
        "expression",
        "uuid",
    ]
    """expression,uuid,"""

    postable_fields = [
        "expression",
        "uuid",
    ]
    """expression,uuid,"""


class DatacollectionQuery(Resource):

    _schema = DatacollectionQuerySchema
