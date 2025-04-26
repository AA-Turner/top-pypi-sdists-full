r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FirmwareHistoryUpdateStateWorker", "FirmwareHistoryUpdateStateWorkerSchema"]
__pdoc__ = {
    "FirmwareHistoryUpdateStateWorkerSchema.resource": False,
    "FirmwareHistoryUpdateStateWorkerSchema.opts": False,
    "FirmwareHistoryUpdateStateWorker": False,
}


class FirmwareHistoryUpdateStateWorkerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FirmwareHistoryUpdateStateWorker object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.firmware_history_update_state_error.FirmwareHistoryUpdateStateErrorSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the firmware_history_update_state_worker. """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the firmware_history_update_state_worker. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of each worker that a node is controlling.

Valid choices:

* idle
* working
* complete
* failed
* waiting_to_retry """

    @property
    def resource(self):
        return FirmwareHistoryUpdateStateWorker

    gettable_fields = [
        "error",
        "node.links",
        "node.name",
        "node.uuid",
        "state",
    ]
    """error,node.links,node.name,node.uuid,state,"""

    patchable_fields = [
        "error",
        "node.name",
        "node.uuid",
        "state",
    ]
    """error,node.name,node.uuid,state,"""

    postable_fields = [
        "error",
        "node.name",
        "node.uuid",
        "state",
    ]
    """error,node.name,node.uuid,state,"""


class FirmwareHistoryUpdateStateWorker(Resource):

    _schema = FirmwareHistoryUpdateStateWorkerSchema
