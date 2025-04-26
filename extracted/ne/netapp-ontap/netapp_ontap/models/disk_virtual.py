r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["DiskVirtual", "DiskVirtualSchema"]
__pdoc__ = {
    "DiskVirtualSchema.resource": False,
    "DiskVirtualSchema.opts": False,
    "DiskVirtual": False,
}


class DiskVirtualSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DiskVirtual object"""

    container = marshmallow_fields.Str(data_key="container", allow_none=True)
    r""" Container name of the virtual disk.

Example: nviet12122018113936-rg """

    object = marshmallow_fields.Str(data_key="object", allow_none=True)
    r""" Object name of the virtual disk.

Example: f1fu63se """

    storage_account = marshmallow_fields.Str(data_key="storage_account", allow_none=True)
    r""" Storage account name of the virtual disk.

Example: nviet12122018113936ps """

    target_address = marshmallow_fields.Str(data_key="target_address", allow_none=True)
    r""" Target address of the virtual disk. """

    @property
    def resource(self):
        return DiskVirtual

    gettable_fields = [
        "container",
        "object",
        "storage_account",
        "target_address",
    ]
    """container,object,storage_account,target_address,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DiskVirtual(Resource):

    _schema = DiskVirtualSchema
