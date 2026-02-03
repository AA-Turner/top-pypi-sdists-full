r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerProvisioningOptionsExcludeAggregates", "ContainerProvisioningOptionsExcludeAggregatesSchema"]
__pdoc__ = {
    "ContainerProvisioningOptionsExcludeAggregatesSchema.resource": False,
    "ContainerProvisioningOptionsExcludeAggregatesSchema.opts": False,
    "ContainerProvisioningOptionsExcludeAggregates": False,
}

class ContainerProvisioningOptionsExcludeAggregatesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerProvisioningOptionsExcludeAggregates object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the container_provisioning_options_exclude_aggregates.

Example: aggr1 """

    @property
    def resource(self):
        return ContainerProvisioningOptionsExcludeAggregates

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class ContainerProvisioningOptionsExcludeAggregates(Resource):

    _schema = ContainerProvisioningOptionsExcludeAggregatesSchema
