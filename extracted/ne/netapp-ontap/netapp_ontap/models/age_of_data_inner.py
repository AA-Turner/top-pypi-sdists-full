r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["AgeOfDataInner", "AgeOfDataInnerSchema"]
__pdoc__ = {
    "AgeOfDataInnerSchema.resource": False,
    "AgeOfDataInnerSchema.opts": False,
    "AgeOfDataInner": False,
}

class AgeOfDataInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AgeOfDataInner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the age category.

Example: Past 1-3 years """

    order = Size(data_key="order", allow_none=True)
    r""" Order of the age category.

Example: 5 """

    total_hits = Size(data_key="total_hits", allow_none=True)
    r""" Total number of hits in this age category.

Example: 20779033 """

    @property
    def resource(self):
        return AgeOfDataInner

    gettable_fields = [
        "name",
        "order",
        "total_hits",
    ]
    """name,order,total_hits,"""

    patchable_fields = [
        "name",
        "order",
        "total_hits",
    ]
    """name,order,total_hits,"""

    postable_fields = [
        "name",
        "order",
        "total_hits",
    ]
    """name,order,total_hits,"""


class AgeOfDataInner(Resource):

    _schema = AgeOfDataInnerSchema
