r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The following operations are supported:

* Creation: POST network/ip/bgp/peer-groups
* Collection Get: GET network/ip/bgp/peer-groups
* Instance Get: GET network/ip/bgp/peer-groups/{uuid}
* Instance Patch: PATCH network/ip/bgp/peer-groups/{uuid}
* Instance Delete: DELETE network/ip/bgp/peer-groups/{uuid}
## Retrieving network BGP sessions information
The IP BGP peer-groups GET API retrieves and displays relevant information pertaining to the BGP peer-groups configured in the cluster. The response can contain a list of multiple BGP peer-groups or a specific peer-group. Each BGP peer-group represents a BGP session configured between a local interface and a peer router.
## Examples
### Retrieving all BGP peer-groups in the cluster
The following example shows the list of all BGP peer-groups configured in a cluster.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(BgpPeerGroup.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    BgpPeerGroup({"name": "pg1", "uuid": "5f22ae9d-87b2-11e9-a3a6-005056bb81a4"}),
    BgpPeerGroup({"name": "pg2", "uuid": "5fd08be3-87b2-11e9-952f-005056bb2170"}),
]

```
</div>
</div>

---
### Retrieving a specific BGP peer-group
The following example shows the response when a specific BGP peer-group is requested. The system returns an error when there is no peer-group with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BgpPeerGroup(uuid="5fd08be3-87b2-11e9-952f-005056bb2170")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
BgpPeerGroup(
    {
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/84fd3375-879a-11e9-a3a6-005056bb81a4"
                }
            },
            "uuid": "84fd3375-879a-11e9-a3a6-005056bb81a4",
        },
        "name": "pg2",
        "state": "up",
        "peer": {"asn": 65501, "address": "10.10.10.1"},
        "uuid": "5fd08be3-87b2-11e9-952f-005056bb2170",
        "local": {
            "interface": {
                "name": "bgp2",
                "uuid": "5e76a305-87b2-11e9-952f-005056bb2170",
                "ip": {"address": "10.10.10.2"},
            },
            "port": {
                "name": "e0h",
                "node": {"name": "node1"},
                "uuid": "f8ff73de-879a-11e9-952f-005056bb2170",
            },
        },
    }
)

```
</div>
</div>

---
### Retrieving specific fields and limiting the output using filters
The following example shows the response when a filter is applied (location.port.node.name=node1) and only certain fields are requested. Filtered fields are in the output in addition to the default fields and requested fields.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            BgpPeerGroup.get_collection(
                fields="local.interface.ip,peer", **{"local.port.node.name": "node1"}
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
    BgpPeerGroup(
        {
            "name": "pg1",
            "peer": {"asn": 65501, "address": "10.10.10.2"},
            "uuid": "5f22ae9d-87b2-11e9-a3a6-005056bb81a4",
            "local": {
                "interface": {"ip": {"address": "10.10.10.1"}},
                "port": {"node": {"name": "node1"}},
            },
        }
    )
]

```
</div>
</div>

---
## Creating a BGP peer-group
The BGP peer-group POST API is used to create a peer-group as shown in the following examples.
<br/>
---
## Examples
### Creating a BGP peer-group with an existing interface
The following example shows how to create a BGP peer-group between an existing interface "bgp1" and peer router with the address "10.10.10.10". The local interface "bgp1" needs to support the management-bgp service, otherwise the system returns an error.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BgpPeerGroup()
    resource.name = "newPg"
    resource.ipspace.name = "Default"
    resource.local.interface.name = "bgp1"
    resource.peer.address = "10.10.10.10"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
BgpPeerGroup(
    {
        "ipspace": {"name": "Default"},
        "name": "newPg",
        "peer": {"address": "10.10.10.10"},
        "uuid": "e3faacc6-87cb-11e9-a3a6-005056bb81a4",
        "local": {"interface": {"name": "bgp1"}},
    }
)

```
</div>
</div>

---
### Creating a BGP peer-group and provisioning a new local interface
The following example shows how to create a BGP peer-group with any local interface. If the local interface doesn't exist, the system will create it first before creating the peer-group.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BgpPeerGroup()
    resource.name = "newPg1"
    resource.ipspace.name = "Default"
    resource.local = {
        "interface": {"name": "newlif"},
        "ip": {"address": "9.9.9.9", "netmask": "24"},
        "port": {"name": "e0f", "node": {"name": "node1"}},
    }
    resource.peer.address = "10.10.10.10"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
BgpPeerGroup(
    {
        "ipspace": {"name": "Default"},
        "name": "newPg1",
        "peer": {"address": "10.10.10.10"},
        "uuid": "c292f069-8872-11e9-a3a6-005056bb81a4",
        "local": {
            "interface": {"name": "newlif"},
            "port": {"name": "e0f", "node": {"name": "node1"}},
        },
    }
)

```
</div>
</div>

---
## Updating BGP peer-groups
The BGP peer-groups PATCH API is used to update attributes of a peer-group.
<br/>
---
## Examples
### Updating the peer router address
The following example shows how the PATCH request changes the peer router IP address.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BgpPeerGroup(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.peer.address = "10.10.10.20"
    resource.patch()

```

---
### Updating the peer-group to a new name
The following example shows how the PATCH request renames the peer-group.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BgpPeerGroup(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.name = "NewName"
    resource.patch()

```

---
## Deleting BGP peer-groups
The BGP peer-groups DELETE API is used to delete an BGP peer-group.
<br/>
---
## Example
### Deleting a BGP peer-group
The following DELETE request deletes a BGP peer-group.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BgpPeerGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BgpPeerGroup(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.delete()

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


__all__ = ["BgpPeerGroup", "BgpPeerGroupSchema"]
__pdoc__ = {
    "BgpPeerGroupSchema.resource": False,
    "BgpPeerGroupSchema.opts": False,
}


class BgpPeerGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BgpPeerGroup object"""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the bgp_peer_group."""

    local = marshmallow_fields.Nested("netapp_ontap.models.bgp_peer_group_local.BgpPeerGroupLocalSchema", data_key="local", unknown=EXCLUDE, allow_none=True)
    r""" Information describing the local interface that is being used to peer with a router using BGP. On a POST operation, an existing BGP interface is used by specifying the interface, or create a new one by specifying the port and IP address."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the peer group

Example: bgpv4peer"""

    peer = marshmallow_fields.Nested("netapp_ontap.models.bgp_peer_group_peer.BgpPeerGroupPeerSchema", data_key="peer", unknown=EXCLUDE, allow_none=True)
    r""" Information describing the router to peer with"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'down']),
        allow_none=True,
    )
    r""" State of the peer group

Valid choices:

* up
* down"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" UUID of the peer group

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return BgpPeerGroup

    gettable_fields = [
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "local",
        "name",
        "peer",
        "state",
        "uuid",
    ]
    """ipspace.links,ipspace.name,ipspace.uuid,local,name,peer,state,uuid,"""

    patchable_fields = [
        "local",
        "name",
        "peer",
    ]
    """local,name,peer,"""

    postable_fields = [
        "ipspace.name",
        "ipspace.uuid",
        "local",
        "name",
        "peer",
    ]
    """ipspace.name,ipspace.uuid,local,name,peer,"""

class BgpPeerGroup(Resource):
    r""" A BGP peer group between a local network interface and a router, for the purpose of announcing VIP interface locations for SVMs in this IPspace. """

    _schema = BgpPeerGroupSchema
    _path = "/api/network/ip/bgp/peer-groups"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the details of all BGP peer groups for VIP.
### Related ONTAP Commands
* `network bgp peer-group show`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all BgpPeerGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent BgpPeerGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["BgpPeerGroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a BGP peer group for VIP.
### Related ONTAP commands
* `network bgp peer-group modify`
* `network bgp peer-group rename`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["BgpPeerGroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["BgpPeerGroup"], NetAppResponse]:
        r"""Creates a new BGP peer group for VIP. Multipath-routing is turned on cluster-wide automatically if the peer group being created results in multiple paths being available for an existing or future VIP interface.<br/>
### Required properties
* `name` - Name of the peer-group to create.
* `ipspace.name` or `ipspace.uuid` or `local.port`
  * Required with local.interface.name or local.ip.address to identify a local interface
  * Optional when local.interface.uuid is specified
* `local.interface.uuid` or `local.interface.name` or `local.ip.address`
  * Required when specifying an existing local interface.
* `local.ip` and `local.port`
  * Required to create a new local interface.
* `peer.address` - IP address of the peer router
### Default property values
If not specified in POST, the following default property values are assigned:
* `is_next_hop` - _false_
* `peer.md5_enabled` - _false_
### Related ONTAP commands
* `network bgp peer-group create`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["BgpPeerGroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a BGP peer group for VIP.
### Related ONTAP commands
* `network bgp peer-group delete`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the details of all BGP peer groups for VIP.
### Related ONTAP Commands
* `network bgp peer-group show`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a BGP peer group for VIP.
### Related ONTAP commands
* `network bgp peer-group show`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
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
        r"""Creates a new BGP peer group for VIP. Multipath-routing is turned on cluster-wide automatically if the peer group being created results in multiple paths being available for an existing or future VIP interface.<br/>
### Required properties
* `name` - Name of the peer-group to create.
* `ipspace.name` or `ipspace.uuid` or `local.port`
  * Required with local.interface.name or local.ip.address to identify a local interface
  * Optional when local.interface.uuid is specified
* `local.interface.uuid` or `local.interface.name` or `local.ip.address`
  * Required when specifying an existing local interface.
* `local.ip` and `local.port`
  * Required to create a new local interface.
* `peer.address` - IP address of the peer router
### Default property values
If not specified in POST, the following default property values are assigned:
* `is_next_hop` - _false_
* `peer.md5_enabled` - _false_
### Related ONTAP commands
* `network bgp peer-group create`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
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
        r"""Updates a BGP peer group for VIP.
### Related ONTAP commands
* `network bgp peer-group modify`
* `network bgp peer-group rename`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
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
        r"""Deletes a BGP peer group for VIP.
### Related ONTAP commands
* `network bgp peer-group delete`

### Learn more
* [`DOC /network/ip/bgp/peer-groups`](#docs-networking-network_ip_bgp_peer-groups)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


