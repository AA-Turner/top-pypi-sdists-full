r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupVdiskProvisioningOptions", "ConsistencyGroupVdiskProvisioningOptionsSchema"]
__pdoc__ = {
    "ConsistencyGroupVdiskProvisioningOptionsSchema.resource": False,
    "ConsistencyGroupVdiskProvisioningOptionsSchema.opts": False,
    "ConsistencyGroupVdiskProvisioningOptions": False,
}


class ConsistencyGroupVdiskProvisioningOptionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupVdiskProvisioningOptions object"""

    action = marshmallow_fields.Str(data_key="action", allow_none=True)
    r""" Operation to perform

Valid choices:

* create """

    count = Size(data_key="count", allow_none=True)
    r""" Number of elements to perform the operation on. """

    @property
    def resource(self):
        return ConsistencyGroupVdiskProvisioningOptions

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "action",
        "count",
    ]
    """action,count,"""

    postable_fields = [
        "action",
        "count",
    ]
    """action,count,"""


class ConsistencyGroupVdiskProvisioningOptions(Resource):

    _schema = ConsistencyGroupVdiskProvisioningOptionsSchema
