r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemHostIoQueue", "NvmeSubsystemHostIoQueueSchema"]
__pdoc__ = {
    "NvmeSubsystemHostIoQueueSchema.resource": False,
    "NvmeSubsystemHostIoQueueSchema.opts": False,
    "NvmeSubsystemHostIoQueue": False,
}


class NvmeSubsystemHostIoQueueSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemHostIoQueue object"""

    count = Size(data_key="count", allow_none=True)
    r""" The number of I/O queue pairs. Absence of this property in GET implies property priority is set and platform and transport protocol specific values for I/O queue count is being used. Valid in GET only.


Example: 4 """

    depth = Size(data_key="depth", allow_none=True)
    r""" The I/O queue depth. Absence of this property in GET implies property priority is set and platform and transport protocol specific values for I/O queue depth is being used. Valid in GET only.


Example: 32 """

    @property
    def resource(self):
        return NvmeSubsystemHostIoQueue

    gettable_fields = [
        "count",
        "depth",
    ]
    """count,depth,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class NvmeSubsystemHostIoQueue(Resource):

    _schema = NvmeSubsystemHostIoQueueSchema
