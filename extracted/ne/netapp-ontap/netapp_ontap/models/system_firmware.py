r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SystemFirmware", "SystemFirmwareSchema"]
__pdoc__ = {
    "SystemFirmwareSchema.resource": False,
    "SystemFirmwareSchema.opts": False,
    "SystemFirmware": False,
}


class SystemFirmwareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SystemFirmware object"""

    boot_media_bios_version = marshmallow_fields.Str(data_key="boot_media_bios_version", allow_none=True)
    r""" BIOS version that is currently staged on the boot media of the node.

Example: 13.16 """

    boot_media_loader_version = marshmallow_fields.Str(data_key="boot_media_loader_version", allow_none=True)
    r""" LOADER version that is currently staged on the boot media of the node.

Example: 8.2.0 """

    install_pending = marshmallow_fields.Boolean(data_key="install_pending", allow_none=True)
    r""" Flag that indicates if the system firmware install is pending. A true value suggests that a node reboot or cluster upgrade is required for completing installation.

Example: false """

    running_bios_version = marshmallow_fields.Str(data_key="running_bios_version", allow_none=True)
    r""" BIOS version that is currently installed on the node.

Example: 13.16 """

    running_loader_version = marshmallow_fields.Str(data_key="running_loader_version", allow_none=True)
    r""" LOADER version that is currently installed on the node.

Example: 8.2.0 """

    @property
    def resource(self):
        return SystemFirmware

    gettable_fields = [
        "boot_media_bios_version",
        "boot_media_loader_version",
        "install_pending",
        "running_bios_version",
        "running_loader_version",
    ]
    """boot_media_bios_version,boot_media_loader_version,install_pending,running_bios_version,running_loader_version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SystemFirmware(Resource):

    _schema = SystemFirmwareSchema
