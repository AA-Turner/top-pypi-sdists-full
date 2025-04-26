r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VdiOnNasDesktops", "VdiOnNasDesktopsSchema"]
__pdoc__ = {
    "VdiOnNasDesktopsSchema.resource": False,
    "VdiOnNasDesktopsSchema.opts": False,
    "VdiOnNasDesktops": False,
}


class VdiOnNasDesktopsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VdiOnNasDesktops object"""

    count = Size(data_key="count", allow_none=True)
    r""" The number of desktops to support. """

    size = Size(data_key="size", allow_none=True)
    r""" The size of the desktops. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.vdi_on_nas_desktops_storage_service.VdiOnNasDesktopsStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" The storage_service field of the vdi_on_nas_desktops. """

    @property
    def resource(self):
        return VdiOnNasDesktops

    gettable_fields = [
        "count",
        "size",
        "storage_service",
    ]
    """count,size,storage_service,"""

    patchable_fields = [
        "count",
        "storage_service",
    ]
    """count,storage_service,"""

    postable_fields = [
        "count",
        "size",
        "storage_service",
    ]
    """count,size,storage_service,"""


class VdiOnNasDesktops(Resource):

    _schema = VdiOnNasDesktopsSchema
