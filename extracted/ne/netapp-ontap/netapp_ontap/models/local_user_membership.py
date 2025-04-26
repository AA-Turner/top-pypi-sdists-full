r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LocalUserMembership", "LocalUserMembershipSchema"]
__pdoc__ = {
    "LocalUserMembershipSchema.resource": False,
    "LocalUserMembershipSchema.opts": False,
    "LocalUserMembership": False,
}


class LocalUserMembershipSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalUserMembership object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the local_user_membership. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Local group name. The maximum supported length of a group name is 256 characters.


Example: SMB_SERVER01\group """

    sid = marshmallow_fields.Str(data_key="sid", allow_none=True)
    r""" The security ID of the local group which uniquely identifies the group. The group SID is automatically generated in POST and it is retrieved using the GET method.


Example: S-1-5-21-256008430-3394229847-3930036330-1001 """

    @property
    def resource(self):
        return LocalUserMembership

    gettable_fields = [
        "links",
        "name",
        "sid",
    ]
    """links,name,sid,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class LocalUserMembership(Resource):

    _schema = LocalUserMembershipSchema
