r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityProxy", "SecurityProxySchema"]
__pdoc__ = {
    "SecurityProxySchema.resource": False,
    "SecurityProxySchema.opts": False,
    "SecurityProxy": False,
}


class SecurityProxySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityProxy object"""

    host = marshmallow_fields.Str(data_key="host", allow_none=True)
    r""" Proxy host.

Example: proxy.eng.com """

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" Proxy password. Password is not audited.

Example: proxypassword """

    port = Size(data_key="port", allow_none=True)
    r""" Proxy port.

Example: 1234 """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Proxy type.

Valid choices:

* http
* https """

    username = marshmallow_fields.Str(data_key="username", allow_none=True)
    r""" Proxy username.

Example: proxyuser """

    @property
    def resource(self):
        return SecurityProxy

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "host",
        "password",
        "port",
        "type",
        "username",
    ]
    """host,password,port,type,username,"""


class SecurityProxy(Resource):

    _schema = SecurityProxySchema
