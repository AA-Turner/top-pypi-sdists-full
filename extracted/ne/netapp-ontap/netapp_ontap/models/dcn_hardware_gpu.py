r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnHardwareGpu", "DcnHardwareGpuSchema"]
__pdoc__ = {
    "DcnHardwareGpuSchema.resource": False,
    "DcnHardwareGpuSchema.opts": False,
    "DcnHardwareGpu": False,
}

class DcnHardwareGpuSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnHardwareGpu object"""

    count = Size(data_key="count", allow_none=True)
    r""" Number count of GPUs on the node.

Example: 4 """

    firmware_release = marshmallow_fields.Str(data_key="firmware_release", allow_none=True)
    r""" Firmware release number. Defined by the GPU manufacturer. """

    memory_size = Size(data_key="memory_size", allow_none=True)
    r""" GPU Memory available on the node, in bytes.

Example: 1024000000 """

    processor = marshmallow_fields.Str(data_key="processor", allow_none=True)
    r""" GPU type on the node. """

    @property
    def resource(self):
        return DcnHardwareGpu

    gettable_fields = [
        "count",
        "firmware_release",
        "memory_size",
        "processor",
    ]
    """count,firmware_release,memory_size,processor,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnHardwareGpu(Resource):

    _schema = DcnHardwareGpuSchema
