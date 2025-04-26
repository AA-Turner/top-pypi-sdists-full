r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PortStatisticsPacketCounters", "PortStatisticsPacketCountersSchema"]
__pdoc__ = {
    "PortStatisticsPacketCountersSchema.resource": False,
    "PortStatisticsPacketCountersSchema.opts": False,
    "PortStatisticsPacketCounters": False,
}


class PortStatisticsPacketCountersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PortStatisticsPacketCounters object"""

    discards = Size(data_key="discards", allow_none=True)
    r""" Total number of discarded packets.

Example: 100 """

    errors = Size(data_key="errors", allow_none=True)
    r""" Number of packet errors.

Example: 200 """

    packets = Size(data_key="packets", allow_none=True)
    r""" Total packet count.

Example: 500 """

    @property
    def resource(self):
        return PortStatisticsPacketCounters

    gettable_fields = [
        "discards",
        "errors",
        "packets",
    ]
    """discards,errors,packets,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class PortStatisticsPacketCounters(Resource):

    _schema = PortStatisticsPacketCountersSchema
