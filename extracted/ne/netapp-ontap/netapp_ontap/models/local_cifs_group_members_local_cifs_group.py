r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LocalCifsGroupMembersLocalCifsGroup", "LocalCifsGroupMembersLocalCifsGroupSchema"]
__pdoc__ = {
    "LocalCifsGroupMembersLocalCifsGroupSchema.resource": False,
    "LocalCifsGroupMembersLocalCifsGroupSchema.opts": False,
    "LocalCifsGroupMembersLocalCifsGroup": False,
}


class LocalCifsGroupMembersLocalCifsGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalCifsGroupMembersLocalCifsGroup object"""

    sid = marshmallow_fields.Str(data_key="sid", allow_none=True)
    r""" The security ID of the local group which uniquely identifies the group. The group SID is automatically generated in POST and it is retrieved using the GET method.


Example: S-1-5-21-256008430-3394229847-3930036330-1001 """

    @property
    def resource(self):
        return LocalCifsGroupMembersLocalCifsGroup

    gettable_fields = [
        "sid",
    ]
    """sid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LocalCifsGroupMembersLocalCifsGroup(Resource):

    _schema = LocalCifsGroupMembersLocalCifsGroupSchema
