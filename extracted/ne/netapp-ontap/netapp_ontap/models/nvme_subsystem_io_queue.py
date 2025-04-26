r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemIoQueue", "NvmeSubsystemIoQueueSchema"]
__pdoc__ = {
    "NvmeSubsystemIoQueueSchema.resource": False,
    "NvmeSubsystemIoQueueSchema.opts": False,
    "NvmeSubsystemIoQueue": False,
}


class NvmeSubsystemIoQueueSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemIoQueue object"""

    default = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_io_queue_default.NvmeSubsystemIoQueueDefaultSchema", unknown=EXCLUDE, data_key="default", allow_none=True)
    r""" The default I/O queue parameters inherited by NVMe hosts in the NVMe subsystem. """

    @property
    def resource(self):
        return NvmeSubsystemIoQueue

    gettable_fields = [
        "default",
    ]
    """default,"""

    patchable_fields = [
        "default",
    ]
    """default,"""

    postable_fields = [
        "default",
    ]
    """default,"""


class NvmeSubsystemIoQueue(Resource):

    _schema = NvmeSubsystemIoQueueSchema
