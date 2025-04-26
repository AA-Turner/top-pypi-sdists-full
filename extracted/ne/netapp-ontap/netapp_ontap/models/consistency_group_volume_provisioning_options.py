r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupVolumeProvisioningOptions", "ConsistencyGroupVolumeProvisioningOptionsSchema"]
__pdoc__ = {
    "ConsistencyGroupVolumeProvisioningOptionsSchema.resource": False,
    "ConsistencyGroupVolumeProvisioningOptionsSchema.opts": False,
    "ConsistencyGroupVolumeProvisioningOptions": False,
}


class ConsistencyGroupVolumeProvisioningOptionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupVolumeProvisioningOptions object"""

    action = marshmallow_fields.Str(data_key="action", allow_none=True)
    r""" Operation to perform

Valid choices:

* create
* add
* remove
* reassign """

    count = Size(data_key="count", allow_none=True)
    r""" Number of elements to perform the operation on. """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_provisioning_options_storage_service.ConsistencyGroupConsistencyGroupsProvisioningOptionsStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" Determines the placement of any storage object created during this operation. """

    @property
    def resource(self):
        return ConsistencyGroupVolumeProvisioningOptions

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "action",
        "count",
        "storage_service",
    ]
    """action,count,storage_service,"""

    postable_fields = [
        "action",
        "count",
        "storage_service",
    ]
    """action,count,storage_service,"""


class ConsistencyGroupVolumeProvisioningOptions(Resource):

    _schema = ConsistencyGroupVolumeProvisioningOptionsSchema
