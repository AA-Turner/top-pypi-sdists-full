r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LocalCifsGroupMembersRecords", "LocalCifsGroupMembersRecordsSchema"]
__pdoc__ = {
    "LocalCifsGroupMembersRecordsSchema.resource": False,
    "LocalCifsGroupMembersRecordsSchema.opts": False,
    "LocalCifsGroupMembersRecords": False,
}


class LocalCifsGroupMembersRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalCifsGroupMembersRecords object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Local user, Active Directory user, or Active Directory group which is a member of the specified local group. """

    @property
    def resource(self):
        return LocalCifsGroupMembersRecords

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


class LocalCifsGroupMembersRecords(Resource):

    _schema = LocalCifsGroupMembersRecordsSchema
