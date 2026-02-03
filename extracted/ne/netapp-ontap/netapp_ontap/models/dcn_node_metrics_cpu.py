r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeMetricsCpu", "DcnNodeMetricsCpuSchema"]
__pdoc__ = {
    "DcnNodeMetricsCpuSchema.resource": False,
    "DcnNodeMetricsCpuSchema.opts": False,
    "DcnNodeMetricsCpu": False,
}

class DcnNodeMetricsCpuSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeMetricsCpu object"""

    memory_used = Size(data_key="memory_used", allow_none=True)
    r""" Average memory usage on the node's CPUs, in bytes.

Example: 1024000000 """

    processor_utilization = Size(data_key="processor_utilization", allow_none=True)
    r""" Average CPU utilization for the node.

Example: 13 """

    @property
    def resource(self):
        return DcnNodeMetricsCpu

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


class DcnNodeMetricsCpu(Resource):

    _schema = DcnNodeMetricsCpuSchema
