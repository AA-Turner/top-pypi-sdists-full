r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemControllerIoQueue", "NvmeSubsystemControllerIoQueueSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerIoQueueSchema.resource": False,
    "NvmeSubsystemControllerIoQueueSchema.opts": False,
    "NvmeSubsystemControllerIoQueue": False,
}


class NvmeSubsystemControllerIoQueueSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemControllerIoQueue object"""

    count = Size(data_key="count", allow_none=True)
    r""" The number of I/O queues available to the controller. """

    depth = marshmallow_fields.List(Size, data_key="depth", allow_none=True)
    r""" The depths of the I/O queues. """

    @property
    def resource(self):
        return NvmeSubsystemControllerIoQueue

    gettable_fields = [
        "count",
        "depth",
    ]
    """count,depth,"""

    patchable_fields = [
        "depth",
    ]
    """depth,"""

    postable_fields = [
        "depth",
    ]
    """depth,"""


class NvmeSubsystemControllerIoQueue(Resource):

    _schema = NvmeSubsystemControllerIoQueueSchema
