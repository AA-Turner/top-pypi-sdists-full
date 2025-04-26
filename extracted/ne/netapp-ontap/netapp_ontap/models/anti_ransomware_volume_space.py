r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AntiRansomwareVolumeSpace", "AntiRansomwareVolumeSpaceSchema"]
__pdoc__ = {
    "AntiRansomwareVolumeSpaceSchema.resource": False,
    "AntiRansomwareVolumeSpaceSchema.opts": False,
    "AntiRansomwareVolumeSpace": False,
}


class AntiRansomwareVolumeSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareVolumeSpace object"""

    snapshot_count = Size(data_key="snapshot_count", allow_none=True)
    r""" Total number of Anti-ransomware backup snapshots. """

    used = Size(data_key="used", allow_none=True)
    r""" Total space in bytes used by the Anti-ransomware feature. """

    used_by_logs = Size(data_key="used_by_logs", allow_none=True)
    r""" Space in bytes used by the Anti-ransomware analytics logs. """

    used_by_snapshots = Size(data_key="used_by_snapshots", allow_none=True)
    r""" Space in bytes used by the Anti-ransomware backup snapshots. """

    @property
    def resource(self):
        return AntiRansomwareVolumeSpace

    gettable_fields = [
        "snapshot_count",
        "used",
        "used_by_logs",
        "used_by_snapshots",
    ]
    """snapshot_count,used,used_by_logs,used_by_snapshots,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AntiRansomwareVolumeSpace(Resource):

    _schema = AntiRansomwareVolumeSpaceSchema
