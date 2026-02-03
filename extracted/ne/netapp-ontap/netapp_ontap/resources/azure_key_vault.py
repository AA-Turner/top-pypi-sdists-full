r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Azure Key Vault (AKV) is a cloud key management service (KMS) that provides a secure store for secrets. This feature
allows ONTAP to securely store its encryption keys using AKV.
In order to use AKV with ONTAP, you must first deploy an Azure application with the appropriate access to an AKV and then provide
ONTAP with the necessary details, such as key vault name, application ID so that ONTAP can communicate with the deployed Azure application.
The properties "state", "azure_reachability" and "ekmip_reachability" are considered advanced properties and are populated only when explicitly requested.
## Examples
### Enabling an AKV configuration for an SVM using the certificate authentication method
The example AKV configuration is enabled for a specific SVM. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key-manager keystore configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault()
    resource.svm = {"uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"}
    resource.client_id = "client1"
    resource.tenant_id = "tenant1"
    resource.name = "https:://mykeyvault.vault.azure.net/"
    resource.key_id = "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74"
    resource.client_certificate = "<CERTIFICATE-CONTENT>"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AzureKeyVault(
    {
        "tenant_id": "tenant1",
        "name": "https:://mykeyvault.vault.azure.net/",
        "client_id": "client1",
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/024cd3cf-9a08-11ea-8d52-005056bbeba5"
            }
        },
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
        "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
        "svm": {"name": "vs0", "uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"},
    }
)

```
</div>
</div>

---
### Creating an inactive AKV configuration for an SVM using the client secret authentication method
The example AKV configuration is created for a specific SVM but is not enabled.
Note the <i>create_inactive=true</i> parameter that is used to indicate that the configuration should be created but not enabled.
Note the <i>return_records=true</i> query parameter is used to obtain the newly created key-manager keystore configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault()
    resource.svm = {"uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"}
    resource.configuration = {"name": "myConfiguration"}
    resource.client_id = "client1"
    resource.tenant_id = "tenant1"
    resource.name = "https:://mykeyvault.vault.azure.net/"
    resource.key_id = "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74"
    resource.client_secret = "myclientPwd"
    resource.post(hydrate=True, create_inactive=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
AzureKeyVault(
    {
        "tenant_id": "tenant1",
        "configuration": {"name": "myConfiguration"},
        "name": "https:://mykeyvault.vault.azure.net/",
        "client_id": "client1",
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
            }
        },
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
        "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
    }
)

```
</div>
</div>

---
### Retrieving the AKVs configured for all clusters and SVMs
The following example shows how to retrieve all configured AKVs along with their configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(AzureKeyVault.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    AzureKeyVault(
        {
            "tenant_id": "tenant1",
            "authentication_method": "client_secret",
            "configuration": {
                "name": "default",
                "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
            },
            "name": "https:://mykeyvault.vault.azure.net/",
            "client_id": "client1",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/security/azure-key-vaults/024cd3cf-9a08-11ea-8d52-005056bbeba5"
                }
            },
            "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
            "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
            "scope": "svm",
            "svm": {"name": "vs0", "uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"},
        }
    ),
    AzureKeyVault(
        {
            "tenant_id": "tenant1",
            "authentication_method": "certificate",
            "configuration": {
                "name": "new-config",
                "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
            },
            "name": "https:://mykeyvault.vault.azure.net/",
            "client_id": "client1",
            "enabled": False,
            "_links": {
                "self": {
                    "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
                }
            },
            "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
            "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
            "scope": "cluster",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific AKV configuration
The following example retrieves a specific AKV configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
AzureKeyVault(
    {
        "tenant_id": "tenant1",
        "authentication_method": "client_secret",
        "configuration": {
            "name": "default",
            "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
        },
        "name": "https:://mykeyvault.vault.azure.net/",
        "client_id": "client1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
            }
        },
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
        "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
        "scope": "cluster",
    }
)

```
</div>
</div>

---
### Retrieving the advanced properties of a specific, enabled AKV configuration
The following example retrieves the advanced properties of a specific enabled AKV configuration (inactive AKV configurations do not have these advanced properties).
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.get(fields='state,azure_reachability,ekmip_reachability"')
    print(resource)

```

---
### Updating the client secret of a specific AKV configuration
The following example updates the client secret of a specific AKV configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.client_secret = "<NEW-SECRET>"
    resource.patch()

```

---
### Updating the client certificate and key of a specific AKV configuration
The following example updates the client certificate and key of a configured AKV for a specific AKV configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.client_certificate = "<CERTIFICATE-CONTENT>"
    resource.patch()

```

---
### Deleting a specific AKV configuration
The following example deletes a specific, enabled AKV.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.delete()

```

---
### Restoring the keys for a specific AKV configuration
The following example restores all the keys of a specific AKV configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.restore()

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
AzureKeyVault({})

```
</div>
</div>

---
### Rekeying the internal key for a specific AKV configuration
The following example rekeys the internal key of a specific AKV configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.rekey_internal()

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
AzureKeyVault({})

```
</div>
</div>

---"""

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


__all__ = ["AzureKeyVault", "AzureKeyVaultSchema"]
__pdoc__ = {
    "AzureKeyVaultSchema.resource": False,
    "AzureKeyVaultSchema.opts": False,
}

class AzureKeyVaultSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AzureKeyVault object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the azure_key_vault."""

    authentication_method = marshmallow_fields.Str(
        data_key="authentication_method",
        validate=enum_validation(['client_secret', 'certificate']),
        allow_none=True,
    )
    r""" Authentication method for the AKV instance.

Valid choices:

* client_secret
* certificate"""

    azure_reachability = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.azure_key_vault_connectivity", "AzureKeyVaultConnectivitySchema"),
                data_key="azure_reachability",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Indicates whether or not the AKV service is reachable from all the nodes in the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    client_certificate = marshmallow_fields.Str(
        data_key="client_certificate",
        allow_none=True,
    )
    r""" PKCS12 Certificate used by the application to prove its identity to AKV.

Example: <CERTIFICATE-CONTENT>"""

    client_id = marshmallow_fields.Str(
        data_key="client_id",
        allow_none=True,
    )
    r""" Application client ID of the deployed Azure application with appropriate access to an AKV.

Example: aaaaaaaa-bbbb-aaaa-bbbb-aaaaaaaaaaaa"""

    client_secret = marshmallow_fields.Str(
        data_key="client_secret",
        allow_none=True,
    )
    r""" Secret used by the application to prove its identity to AKV.

Example: abcdef"""

    configuration = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.security_keystore_configuration", "SecurityKeystoreConfigurationSchema"),
                data_key="configuration",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Security keystore object reference."""

    ekmip_reachability = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.aws_kms_ekmip_reachability", "AwsKmsEkmipReachabilitySchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="ekmip_reachability",
                allow_none=True
            )
    r""" Provides the connectivity status for the given SVM on the given node to all EKMIP servers configured on all nodes of the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether the configuration is enabled."""

    key_id = marshmallow_fields.Str(
        data_key="key_id",
        allow_none=True,
    )
    r""" Key Identifier of AKV key encryption key.

Example: https://keyvault1.vault.azure.net/keys/key1/12345678901234567890123456789012"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the deployed AKV that will be used by ONTAP for storing keys.

Example: https://kmip-akv-keyvault.vault.azure.net/"""

    oauth_host = marshmallow_fields.Str(
        data_key="oauth_host",
        allow_none=True,
    )
    r""" Open authorization server host name.

Example: login.microsoftonline.com"""

    port = Size(
        data_key="port",
        allow_none=True,
    )
    r""" Authorization server and vault port number.

Example: 443"""

    proxy_host = marshmallow_fields.Str(
        data_key="proxy_host",
        allow_none=True,
    )
    r""" Proxy host.

Example: proxy.eng.com"""

    proxy_password = marshmallow_fields.Str(
        data_key="proxy_password",
        allow_none=True,
    )
    r""" Proxy password. Password is not audited.

Example: proxypassword"""

    proxy_port = Size(
        data_key="proxy_port",
        allow_none=True,
    )
    r""" Proxy port.

Example: 1234"""

    proxy_type = marshmallow_fields.Str(
        data_key="proxy_type",
        validate=enum_validation(['http', 'https']),
        allow_none=True,
    )
    r""" Type of proxy.

Valid choices:

* http
* https"""

    proxy_username = marshmallow_fields.Str(
        data_key="proxy_username",
        allow_none=True,
    )
    r""" Proxy username.

Example: proxyuser"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster"""

    skip_verification = marshmallow_fields.Boolean(
        data_key="skip_verification",
        allow_none=True,
    )
    r""" Set to true to skip the verification of the updated user credentials when updating credentials. The default value is false.

Example: false"""

    state = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.azure_key_vault_state", "AzureKeyVaultStateSchema"),
                data_key="state",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Indicates whether or not the AKV wrapped internal key is available cluster wide.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                data_key="svm",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The svm field of the azure_key_vault."""

    tenant_id = marshmallow_fields.Str(
        data_key="tenant_id",
        allow_none=True,
    )
    r""" Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.

Example: zzzzzzzz-yyyy-zzzz-yyyy-zzzzzzzzzzzz"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" A unique identifier for the Azure Key Vault (AKV).

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    vault_host = marshmallow_fields.Str(
        data_key="vault_host",
        allow_none=True,
    )
    r""" AKV host subdomain.

Example: vault.azure.net"""

    verify_host = marshmallow_fields.Boolean(
        data_key="verify_host",
        allow_none=True,
    )
    r""" Verify the identity of the AKV host name.

Example: false"""

    verify_ip = marshmallow_fields.Boolean(
        data_key="verify_ip",
        allow_none=True,
    )
    r""" Verify the identity of the AKV IP address.

Example: false"""

    @property
    def resource(self):
        return AzureKeyVault

    gettable_fields = [
        "links",
        "authentication_method",
        "azure_reachability",
        "client_id",
        "configuration",
        "ekmip_reachability",
        "enabled",
        "key_id",
        "name",
        "oauth_host",
        "port",
        "proxy_host",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "scope",
        "skip_verification",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tenant_id",
        "uuid",
        "vault_host",
        "verify_host",
        "verify_ip",
    ]
    """links,authentication_method,azure_reachability,client_id,configuration,ekmip_reachability,enabled,key_id,name,oauth_host,port,proxy_host,proxy_port,proxy_type,proxy_username,scope,skip_verification,state,svm.links,svm.name,svm.uuid,tenant_id,uuid,vault_host,verify_host,verify_ip,"""

    patchable_fields = [
        "client_certificate",
        "client_id",
        "client_secret",
        "oauth_host",
        "port",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "skip_verification",
        "tenant_id",
        "vault_host",
        "verify_host",
        "verify_ip",
    ]
    """client_certificate,client_id,client_secret,oauth_host,port,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,skip_verification,tenant_id,vault_host,verify_host,verify_ip,"""

    postable_fields = [
        "client_certificate",
        "client_id",
        "client_secret",
        "configuration",
        "key_id",
        "name",
        "oauth_host",
        "port",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "skip_verification",
        "svm.name",
        "svm.uuid",
        "tenant_id",
        "vault_host",
    ]
    """client_certificate,client_id,client_secret,configuration,key_id,name,oauth_host,port,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,skip_verification,svm.name,svm.uuid,tenant_id,vault_host,"""

class AzureKeyVault(Resource):
    """Allows interaction with AzureKeyVault objects on the host"""

    _schema = AzureKeyVaultSchema
    _path = "/api/security/azure-key-vaults"
    _keys = ["uuid"]
    _action_form_data_parameters = { 'file':'file', }

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves AKVs configured for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external azure show`
* `security key-manager external azure check`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all AzureKeyVault resources that match the provided query"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def fast_get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["RawResource"]:
        """Returns a list of RawResources that represent AzureKeyVault resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["AzureKeyVault"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the AKV configuration.
### Optional properties
* `client_secret` or `client_certificate` - New secret or new PKCS12 certificate used to prove the application's identity to the AKV.
* `proxy_type` - Type of proxy (http, https etc.) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `port` - Authorization server and vault port number.
* `oauth_host` - Open authorization server host name.
* `vault_host` - AKV host subdomain.
* `verify_host` - Verify the identity of the AKV host name.
* `verify_ip ` - Verify the identity of the AKV IP address.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `client_id` - Application (client) ID of the deployed Azure application with appropriate access to an AKV.
* `tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
* `skip_verification` - Skip the verification of the updated credentials, set to true to bypass the verification. The default value is false.
### Related ONTAP commands
* `security key-manager external azure update-client-secret`
* `security key-manager external azure update-credentials`
* `security key-manager external azure update-config`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["AzureKeyVault"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["AzureKeyVault"], NetAppResponse]:
        r"""Configures the AKV configuration for all clusters and SVMs.
### Required properties:
* `svm.uuid` or `svm.name` - Existing SVM in which to create a AKV.
* `client_id` - Application (client) ID of the deployed Azure application with appropriate access to an AKV.
* `tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
* `client_secret` or `client_certificate` - Secret or PKCS12 Certificate used by the application to prove its identity to AKV.
* `key_id`- Key Identifier of AKV encryption key.
* `name` - Name of the deployed AKV used by ONTAP for storing keys.
### Optional properties:
* `port` - Authorization server and vault port number.
* `oauth_host` - Open authorization server host name.
* `vault_host` - AKV host subdomain.
* `proxy_type` - Type of proxy (http, https etc.) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `configuration.name` - The configuration name to use when also setting the `create_inactive` flag.
### Optional parameters:
* `create_inactive` - Create an AKV configuration without enabling it. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external azure enable`
* `security key-manager external azure create-config`
* `security key-manager external azure update-config`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["AzureKeyVault"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an AKV configuration.
### Related ONTAP commands
* `security key-manager external azure disable`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves AKVs configured for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external azure show`
* `security key-manager external azure check`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the AKV configuration for the SVM specified by the UUID.
### Related ONTAP commands
* `security key-manager external azure show`
* `security key-manager external azure check`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
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
        r"""Configures the AKV configuration for all clusters and SVMs.
### Required properties:
* `svm.uuid` or `svm.name` - Existing SVM in which to create a AKV.
* `client_id` - Application (client) ID of the deployed Azure application with appropriate access to an AKV.
* `tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
* `client_secret` or `client_certificate` - Secret or PKCS12 Certificate used by the application to prove its identity to AKV.
* `key_id`- Key Identifier of AKV encryption key.
* `name` - Name of the deployed AKV used by ONTAP for storing keys.
### Optional properties:
* `port` - Authorization server and vault port number.
* `oauth_host` - Open authorization server host name.
* `vault_host` - AKV host subdomain.
* `proxy_type` - Type of proxy (http, https etc.) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `configuration.name` - The configuration name to use when also setting the `create_inactive` flag.
### Optional parameters:
* `create_inactive` - Create an AKV configuration without enabling it. This flag is set to "false" by default.
### Related ONTAP commands
* `security key-manager external azure enable`
* `security key-manager external azure create-config`
* `security key-manager external azure update-config`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
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
        r"""Updates the AKV configuration.
### Optional properties
* `client_secret` or `client_certificate` - New secret or new PKCS12 certificate used to prove the application's identity to the AKV.
* `proxy_type` - Type of proxy (http, https etc.) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `port` - Authorization server and vault port number.
* `oauth_host` - Open authorization server host name.
* `vault_host` - AKV host subdomain.
* `verify_host` - Verify the identity of the AKV host name.
* `verify_ip ` - Verify the identity of the AKV IP address.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `client_id` - Application (client) ID of the deployed Azure application with appropriate access to an AKV.
* `tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
* `skip_verification` - Skip the verification of the updated credentials, set to true to bypass the verification. The default value is false.
### Related ONTAP commands
* `security key-manager external azure update-client-secret`
* `security key-manager external azure update-credentials`
* `security key-manager external azure update-config`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
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
        r"""Deletes an AKV configuration.
### Related ONTAP commands
* `security key-manager external azure disable`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    def rekey_external(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Rekeys the external key in the key hierarchy for an SVM with an AKV configuration.
### Required properties
* `key_id` - Key identifier of the new AKV key encryption key.
### Related ONTAP commands
* `security key-manager external azure rekey-external`
"""
        return super()._action(
            "rekey-external", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    rekey_external.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)
    def rekey_internal(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Rekeys the internal key in the key hierarchy for an SVM with an AKV configuration.
### Related ONTAP commands
* `security key-manager external azure rekey-internal`
"""
        return super()._action(
            "rekey-internal", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    rekey_internal.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)
    def restore(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Restore the keys for an SVM from a configured AKV.
### Related ONTAP commands
* `security key-manager external azure restore`
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

