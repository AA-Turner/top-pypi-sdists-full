r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ZappS3BucketProtectionType", "ZappS3BucketProtectionTypeSchema"]
__pdoc__ = {
    "ZappS3BucketProtectionTypeSchema.resource": False,
    "ZappS3BucketProtectionTypeSchema.opts": False,
    "ZappS3BucketProtectionType": False,
}


class ZappS3BucketProtectionTypeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ZappS3BucketProtectionType object"""

    remote_rpo = marshmallow_fields.Str(data_key="remote_rpo", allow_none=True)
    r""" The remote RPO of the application.

Valid choices:

* none
* zero """

    @property
    def resource(self):
        return ZappS3BucketProtectionType

    gettable_fields = [
        "remote_rpo",
    ]
    """remote_rpo,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "remote_rpo",
    ]
    """remote_rpo,"""


class ZappS3BucketProtectionType(Resource):

    _schema = ZappS3BucketProtectionTypeSchema
