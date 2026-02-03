r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataClassifierInner", "DataClassifierInnerSchema"]
__pdoc__ = {
    "DataClassifierInnerSchema.resource": False,
    "DataClassifierInnerSchema.opts": False,
    "DataClassifierInner": False,
}

class DataClassifierInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataClassifierInner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the data classifier.

Example: Contract Data """

    tag = marshmallow_fields.Str(data_key="tag", allow_none=True)
    r""" Tag of the data classifier.

Example: CLS_DATA00001 """

    total_hits = Size(data_key="total_hits", allow_none=True)
    r""" Total number of hits for the data classifier.

Example: 876543 """

    @property
    def resource(self):
        return DataClassifierInner

    gettable_fields = [
        "name",
        "tag",
        "total_hits",
    ]
    """name,tag,total_hits,"""

    patchable_fields = [
        "name",
        "tag",
        "total_hits",
    ]
    """name,tag,total_hits,"""

    postable_fields = [
        "name",
        "tag",
        "total_hits",
    ]
    """name,tag,total_hits,"""


class DataClassifierInner(Resource):

    _schema = DataClassifierInnerSchema
