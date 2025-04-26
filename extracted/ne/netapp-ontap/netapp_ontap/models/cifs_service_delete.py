r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsServiceDelete", "CifsServiceDeleteSchema"]
__pdoc__ = {
    "CifsServiceDeleteSchema.resource": False,
    "CifsServiceDeleteSchema.opts": False,
    "CifsServiceDelete": False,
}


class CifsServiceDeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsServiceDelete object"""

    ad_domain = marshmallow_fields.Nested("netapp_ontap.models.ad_domain_delete.AdDomainDeleteSchema", unknown=EXCLUDE, data_key="ad_domain", allow_none=True)
    r""" The ad_domain field of the cifs_service_delete. """

    auth_user_type = marshmallow_fields.Str(data_key="auth_user_type", allow_none=True)
    r""" Specifies the type of user who can access the SMB Volume. The default is domain_user. In the case of a hybrid-user, ONTAP won't contact on-premise ADDS.


Valid choices:

* domain_user
* hybrid_user """

    authentication_method = marshmallow_fields.Str(data_key="authentication_method", allow_none=True)
    r""" Specifies the authentication method.
The available values are:

  * client_secret
  * certificate


Valid choices:

* client_secret
* certificate """

    client_certificate = marshmallow_fields.Str(data_key="client_certificate", allow_none=True)
    r""" PKCS12 certificate used by the application to prove its identity to AKV.

Example: PEM Cert """

    client_id = marshmallow_fields.Str(data_key="client_id", allow_none=True)
    r""" Application client ID of the deployed Azure application with appropriate access to an AKV or EntraId.

Example: e959d1b5-5a63-4284-9268-851e30e3eceb """

    client_secret = marshmallow_fields.Str(data_key="client_secret", allow_none=True)
    r""" Secret used by the application to prove its identity to AKV.

Example: _8E8Q~Qu866jtihUE3ia4Q5Y5IDEVC6UfskbZa6X """

    key_vault_uri = marshmallow_fields.Str(data_key="key_vault_uri", allow_none=True)
    r""" URI of the deployed AKV that is used by ONTAP for storing keys.

Example: https://kmip-akv-keyvault.vault.azure.net/ """

    oauth_host = marshmallow_fields.Str(data_key="oauth_host", allow_none=True)
    r""" Open authorization server host name.

Example: login.microsoftonline.com """

    proxy_host = marshmallow_fields.Str(data_key="proxy_host", allow_none=True)
    r""" Proxy host.

Example: proxy.eng.com """

    proxy_password = marshmallow_fields.Str(data_key="proxy_password", allow_none=True)
    r""" Proxy password. Password is not audited.

Example: proxypassword """

    proxy_port = Size(data_key="proxy_port", allow_none=True)
    r""" Proxy port.

Example: 1234 """

    proxy_type = marshmallow_fields.Str(data_key="proxy_type", allow_none=True)
    r""" Proxy type.

Valid choices:

* http
* https """

    proxy_username = marshmallow_fields.Str(data_key="proxy_username", allow_none=True)
    r""" Proxy username.

Example: proxyuser """

    tenant_id = marshmallow_fields.Str(data_key="tenant_id", allow_none=True)
    r""" Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV or EntraId.

Example: c9f32fcb-4ab7-40fe-af1b-1850d46cfbbe """

    timeout = Size(data_key="timeout", allow_none=True)
    r""" AKV connection timeout, in seconds. The allowed range is between 0 to 30 seconds.

Example: 25 """

    verify_host = marshmallow_fields.Boolean(data_key="verify_host", allow_none=True)
    r""" Verify the identity of the AKV host name. By default, verify_host is set to true. """

    workgroup = marshmallow_fields.Str(data_key="workgroup", allow_none=True)
    r""" The workgroup name.

Example: workgrp1 """

    @property
    def resource(self):
        return CifsServiceDelete

    gettable_fields = [
        "ad_domain",
        "auth_user_type",
        "authentication_method",
        "client_id",
        "key_vault_uri",
        "oauth_host",
        "proxy_host",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "tenant_id",
        "timeout",
        "verify_host",
        "workgroup",
    ]
    """ad_domain,auth_user_type,authentication_method,client_id,key_vault_uri,oauth_host,proxy_host,proxy_port,proxy_type,proxy_username,tenant_id,timeout,verify_host,workgroup,"""

    patchable_fields = [
        "ad_domain",
        "auth_user_type",
        "authentication_method",
        "client_certificate",
        "client_id",
        "client_secret",
        "key_vault_uri",
        "oauth_host",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "tenant_id",
        "timeout",
        "verify_host",
        "workgroup",
    ]
    """ad_domain,auth_user_type,authentication_method,client_certificate,client_id,client_secret,key_vault_uri,oauth_host,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,tenant_id,timeout,verify_host,workgroup,"""

    postable_fields = [
        "ad_domain",
        "auth_user_type",
        "authentication_method",
        "client_certificate",
        "client_id",
        "client_secret",
        "key_vault_uri",
        "oauth_host",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "tenant_id",
        "timeout",
        "verify_host",
        "workgroup",
    ]
    """ad_domain,auth_user_type,authentication_method,client_certificate,client_id,client_secret,key_vault_uri,oauth_host,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,tenant_id,timeout,verify_host,workgroup,"""


class CifsServiceDelete(Resource):

    _schema = CifsServiceDeleteSchema
