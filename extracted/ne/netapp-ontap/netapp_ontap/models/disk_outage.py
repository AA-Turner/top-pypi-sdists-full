r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["DiskOutage", "DiskOutageSchema"]
__pdoc__ = {
    "DiskOutageSchema.resource": False,
    "DiskOutageSchema.opts": False,
    "DiskOutage": False,
}


class DiskOutageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DiskOutage object"""

    persistently_failed = marshmallow_fields.Boolean(data_key="persistently_failed", allow_none=True)
    r""" Indicates whether RAID maintains the state of this disk as failed across reboots. """

    reason = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE, data_key="reason", allow_none=True)
    r""" This error message and code explaining the disk failure. """

    @property
    def resource(self):
        return DiskOutage

    gettable_fields = [
        "persistently_failed",
        "reason",
    ]
    """persistently_failed,reason,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DiskOutage(Resource):

    _schema = DiskOutageSchema
