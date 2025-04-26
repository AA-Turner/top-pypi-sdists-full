r"""
Copyright &copy; 2024 NetApp Inc.
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
    resource.name = "https:://mykeyvault.azure.vault.net/"
    resource.key_id = "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74"
    resource.client_certificate = "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"
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
        "name": "https:://mykeyvault.azure.vault.net/",
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/024cd3cf-9a08-11ea-8d52-005056bbeba5"
            }
        },
        "svm": {"name": "vs0", "uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"},
        "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
        "tenant_id": "tenant1",
        "client_id": "client1",
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
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
    resource.name = "https:://mykeyvault.azure.vault.net/"
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
        "configuration": {"name": "myConfiguration"},
        "name": "https:://mykeyvault.azure.vault.net/",
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
            }
        },
        "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
        "tenant_id": "tenant1",
        "client_id": "client1",
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
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
            "configuration": {
                "name": "default",
                "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
            },
            "name": "https:://mykeyvault.azure.vault.net/",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/security/azure-key-vaults/024cd3cf-9a08-11ea-8d52-005056bbeba5"
                }
            },
            "authentication_method": "client_secret",
            "svm": {"name": "vs0", "uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"},
            "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
            "tenant_id": "tenant1",
            "client_id": "client1",
            "scope": "svm",
            "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
        }
    ),
    AzureKeyVault(
        {
            "configuration": {
                "name": "new-config",
                "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
            },
            "name": "https:://mykeyvault.azure.vault.net/",
            "enabled": False,
            "_links": {
                "self": {
                    "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
                }
            },
            "authentication_method": "certificate",
            "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
            "tenant_id": "tenant1",
            "client_id": "client1",
            "scope": "cluster",
            "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
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
        "configuration": {
            "name": "default",
            "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
        },
        "name": "https:://mykeyvault.azure.vault.net/",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
            }
        },
        "authentication_method": "client_secret",
        "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
        "tenant_id": "tenant1",
        "client_id": "client1",
        "scope": "cluster",
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74",
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
    resource.client_secret = "newSecret"
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
    resource.client_certificate = "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"
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
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
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

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
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

    azure_reachability = marshmallow_fields.Nested("netapp_ontap.models.azure_key_vault_connectivity.AzureKeyVaultConnectivitySchema", data_key="azure_reachability", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether or not the AKV service is reachable from all the nodes in the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    client_certificate = marshmallow_fields.Str(
        data_key="client_certificate",
        allow_none=True,
    )
    r""" PKCS12 Certificate used by the application to prove its identity to AKV.

Example: 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"""

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

    configuration = marshmallow_fields.Nested("netapp_ontap.models.security_keystore_configuration.SecurityKeystoreConfigurationSchema", data_key="configuration", unknown=EXCLUDE, allow_none=True)
    r""" Security keystore object reference."""

    ekmip_reachability = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.aws_kms_ekmip_reachability.AwsKmsEkmipReachabilitySchema", unknown=EXCLUDE, allow_none=True), data_key="ekmip_reachability", allow_none=True)
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

    state = marshmallow_fields.Nested("netapp_ontap.models.azure_key_vault_state.AzureKeyVaultStateSchema", data_key="state", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether or not the AKV wrapped internal key is available cluster wide.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
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

