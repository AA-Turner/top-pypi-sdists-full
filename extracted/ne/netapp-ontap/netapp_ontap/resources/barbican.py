r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Barbican Key Management Services (KMS) is a key management service that provides a secure store for encryption keys. This feature
allows ONTAP to securely protect its encryption keys using Barbican KMS.
Before you can use Barbican KMS with ONTAP, you must provide ONTAP with the necessary details to allow ONTAP to communicate with the deployed Barbican application.
These details include the key ID URL, Keystone authentication URL, and the application credentials ID and secret.
The property `barbican_reachability` is considered an advanced property and is populated only when explicitly requested.
## Examples
### Creating an inactive Barbican configuration for an SVM
The example Barbican configuration is created for a specific SVM but is not enabled.
Note the <i>return_records=true</i> query parameter can be used to return the newly created key-manager keystore configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Barbican

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Barbican()
    resource.svm = {"name": "barbican_svm"}
    resource.configuration = {"name": "myConfiguration"}
    resource.application_cred_id = "app1"
    resource.application_cred_secret = "secret1"
    resource.key_id = (
        "https://sample.keyid.com:9311/v1/secrets/5c610a4f-ea97-44b5-8682-f4daeafa9647/"
    )
    resource.keystone_url = "https://sample.keystone.com:5000/v3/auth/tokens"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Barbican(
    {
        "svm": {"name": "barbican_svm"},
        "key_id": "https://sample.keyid.com:9311/v1/secrets/5c610a4f-ea97-44b5-8682-f4daeafa9647/",
        "configuration": {"name": "myConfiguration"},
        "application_cred_id": "app1",
        "keystone_url": "https://sample.keystone.com:5000/v3/auth/tokens",
        "application_cred_secret": "secret1",
    }
)

```
</div>
</div>

---
### Listing all Barbican configurations
The following example shows how to retrieve a list of all created Barbican configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Barbican

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Barbican.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    Barbican(
        {
            "uuid": "5a134975-fa58-11ef-8c9f-005056bbeee5",
            "configuration": {
                "uuid": "5a134975-fa58-11ef-8c9f-005056bbeee5",
                "name": "myConfiguration",
            },
            "_links": {
                "self": {
                    "href": "/api/security/barbican-kms/5a134975-fa58-11ef-8c9f-005056bbeee5"
                }
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific Barbican configuration
The following example shows how to retrieve information for a specific Barbican configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Barbican

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Barbican(uuid="5a134975-fa58-11ef-8c9f-005056bbeee5")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Barbican(
    {
        "proxy_host": "",
        "svm": {"uuid": "ec8e0954-fa10-11ef-8c9f-005056bbeee5", "name": "barbican_svm"},
        "uuid": "5a134975-fa58-11ef-8c9f-005056bbeee5",
        "key_id": "https://sample.keyid.com:9311/v1/secrets/5c610a4f-ea97-44b5-8682-f4daeafa9647/",
        "verify_host": True,
        "proxy_port": 0,
        "configuration": {
            "uuid": "5a134975-fa58-11ef-8c9f-005056bbeee5",
            "name": "myConfiguration",
        },
        "proxy_type": "https",
        "proxy_username": "",
        "application_cred_id": "app1",
        "timeout": 10,
        "scope": "svm",
        "verify": True,
        "enabled": False,
        "keystone_url": "https://sample.keystone.com:5000/v3/auth/tokens",
        "_links": {
            "self": {
                "href": "/api/security/barbican-kms/5a134975-fa58-11ef-8c9f-005056bbeee5"
            }
        },
    }
)

```
</div>
</div>

---
### Retrieving an advanced property for a specific Barbican configuration
The following example shows how to retrieve an advanced property for a specific Barbican configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Barbican

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Barbican(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.get(fields="barbican_reachability")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Barbican(
    {
        "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
        "barbican_reachability": {"message": "", "reachable": True, "code": "0"},
        "configuration": {
            "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
            "name": "myConfiguration",
        },
        "_links": {
            "self": {
                "href": "/api/security/barbican-kms/f72098a2-e908-11ea-bd56-005056bb4222"
            }
        },
    }
)

```
</div>
</div>

---
### Updating the application credentials ID and secret for a specific Barbican configuration
The following example shows how to update the application credentials for a specific Barbican configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Barbican

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Barbican(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.application_cred_id = "app345"
    resource.application_cred_secret = "secret"
    resource.patch()

```

---
### Enabling a Barbican configuration
The newly created Barbican configuration is inactive by default. Use the REST API PATCH method "/api/security/key-stores/{uuid}" to enable the configuration.
<br/>
---
### Restoring keys
The following example shows how to restore keys for a specific Barbican configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Barbican

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Barbican(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.restore()

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
Barbican({})

```
</div>
</div>

---
### Rekey the internal key
The following example shows how to rekey the internal key based on a specific Barbican configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Barbican

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Barbican(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.rekey_internal()

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Barbican({})

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


__all__ = ["Barbican", "BarbicanSchema"]
__pdoc__ = {
    "BarbicanSchema.resource": False,
    "BarbicanSchema.opts": False,
}


class BarbicanSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Barbican object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the barbican."""

    application_cred_id = marshmallow_fields.Str(
        data_key="application_cred_id",
        allow_none=True,
    )
    r""" Keystone application credentials ID required to access the specified Barbican KMS.

Example: 63e3cb77f84f42b7a0395a3efb7636f9"""

    application_cred_secret = marshmallow_fields.Str(
        data_key="application_cred_secret",
        allow_none=True,
    )
    r""" Keystone application credentials secret required to access the specified Barbican KMS. It is not audited.

Example: secret"""

    barbican_reachability = marshmallow_fields.Nested("netapp_ontap.models.barbican_connectivity.BarbicanConnectivitySchema", data_key="barbican_reachability", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether the Barbican KMS is reachable from all nodes in the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET request or an instance GET request unless it is explicitly requested using the field's query parameter or GET for all advanced properties is enabled."""

    configuration = marshmallow_fields.Nested("netapp_ontap.models.security_keystore_configuration.SecurityKeystoreConfigurationSchema", data_key="configuration", unknown=EXCLUDE, allow_none=True)
    r""" Security keystore object reference."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether the configuration is enabled."""

    key_id = marshmallow_fields.Str(
        data_key="key_id",
        allow_none=True,
    )
    r""" Key Identifier URL of the Barbican KMS key encryption key. Must be an HTTPS URL.

Example: https://172.29.58.184:9311/v1/secrets/5c610a4f-ea97-44b5-8682-f4daeafa9647"""

    keystone_url = marshmallow_fields.Str(
        data_key="keystone_url",
        allow_none=True,
    )
    r""" Keystone URL for the access token. Must be an HTTPS URL.

Example: https://keystoneip:5000/v3/auth/tokens"""

    proxy_host = marshmallow_fields.Str(
        data_key="proxy_host",
        allow_none=True,
    )
    r""" Proxy host name.

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
    r""" Proxy port number.

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

    state = marshmallow_fields.Nested("netapp_ontap.models.barbican_state.BarbicanStateSchema", data_key="state", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether or not the SVM key encryption key (KEK) is available cluster wide.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the barbican."""

    timeout = Size(
        data_key="timeout",
        allow_none=True,
    )
    r""" Connection timeout in seconds.

Example: 60"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" A unique identifier of the Barbican KMS.

Example: 1cd8a442-86d1-11e0-ae1c-123478563434"""

    verify = marshmallow_fields.Boolean(
        data_key="verify",
        allow_none=True,
    )
    r""" Verify the identity of the Barbican KMS."""

    verify_host = marshmallow_fields.Boolean(
        data_key="verify_host",
        allow_none=True,
    )
    r""" Verify the identity of the Barbican KMS host name."""

    @property
    def resource(self):
        return Barbican

    gettable_fields = [
        "links",
        "application_cred_id",
        "barbican_reachability",
        "configuration",
        "enabled",
        "key_id",
        "keystone_url",
        "proxy_host",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "scope",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "timeout",
        "uuid",
        "verify",
        "verify_host",
    ]
    """links,application_cred_id,barbican_reachability,configuration,enabled,key_id,keystone_url,proxy_host,proxy_port,proxy_type,proxy_username,scope,state,svm.links,svm.name,svm.uuid,timeout,uuid,verify,verify_host,"""

    patchable_fields = [
        "application_cred_id",
        "application_cred_secret",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "timeout",
        "verify",
        "verify_host",
    ]
    """application_cred_id,application_cred_secret,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,timeout,verify,verify_host,"""

    postable_fields = [
        "application_cred_id",
        "application_cred_secret",
        "configuration",
        "key_id",
        "keystone_url",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "svm.name",
        "svm.uuid",
        "timeout",
        "verify",
        "verify_host",
    ]
    """application_cred_id,application_cred_secret,configuration,key_id,keystone_url,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,svm.name,svm.uuid,timeout,verify,verify_host,"""

class Barbican(Resource):
    """Allows interaction with Barbican objects on the host"""

    _schema = BarbicanSchema
    _path = "/api/security/barbican-kms"
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
        r"""Retrieves Barbican KMS configurations for all SVMs.
### Related ONTAP commands
* `security key-manager external barbican show`
* `security key-manager external barbican check`

### Learn more
* [`DOC /security/barbican-kms`](#docs-security-security_barbican-kms)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Barbican resources that match the provided query"""
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
        """Returns a list of RawResources that represent Barbican resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Barbican"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the Barbican KMS configuration.
### Optional properties
* `application_cred_id` - New credentials used to verify the application's identity to the Barbican KMS. You must provide both `application_cred_id` and `application_cred_secret` to update the credentials.
* `application_cred_secret` - New credentials secret used to verify the application's identity to the Barbican KMS. You must provide both `application_cred_id` and `application_cred_secret` to update the credentials.
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `verify` - Verify the identity of the Barbican KMS?
* `verify_host` - Verify the identity of the Barbican KMS host name?
* `timeout` - Connection timeout in seconds.
### Related ONTAP commands
* `security key-manager external barbican update-credentials`
* `security key-manager external barbican update-config`

### Learn more
* [`DOC /security/barbican-kms`](#docs-security-security_barbican-kms)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Barbican"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Barbican"], NetAppResponse]:
        r"""Creates a Barbican KMS configuration for the specified SVM.
### Required properties
* `configuration.name` - Name for the new Barbican configuration.
* `svm.uuid` or `svm.name` - Existing SVM in which to create a Barbican KMS.
* `key_id` - Barbican key URL.
* `keystone_url` - Keystone authentication URL.
* `application_cred_id` - Keystone authentication application ID with access to the Barbican KMS.
* `application_cred_secret`- Application credentials secret to authenticate the application credentials ID with Keystone.
### Optional properties
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `verify` - Verify the identity of the Barbican KMS?
* `verify_host` - Verify the identity of the Barbican KMS host name?
* `timeout` - Connection timeout in seconds.
### Related ONTAP commands
* `security key-manager external barbican create-config`

### Learn more
* [`DOC /security/barbican-kms`](#docs-security-security_barbican-kms)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Barbican KMS configurations for all SVMs.
### Related ONTAP commands
* `security key-manager external barbican show`
* `security key-manager external barbican check`

### Learn more
* [`DOC /security/barbican-kms`](#docs-security-security_barbican-kms)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Barbican KMS configuration for the SVM specified by the UUID.
### Related ONTAP commands
* `security key-manager external barbican show`
* `security key-manager external barbican check`

### Learn more
* [`DOC /security/barbican-kms`](#docs-security-security_barbican-kms)"""
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
        r"""Creates a Barbican KMS configuration for the specified SVM.
### Required properties
* `configuration.name` - Name for the new Barbican configuration.
* `svm.uuid` or `svm.name` - Existing SVM in which to create a Barbican KMS.
* `key_id` - Barbican key URL.
* `keystone_url` - Keystone authentication URL.
* `application_cred_id` - Keystone authentication application ID with access to the Barbican KMS.
* `application_cred_secret`- Application credentials secret to authenticate the application credentials ID with Keystone.
### Optional properties
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `verify` - Verify the identity of the Barbican KMS?
* `verify_host` - Verify the identity of the Barbican KMS host name?
* `timeout` - Connection timeout in seconds.
### Related ONTAP commands
* `security key-manager external barbican create-config`

### Learn more
* [`DOC /security/barbican-kms`](#docs-security-security_barbican-kms)"""
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
        r"""Updates the Barbican KMS configuration.
### Optional properties
* `application_cred_id` - New credentials used to verify the application's identity to the Barbican KMS. You must provide both `application_cred_id` and `application_cred_secret` to update the credentials.
* `application_cred_secret` - New credentials secret used to verify the application's identity to the Barbican KMS. You must provide both `application_cred_id` and `application_cred_secret` to update the credentials.
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `verify` - Verify the identity of the Barbican KMS?
* `verify_host` - Verify the identity of the Barbican KMS host name?
* `timeout` - Connection timeout in seconds.
### Related ONTAP commands
* `security key-manager external barbican update-credentials`
* `security key-manager external barbican update-config`

### Learn more
* [`DOC /security/barbican-kms`](#docs-security-security_barbican-kms)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)


    def rekey_internal(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Rekeys the internal key in the key hierarchy for an SVM with a Barbican KMS configuration.
### Related ONTAP commands
* `security key-manager external barbican rekey-internal`
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
        r"""Restores the keys for an SVM from a configured Barbican KMS.
### Related ONTAP commands
* `security key-manager external barbican restore`
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

