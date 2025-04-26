r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["File", "FileSchema"]
__pdoc__ = {
    "FileSchema.resource": False,
    "FileSchema.opts": False,
    "File": False,
}


class FileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the File object"""

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Path of the file or directory. """

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the file. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the file. """

    @property
    def resource(self):
        return File

    gettable_fields = [
        "path",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """path,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "path",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """path,svm.name,svm.uuid,volume.name,volume.uuid,"""

    postable_fields = [
        "path",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """path,svm.name,svm.uuid,volume.name,volume.uuid,"""


class File(Resource):

    _schema = FileSchema
