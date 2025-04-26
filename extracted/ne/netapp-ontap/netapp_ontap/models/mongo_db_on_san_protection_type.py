r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MongoDbOnSanProtectionType", "MongoDbOnSanProtectionTypeSchema"]
__pdoc__ = {
    "MongoDbOnSanProtectionTypeSchema.resource": False,
    "MongoDbOnSanProtectionTypeSchema.opts": False,
    "MongoDbOnSanProtectionType": False,
}


class MongoDbOnSanProtectionTypeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MongoDbOnSanProtectionType object"""

    local_rpo = marshmallow_fields.Str(data_key="local_rpo", allow_none=True)
    r""" The local RPO of the application.

Valid choices:

* hourly
* none """

    remote_rpo = marshmallow_fields.Str(data_key="remote_rpo", allow_none=True)
    r""" The remote RPO of the application.

Valid choices:

* none
* zero """

    @property
    def resource(self):
        return MongoDbOnSanProtectionType

    gettable_fields = [
        "local_rpo",
        "remote_rpo",
    ]
    """local_rpo,remote_rpo,"""

    patchable_fields = [
        "local_rpo",
    ]
    """local_rpo,"""

    postable_fields = [
        "local_rpo",
        "remote_rpo",
    ]
    """local_rpo,remote_rpo,"""


class MongoDbOnSanProtectionType(Resource):

    _schema = MongoDbOnSanProtectionTypeSchema
