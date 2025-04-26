r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["KeyServerNoRecords", "KeyServerNoRecordsSchema"]
__pdoc__ = {
    "KeyServerNoRecordsSchema.resource": False,
    "KeyServerNoRecordsSchema.opts": False,
    "KeyServerNoRecords": False,
}


class KeyServerNoRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyServerNoRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the key_server_no_records. """

    connectivity = marshmallow_fields.Nested("netapp_ontap.models.key_server_state_array.KeyServerStateArraySchema", unknown=EXCLUDE, data_key="connectivity", allow_none=True)
    r""" A container for holding an array of the key server connectivity state for each node. """

    password = marshmallow_fields.Str(data_key="password", allow_none=True)
    r""" Password credentials for connecting with the key server. This is not audited.

Example: password """

    server = marshmallow_fields.Str(data_key="server", allow_none=True)
    r""" External key server for key management. If no port is provided, a default port of 5696 is used. Not valid in POST if `records` is provided.

Example: bulkkeyserver.com:5698 """

    timeout = Size(data_key="timeout", allow_none=True)
    r""" I/O timeout in seconds for communicating with the key server.

Example: 60 """

    username = marshmallow_fields.Str(data_key="username", allow_none=True)
    r""" KMIP username credentials for connecting with the key server.

Example: username """

    @property
    def resource(self):
        return KeyServerNoRecords

    gettable_fields = [
        "links",
        "connectivity",
        "server",
        "timeout",
        "username",
    ]
    """links,connectivity,server,timeout,username,"""

    patchable_fields = [
        "password",
        "timeout",
        "username",
    ]
    """password,timeout,username,"""

    postable_fields = [
        "server",
    ]
    """server,"""


class KeyServerNoRecords(Resource):

    _schema = KeyServerNoRecordsSchema
