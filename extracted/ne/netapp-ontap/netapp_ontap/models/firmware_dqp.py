r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FirmwareDqp", "FirmwareDqpSchema"]
__pdoc__ = {
    "FirmwareDqpSchema.resource": False,
    "FirmwareDqpSchema.opts": False,
    "FirmwareDqp": False,
}


class FirmwareDqpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FirmwareDqp object"""

    file_name = marshmallow_fields.Str(data_key="file_name", allow_none=True)
    r""" Firmware file name

Example: qual_devices_v3 """

    record_count = marshmallow_fields.Nested("netapp_ontap.models.firmware_dqp_record_count.FirmwareDqpRecordCountSchema", unknown=EXCLUDE, data_key="record_count", allow_none=True)
    r""" The record_count field of the firmware_dqp. """

    revision = marshmallow_fields.Str(data_key="revision", allow_none=True)
    r""" Firmware revision

Example: 20200117 """

    version = marshmallow_fields.Str(data_key="version", allow_none=True)
    r""" Firmware version

Example: 3.18 """

    @property
    def resource(self):
        return FirmwareDqp

    gettable_fields = [
        "file_name",
        "record_count",
        "revision",
        "version",
    ]
    """file_name,record_count,revision,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FirmwareDqp(Resource):

    _schema = FirmwareDqpSchema
