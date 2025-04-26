r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FileInfoLinks", "FileInfoLinksSchema"]
__pdoc__ = {
    "FileInfoLinksSchema.resource": False,
    "FileInfoLinksSchema.opts": False,
    "FileInfoLinks": False,
}


class FileInfoLinksSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FileInfoLinks object"""

    metadata = marshmallow_fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="metadata", allow_none=True)
    r""" The metadata field of the file_info_links. """

    self_ = marshmallow_fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="self", allow_none=True)
    r""" The self_ field of the file_info_links. """

    @property
    def resource(self):
        return FileInfoLinks

    gettable_fields = [
        "metadata",
        "self_",
    ]
    """metadata,self_,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FileInfoLinks(Resource):

    _schema = FileInfoLinksSchema
