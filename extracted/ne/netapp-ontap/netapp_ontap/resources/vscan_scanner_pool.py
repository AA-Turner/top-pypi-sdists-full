r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A scanner-pool defines the Vscan servers and privileged users that can connect to SVMs and a scanner policy or role determines whether a scanner-pool is active. You can configure a scanner-pool to be used on the local cluster or any other cluster in an MCC/DR setup.
## Examples
### Retrieving all fields for all scanner-pools of an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            VscanScannerPool.get_collection("<svm-uuid>", fields="*", return_timeout=15)
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    VscanScannerPool(
        {
            "servers": ["1.1.1.1", "10.72.204.27"],
            "name": "scanner-1",
            "role": "primary",
            "privileged_users": ["cifs\\u1", "cifs\\u2"],
            "svm": {"uuid": "0e2f7c91-f227-11e8-9601-0050568ecc06"},
        }
    ),
    VscanScannerPool(
        {
            "servers": ["1.1.1.1", "10.72.204.27"],
            "name": "scanner-2",
            "role": "secondary",
            "privileged_users": ["cifs\\u1", "cifs\\u2"],
            "svm": {"uuid": "0e2f7c91-f227-11e8-9601-0050568ecc06"},
        }
    ),
]

```
</div>
</div>

### Retrieving all scanner-pools with *role* set as *secondary*
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            VscanScannerPool.get_collection(
                "<svm-uuid>", role="secondary", fields="*", return_timeout=15
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    VscanScannerPool(
        {
            "cluster": {
                "name": "Cluster3",
                "uuid": "0933f9b5-f226-11e8-9601-0050568ecc06",
            },
            "servers": ["1.1.1.1", "10.72.204.27"],
            "name": "scanner-2",
            "role": "secondary",
            "privileged_users": ["cifs\\u1", "cifs\\u2"],
            "svm": {"name": "vs1", "uuid": "0e2f7c91-f227-11e8-9601-0050568ecc06"},
        }
    )
]

```
</div>
</div>

### Retrieving the specified scanner-pool associated with an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanScannerPool(
        "0e2f7c91-f227-11e8-9601-0050568ecc06", name="scanner-1"
    )
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
VscanScannerPool(
    {
        "cluster": {"name": "Cluster3", "uuid": "0933f9b5-f226-11e8-9601-0050568ecc06"},
        "servers": ["1.1.1.1", "10.72.204.27"],
        "name": "scanner-1",
        "role": "primary",
        "privileged_users": ["cifs\\u1", "cifs\\u2"],
        "svm": {"name": "vs1", "uuid": "0e2f7c91-f227-11e8-9601-0050568ecc06"},
    }
)

```
</div>
</div>

### Creating a scanner-pool for an SVM with all fields specified
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanScannerPool("b103be27-17b8-11e9-b451-0050568ecd85")
    resource.cluster = {
        "name": "Cluster1",
        "uuid": "ab746d77-17b7-11e9-b450-0050568ecd85",
    }
    resource.name = "test-scanner"
    resource.privileged_users = ["cifs\\u1", "cifs\\u2"]
    resource.role = "primary"
    resource.servers = ["1.1.1.1", "10.72.204.27"]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
VscanScannerPool(
    {
        "cluster": {"name": "Cluster1", "uuid": "ab746d77-17b7-11e9-b450-0050568ecd85"},
        "servers": ["1.1.1.1", "10.72.204.27"],
        "name": "test-scanner",
        "role": "primary",
        "privileged_users": ["cifs\\u1", "cifs\\u2"],
    }
)

```
</div>
</div>

### Creating a scanner-pool for an SVM with an unspecified role and cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanScannerPool("b103be27-17b8-11e9-b451-0050568ecd85")
    resource.name = "test-scanner-1"
    resource.privileged_users = ["cifs\\u1", "cifs\\u2"]
    resource.servers = ["1.1.1.1", "10.72.204.27"]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
VscanScannerPool(
    {
        "servers": ["1.1.1.1", "10.72.204.27"],
        "name": "test-scanner-1",
        "privileged_users": ["cifs\\u1", "cifs\\u2"],
    }
)

```
</div>
</div>

### Updating a scanner-pool for an SVM with all of the fields specified
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanScannerPool(
        "0e2f7c91-f227-11e8-9601-0050568ecc06", name="test-scanner-1"
    )
    resource.cluster = {
        "name": "Cluster3",
        "uuid": "0933f9b5-f226-11e8-9601-0050568ecc06",
    }
    resource.privileged_users = ["cifs\\u1", "cifs\\u2"]
    resource.role = "secondary"
    resource.servers = ["1.1.1.1", "10.72.204.27"]
    resource.patch()

```

### Updating the "role" of a scanner-pool for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanScannerPool(
        "0e2f7c91-f227-11e8-9601-0050568ecc06", name="test-scanner-1"
    )
    resource.cluster = {
        "name": "Cluster3",
        "uuid": "0933f9b5-f226-11e8-9601-0050568ecc06",
    }
    resource.role = "primary"
    resource.patch()

```

### Deleting a scanner-pool for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanScannerPool

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanScannerPool(
        "0e2f7c91-f227-11e8-9601-0050568ecc06", name="test-scanner-1"
    )
    resource.delete()

```
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


__all__ = ["VscanScannerPool", "VscanScannerPoolSchema"]
__pdoc__ = {
    "VscanScannerPoolSchema.resource": False,
    "VscanScannerPoolSchema.opts": False,
}


class VscanScannerPoolSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanScannerPool object"""

    cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="cluster", unknown=EXCLUDE, allow_none=True)
    r""" The cluster field of the vscan_scanner_pool."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=256),
        allow_none=True,
    )
    r""" Specifies the name of the scanner pool. Scanner pool name can be up to 256 characters long and is a string that can only contain any combination of ASCII-range alphanumeric characters a-z, A-Z, 0-9), "_", "-" and ".".

Example: scanner-1"""

    privileged_users = marshmallow_fields.List(marshmallow_fields.Str, data_key="privileged_users", allow_none=True)
    r""" Specifies a list of privileged users. A valid form of privileged user-name is "domain-name\user-name". Privileged user-names are stored and treated as case-insensitive strings. Virus scanners must use one of the registered privileged users for connecting to clustered Data ONTAP for exchanging virus-scanning protocol messages and to access file for scanning, remedying and quarantining operations.

Example: ["cifs\\u1","cifs\\u2"]"""

    role = marshmallow_fields.Str(
        data_key="role",
        validate=enum_validation(['primary', 'secondary', 'idle']),
        allow_none=True,
    )
    r""" Specifies the role of the scanner pool. The possible values are:

  * primary   - Always active.
  * secondary - Active only when none of the primary external virus-scanning servers are connected.
  * idle      - Always inactive.


Valid choices:

* primary
* secondary
* idle"""

    servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="servers", allow_none=True)
    r""" Specifies a list of IP addresses or FQDN for each Vscan server host names which are allowed to connect to clustered ONTAP.

Example: ["1.1.1.1","10.72.204.27","vmwin204-27.fsct.nb"]"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the vscan_scanner_pool."""

    @property
    def resource(self):
        return VscanScannerPool

    gettable_fields = [
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "name",
        "privileged_users",
        "role",
        "servers",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """cluster.links,cluster.name,cluster.uuid,name,privileged_users,role,servers,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "cluster.name",
        "cluster.uuid",
        "privileged_users",
        "role",
        "servers",
    ]
    """cluster.name,cluster.uuid,privileged_users,role,servers,"""

    postable_fields = [
        "cluster.name",
        "cluster.uuid",
        "name",
        "privileged_users",
        "role",
        "servers",
    ]
    """cluster.name,cluster.uuid,name,privileged_users,role,servers,"""

class VscanScannerPool(Resource):
    r""" Scanner pool is a set of attributes which are used to validate and manage connections between clustered ONTAP and external virus-scanning server, or "Vscan server". """

    _schema = VscanScannerPoolSchema
    _path = "/api/protocols/vscan/{svm[uuid]}/scanner-pools"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the Vscan scanner-pool configuration of an SVM.
### Related ONTAP commands
* `vserver vscan scanner-pool show`
* `vserver vscan scanner-pool privileged-users show`
* `vserver vscan scanner-pool servers show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all VscanScannerPool resources that match the provided query"""
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
        """Returns a list of RawResources that represent VscanScannerPool resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["VscanScannerPool"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the Vscan scanner-pool configuration of an SVM.<br/>
Important notes:
* Along with servers and privileged-users, the role of a scanner-pool can also be updated with the cluster on which a scanner-pool is allowed.
* If role is specified and cluster isn't, then role is applied to the local cluster.
### Related ONTAP commands
* `vserver vscan scanner-pool modify`
* `vserver vscan scanner-pool apply-policy`
* `vserver vscan scanner-pool privileged-users add`
* `vserver vscan scanner-pool privileged-users remove`
* `vserver vscan scanner-pool servers remove`
* `vserver vscan scanner-pool servers add`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["VscanScannerPool"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["VscanScannerPool"], NetAppResponse]:
        r"""Creates a Vscan scanner-pool configuration for a specified SVM. You can create a scanner-pool with all fields specified or only mandatory fields specified.<br/>
Important notes:
* A scanner-pool must have servers and privileged users specified.
* If the role or cluster is not specified, the scanner-pool is created on the local cluster with the role set as primary.
*`Only one of the fields cluster-uuid or cluster-name is required.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the Vscan configuration.
* `name` - Scanner-pool name.
* `privileged_users` - List of privileged users.
* `servers` - List of server IP addresses or FQDNs.
### Recommended optional properties
* `role` - Setting a role for a scanner-pool is recommended.
* `cluster` - Passing the cluster name or UUID (or both) in a multi-cluster environment is recommended.
### Default property values
If not specified in POST, the following default property values are assigned:
* `role` - _primary_
* `cluster.name` - Local cluster name.
* `cluster.uuid` - Local cluster UUID.
### Related ONTAP commands
* `vserver vscan scanner-pool create`
* `vserver vscan scanner-pool apply-policy`
* `vserver vscan scanner-pool privileged-users add`
* `vserver vscan scanner-pool servers add`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["VscanScannerPool"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a Vscan scanner-pool configuration.<br/>
Important notes:
* The Vscan scanner-pool DELETE endpoint deletes all of the Vscan scanner-pools for a specified SVM.
* If a Vscan is enabled, it requires at least one scanner-pool to be in the active state. Therefore, disable Vscan on the specified SVM so all the scanner-pools configured on that SVM can be deleted.
### Related ONTAP commands
* `vserver vscan scanner-pool delete`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the Vscan scanner-pool configuration of an SVM.
### Related ONTAP commands
* `vserver vscan scanner-pool show`
* `vserver vscan scanner-pool privileged-users show`
* `vserver vscan scanner-pool servers show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the configuration of a specified scanner-pool of an SVM.
### Related ONTAP commands
* `vserver vscan scanner-pool show`
* `vserver vscan scanner-pool privileged-users show`
* `vserver vscan scanner-pool servers show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
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
        r"""Creates a Vscan scanner-pool configuration for a specified SVM. You can create a scanner-pool with all fields specified or only mandatory fields specified.<br/>
Important notes:
* A scanner-pool must have servers and privileged users specified.
* If the role or cluster is not specified, the scanner-pool is created on the local cluster with the role set as primary.
*`Only one of the fields cluster-uuid or cluster-name is required.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the Vscan configuration.
* `name` - Scanner-pool name.
* `privileged_users` - List of privileged users.
* `servers` - List of server IP addresses or FQDNs.
### Recommended optional properties
* `role` - Setting a role for a scanner-pool is recommended.
* `cluster` - Passing the cluster name or UUID (or both) in a multi-cluster environment is recommended.
### Default property values
If not specified in POST, the following default property values are assigned:
* `role` - _primary_
* `cluster.name` - Local cluster name.
* `cluster.uuid` - Local cluster UUID.
### Related ONTAP commands
* `vserver vscan scanner-pool create`
* `vserver vscan scanner-pool apply-policy`
* `vserver vscan scanner-pool privileged-users add`
* `vserver vscan scanner-pool servers add`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
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
        r"""Updates the Vscan scanner-pool configuration of an SVM.<br/>
Important notes:
* Along with servers and privileged-users, the role of a scanner-pool can also be updated with the cluster on which a scanner-pool is allowed.
* If role is specified and cluster isn't, then role is applied to the local cluster.
### Related ONTAP commands
* `vserver vscan scanner-pool modify`
* `vserver vscan scanner-pool apply-policy`
* `vserver vscan scanner-pool privileged-users add`
* `vserver vscan scanner-pool privileged-users remove`
* `vserver vscan scanner-pool servers remove`
* `vserver vscan scanner-pool servers add`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
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
        r"""Deletes a Vscan scanner-pool configuration.<br/>
Important notes:
* The Vscan scanner-pool DELETE endpoint deletes all of the Vscan scanner-pools for a specified SVM.
* If a Vscan is enabled, it requires at least one scanner-pool to be in the active state. Therefore, disable Vscan on the specified SVM so all the scanner-pools configured on that SVM can be deleted.
### Related ONTAP commands
* `vserver vscan scanner-pool delete`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/scanner-pools`](#docs-NAS-protocols_vscan_{svm.uuid}_scanner-pools)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


