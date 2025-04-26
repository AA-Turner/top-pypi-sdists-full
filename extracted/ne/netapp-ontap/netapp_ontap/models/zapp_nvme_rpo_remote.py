r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappNvmeRpoRemote", "ZappNvmeRpoRemoteSchema"]
__pdoc__ = {
    "ZappNvmeRpoRemoteSchema.resource": False,
    "ZappNvmeRpoRemoteSchema.opts": False,
    "ZappNvmeRpoRemote": False,
}


class ZappNvmeRpoRemoteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappNvmeRpoRemote object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The remote RPO of the application.

Valid choices:

* none
* zero """

    @property
    def resource(self):
        return ZappNvmeRpoRemote

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
    ]
    """name,"""


class ZappNvmeRpoRemote(Resource):

    _schema = ZappNvmeRpoRemoteSchema
