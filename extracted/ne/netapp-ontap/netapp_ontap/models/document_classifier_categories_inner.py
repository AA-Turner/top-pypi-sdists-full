r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DocumentClassifierCategoriesInner", "DocumentClassifierCategoriesInnerSchema"]
__pdoc__ = {
    "DocumentClassifierCategoriesInnerSchema.resource": False,
    "DocumentClassifierCategoriesInnerSchema.opts": False,
    "DocumentClassifierCategoriesInner": False,
}

class DocumentClassifierCategoriesInnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DocumentClassifierCategoriesInner object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the document classifier category.

Example: Financial Documents """

    tag = marshmallow_fields.Str(data_key="tag", allow_none=True)
    r""" Tag of the data classifier.

Example: CAT_DOC0000 """

    total_hits = Size(data_key="total_hits", allow_none=True)
    r""" Total number of hits for the document classifier category.

Example: 4567890 """

    @property
    def resource(self):
        return DocumentClassifierCategoriesInner

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


class DocumentClassifierCategoriesInner(Resource):

    _schema = DocumentClassifierCategoriesInnerSchema
