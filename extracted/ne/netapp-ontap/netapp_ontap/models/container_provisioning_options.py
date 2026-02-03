r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerProvisioningOptions", "ContainerProvisioningOptionsSchema"]
__pdoc__ = {
    "ContainerProvisioningOptionsSchema.resource": False,
    "ContainerProvisioningOptionsSchema.opts": False,
    "ContainerProvisioningOptions": False,
}

class ContainerProvisioningOptionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerProvisioningOptions object"""

    exclude_aggregates = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.container_provisioning_options_exclude_aggregates", "ContainerProvisioningOptionsExcludeAggregatesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="exclude_aggregates",
                allow_none=True
                )
    r""" A list of aggregates to exclude when determining the placement of the volume. """

    @property
    def resource(self):
        return ContainerProvisioningOptions

    gettable_fields = [
        "exclude_aggregates",
    ]
    """exclude_aggregates,"""

    patchable_fields = [
        "exclude_aggregates",
    ]
    """exclude_aggregates,"""

    postable_fields = [
        "exclude_aggregates",
    ]
    """exclude_aggregates,"""


class ContainerProvisioningOptions(Resource):

    _schema = ContainerProvisioningOptionsSchema
