r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityOauth2Introspection", "SecurityOauth2IntrospectionSchema"]
__pdoc__ = {
    "SecurityOauth2IntrospectionSchema.resource": False,
    "SecurityOauth2IntrospectionSchema.opts": False,
    "SecurityOauth2Introspection": False,
}


class SecurityOauth2IntrospectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityOauth2Introspection object"""

    endpoint_uri = marshmallow_fields.Str(data_key="endpoint_uri", allow_none=True)
    r""" The token introspection endpoint URI.

Example: https://examplelab.customer.com/token/introspect """

    interval = marshmallow_fields.Str(data_key="interval", allow_none=True)
    r""" The refresh interval for caching tokens, in ISO-8601 format. This can be set to the value \"disabled\" to disable caching of tokens. When set to 0, tokens are cached according to the expiry period in them. Otherwise, it can be set to a value from 1 second to 2147483647 seconds.

Example: PT1H """

    @property
    def resource(self):
        return SecurityOauth2Introspection

    gettable_fields = [
        "endpoint_uri",
        "interval",
    ]
    """endpoint_uri,interval,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "endpoint_uri",
        "interval",
    ]
    """endpoint_uri,interval,"""


class SecurityOauth2Introspection(Resource):

    _schema = SecurityOauth2IntrospectionSchema
