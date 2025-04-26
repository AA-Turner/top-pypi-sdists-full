r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityOauth2Jwks", "SecurityOauth2JwksSchema"]
__pdoc__ = {
    "SecurityOauth2JwksSchema.resource": False,
    "SecurityOauth2JwksSchema.opts": False,
    "SecurityOauth2Jwks": False,
}


class SecurityOauth2JwksSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityOauth2Jwks object"""

    provider_uri = marshmallow_fields.Str(data_key="provider_uri", allow_none=True)
    r""" The URI on which the JSON Web Key Set (JWKS) are hosted.

Example: https://examplelab.customer.com/pf/JWKS """

    refresh_interval = marshmallow_fields.Str(data_key="refresh_interval", allow_none=True)
    r""" The refresh interval for the JSON Web Key Set (JWKS), in ISO-8601 format. This can be set to a value from 300 seconds to 2147483647 seconds.

Example: PT2H """

    @property
    def resource(self):
        return SecurityOauth2Jwks

    gettable_fields = [
        "provider_uri",
        "refresh_interval",
    ]
    """provider_uri,refresh_interval,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "provider_uri",
        "refresh_interval",
    ]
    """provider_uri,refresh_interval,"""


class SecurityOauth2Jwks(Resource):

    _schema = SecurityOauth2JwksSchema
