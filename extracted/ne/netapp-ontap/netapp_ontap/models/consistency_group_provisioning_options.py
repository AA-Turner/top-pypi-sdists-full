r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupProvisioningOptions", "ConsistencyGroupProvisioningOptionsSchema"]
__pdoc__ = {
    "ConsistencyGroupProvisioningOptionsSchema.resource": False,
    "ConsistencyGroupProvisioningOptionsSchema.opts": False,
    "ConsistencyGroupProvisioningOptions": False,
}


class ConsistencyGroupProvisioningOptionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupProvisioningOptions object"""

    action = marshmallow_fields.Str(data_key="action", allow_none=True)
    r""" Operation to perform

Valid choices:

* create
* add
* remove
* promote
* demote """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" New name for consistency group. Required to resolve naming collisions. """

    storage_service = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_provisioning_options_storage_service.ConsistencyGroupConsistencyGroupsProvisioningOptionsStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service", allow_none=True)
    r""" Determines the placement of any storage object created during this operation. """

    @property
    def resource(self):
        return ConsistencyGroupProvisioningOptions

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "action",
        "name",
        "storage_service",
    ]
    """action,name,storage_service,"""

    postable_fields = [
        "action",
        "name",
        "storage_service",
    ]
    """action,name,storage_service,"""


class ConsistencyGroupProvisioningOptions(Resource):

    _schema = ConsistencyGroupProvisioningOptionsSchema
