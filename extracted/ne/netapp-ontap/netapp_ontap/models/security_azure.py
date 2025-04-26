r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityAzure", "SecurityAzureSchema"]
__pdoc__ = {
    "SecurityAzureSchema.resource": False,
    "SecurityAzureSchema.opts": False,
    "SecurityAzure": False,
}


class SecurityAzureSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityAzure object"""

    client_certificate = marshmallow_fields.Str(data_key="client_certificate", allow_none=True)
    r""" PKCS12 certificate used by the application to prove its identity to AKV.

Example: PEM Cert """

    client_id = marshmallow_fields.Str(data_key="client_id", allow_none=True)
    r""" Application client ID of the deployed Azure application with appropriate access to an AKV.

Example: aaaaaaaa-bbbb-aaaa-bbbb-aaaaaaaaaaaa """

    client_secret = marshmallow_fields.Str(data_key="client_secret", allow_none=True)
    r""" Secret used by the application to prove its identity to AKV.

Example: abcdef """

    key_vault = marshmallow_fields.Str(data_key="key_vault", allow_none=True)
    r""" URI of the deployed AKV that is used by ONTAP for storing keys.

Example: https://kmip-akv-keyvault.vault.azure.net/ """

    oauth_host = marshmallow_fields.Str(data_key="oauth_host", allow_none=True)
    r""" Open authorization server host name.

Example: login.microsoftonline.com """

    proxy = marshmallow_fields.Nested("netapp_ontap.models.security_proxy.SecurityProxySchema", unknown=EXCLUDE, data_key="proxy", allow_none=True)
    r""" The proxy field of the security_azure. """

    tenant_id = marshmallow_fields.Str(data_key="tenant_id", allow_none=True)
    r""" Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.

Example: zzzzzzzz-yyyy-zzzz-yyyy-zzzzzzzzzzzz """

    timeout = Size(data_key="timeout", allow_none=True)
    r""" AKV connection timeout, in seconds. The allowed range is between 0 to 30 seconds.

Example: 25 """

    verify_host = marshmallow_fields.Boolean(data_key="verify_host", allow_none=True)
    r""" Verify the identity of the AKV host name. By default, verify_host is set to true. """

    @property
    def resource(self):
        return SecurityAzure

    gettable_fields = [
        "proxy",
    ]
    """proxy,"""

    patchable_fields = [
        "proxy",
    ]
    """proxy,"""

    postable_fields = [
        "client_certificate",
        "client_id",
        "client_secret",
        "key_vault",
        "oauth_host",
        "proxy",
        "tenant_id",
        "timeout",
        "verify_host",
    ]
    """client_certificate,client_id,client_secret,key_vault,oauth_host,proxy,tenant_id,timeout,verify_host,"""


class SecurityAzure(Resource):

    _schema = SecurityAzureSchema
