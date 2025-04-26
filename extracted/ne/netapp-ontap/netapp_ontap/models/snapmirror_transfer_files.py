r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorTransferFiles", "SnapmirrorTransferFilesSchema"]
__pdoc__ = {
    "SnapmirrorTransferFilesSchema.resource": False,
    "SnapmirrorTransferFilesSchema.opts": False,
    "SnapmirrorTransferFiles": False,
}


class SnapmirrorTransferFilesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorTransferFiles object"""

    destination_path = marshmallow_fields.Str(data_key="destination_path", allow_none=True)
    r""" The destination_path field of the snapmirror_transfer_files.

Example: /dirb/file2 """

    source_path = marshmallow_fields.Str(data_key="source_path", allow_none=True)
    r""" The source_path field of the snapmirror_transfer_files.

Example: /dira/file1 """

    @property
    def resource(self):
        return SnapmirrorTransferFiles

    gettable_fields = [
        "destination_path",
        "source_path",
    ]
    """destination_path,source_path,"""

    patchable_fields = [
        "destination_path",
        "source_path",
    ]
    """destination_path,source_path,"""

    postable_fields = [
        "destination_path",
        "source_path",
    ]
    """destination_path,source_path,"""


class SnapmirrorTransferFiles(Resource):

    _schema = SnapmirrorTransferFilesSchema
