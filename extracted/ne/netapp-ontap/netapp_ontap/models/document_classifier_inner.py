r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DocumentClassifierInner", "DocumentClassifierInnerSchema"]
__pdoc__ = {
    "DocumentClassifierInnerSchema.resource": False,
    "DocumentClassifierInnerSchema.opts": False,
    "DocumentClassifierInner": False,
}

class DocumentClassifierInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DocumentClassifierInner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the document classifier.

Example: Invoice Document """

    tag = marshmallow_fields.Str(data_key="tag", allow_none=True)
    r""" Tag of the data classifier.

Example: CLS_DOC00000 """

    total_hits = Size(data_key="total_hits", allow_none=True)
    r""" Total number of hits for the document classifier.

Example: 1234567 """

    @property
    def resource(self):
        return DocumentClassifierInner

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


class DocumentClassifierInner(Resource):

    _schema = DocumentClassifierInnerSchema
