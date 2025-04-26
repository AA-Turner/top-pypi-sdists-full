r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ActiveDirectoryDelete", "ActiveDirectoryDeleteSchema"]
__pdoc__ = {
    "ActiveDirectoryDeleteSchema.resource": False,
    "ActiveDirectoryDeleteSchema.opts": False,
    "ActiveDirectoryDelete": False,
}


class ActiveDirectoryDeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ActiveDirectoryDelete object"""

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" Administrator password required for Active Directory account creation.

Example: testpwd """

    username = marshmallow_fields.Str(data_key="username", allow_none=True)
    r""" Administrator username required for Active Directory account creation.

Example: admin """

    @property
    def resource(self):
        return ActiveDirectoryDelete

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "password",
        "username",
    ]
    """password,username,"""

    postable_fields = [
        "password",
        "username",
    ]
    """password,username,"""


class ActiveDirectoryDelete(Resource):

    _schema = ActiveDirectoryDeleteSchema
