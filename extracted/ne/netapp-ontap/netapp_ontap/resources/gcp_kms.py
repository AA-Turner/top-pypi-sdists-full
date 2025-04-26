r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Google Cloud Key Management Services is a cloud key management service (KMS) that provides a secure store for encryption keys. This feature
allows ONTAP to securely protect its encryption keys using Google Cloud KMS.
In order to use Google Cloud KMS with ONTAP, a user must first deploy a Google Cloud application with appropriate access to the Google Cloud KMS and then provide
ONTAP with the necessary details, such as, project ID, key ring name, location, key name and application credentials to allow ONTAP to communicate
with the deployed Google Cloud application.
The properties `state`, `google_reachability` and `ekmip_reachability` are considered advanced properties and are populated only when explicitly requested.
## Examples
### Enabling GCKMS for an SVM
The following example shows how to enable GCKMS at the SVM-scope. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GcpKms()
    resource.svm = {"uuid": "f36ff553-e713-11ea-bd56-005056bb4222"}
    resource.project_id = "testProj"
    resource.key_ring_name = "testKeyRing"
    resource.key_ring_location = "global"
    resource.key_name = "key1"
    resource.application_credentials = (
        '{"client_email": "my@account.email.com", "private_key": "ValidPrivateKey"}'
    )
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
GcpKms(
    {
        "_links": {
            "self": {
                "href": "/api/security/gcp-kms/f72098a2-e908-11ea-bd56-005056bb4222"
            }
        },
        "svm": {"name": "vs0", "uuid": "f36ff553-e713-11ea-bd56-005056bb4222"},
        "key_ring_location": "global",
        "project_id": "testProj",
        "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
        "key_ring_name": "testKeyRing",
        "key_name": "key1",
    }
)

```
</div>
</div>

---
### Retrieving all GCKMS configurations
The following example shows how to retrieve all GCKMS configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(GcpKms.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    GcpKms(
        {
            "_links": {
                "self": {
                    "href": "/api/security/gcp-kms/f72098a2-e908-11ea-bd56-005056bb4222"
                }
            },
            "svm": {"name": "vs0", "uuid": "f36ff553-e713-11ea-bd56-005056bb4222"},
            "key_ring_location": "global",
            "project_id": "testProj",
            "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
            "scope": "svm",
            "key_ring_name": "testKeyRing",
            "key_name": "key1",
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific GCKMS configuration
The following example shows how to retrieve information for a specific GCKMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GcpKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
GcpKms(
    {
        "_links": {
            "self": {
                "href": "/api/security/gcp-kms/f72098a2-e908-11ea-bd56-005056bb4222"
            }
        },
        "svm": {"name": "vs0", "uuid": "f36ff553-e713-11ea-bd56-005056bb4222"},
        "key_ring_location": "global",
        "project_id": "testProj",
        "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
        "scope": "svm",
        "key_ring_name": "testKeyRing",
        "key_name": "key1",
    }
)

```
</div>
</div>

---
### Retrieving a specific GCKMS's advanced properties
The following example shows how to retrieve advanced properties for a specific GCKMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GcpKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.get(fields="state,google_reachability,ekmip_reachability")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
GcpKms(
    {
        "_links": {
            "self": {
                "href": "/api/security/gcp-kms/f72098a2-e908-11ea-bd56-005056bb4222"
            }
        },
        "google_reachability": {"message": "", "reachable": True, "code": "0"},
        "uuid": "f72098a2-e908-11ea-bd56-005056bb4222",
        "state": {
            "message": "The Google Cloud Key Management Service key protection is unavailable on the following nodes: cluster1-node1.",
            "code": "65537708",
            "cluster_state": False,
        },
        "ekmip_reachability": [
            {
                "message": "",
                "reachable": True,
                "code": "0",
                "node": {
                    "name": "node1",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/d208115f-7721-11eb-bf83-005056bb150e"
                        }
                    },
                    "uuid": "d208115f-7721-11eb-bf83-005056bb150e",
                },
            },
            {
                "message": "",
                "reachable": True,
                "code": "0",
                "node": {
                    "name": "node2",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/e208115f-7721-11eb-bf83-005056bb150e"
                        }
                    },
                    "uuid": "e208115f-7721-11eb-bf83-005056bb150e",
                },
            },
        ],
    }
)

```
</div>
</div>

---
### Updating the application credentials of a specific GCKMS configuration
The following example shows how to update the application credentials for a specific GCKMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GcpKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.application_credentials = (
        '{"client_email": "new@account.com", "private_key": "ValidPrivateKey"}'
    )
    resource.patch()

```

---
### Updating the application credentials and applying a privileged account for impersonation.
The following example shows how to set a privileged account on an existing GCKMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GcpKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.application_credentials = '{"client_email": "unprivileged@account.com", "private_key": "ValidPrivateKeyforUnprivilegedAccount"}'
    resource.privileged_account = "privileged@account.com"
    resource.patch()

```

---
### Deleting a specific GCKMS configuration
The following example shows how to delete a specific GCKMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GcpKms(uuid="f72098a2-e908-11ea-bd56-005056bb4222")
    resource.delete()

```

---
### Restoring keys from a KMIP server
The following example shows how to restore keys for a GCKMS configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GcpKms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GcpKms(uuid="33820b57-ec90-11ea-875e-005056bbf3f0")
    resource.restore()

```

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


__all__ = ["GcpKms", "GcpKmsSchema"]
__pdoc__ = {
    "GcpKmsSchema.resource": False,
    "GcpKmsSchema.opts": False,
}


class GcpKmsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GcpKms object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the gcp_kms."""

    application_credentials = marshmallow_fields.Str(
        data_key="application_credentials",
        allow_none=True,
    )
    r""" Google Cloud application's service account credentials required to access the specified KMS. The client_email and private_key fields of the service account holder are required.

Example: {"private_key":"ValidPrivateKey","client_email":"my@account.email.com"}"""

    caller_account = marshmallow_fields.Str(
        data_key="caller_account",
        allow_none=True,
    )
    r""" Google Cloud KMS caller account email

Example: myaccount@myproject.com"""

    cloudkms_host = marshmallow_fields.Str(
        data_key="cloudkms_host",
        allow_none=True,
    )
    r""" Google Cloud KMS host subdomain.

Example: cloudkms.googleapis.com"""

    ekmip_reachability = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.azure_key_vault_ekmip_reachability.AzureKeyVaultEkmipReachabilitySchema", unknown=EXCLUDE, allow_none=True), data_key="ekmip_reachability", allow_none=True)
    r""" Provides the connectivity status for the given SVM on the given node to all EKMIP servers configured on all nodes of the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    google_reachability = marshmallow_fields.Nested("netapp_ontap.models.gcp_connectivity.GcpConnectivitySchema", data_key="google_reachability", unknown=EXCLUDE, allow_none=True)
    r""" Indicates whether or not the Google Cloud KMS is reachable from all nodes in the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    key_name = marshmallow_fields.Str(
        data_key="key_name",
        allow_none=True,
    )
    r""" Key Identifier of Google Cloud KMS key encryption key.

Example: cryptokey1"""

    key_ring_location = marshmallow_fields.Str(
        data_key="key_ring_location",
        allow_none=True,
    )
    r""" Google Cloud KMS key ring location.

Example: global"""

    key_ring_name = marshmallow_fields.Str(
        data_key="key_ring_name",
        allow_none=True,
    )
    r""" Google Cloud KMS key ring name of the deployed Google Cloud application.

Example: gcpapp1-keyring"""

    oauth_host = marshmallow_fields.Str(
        data_key="oauth_host",
        allow_none=True,
    )
    r""" Open authorization server host name.

Example: oauth2.googleapis.com"""

    oauth_url = marshmallow_fields.Str(
        data_key="oauth_url",
        allow_none=True,
    )
    r""" Open authorization URL for the access token.

Example: https://oauth2.googleapis.com/token"""

    port = Size(
        data_key="port",
        allow_none=True,
    )
    r""" Authorization server and Google Cloud KMS port number.

Example: 443"""

    privileged_account = marshmallow_fields.Str(
        data_key="privileged_account",
        allow_none=True,
    )
    r""" Google Cloud KMS account to impersonate.

Example: myserviceaccount@myproject.iam.gserviceaccount.com"""

    project_id = marshmallow_fields.Str(
        data_key="project_id",
        allow_none=True,
    )
    r""" Google Cloud project (application) ID of the deployed Google Cloud application that has appropriate access to the Google Cloud KMS.

Example: gcpapp1"""

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

    state = marshmallow_fields.Nested("netapp_ontap.models.gcp_kms_state.GcpKmsStateSchema", data_key="state", unknown=EXCLUDE, allow_none=True)
    r""" Google Cloud Key Management Services is a cloud key management service (KMS) that provides a secure store for encryption keys. This object indicates whether or not the Google Cloud KMS key protection is available on all nodes in the cluster.
This is an advanced property; there is an added computational cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the gcp_kms."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" A unique identifier for the Google Cloud KMS.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    verify_host = marshmallow_fields.Boolean(
        data_key="verify_host",
        allow_none=True,
    )
    r""" Verify the identity of the Google Cloud KMS host name."""

    verify_ip = marshmallow_fields.Boolean(
        data_key="verify_ip",
        allow_none=True,
    )
    r""" Verify the identity of the Google Cloud KMS IP address."""

    @property
    def resource(self):
        return GcpKms

    gettable_fields = [
        "links",
        "caller_account",
        "cloudkms_host",
        "ekmip_reachability",
        "google_reachability",
        "key_name",
        "key_ring_location",
        "key_ring_name",
        "oauth_host",
        "oauth_url",
        "port",
        "privileged_account",
        "project_id",
        "proxy_host",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "scope",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "verify_host",
        "verify_ip",
    ]
    """links,caller_account,cloudkms_host,ekmip_reachability,google_reachability,key_name,key_ring_location,key_ring_name,oauth_host,oauth_url,port,privileged_account,project_id,proxy_host,proxy_port,proxy_type,proxy_username,scope,state,svm.links,svm.name,svm.uuid,uuid,verify_host,verify_ip,"""

    patchable_fields = [
        "application_credentials",
        "cloudkms_host",
        "oauth_host",
        "oauth_url",
        "port",
        "privileged_account",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "verify_host",
        "verify_ip",
    ]
    """application_credentials,cloudkms_host,oauth_host,oauth_url,port,privileged_account,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,verify_host,verify_ip,"""

    postable_fields = [
        "application_credentials",
        "cloudkms_host",
        "key_name",
        "key_ring_location",
        "key_ring_name",
        "oauth_host",
        "oauth_url",
        "port",
        "privileged_account",
        "project_id",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "svm.name",
        "svm.uuid",
        "verify_host",
        "verify_ip",
    ]
    """application_credentials,cloudkms_host,key_name,key_ring_location,key_ring_name,oauth_host,oauth_url,port,privileged_account,project_id,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,svm.name,svm.uuid,verify_host,verify_ip,"""

class GcpKms(Resource):
    """Allows interaction with GcpKms objects on the host"""

    _schema = GcpKmsSchema
    _path = "/api/security/gcp-kms"
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
        r"""Retrieves Google Cloud KMS configurations for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external gcp show`
* `security key-manager external gcp check`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all GcpKms resources that match the provided query"""
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
        """Returns a list of RawResources that represent GcpKms resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["GcpKms"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the Google Cloud KMS configuration.
### Optional properties
* `application_credentials` - New credentials used to verify the application's identity to the Google Cloud KMS.
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `port` - Authorization server and Google Cloud KMS port number.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `project_id` - Google Cloud project (application) ID of the deployed Google Cloud application with appropriate access to the Google Cloud KMS.
* `key_ring_name` - Google Cloud KMS key ring name of the deployed Google Cloud application with appropriate access to the specified Google Cloud KMS.
* `key_ring_location` - Google Cloud KMS key ring location.
* `cloudkms_host` - Google Cloud KMS host subdomain.
* `oauth_host` - Open authorization server host name.
* `oauth_url` - Open authorization URL for the access token.
* `verify_host` - Verify the identity of the Google Cloud KMS host name.
* `verify_ip ` - Verify identity of Google Cloud KMS IP address.
* `privileged_account` - Account used to impersonate Google Cloud KMS requests.
### Related ONTAP commands
* `security key-manager external gcp update-credentials`
* `security key-manager external gcp update-config`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["GcpKms"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["GcpKms"], NetAppResponse]:
        r"""Configures the Google Cloud KMS configuration for the specified SVM.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create a Google Cloud KMS.
* `project_id` - Google Cloud project (application) ID of the deployed Google Cloud application with appropriate access to the Google Cloud KMS.
* `key_ring_name` - Google Cloud KMS key ring name of the deployed Google Cloud application with appropriate access to the specified Google Cloud KMS.
* `key_ring_location` - Google Cloud KMS key ring location.
* `key_name`- Key Identifier of the Google Cloud KMS key encryption key.
* `application_credentials` - Google Cloud application's service account credentials required to access the specified KMS. It is a JSON file containing an email address and the private key of the service account holder.
### Optional properties
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `port` - Authorization server and Google Cloud KMS port number.
* `cloudkms_host` - Google Cloud KMS host subdomain.
* `oauth_host` - Open authorization server host name.
* `oauth_url` - Open authorization URL for the access token.
* `privileged_account` - Account used to impersonate Google Cloud KMS requests.
* `verify_ip` - Verify identity of Google Cloud KMS IP address.
* `verify_host` - Verify the identity of the Google Cloud KMS host name.
### Related ONTAP commands
* `security key-manager external gcp enable`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["GcpKms"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a Google Cloud KMS configuration.
### Related ONTAP commands
* `security key-manager external gcp disable`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Google Cloud KMS configurations for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external gcp show`
* `security key-manager external gcp check`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Google Cloud KMS configuration for the SVM specified by the UUID.
### Related ONTAP commands
* `security key-manager external gcp show`
* `security key-manager external gcp check`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
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
        r"""Configures the Google Cloud KMS configuration for the specified SVM.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create a Google Cloud KMS.
* `project_id` - Google Cloud project (application) ID of the deployed Google Cloud application with appropriate access to the Google Cloud KMS.
* `key_ring_name` - Google Cloud KMS key ring name of the deployed Google Cloud application with appropriate access to the specified Google Cloud KMS.
* `key_ring_location` - Google Cloud KMS key ring location.
* `key_name`- Key Identifier of the Google Cloud KMS key encryption key.
* `application_credentials` - Google Cloud application's service account credentials required to access the specified KMS. It is a JSON file containing an email address and the private key of the service account holder.
### Optional properties
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `port` - Authorization server and Google Cloud KMS port number.
* `cloudkms_host` - Google Cloud KMS host subdomain.
* `oauth_host` - Open authorization server host name.
* `oauth_url` - Open authorization URL for the access token.
* `privileged_account` - Account used to impersonate Google Cloud KMS requests.
* `verify_ip` - Verify identity of Google Cloud KMS IP address.
* `verify_host` - Verify the identity of the Google Cloud KMS host name.
### Related ONTAP commands
* `security key-manager external gcp enable`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
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
        r"""Updates the Google Cloud KMS configuration.
### Optional properties
* `application_credentials` - New credentials used to verify the application's identity to the Google Cloud KMS.
* `proxy_type` - Type of proxy (http/https) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `port` - Authorization server and Google Cloud KMS port number.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `project_id` - Google Cloud project (application) ID of the deployed Google Cloud application with appropriate access to the Google Cloud KMS.
* `key_ring_name` - Google Cloud KMS key ring name of the deployed Google Cloud application with appropriate access to the specified Google Cloud KMS.
* `key_ring_location` - Google Cloud KMS key ring location.
* `cloudkms_host` - Google Cloud KMS host subdomain.
* `oauth_host` - Open authorization server host name.
* `oauth_url` - Open authorization URL for the access token.
* `verify_host` - Verify the identity of the Google Cloud KMS host name.
* `verify_ip ` - Verify identity of Google Cloud KMS IP address.
* `privileged_account` - Account used to impersonate Google Cloud KMS requests.
### Related ONTAP commands
* `security key-manager external gcp update-credentials`
* `security key-manager external gcp update-config`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
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
        r"""Deletes a Google Cloud KMS configuration.
### Related ONTAP commands
* `security key-manager external gcp disable`

### Learn more
* [`DOC /security/gcp-kms`](#docs-security-security_gcp-kms)"""
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
        r"""Rekeys the external key in the key hierarchy for an SVM with a Google Cloud KMS configuration.
### Related ONTAP commands
* `security key-manager external gcp rekey-external`
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
        r"""Rekeys the internal key in the key hierarchy for an SVM with a Google Cloud KMS configuration.
### Related ONTAP commands
* `security key-manager external gcp rekey-internal`
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
        r"""Restores the keys for an SVM from a configured Google Cloud KMS.
### Related ONTAP commands
* `security key-manager external gcp restore`
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

