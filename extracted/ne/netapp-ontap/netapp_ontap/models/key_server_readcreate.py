r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["KeyServerReadcreate", "KeyServerReadcreateSchema"]
__pdoc__ = {
    "KeyServerReadcreateSchema.resource": False,
    "KeyServerReadcreateSchema.opts": False,
    "KeyServerReadcreate": False,
}


class KeyServerReadcreateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyServerReadcreate object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the key_server_readcreate. """

    connectivity = marshmallow_fields.Nested("netapp_ontap.models.key_server_state_array.KeyServerStateArraySchema", unknown=EXCLUDE, data_key="connectivity", allow_none=True)
    r""" A container for holding an array of the key server connectivity state for each node. """

    secondary_key_servers = marshmallow_fields.Str(data_key="secondary_key_servers", allow_none=True)
    r""" A comma delimited string of the secondary key servers associated with the primary key server.

Example: secondary1.com, 10.2.3.4 """

    server = marshmallow_fields.Str(data_key="server", allow_none=True)
    r""" External key server for key management. If no port is provided, a default port of 5696 is used.

Example: keyserver1.com:5698 """

    timeout = Size(data_key="timeout", allow_none=True)
    r""" I/O timeout in seconds for communicating with the key server.

Example: 60 """

    username = marshmallow_fields.Str(data_key="username", allow_none=True)
    r""" Username credentials for connecting with the key server.

Example: admin """

    @property
    def resource(self):
        return KeyServerReadcreate

    gettable_fields = [
        "links",
        "connectivity",
        "secondary_key_servers",
        "server",
        "timeout",
        "username",
    ]
    """links,connectivity,secondary_key_servers,server,timeout,username,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "server",
    ]
    """server,"""


class KeyServerReadcreate(Resource):

    _schema = KeyServerReadcreateSchema
