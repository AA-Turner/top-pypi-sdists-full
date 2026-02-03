r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeMetricsGpu", "DcnNodeMetricsGpuSchema"]
__pdoc__ = {
    "DcnNodeMetricsGpuSchema.resource": False,
    "DcnNodeMetricsGpuSchema.opts": False,
    "DcnNodeMetricsGpu": False,
}

class DcnNodeMetricsGpuSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeMetricsGpu object"""

    memory_used = Size(data_key="memory_used", allow_none=True)
    r""" Average memory usage on the node's GPUs, in bytes.

Example: 1024000000 """

    processor_utilization = Size(data_key="processor_utilization", allow_none=True)
    r""" Average GPU utilization for the node.

Example: 13 """

    @property
    def resource(self):
        return DcnNodeMetricsGpu

    gettable_fields = [
        "memory_used",
        "processor_utilization",
    ]
    """memory_used,processor_utilization,"""

    patchable_fields = [
        "memory_used",
        "processor_utilization",
    ]
    """memory_used,processor_utilization,"""

    postable_fields = [
        "memory_used",
        "processor_utilization",
    ]
    """memory_used,processor_utilization,"""


class DcnNodeMetricsGpu(Resource):

    _schema = DcnNodeMetricsGpuSchema
