r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesControllerCpu", "ClusterNodesControllerCpuSchema"]
__pdoc__ = {
    "ClusterNodesControllerCpuSchema.resource": False,
    "ClusterNodesControllerCpuSchema.opts": False,
    "ClusterNodesControllerCpu": False,
}


class ClusterNodesControllerCpuSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesControllerCpu object"""

    count = Size(data_key="count", allow_none=True)
    r""" Number of CPUs on the node.

Example: 20 """

    firmware_release = marshmallow_fields.Str(data_key="firmware_release", allow_none=True)
    r""" Firmware release number. Defined by the CPU manufacturer. """

    processor = marshmallow_fields.Str(data_key="processor", allow_none=True)
    r""" CPU type on the node. """

    @property
    def resource(self):
        return ClusterNodesControllerCpu

    gettable_fields = [
        "count",
        "firmware_release",
        "processor",
    ]
    """count,firmware_release,processor,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesControllerCpu(Resource):

    _schema = ClusterNodesControllerCpuSchema
