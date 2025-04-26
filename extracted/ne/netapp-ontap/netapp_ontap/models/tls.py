r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["Tls", "TlsSchema"]
__pdoc__ = {
    "TlsSchema.resource": False,
    "TlsSchema.opts": False,
    "Tls": False,
}


class TlsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Tls object"""

    cipher_suites = marshmallow_fields.List(marshmallow_fields.Str, data_key="cipher_suites", allow_none=True)
    r""" Names a cipher suite that the system can select during TLS handshakes. A list of available options can be found on the Internet Assigned Number Authority (IANA) website. """

    protocol_versions = marshmallow_fields.List(marshmallow_fields.Str, data_key="protocol_versions", allow_none=True)
    r""" Names a TLS protocol version that the system can select during TLS handshakes. The use of SSLv3 or TLSv1 is discouraged. """

    @property
    def resource(self):
        return Tls

    gettable_fields = [
        "cipher_suites",
        "protocol_versions",
    ]
    """cipher_suites,protocol_versions,"""

    patchable_fields = [
        "cipher_suites",
        "protocol_versions",
    ]
    """cipher_suites,protocol_versions,"""

    postable_fields = [
        "cipher_suites",
        "protocol_versions",
    ]
    """cipher_suites,protocol_versions,"""


class Tls(Resource):

    _schema = TlsSchema
