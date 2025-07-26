r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Firmware", "FirmwareSchema"]
__pdoc__ = {
    "FirmwareSchema.resource": False,
    "FirmwareSchema.opts": False,
    "Firmware": False,
}


class FirmwareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Firmware object"""

    cluster_fw_progress = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.firmware_update_progress.FirmwareUpdateProgressSchema", unknown=EXCLUDE, allow_none=True), data_key="cluster_fw_progress", allow_none=True)
    r""" The cluster_fw_progress field of the firmware. """

    disk = marshmallow_fields.Nested("netapp_ontap.models.firmware_disk.FirmwareDiskSchema", unknown=EXCLUDE, data_key="disk", allow_none=True)
    r""" The disk field of the firmware. """

    dqp = marshmallow_fields.Nested("netapp_ontap.models.firmware_dqp.FirmwareDqpSchema", unknown=EXCLUDE, data_key="dqp", allow_none=True)
    r""" The dqp field of the firmware. """

    shelf = marshmallow_fields.Nested("netapp_ontap.models.firmware_shelf.FirmwareShelfSchema", unknown=EXCLUDE, data_key="shelf", allow_none=True)
    r""" The shelf field of the firmware. """

    sp_bmc = marshmallow_fields.Nested("netapp_ontap.models.firmware_sp_bmc.FirmwareSpBmcSchema", unknown=EXCLUDE, data_key="sp_bmc", allow_none=True)
    r""" The sp_bmc field of the firmware. """

    system_firmware = marshmallow_fields.Nested("netapp_ontap.models.system_firmware.SystemFirmwareSchema", unknown=EXCLUDE, data_key="system_firmware", allow_none=True)
    r""" The system_firmware field of the firmware. """

    @property
    def resource(self):
        return Firmware

    gettable_fields = [
        "cluster_fw_progress",
        "disk",
        "dqp",
        "shelf",
        "sp_bmc",
        "system_firmware",
    ]
    """cluster_fw_progress,disk,dqp,shelf,sp_bmc,system_firmware,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class Firmware(Resource):

    _schema = FirmwareSchema
