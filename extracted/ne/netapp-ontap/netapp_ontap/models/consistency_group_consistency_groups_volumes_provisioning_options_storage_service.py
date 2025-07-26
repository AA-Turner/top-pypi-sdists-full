r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageService", "ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageServiceSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageServiceSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageServiceSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageService": False,
}


class ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageService object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage service name. If not specified, the default value is the most performant for the platform.


Valid choices:

* extreme
* performance
* value """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageService

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


class ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageService(Resource):

    _schema = ConsistencyGroupConsistencyGroupsVolumesProvisioningOptionsStorageServiceSchema
