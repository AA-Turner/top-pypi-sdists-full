r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ArwVserver", "ArwVserverSchema"]
__pdoc__ = {
    "ArwVserverSchema.resource": False,
    "ArwVserverSchema.opts": False,
    "ArwVserver": False,
}


class ArwVserverSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ArwVserver object"""

    event_log = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume_event_log.AntiRansomwareVolumeEventLogSchema", unknown=EXCLUDE, data_key="event_log", allow_none=True)
    r""" The event_log field of the arw_vserver. """

    @property
    def resource(self):
        return ArwVserver

    gettable_fields = [
        "event_log",
    ]
    """event_log,"""

    patchable_fields = [
        "event_log",
    ]
    """event_log,"""

    postable_fields = [
        "event_log",
    ]
    """event_log,"""


class ArwVserver(Resource):

    _schema = ArwVserverSchema
