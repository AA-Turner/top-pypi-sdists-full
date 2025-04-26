r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FirmwareDqpRecordCount", "FirmwareDqpRecordCountSchema"]
__pdoc__ = {
    "FirmwareDqpRecordCountSchema.resource": False,
    "FirmwareDqpRecordCountSchema.opts": False,
    "FirmwareDqpRecordCount": False,
}


class FirmwareDqpRecordCountSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FirmwareDqpRecordCount object"""

    alias = Size(data_key="alias", allow_none=True)
    r""" Alias record count

Example: 200 """

    device = Size(data_key="device", allow_none=True)
    r""" Device record count

Example: 29 """

    drive = Size(data_key="drive", allow_none=True)
    r""" Drive record count

Example: 680 """

    system = Size(data_key="system", allow_none=True)
    r""" System record count

Example: 3 """

    @property
    def resource(self):
        return FirmwareDqpRecordCount

    gettable_fields = [
        "alias",
        "device",
        "drive",
        "system",
    ]
    """alias,device,drive,system,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FirmwareDqpRecordCount(Resource):

    _schema = FirmwareDqpRecordCountSchema
