r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FirmwareUpdateProgressState", "FirmwareUpdateProgressStateSchema"]
__pdoc__ = {
    "FirmwareUpdateProgressStateSchema.resource": False,
    "FirmwareUpdateProgressStateSchema.opts": False,
    "FirmwareUpdateProgressState": False,
}


class FirmwareUpdateProgressStateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FirmwareUpdateProgressState object"""

    attempts = Size(data_key="attempts", allow_none=True)
    r""" The attempts field of the firmware_update_progress_state.

Example: 3 """

    code = Size(data_key="code", allow_none=True)
    r""" Code corresponding to the status message.

Example: 2228325 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message returned when a cluster firmware update job fails.

Example: Cannot open local staging ZIP file disk_firmware.zip """

    status = marshmallow_fields.Str(data_key="status", allow_none=True)
    r""" The status field of the firmware_update_progress_state.

Valid choices:

* idle
* working
* complete
* failed
* waiting_to_retry """

    worker_node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="worker_node", allow_none=True)
    r""" The worker_node field of the firmware_update_progress_state. """

    @property
    def resource(self):
        return FirmwareUpdateProgressState

    gettable_fields = [
        "attempts",
        "code",
        "message",
        "status",
        "worker_node.links",
        "worker_node.name",
        "worker_node.uuid",
    ]
    """attempts,code,message,status,worker_node.links,worker_node.name,worker_node.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FirmwareUpdateProgressState(Resource):

    _schema = FirmwareUpdateProgressStateSchema
