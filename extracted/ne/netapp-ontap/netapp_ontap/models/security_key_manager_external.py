r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityKeyManagerExternal", "SecurityKeyManagerExternalSchema"]
__pdoc__ = {
    "SecurityKeyManagerExternalSchema.resource": False,
    "SecurityKeyManagerExternalSchema.opts": False,
    "SecurityKeyManagerExternal": False,
}


class SecurityKeyManagerExternalSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityKeyManagerExternal object"""

    client_certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", unknown=EXCLUDE, data_key="client_certificate", allow_none=True)
    r""" The client_certificate field of the security_key_manager_external. """

    server_ca_certificates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", unknown=EXCLUDE, allow_none=True), data_key="server_ca_certificates", allow_none=True)
    r""" The array of certificates that are common for all the keyservers per SVM. """

    servers = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.key_server_readcreate.KeyServerReadcreateSchema", unknown=EXCLUDE, allow_none=True), data_key="servers", allow_none=True)
    r""" The set of external key servers. """

    @property
    def resource(self):
        return SecurityKeyManagerExternal

    gettable_fields = [
        "client_certificate.links",
        "client_certificate.name",
        "client_certificate.uuid",
        "server_ca_certificates.links",
        "server_ca_certificates.name",
        "server_ca_certificates.uuid",
        "servers",
    ]
    """client_certificate.links,client_certificate.name,client_certificate.uuid,server_ca_certificates.links,server_ca_certificates.name,server_ca_certificates.uuid,servers,"""

    patchable_fields = [
        "client_certificate.name",
        "client_certificate.uuid",
        "server_ca_certificates.name",
        "server_ca_certificates.uuid",
    ]
    """client_certificate.name,client_certificate.uuid,server_ca_certificates.name,server_ca_certificates.uuid,"""

    postable_fields = [
        "client_certificate.name",
        "client_certificate.uuid",
        "server_ca_certificates.name",
        "server_ca_certificates.uuid",
        "servers",
    ]
    """client_certificate.name,client_certificate.uuid,server_ca_certificates.name,server_ca_certificates.uuid,servers,"""


class SecurityKeyManagerExternal(Resource):

    _schema = SecurityKeyManagerExternalSchema
