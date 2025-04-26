r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This endpoint is used to retrieve or modify the SSH security configuration of a data SVM.<br/>
The SSH security algorithms include key exchange algorithms, ciphers for payload encryption, MAC algorithms, host key algorithms and the maximum authentication retry attempts allowed before closing the connection. svm.uuid corresponds to the UUID of the SVM for which the SSH security setting is being retrieved or modified and it is obtained from the response body of a GET operation performed on the <i>api/security/ssh/svms</i> API.
## Examples
### Updating the SSH security parameters
Specify the algorithms in the body of the PATCH request.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmSshServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SvmSshServer(**{"svm.uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"})
    resource.ciphers = ["aes256_ctr", "aes192_ctr"]
    resource.key_exchange_algorithms = [
        "diffie_hellman_group_exchange_sha256",
        "ecdh_sha2_nistp256",
        "diffie_hellman_group16_sha512",
    ]
    resource.mac_algorithms = ["hmac_sha2_512_etm", "umac_128_etm"]
    resource.host_key_algorithms = ["ecdsa_sha2_nistp256", "ssh_ed25519"]
    resource.is_rsa_in_publickey_algorithms_enabled = False
    resource.max_authentication_retry_count = 3
    resource.patch()

```

### Retrieving the SSH security configuration of an SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SvmSshServer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SvmSshServer(**{"svm.uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SvmSshServer(
    {
        "host_key_algorithms": ["ecdsa_sha2_nistp256", "ssh_ed25519"],
        "key_exchange_algorithms": [
            "diffie_hellman_group_exchange_sha256",
            "ecdh_sha2_nistp256",
            "diffie_hellman_group16_sha512",
        ],
        "max_authentication_retry_count": 3,
        "_links": {
            "self": {
                "href": "/api/security/ssh/svms/02c9e252-41be-11e9-81d5-00a0986138f7"
            }
        },
        "ciphers": ["aes256_ctr", "aes192_ctr"],
        "is_rsa_in_publickey_algorithms_enabled": False,
        "mac_algorithms": ["hmac_sha2_512_etm", "umac_128_etm"],
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/02c9e252-41be-11e9-81d5-00a0986138f7"}
            },
            "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7",
        },
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


__all__ = ["SvmSshServer", "SvmSshServerSchema"]
__pdoc__ = {
    "SvmSshServerSchema.resource": False,
    "SvmSshServerSchema.opts": False,
}


class SvmSshServerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmSshServer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the svm_ssh_server."""

    ciphers = marshmallow_fields.List(marshmallow_fields.Str, data_key="ciphers", allow_none=True)
    r""" Ciphers for encrypting the data.

Example: ["aes256_ctr","aes192_ctr","aes128_ctr"]"""

    host_key_algorithms = marshmallow_fields.List(marshmallow_fields.Str, data_key="host_key_algorithms", allow_none=True)
    r""" Host key algorithms. The host key algorithm 'ssh_ed25519' can be configured only in non-FIPS mode.

Example: ["ecdsa_sha2_nistp256","ssh_ed25519","ssh_rsa"]"""

    is_rsa_in_publickey_algorithms_enabled = marshmallow_fields.Boolean(
        data_key="is_rsa_in_publickey_algorithms_enabled",
        allow_none=True,
    )
    r""" Enables or disables the _ssh-rsa_ signature scheme, which uses the SHA-1 hash algorithm, for RSA keys in public key algorithms. If this flag is _false_, older SSH implementations might fail to authenticate using RSA keys. This flag should be enabled only as a temporary measure until legacy SSH client implementations can be upgraded or reconfigured with another key type, for example: ECDSA."""

    key_exchange_algorithms = marshmallow_fields.List(marshmallow_fields.Str, data_key="key_exchange_algorithms", allow_none=True)
    r""" Key exchange algorithms.

Example: ["diffie_hellman_group_exchange_sha256","ecdh_sha2_nistp256"]"""

    mac_algorithms = marshmallow_fields.List(marshmallow_fields.Str, data_key="mac_algorithms", allow_none=True)
    r""" MAC algorithms.

Example: ["hmac_sha2_512","hmac_sha2_512_etm"]"""

    max_authentication_retry_count = Size(
        data_key="max_authentication_retry_count",
        validate=integer_validation(minimum=2, maximum=6),
        allow_none=True,
    )
    r""" Maximum authentication retries allowed before closing the connection."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the svm_ssh_server."""

    @property
    def resource(self):
        return SvmSshServer

    gettable_fields = [
        "links",
        "ciphers",
        "host_key_algorithms",
        "is_rsa_in_publickey_algorithms_enabled",
        "key_exchange_algorithms",
        "mac_algorithms",
        "max_authentication_retry_count",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,ciphers,host_key_algorithms,is_rsa_in_publickey_algorithms_enabled,key_exchange_algorithms,mac_algorithms,max_authentication_retry_count,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "ciphers",
        "host_key_algorithms",
        "is_rsa_in_publickey_algorithms_enabled",
        "key_exchange_algorithms",
        "mac_algorithms",
        "max_authentication_retry_count",
        "svm.name",
        "svm.uuid",
    ]
    """ciphers,host_key_algorithms,is_rsa_in_publickey_algorithms_enabled,key_exchange_algorithms,mac_algorithms,max_authentication_retry_count,svm.name,svm.uuid,"""

    postable_fields = [
        "ciphers",
        "host_key_algorithms",
        "is_rsa_in_publickey_algorithms_enabled",
        "key_exchange_algorithms",
        "mac_algorithms",
        "max_authentication_retry_count",
        "svm.name",
        "svm.uuid",
    ]
    """ciphers,host_key_algorithms,is_rsa_in_publickey_algorithms_enabled,key_exchange_algorithms,mac_algorithms,max_authentication_retry_count,svm.name,svm.uuid,"""

class SvmSshServer(Resource):
    """Allows interaction with SvmSshServer objects on the host"""

    _schema = SvmSshServerSchema
    _path = "/api/security/ssh/svms"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the SSH server configuration for all the data SVMs.
### Related ONTAP commands
* `security ssh`

### Learn more
* [`DOC /security/ssh/svms`](#docs-security-security_ssh_svms)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SvmSshServer resources that match the provided query"""
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
        """Returns a list of RawResources that represent SvmSshServer resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SvmSshServer"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SSH server configuration for the specified data SVM.
### Optional parameters
* `ciphers` - Encryption algorithms for the payload
* `key_exchange_algorithms` - SSH key exchange algorithms
* `host_key_algorithms` - Host key algorithms
* `mac_algorithms` - MAC algorithms
* `max_authentication_retry_count` - Maximum authentication retries allowed before closing the connection
* `is_rsa_in_publickey_algorithms_enabled` - _ssh-rsa_ enabled status for public key algorithms
### Related ONTAP commands
* `security ssh`

### Learn more
* [`DOC /security/ssh/svms/{svm.uuid}`](#docs-security-security_ssh_svms_{svm.uuid})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the SSH server configuration for all the data SVMs.
### Related ONTAP commands
* `security ssh`

### Learn more
* [`DOC /security/ssh/svms`](#docs-security-security_ssh_svms)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the SSH server configuration for the specified data SVM.
### Related ONTAP commands
* `security ssh`

### Learn more
* [`DOC /security/ssh/svms/{svm.uuid}`](#docs-security-security_ssh_svms_{svm.uuid})"""
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
        r"""Updates the SSH server configuration for the specified data SVM.
### Optional parameters
* `ciphers` - Encryption algorithms for the payload
* `key_exchange_algorithms` - SSH key exchange algorithms
* `host_key_algorithms` - Host key algorithms
* `mac_algorithms` - MAC algorithms
* `max_authentication_retry_count` - Maximum authentication retries allowed before closing the connection
* `is_rsa_in_publickey_algorithms_enabled` - _ssh-rsa_ enabled status for public key algorithms
### Related ONTAP commands
* `security ssh`

### Learn more
* [`DOC /security/ssh/svms/{svm.uuid}`](#docs-security-security_ssh_svms_{svm.uuid})"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



