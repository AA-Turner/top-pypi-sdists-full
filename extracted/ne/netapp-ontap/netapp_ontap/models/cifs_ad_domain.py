r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsAdDomain", "CifsAdDomainSchema"]
__pdoc__ = {
    "CifsAdDomainSchema.resource": False,
    "CifsAdDomainSchema.opts": False,
    "CifsAdDomain": False,
}


class CifsAdDomainSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsAdDomain object"""

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" The account password of the user with permissions to reset the password in the organizational unit for the machine account. """

    user = marshmallow_fields.Str(data_key="user", allow_none=True)
    r""" The username of a user with permissions to reset the password in the organizational unit for the machine account. """

    @property
    def resource(self):
        return CifsAdDomain

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "password",
        "user",
    ]
    """password,user,"""

    postable_fields = [
        "password",
        "user",
    ]
    """password,user,"""


class CifsAdDomain(Resource):

    _schema = CifsAdDomainSchema
