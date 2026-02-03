r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["LunProvisioningOptionsExcludeAggregates", "LunProvisioningOptionsExcludeAggregatesSchema"]
__pdoc__ = {
    "LunProvisioningOptionsExcludeAggregatesSchema.resource": False,
    "LunProvisioningOptionsExcludeAggregatesSchema.opts": False,
    "LunProvisioningOptionsExcludeAggregates": False,
}

class LunProvisioningOptionsExcludeAggregatesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunProvisioningOptionsExcludeAggregates object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The aggregate name.


Example: aggr1 """

    @property
    def resource(self):
        return LunProvisioningOptionsExcludeAggregates

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


class LunProvisioningOptionsExcludeAggregates(Resource):

    _schema = LunProvisioningOptionsExcludeAggregatesSchema
