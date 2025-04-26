r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchPortStatistics", "SwitchPortStatisticsSchema"]
__pdoc__ = {
    "SwitchPortStatisticsSchema.resource": False,
    "SwitchPortStatisticsSchema.opts": False,
    "SwitchPortStatistics": False,
}


class SwitchPortStatisticsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortStatistics object"""

    receive_raw = marshmallow_fields.Nested("netapp_ontap.models.port_statistics_packet_counters.PortStatisticsPacketCountersSchema", unknown=EXCLUDE, data_key="receive_raw", allow_none=True)
    r""" These are raw packet-related counters for the Ethernet port. """

    transmit_raw = marshmallow_fields.Nested("netapp_ontap.models.port_statistics_packet_counters.PortStatisticsPacketCountersSchema", unknown=EXCLUDE, data_key="transmit_raw", allow_none=True)
    r""" These are raw packet-related counters for the Ethernet port. """

    @property
    def resource(self):
        return SwitchPortStatistics

    gettable_fields = [
        "receive_raw",
        "transmit_raw",
    ]
    """receive_raw,transmit_raw,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SwitchPortStatistics(Resource):

    _schema = SwitchPortStatisticsSchema
