r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
ONTAP supports SSH server that can be accessed from any standard SSH client. A user account needs to be associated with SSH as the application (refer the documentation for <i>api/security/accounts</i> [`DOC /security/accounts`](#docs-security-security_accounts)). Upon connecting from a client, the user is authenticated and a command line shell is presented.<br/>
This endpoint is used to retrieve or modify the SSH configuration at the cluster level. The configuration consists of SSH security parameters (security algorithms, maximum authentication retry attempts allowed before closing the connection, and _ssh-rsa_ enabled status for public key algorithms) and SSH connection limits.<br/>
The security algorithms include SSH key exchange algorithms, ciphers for payload encryption, MAC algorithms and host key algorithms. This configuration is the default for all newly created SVMs; existing SVM configurations are not impacted.
The SSH connection limits include maximum connections per second, maximum simultaneous sessions from the same client host, and overall maximum SSH connections at any given point in time. The connection limits are per node and will be the same for all nodes in the cluster.
## Examples
### Updating the SSH security parameters
Specify the algorithms in the body of the PATCH request.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterSshServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterSshServer()
    resource.ciphers = ["aes256_ctr", "aes192_ctr"]
    resource.key_exchange_algorithms = [
        "diffie_hellman_group_exchange_sha256",
        "ecdh_sha2_nistp256",
        "diffie_hellman_group18_sha512",
    ]
    resource.mac_algorithms = ["hmac_sha2_512_etm", "umac_128_etm"]
    resource.host_key_algorithms = ["ecdsa_sha2_nistp256", "ssh_rsa"]
    resource.max_authentication_retry_count = 3
    resource.is_rsa_in_publickey_algorithms_enabled = True
    resource.patch()

```

### Updating the SSH connection limits
Specify the connection limits in the body of the PATCH request.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterSshServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterSshServer()
    resource.connections_per_second = 8
    resource.max_instances = 10
    resource.per_source_limit = 5
    resource.patch()

```

### Retrieving the cluster SSH server configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterSshServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterSshServer()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
ClusterSshServer(
    {
        "host_key_algorithms": ["ecdsa_sha2_nistp256", "ssh_rsa"],
        "key_exchange_algorithms": [
            "diffie_hellman_group_exchange_sha256",
            "ecdh_sha2_nistp256",
            "diffie_hellman_group18_sha512",
        ],
        "max_authentication_retry_count": 3,
        "_links": {"self": {"href": "/api/security/ssh"}},
        "ciphers": ["aes256_ctr", "aes192_ctr"],
        "is_rsa_in_publickey_algorithms_enabled": True,
        "mac_algorithms": ["hmac_sha2_512_etm", "umac_128_etm"],
        "connections_per_second": 8,
        "max_instances": 10,
        "per_source_limit": 5,
    }
)

```
</div>
</div>
"""

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


__all__ = ["ClusterSshServer", "ClusterSshServerSchema"]
__pdoc__ = {
    "ClusterSshServerSchema.resource": False,
    "ClusterSshServerSchema.opts": False,
}


class ClusterSshServerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterSshServer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cluster_ssh_server."""

    ciphers = marshmallow_fields.List(marshmallow_fields.Str, data_key="ciphers", allow_none=True)
    r""" Ciphers for encrypting the data.

Example: ["aes256_ctr","aes192_ctr","aes128_ctr"]"""

    connections_per_second = Size(
        data_key="connections_per_second",
        validate=integer_validation(minimum=1, maximum=70),
        allow_none=True,
    )
    r""" Maximum connections allowed per second."""

    host_key_algorithms = marshmallow_fields.List(marshmallow_fields.Str, data_key="host_key_algorithms", allow_none=True)
    r""" Host key algorithms. The host key algorithm 'ssh_ed25519' can be configured only in non-FIPS mode.

Example: ["ecdsa_sha2_nistp256","ssh_rsa"]"""

    is_rsa_in_publickey_algorithms_enabled = marshmallow_fields.Boolean(
        data_key="is_rsa_in_publickey_algorithms_enabled",
        allow_none=True,
    )
    r""" Enables or disables the _ssh-rsa_ signature scheme, which uses the SHA-1 hash algorithm, for RSA keys in public key algorithms. If this flag is _false_, older SSH implementations might fail to authenticate using RSA keys. This flag should be enabled only as a temporary measure until legacy SSH client implementations can be upgraded or reconfigured with another key type, for example: ECDSA."""

    key_exchange_algorithms = marshmallow_fields.List(marshmallow_fields.Str, data_key="key_exchange_algorithms", allow_none=True)
    r""" Key exchange algorithms.

Example: ["diffie_hellman_group_exchange_sha256","ecdh_sha2_nistp256","diffie_hellman_group18_sha512"]"""

    mac_algorithms = marshmallow_fields.List(marshmallow_fields.Str, data_key="mac_algorithms", allow_none=True)
    r""" MAC algorithms.

Example: ["hmac_sha2_512","hmac_sha2_512_etm"]"""

    max_authentication_retry_count = Size(
        data_key="max_authentication_retry_count",
        validate=integer_validation(minimum=2, maximum=6),
        allow_none=True,
    )
    r""" Maximum authentication retries allowed before closing the connection."""

    max_instances = Size(
        data_key="max_instances",
        validate=integer_validation(minimum=1, maximum=128),
        allow_none=True,
    )
    r""" Maximum possible simultaneous connections."""

    per_source_limit = Size(
        data_key="per_source_limit",
        validate=integer_validation(minimum=1, maximum=64),
        allow_none=True,
    )
    r""" Maximum connections from the same client host."""

    @property
    def resource(self):
        return ClusterSshServer

    gettable_fields = [
        "links",
        "ciphers",
        "connections_per_second",
        "host_key_algorithms",
        "is_rsa_in_publickey_algorithms_enabled",
        "key_exchange_algorithms",
        "mac_algorithms",
        "max_authentication_retry_count",
        "max_instances",
        "per_source_limit",
    ]
    """links,ciphers,connections_per_second,host_key_algorithms,is_rsa_in_publickey_algorithms_enabled,key_exchange_algorithms,mac_algorithms,max_authentication_retry_count,max_instances,per_source_limit,"""

    patchable_fields = [
        "ciphers",
        "connections_per_second",
        "host_key_algorithms",
        "is_rsa_in_publickey_algorithms_enabled",
        "key_exchange_algorithms",
        "mac_algorithms",
        "max_authentication_retry_count",
        "max_instances",
        "per_source_limit",
    ]
    """ciphers,connections_per_second,host_key_algorithms,is_rsa_in_publickey_algorithms_enabled,key_exchange_algorithms,mac_algorithms,max_authentication_retry_count,max_instances,per_source_limit,"""

    postable_fields = [
        "ciphers",
        "connections_per_second",
        "host_key_algorithms",
        "is_rsa_in_publickey_algorithms_enabled",
        "key_exchange_algorithms",
        "mac_algorithms",
        "max_authentication_retry_count",
        "max_instances",
        "per_source_limit",
    ]
    """ciphers,connections_per_second,host_key_algorithms,is_rsa_in_publickey_algorithms_enabled,key_exchange_algorithms,mac_algorithms,max_authentication_retry_count,max_instances,per_source_limit,"""

class ClusterSshServer(Resource):
    """Allows interaction with ClusterSshServer objects on the host"""

    _schema = ClusterSshServerSchema
    _path = "/api/security/ssh"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster SSH server ciphers, MAC algorithms, key exchange algorithms, host key algorithms, connection limits, and _ssh-rsa_ enabled status for public key algorithms.
### Related ONTAP commands
* `security ssh`
* `security protocol ssh`

### Learn more
* [`DOC /security/ssh`](#docs-security-security_ssh)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SSH server setting for a cluster.
### Optional parameters
* `ciphers` - Encryption algorithms for the payload
* `key_exchange_algorithms` - SSH key exchange algorithms
* `mac_algorithms` - MAC algorithms
* `host_key_algorithms` - Host key algorithms
* `max_authentication_retry_count` - Maximum authentication retries allowed before closing the connection
* `connections_per_second` - Maximum allowed connections per second
* `max_instances` - Maximum allowed connections per node
* `is_rsa_in_publickey_algorithms_enabled` - _ssh-rsa_ enabled status for public key algorithms
* `per_source_limit` - Maximum allowed connections from the same client host
### Related ONTAP commands
* `security ssh`
* `security protocol ssh`

### Learn more
* [`DOC /security/ssh`](#docs-security-security_ssh)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



