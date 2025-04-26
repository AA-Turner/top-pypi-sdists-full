r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesController", "ClusterNodesControllerSchema"]
__pdoc__ = {
    "ClusterNodesControllerSchema.resource": False,
    "ClusterNodesControllerSchema.opts": False,
    "ClusterNodesController": False,
}


class ClusterNodesControllerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesController object"""

    board = marshmallow_fields.Str(data_key="board", allow_none=True)
    r""" Type of the system board. This is defined by vendor.

Example: System Board XXVIII """

    cpu = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_controller_cpu.ClusterNodesControllerCpuSchema", unknown=EXCLUDE, data_key="cpu", allow_none=True)
    r""" CPU information. """

    failed_fan = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_controller_failed_fan.ClusterNodesControllerFailedFanSchema", unknown=EXCLUDE, data_key="failed_fan", allow_none=True)
    r""" The failed_fan field of the cluster_nodes_controller. """

    failed_power_supply = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_controller_failed_power_supply.ClusterNodesControllerFailedPowerSupplySchema", unknown=EXCLUDE, data_key="failed_power_supply", allow_none=True)
    r""" The failed_power_supply field of the cluster_nodes_controller. """

    flash_cache = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_controller_flash_cache.ClusterNodesControllerFlashCacheSchema", unknown=EXCLUDE, allow_none=True), data_key="flash_cache", allow_none=True)
    r""" A list of Flash-Cache devices. Only returned when requested by name. """

    frus = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_controller_frus.ClusterNodesControllerFrusSchema", unknown=EXCLUDE, allow_none=True), data_key="frus", allow_none=True)
    r""" List of FRUs on the node. Only returned when requested by name. """

    memory_size = Size(data_key="memory_size", allow_none=True)
    r""" Memory available on the node, in bytes.

Example: 1024000000 """

    over_temperature = marshmallow_fields.Str(data_key="over_temperature", allow_none=True)
    r""" Specifies whether the hardware is currently operating outside of its recommended temperature range. The hardware shuts down if the temperature exceeds critical thresholds.

Valid choices:

* over
* normal """

    @property
    def resource(self):
        return ClusterNodesController

    gettable_fields = [
        "board",
        "cpu",
        "failed_fan",
        "failed_power_supply",
        "flash_cache",
        "frus",
        "memory_size",
        "over_temperature",
    ]
    """board,cpu,failed_fan,failed_power_supply,flash_cache,frus,memory_size,over_temperature,"""

    patchable_fields = [
        "cpu",
        "failed_fan",
        "failed_power_supply",
        "frus",
    ]
    """cpu,failed_fan,failed_power_supply,frus,"""

    postable_fields = [
        "cpu",
        "failed_fan",
        "failed_power_supply",
        "frus",
    ]
    """cpu,failed_fan,failed_power_supply,frus,"""


class ClusterNodesController(Resource):

    _schema = ClusterNodesControllerSchema
