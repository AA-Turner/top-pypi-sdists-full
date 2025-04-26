r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to display and update connection status information for external FPolicy servers.
You must keep the following in mind while using these endpoints:

* If the passthrough_read field is set to true in a GET collection call, only FPolicy passthrough-read connections are returned.
* If the passthrough_read field is not provided or set to false in a GET collection call, only FPolicy server connections are returned.
## Examples
### Retrieving the FPolicy server connections for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyConnection

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(FpolicyConnection.get_collection("*", passthrough_read=False, fields="*"))
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    FpolicyConnection(
        {
            "update_time": "2021-06-17T16:05:15+05:30",
            "node": {
                "name": "user-vsim4",
                "uuid": "8ca36b68-c501-11eb-b82c-0050568e5902",
            },
            "state": "disconnected",
            "disconnected_reason": {
                "message": "No local lif present to connect to FPolicy server.",
                "code": 9305,
            },
            "svm": {"name": "vs1", "uuid": "9f738ac5-c502-11eb-b82c-0050568e5902"},
            "type": "primary",
            "policy": {"name": "p1"},
            "server": "192.168.137.78",
        }
    ),
    FpolicyConnection(
        {
            "update_time": "2021-06-17T16:05:15+05:30",
            "node": {
                "name": "user-vsim4",
                "uuid": "8ca36b68-c501-11eb-b82c-0050568e5902",
            },
            "state": "disconnected",
            "disconnected_reason": {
                "message": "No local lif present to connect to FPolicy server.",
                "code": 9305,
            },
            "svm": {"name": "vs1", "uuid": "9f738ac5-c502-11eb-b82c-0050568e5902"},
            "type": "primary",
            "policy": {"name": "p2"},
            "server": "192.168.136.38",
        }
    ),
    FpolicyConnection(
        {
            "update_time": "2021-06-17T16:05:15+05:30",
            "node": {
                "name": "user-vsim4",
                "uuid": "8ca36b68-c501-11eb-b82c-0050568e5902",
            },
            "state": "disconnected",
            "disconnected_reason": {
                "message": "No local lif present to connect to FPolicy server.",
                "code": 9305,
            },
            "svm": {"name": "vs2", "uuid": "b6df362b-c502-11eb-b82c-0050568e5902"},
            "type": "primary",
            "policy": {"name": "pol1"},
            "server": "192.168.129.146",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all FPolicy passthrough read connections for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyConnection

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyConnection.get_collection(
                "*", passthrough_read=True, fields="*", return_timeout=15
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
    FpolicyConnection(
        {
            "session_uuid": "2410d348-c7cb-11eb-a07a-0050568ebc01",
            "node": {
                "name": "user-vsim3",
                "uuid": "55693090-c7c8-11eb-a07a-0050568ebc01",
            },
            "state": "connected",
            "svm": {"name": "vs2", "uuid": "a69e938d-c7ca-11eb-a07a-0050568ebc01"},
            "policy": {"name": "pol1"},
            "server": "192.168.129.146",
        }
    ),
    FpolicyConnection(
        {
            "session_uuid": "288f7002-c7cb-11eb-a07a-0050568ebc01",
            "node": {
                "name": "user-vsim3",
                "uuid": "55693090-c7c8-11eb-a07a-0050568ebc01",
            },
            "state": "connected",
            "svm": {"name": "vs2", "uuid": "a69e938d-c7ca-11eb-a07a-0050568ebc01"},
            "policy": {"name": "pol2"},
            "server": "192.168.129.146",
        }
    ),
]

```
</div>
</div>

---
### Retrieving the FPolicy server connections for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyConnection

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyConnection.get_collection(
                "9f738ac5-c502-11eb-b82c-0050568e5902",
                passthrough_read=False,
                fields="*",
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    FpolicyConnection(
        {
            "update_time": "2021-06-17T16:05:15+05:30",
            "node": {
                "name": "user-vsim4",
                "uuid": "8ca36b68-c501-11eb-b82c-0050568e5902",
            },
            "state": "disconnected",
            "disconnected_reason": {
                "message": "No local lif present to connect to FPolicy server.",
                "code": 9305,
            },
            "svm": {"name": "vs1", "uuid": "9f738ac5-c502-11eb-b82c-0050568e5902"},
            "type": "primary",
            "policy": {"name": "p1"},
            "server": "192.168.137.78",
        }
    ),
    FpolicyConnection(
        {
            "update_time": "2021-06-17T16:05:15+05:30",
            "node": {
                "name": "user-vsim4",
                "uuid": "8ca36b68-c501-11eb-b82c-0050568e5902",
            },
            "state": "disconnected",
            "disconnected_reason": {
                "message": "No local lif present to connect to FPolicy server.",
                "code": 9305,
            },
            "svm": {"name": "vs1", "uuid": "9f738ac5-c502-11eb-b82c-0050568e5902"},
            "type": "primary",
            "policy": {"name": "p2"},
            "server": "192.168.136.38",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific FPolicy server connection
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyConnection

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyConnection(
        "9f738ac5-c502-11eb-b82c-0050568e5902",
        server="192.168.137.78",
        **{"policy.name": "p1", "node.uuid": "8ca36b68-c501-11eb-b82c-0050568e5902"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
FpolicyConnection(
    {
        "update_time": "2021-06-17T16:05:15+05:30",
        "node": {"name": "user-vsim4", "uuid": "8ca36b68-c501-11eb-b82c-0050568e5902"},
        "state": "disconnected",
        "disconnected_reason": {
            "message": "No local lif present to connect to FPolicy server.",
            "code": 9305,
        },
        "svm": {"name": "vs1", "uuid": "9f738ac5-c502-11eb-b82c-0050568e5902"},
        "type": "primary",
        "policy": {"name": "p1"},
        "server": "192.168.137.78",
    }
)

```
</div>
</div>

---
### Updating the FPolicy server connection
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyConnection

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyConnection(
        "9f738ac5-c502-11eb-b82c-0050568e5902",
        server="192.168.137.78",
        **{"policy.name": "p1", "node.uuid": "8ca36b68-c501-11eb-b82c-0050568e5902"}
    )
    resource.patch()

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


__all__ = ["FpolicyConnection", "FpolicyConnectionSchema"]
__pdoc__ = {
    "FpolicyConnectionSchema.resource": False,
    "FpolicyConnectionSchema.opts": False,
}


class FpolicyConnectionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyConnection object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the fpolicy_connection."""

    disconnected_reason = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_connection_disconnected_reason.FpolicyConnectionDisconnectedReasonSchema", data_key="disconnected_reason", unknown=EXCLUDE, allow_none=True)
    r""" Indicates the reason for FPolicy server disconnection."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the fpolicy_connection."""

    policy = marshmallow_fields.Nested("netapp_ontap.resources.fpolicy_policy.FpolicyPolicySchema", data_key="policy", unknown=EXCLUDE, allow_none=True)
    r""" The policy field of the fpolicy_connection."""

    server = marshmallow_fields.Str(
        data_key="server",
        allow_none=True,
    )
    r""" IP address of the FPolicy server.

Example: 10.132.145.20"""

    session_uuid = marshmallow_fields.Str(
        data_key="session_uuid",
        allow_none=True,
    )
    r""" Unique session ID associated with each connection to the FPolicy server and it can be used to identify
the established connection.


Example: 5224ec64-b336-11eb-841c-0050568e14c2"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['connected', 'disconnected']),
        allow_none=True,
    )
    r""" Specifies the FPolicy server connection state indicating if it is in the connected or disconnected state.
The following is a list of the possible states:

* connected                 - Connected
* disconnected              - Disconnected


Valid choices:

* connected
* disconnected"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the fpolicy_connection."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['primary', 'secondary']),
        allow_none=True,
    )
    r""" FPolicy server type. The possible values are:

  * primary - Primary server
  * secondary  - Secondary server


Valid choices:

* primary
* secondary"""

    update_time = ImpreciseDateTime(
        data_key="update_time",
        allow_none=True,
    )
    r""" Specifies the time at which FPolicy server is connected or disconnected.

Example: 2019-06-12T15:00:16.000+0000"""

    @property
    def resource(self):
        return FpolicyConnection

    gettable_fields = [
        "links",
        "disconnected_reason",
        "node.links",
        "node.name",
        "node.uuid",
        "policy.links",
        "policy.name",
        "server",
        "session_uuid",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "update_time",
    ]
    """links,disconnected_reason,node.links,node.name,node.uuid,policy.links,policy.name,server,session_uuid,state,svm.links,svm.name,svm.uuid,type,update_time,"""

    patchable_fields = [
        "state",
    ]
    """state,"""

    postable_fields = [
        "state",
    ]
    """state,"""

class FpolicyConnection(Resource):
    r""" Displays the connection status information of the FPolicy server. """

    _schema = FpolicyConnectionSchema
    _path = "/api/protocols/fpolicy/{svm[uuid]}/connections"
    _keys = ["svm.uuid", "node.uuid", "policy.name", "server"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the statuses of FPolicy servers.
### Related ONTAP commands
* `vserver fpolicy show-engine`
* `vserver fpolicy show-passthrough-read-connection`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/connections`](#docs-NAS-protocols_fpolicy_{svm.uuid}_connections)
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
        """Returns a count of all FpolicyConnection resources that match the provided query"""
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
        """Returns a list of RawResources that represent FpolicyConnection resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FpolicyConnection"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the status of an FPolicy server.
### Related ONTAP commands
* `vserver fpolicy engine-connect`
* `vserver fpolicy engine-disconnect`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/connections`](#docs-NAS-protocols_fpolicy_{svm.uuid}_connections)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the statuses of FPolicy servers.
### Related ONTAP commands
* `vserver fpolicy show-engine`
* `vserver fpolicy show-passthrough-read-connection`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/connections`](#docs-NAS-protocols_fpolicy_{svm.uuid}_connections)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the status of an FPolicy server.
### Related ONTAP commands
* `vserver fpolicy show-engine`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/connections`](#docs-NAS-protocols_fpolicy_{svm.uuid}_connections)
"""
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
        r"""Updates the status of an FPolicy server.
### Related ONTAP commands
* `vserver fpolicy engine-connect`
* `vserver fpolicy engine-disconnect`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/connections`](#docs-NAS-protocols_fpolicy_{svm.uuid}_connections)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



