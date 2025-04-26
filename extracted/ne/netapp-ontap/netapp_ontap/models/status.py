r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Status", "StatusSchema"]
__pdoc__ = {
    "StatusSchema.resource": False,
    "StatusSchema.opts": False,
    "Status": False,
}


class StatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Status object"""

    code = Size(data_key="code", allow_none=True)
    r""" Code corresponding to the status message. Code is 0 when the state is 'up'.


Example: 6684732 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Detailed description of the validation state if the state is 'down' or
the response time of the DNS server if the state is 'up'. """

    name_server = marshmallow_fields.Str(data_key="name_server", allow_none=True)
    r""" The IP address of the DNS server. The address can be either an IPv4 or an IPv6 address.


Example: 10.10.10.10 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The validation status of the DNS server.


Valid choices:

* up
* down """

    @property
    def resource(self):
        return Status

    gettable_fields = [
        "code",
        "message",
        "name_server",
        "state",
    ]
    """code,message,name_server,state,"""

    patchable_fields = [
        "code",
        "message",
        "name_server",
        "state",
    ]
    """code,message,name_server,state,"""

    postable_fields = [
        "code",
        "message",
        "name_server",
        "state",
    ]
    """code,message,name_server,state,"""


class Status(Resource):

    _schema = StatusSchema
