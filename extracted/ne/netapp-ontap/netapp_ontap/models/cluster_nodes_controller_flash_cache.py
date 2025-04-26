r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesControllerFlashCache", "ClusterNodesControllerFlashCacheSchema"]
__pdoc__ = {
    "ClusterNodesControllerFlashCacheSchema.resource": False,
    "ClusterNodesControllerFlashCacheSchema.opts": False,
    "ClusterNodesControllerFlashCache": False,
}


class ClusterNodesControllerFlashCacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesControllerFlashCache object"""

    capacity = Size(data_key="capacity", allow_none=True)
    r""" Size in bytes

Example: 1024000000000 """

    device_id = Size(data_key="device_id", allow_none=True)
    r""" The device_id field of the cluster_nodes_controller_flash_cache.

Example: 0 """

    firmware_file = marshmallow_fields.Str(data_key="firmware_file", allow_none=True)
    r""" The firmware_file field of the cluster_nodes_controller_flash_cache.

Example: X9170_O000Z6300NVM """

    firmware_version = marshmallow_fields.Str(data_key="firmware_version", allow_none=True)
    r""" The firmware_version field of the cluster_nodes_controller_flash_cache.

Example: NA05 """

    hardware_revision = marshmallow_fields.Str(data_key="hardware_revision", allow_none=True)
    r""" The hardware_revision field of the cluster_nodes_controller_flash_cache.

Example: A1 """

    model = marshmallow_fields.Str(data_key="model", allow_none=True)
    r""" The model field of the cluster_nodes_controller_flash_cache.

Example: X1970A """

    part_number = marshmallow_fields.Str(data_key="part_number", allow_none=True)
    r""" The part_number field of the cluster_nodes_controller_flash_cache.

Example: 119-00207 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" The serial_number field of the cluster_nodes_controller_flash_cache.

Example: A22P5061550000187 """

    slot = marshmallow_fields.Str(data_key="slot", allow_none=True)
    r""" The slot field of the cluster_nodes_controller_flash_cache.

Example: 6-1 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the cluster_nodes_controller_flash_cache.

Valid choices:

* ok
* erasing
* erased
* failed
* removed """

    @property
    def resource(self):
        return ClusterNodesControllerFlashCache

    gettable_fields = [
        "capacity",
        "device_id",
        "firmware_file",
        "firmware_version",
        "hardware_revision",
        "model",
        "part_number",
        "serial_number",
        "slot",
        "state",
    ]
    """capacity,device_id,firmware_file,firmware_version,hardware_revision,model,part_number,serial_number,slot,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesControllerFlashCache(Resource):

    _schema = ClusterNodesControllerFlashCacheSchema
