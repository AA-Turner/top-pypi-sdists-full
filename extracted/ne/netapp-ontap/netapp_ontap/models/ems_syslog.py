r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsSyslog", "EmsSyslogSchema"]
__pdoc__ = {
    "EmsSyslogSchema.resource": False,
    "EmsSyslogSchema.opts": False,
    "EmsSyslog": False,
}


class EmsSyslogSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsSyslog object"""

    format = marshmallow_fields.Nested("netapp_ontap.models.ems_syslog_format.EmsSyslogFormatSchema", unknown=EXCLUDE, data_key="format", allow_none=True)
    r""" The format field of the ems_syslog. """

    port = Size(data_key="port", allow_none=True)
    r""" Syslog Port.

Example: 514 """

    transport = marshmallow_fields.Str(data_key="transport", allow_none=True)
    r""" Syslog Transport Protocol.

Valid choices:

* udp_unencrypted
* tcp_unencrypted
* tcp_encrypted """

    @property
    def resource(self):
        return EmsSyslog

    gettable_fields = [
        "format",
        "port",
        "transport",
    ]
    """format,port,transport,"""

    patchable_fields = [
        "format",
        "port",
        "transport",
    ]
    """format,port,transport,"""

    postable_fields = [
        "format",
        "port",
        "transport",
    ]
    """format,port,transport,"""


class EmsSyslog(Resource):

    _schema = EmsSyslogSchema
