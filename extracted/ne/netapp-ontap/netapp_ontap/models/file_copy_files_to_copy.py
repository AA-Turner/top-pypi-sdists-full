r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FileCopyFilesToCopy", "FileCopyFilesToCopySchema"]
__pdoc__ = {
    "FileCopyFilesToCopySchema.resource": False,
    "FileCopyFilesToCopySchema.opts": False,
    "FileCopyFilesToCopy": False,
}


class FileCopyFilesToCopySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FileCopyFilesToCopy object"""

    destination = marshmallow_fields.Nested("netapp_ontap.models.file.FileSchema", unknown=EXCLUDE, data_key="destination", allow_none=True)
    r""" The destination field of the file_copy_files_to_copy. """

    source = marshmallow_fields.Nested("netapp_ontap.models.file.FileSchema", unknown=EXCLUDE, data_key="source", allow_none=True)
    r""" The source field of the file_copy_files_to_copy. """

    @property
    def resource(self):
        return FileCopyFilesToCopy

    gettable_fields = [
        "destination.path",
        "destination.svm",
        "destination.volume",
        "source.path",
        "source.svm",
        "source.volume",
    ]
    """destination.path,destination.svm,destination.volume,source.path,source.svm,source.volume,"""

    patchable_fields = [
        "destination.path",
        "destination.svm",
        "destination.volume",
        "source.path",
        "source.svm",
        "source.volume",
    ]
    """destination.path,destination.svm,destination.volume,source.path,source.svm,source.volume,"""

    postable_fields = [
        "destination.path",
        "destination.svm",
        "destination.volume",
        "source.path",
        "source.svm",
        "source.volume",
    ]
    """destination.path,destination.svm,destination.volume,source.path,source.svm,source.volume,"""


class FileCopyFilesToCopy(Resource):

    _schema = FileCopyFilesToCopySchema
