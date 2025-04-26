r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeProtocolRawPerformanceStatOther", "VolumeProtocolRawPerformanceStatOtherSchema"]
__pdoc__ = {
    "VolumeProtocolRawPerformanceStatOtherSchema.resource": False,
    "VolumeProtocolRawPerformanceStatOtherSchema.opts": False,
    "VolumeProtocolRawPerformanceStatOther": False,
}


class VolumeProtocolRawPerformanceStatOtherSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeProtocolRawPerformanceStatOther object"""

    count = Size(data_key="count", allow_none=True)
    r""" Number of operations of the given type performed on this volume.

Example: 1000 """

    total_time = Size(data_key="total_time", allow_none=True)
    r""" The raw data component latency in microseconds measured within ONTAP for all operations of the given type.

Example: 200 """

    @property
    def resource(self):
        return VolumeProtocolRawPerformanceStatOther

    gettable_fields = [
        "count",
        "total_time",
    ]
    """count,total_time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class VolumeProtocolRawPerformanceStatOther(Resource):

    _schema = VolumeProtocolRawPerformanceStatOtherSchema
