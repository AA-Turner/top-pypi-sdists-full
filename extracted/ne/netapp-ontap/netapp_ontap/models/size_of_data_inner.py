r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SizeOfDataInner", "SizeOfDataInnerSchema"]
__pdoc__ = {
    "SizeOfDataInnerSchema.resource": False,
    "SizeOfDataInnerSchema.opts": False,
    "SizeOfDataInner": False,
}

class SizeOfDataInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SizeOfDataInner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the size category.

Example: 1KB <-> 1MB """

    order = Size(data_key="order", allow_none=True)
    r""" Order of the size category.

Example: 2 """

    total_hits = Size(data_key="total_hits", allow_none=True)
    r""" Total number of hits in this size category.

Example: 33403466 """

    @property
    def resource(self):
        return SizeOfDataInner

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


class SizeOfDataInner(Resource):

    _schema = SizeOfDataInnerSchema
