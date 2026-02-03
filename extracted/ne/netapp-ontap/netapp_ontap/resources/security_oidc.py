r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to manage the OpenID Connect (OIDC) authentication configuration for the cluster. The POST method is used to create a new OIDC configuration, while the GET method is used to retrieve the current OIDC configuration.
The PATCH method is used to enable or disable the OIDC feature, and the DELETE method is used to remove an existing OIDC configuration.
<br />
---
## Examples
### Retrieving the OIDC configuration in the cluster
The following output shows the OIDC configuration in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityOidc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityOidc()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecurityOidc(
    {
        "_links": {"self": {"href": "/api/security/authentication/cluster/oidc"}},
        "remote_user_claim": "unique_name",
        "authorization_endpoint": "https://example.com/adfs/oauth2/authorize/",
        "access_token_issuer": "https://example.com/adfs/services/trust",
        "redirect_ipaddress": "10.10.10.10",
        "client_secret_hash": "<HASHED-CLIENT-SECRET>",
        "issuer": "https://example.com/adfs",
        "client_id": "client-id-value",
        "jwks_refresh_interval": "PT1H",
        "provider": "adfs",
        "outgoing_proxy": "https://johndoe:secretpass@proxy.example.com:8080",
        "token_endpoint": "https://example.com/adfs/oauth2/token/",
        "provider_jwks_uri": "https://example.com/adfs/discovery/keys",
        "skip_uri_validation": False,
        "end_session_endpoint": "https://example.com/adfs/oauth2/logout",
        "enabled": False,
    }
)

```
</div>
</div>

---
### Creating the OIDC configuration in the cluster
The following output shows how to create the OIDC configuration in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityOidc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityOidc()
    resource.provider = "adfs"
    resource.issuer = "https://example.com/adfs"
    resource.client_id = "client-id-value"
    resource.client_secret = "<CLIENT-SECRET>"
    resource.provider_jwks_uri = "https://example.com/adfs/discovery/keys"
    resource.remote_user_claim = "unique_name"
    resource.authorization_endpoint = "https://example.com/adfs/oauth2/authorize/"
    resource.token_endpoint = "https://example.com/adfs/oauth2/token/"
    resource.skip_uri_validation = False
    resource.redirect_ipaddress = "10.10.10.10"
    resource.end_session_endpoint = "https://example.com/adfs/oauth2/logout"
    resource.jwks_refresh_interval = "PT1H"
    resource.outgoing_proxy = "https://johndoe:secretpass@proxy.example.com:8080"
    resource.access_token_issuer = "https://example.com/adfs/services/trust"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SecurityOidc(
    {
        "remote_user_claim": "unique_name",
        "authorization_endpoint": "https://example.com/adfs/oauth2/authorize/",
        "access_token_issuer": "https://example.com/adfs/services/trust",
        "redirect_ipaddress": "10.10.10.10",
        "issuer": "https://example.com/adfs",
        "client_id": "client-id-value",
        "jwks_refresh_interval": "PT1H",
        "client_secret": "<CLIENT-SECRET>",
        "provider": "adfs",
        "outgoing_proxy": "https://johndoe:secretpass@proxy.example.com:8080",
        "token_endpoint": "https://example.com/adfs/oauth2/token/",
        "provider_jwks_uri": "https://example.com/adfs/discovery/keys",
        "skip_uri_validation": False,
        "end_session_endpoint": "https://example.com/adfs/oauth2/logout",
    }
)

```
</div>
</div>

---
### Updating the OIDC configuration in the cluster
The following output shows how to update the OIDC configuration in the cluster.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityOidc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityOidc()
    resource.enabled = True
    resource.patch()

```

---
### Deleting the OIDC configuration in the cluster
The following output shows how to delete the OIDC configuration in the cluster.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityOidc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityOidc()
    resource.delete()

```
"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SecurityOidc", "SecurityOidcSchema"]
__pdoc__ = {
    "SecurityOidcSchema.resource": False,
    "SecurityOidcSchema.opts": False,
}

class SecurityOidcSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityOidc object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the security_oidc."""

    access_token_issuer = marshmallow_fields.Str(
        data_key="access_token_issuer",
        allow_none=True,
    )
    r""" The issuer value for the access token when it is different from the OpenID Connect issuer.

Example: https://example.netapp.com/adfs/services/trust"""

    authorization_endpoint = marshmallow_fields.Str(
        data_key="authorization_endpoint",
        allow_none=True,
    )
    r""" The URI of the authorization endpoint for the OpenID Connect provider.

Example: https://example.netapp.com/adfs/oauth2/authorize"""

    client_id = marshmallow_fields.Str(
        data_key="client_id",
        allow_none=True,
    )
    r""" The client ID for the application.

Example: 1234567890abcdef"""

    client_secret = marshmallow_fields.Str(
        data_key="client_secret",
        allow_none=True,
    )
    r""" The client secret for the application.

Example: 1234567890abcdef1234567890abcdef"""

    client_secret_hash = marshmallow_fields.Str(
        data_key="client_secret_hash",
        allow_none=True,
    )
    r""" The hash of the client secret for the application.

Example: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether the OpenID Connect configuration is enabled.

Example: true"""

    end_session_endpoint = marshmallow_fields.Str(
        data_key="end_session_endpoint",
        allow_none=True,
    )
    r""" The URI of the end session endpoint for the OpenID Connect provider.

Example: https://example.netapp.com/adfs/oauth2/logout"""

    issuer = marshmallow_fields.Str(
        data_key="issuer",
        allow_none=True,
    )
    r""" The URI of the OpenID Connect provider.

Example: https://example.netapp.com/adfs"""

    jwks_refresh_interval = marshmallow_fields.Str(
        data_key="jwks_refresh_interval",
        allow_none=True,
    )
    r""" The refresh interval for the JSON Web Key Set (JWKS), in ISO-8601 format. This can be set to a value from 300 seconds to 2147483647 seconds.

Example: PT2H"""

    outgoing_proxy = marshmallow_fields.Str(
        data_key="outgoing_proxy",
        allow_none=True,
    )
    r""" Outgoing proxy to access external identity providers (IdPs). If not specified, no proxy is configured.

Example: https://johndoe:secretpass@proxy.example.com:8080"""

    provider = marshmallow_fields.Str(
        data_key="provider",
        validate=enum_validation(['adfs', 'entra']),
        allow_none=True,
    )
    r""" The OpenID Connect provider type.

Valid choices:

* adfs
* entra"""

    provider_jwks_uri = marshmallow_fields.Str(
        data_key="provider_jwks_uri",
        allow_none=True,
    )
    r""" The URI of the JSON Web Key Set (JWKS) for the OpenID Connect provider.

Example: https://example.netapp.com/adfs/discovery/v2.0/keys"""

    redirect_ipaddress = marshmallow_fields.Str(
        data_key="redirect_ipaddress",
        allow_none=True,
    )
    r""" The IP address to redirect to after authentication.

Example: 10.10.10.10"""

    remote_user_claim = marshmallow_fields.Str(
        data_key="remote_user_claim",
        allow_none=True,
    )
    r""" The claim used to identify the remote user.

Example: unique_name"""

    skip_uri_validation = marshmallow_fields.Boolean(
        data_key="skip_uri_validation",
        allow_none=True,
    )
    r""" Indicates whether to skip URI validation.

Example: false"""

    token_endpoint = marshmallow_fields.Str(
        data_key="token_endpoint",
        allow_none=True,
    )
    r""" The URI of the token endpoint for the OpenID Connect provider.

Example: https://example.netapp.com/adfs/oauth2/token"""

    @property
    def resource(self):
        return SecurityOidc

    gettable_fields = [
        "links",
        "access_token_issuer",
        "authorization_endpoint",
        "client_id",
        "client_secret",
        "client_secret_hash",
        "enabled",
        "end_session_endpoint",
        "issuer",
        "jwks_refresh_interval",
        "outgoing_proxy",
        "provider",
        "provider_jwks_uri",
        "redirect_ipaddress",
        "remote_user_claim",
        "skip_uri_validation",
        "token_endpoint",
    ]
    """links,access_token_issuer,authorization_endpoint,client_id,client_secret,client_secret_hash,enabled,end_session_endpoint,issuer,jwks_refresh_interval,outgoing_proxy,provider,provider_jwks_uri,redirect_ipaddress,remote_user_claim,skip_uri_validation,token_endpoint,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "access_token_issuer",
        "authorization_endpoint",
        "client_id",
        "client_secret",
        "end_session_endpoint",
        "issuer",
        "jwks_refresh_interval",
        "outgoing_proxy",
        "provider",
        "provider_jwks_uri",
        "redirect_ipaddress",
        "remote_user_claim",
        "skip_uri_validation",
        "token_endpoint",
    ]
    """access_token_issuer,authorization_endpoint,client_id,client_secret,end_session_endpoint,issuer,jwks_refresh_interval,outgoing_proxy,provider,provider_jwks_uri,redirect_ipaddress,remote_user_claim,skip_uri_validation,token_endpoint,"""

class SecurityOidc(Resource):
    """Allows interaction with SecurityOidc objects on the host"""

    _schema = SecurityOidcSchema
    _path = "/api/security/authentication/cluster/oidc"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the OIDC configuration in the cluster.
### Related ONTAP commands
* `security oidc show`

### Learn more
* [`DOC /security/authentication/cluster/oidc`](#docs-security-security_authentication_cluster_oidc)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates the OIDC configuration in the cluster.
### Optional properties
* `skip_uri_validation`
* `jwks_refresh_interval`
* `outgoing_proxy`
* `access_token_issuer`
### Related ONTAP commands
* `security oidc create`

### Learn more
* [`DOC /security/authentication/cluster/oidc`](#docs-security-security_authentication_cluster_oidc)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the OIDC configuration in the cluster.
### Required properties
* `enabled`
### Related ONTAP commands
* `security oidc modify`

### Learn more
* [`DOC /security/authentication/cluster/oidc`](#docs-security-security_authentication_cluster_oidc)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the OIDC configuration in the cluster.
### Related ONTAP commands
* `security oidc delete`

### Learn more
* [`DOC /security/authentication/cluster/oidc`](#docs-security-security_authentication_cluster_oidc)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


