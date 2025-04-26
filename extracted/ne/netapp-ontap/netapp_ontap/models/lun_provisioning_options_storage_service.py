r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunProvisioningOptionsStorageService", "LunProvisioningOptionsStorageServiceSchema"]
__pdoc__ = {
    "LunProvisioningOptionsStorageServiceSchema.resource": False,
    "LunProvisioningOptionsStorageServiceSchema.opts": False,
    "LunProvisioningOptionsStorageService": False,
}


class LunProvisioningOptionsStorageServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunProvisioningOptionsStorageService object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage service name. If not specified, the default value is the most performant for the platform.


Valid choices:

* extreme
* performance
* value """

    @property
    def resource(self):
        return LunProvisioningOptionsStorageService

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
    ]
    """name,"""


class LunProvisioningOptionsStorageService(Resource):

    _schema = LunProvisioningOptionsStorageServiceSchema
