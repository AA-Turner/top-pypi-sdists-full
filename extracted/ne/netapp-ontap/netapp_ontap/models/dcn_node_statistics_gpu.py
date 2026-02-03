r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeStatisticsGpu", "DcnNodeStatisticsGpuSchema"]
__pdoc__ = {
    "DcnNodeStatisticsGpuSchema.resource": False,
    "DcnNodeStatisticsGpuSchema.opts": False,
    "DcnNodeStatisticsGpu": False,
}

class DcnNodeStatisticsGpuSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeStatisticsGpu object"""

    memory_used = Size(data_key="memory_used", allow_none=True)
    r""" Current memory usage on the node, in bytes.

Example: 1024000000 """

    processor_utilization_base = Size(data_key="processor_utilization_base", allow_none=True)
    r""" Base counter for GPU utilization.

Example: 35042835393 """

    processor_utilization_raw = Size(data_key="processor_utilization_raw", allow_none=True)
    r""" Raw GPU utilization for the node. Divide this by the processor_utilization_base to calculate the percentage GPU utilization for the node.

Example: 2514992973 """

    @property
    def resource(self):
        return DcnNodeStatisticsGpu

    gettable_fields = [
        "memory_used",
        "processor_utilization_base",
        "processor_utilization_raw",
    ]
    """memory_used,processor_utilization_base,processor_utilization_raw,"""

    patchable_fields = [
        "memory_used",
        "processor_utilization_base",
        "processor_utilization_raw",
    ]
    """memory_used,processor_utilization_base,processor_utilization_raw,"""

    postable_fields = [
        "memory_used",
        "processor_utilization_base",
        "processor_utilization_raw",
    ]
    """memory_used,processor_utilization_base,processor_utilization_raw,"""


class DcnNodeStatisticsGpu(Resource):

    _schema = DcnNodeStatisticsGpuSchema
