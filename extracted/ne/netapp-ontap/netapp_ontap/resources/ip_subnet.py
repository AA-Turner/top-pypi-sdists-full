r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The following operations are supported:

* Creation: POST network/ip/subnets
* Collection Get: GET network/ip/subnets
* Instance Get: GET network/ip/subnets/{uuid}
* Instance Patch: PATCH network/ip/subnets/{uuid}
* Instance Delete: DELETE network/ip/subnets/{uuid}
## Retrieving IP subnet information
The IP subnets GET API retrieves and displays relevant information pertaining to the subnets configured in the cluster. The response can contain a list of multiple subnets or a specific subnet.
## Examples
### Retrieving all subnets in the cluster
The following example shows the list of all subnets configured in a cluster.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(IpSubnet.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    IpSubnet(
        {
            "name": "Subnet-002",
            "uuid": "451d8d99-582c-11ec-8572-005056acd597",
            "_links": {
                "self": {
                    "href": "/api/network/ip/subnets/451d8d99-582c-11ec-8572-005056acd597"
                }
            },
        }
    ),
    IpSubnet(
        {
            "name": "Subnet-001",
            "uuid": "615b722f-5795-11ec-8572-005056acd597",
            "_links": {
                "self": {
                    "href": "/api/network/ip/subnets/615b722f-5795-11ec-8572-005056acd597"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific subnet
The following example shows the response when a specific subnet is requested. This is equivalent to fields=*, which returns most of the fields. The system returns an error when there is no subnet with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpSubnet(uuid="451d8d99-582c-11ec-8572-005056acd597")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
IpSubnet(
    {
        "broadcast_domain": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/9a1dce3b-5780-11ec-8572-005056acd597"
                }
            },
            "uuid": "9a1dce3b-5780-11ec-8572-005056acd597",
        },
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/6f62c691-5780-11ec-8572-005056acd597"
                }
            },
            "uuid": "6f62c691-5780-11ec-8572-005056acd597",
        },
        "name": "Subnet-002",
        "uuid": "451d8d99-582c-11ec-8572-005056acd597",
        "_links": {
            "self": {
                "href": "/api/network/ip/subnets/451d8d99-582c-11ec-8572-005056acd597"
            }
        },
        "subnet": {"netmask": "24", "family": "ipv4", "address": "10.2.1.0"},
        "gateway": "10.2.1.1",
    }
)

```
</div>
</div>

---
### Retrieving all the fields for a specific subnet
The following example shows the response when all the fields for a specific subnet are requested, returning everything that fields=* returns plus the IP ranges and count fields. The system returns an error when there is no subnet with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpSubnet(uuid="451d8d99-582c-11ec-8572-005056acd597")
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
IpSubnet(
    {
        "broadcast_domain": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/9a1dce3b-5780-11ec-8572-005056acd597"
                }
            },
            "uuid": "9a1dce3b-5780-11ec-8572-005056acd597",
        },
        "ip_ranges": [
            {"end": "10.2.1.22", "family": "ipv4", "start": "10.2.1.10"},
            {"end": "10.2.1.200", "family": "ipv4", "start": "10.2.1.101"},
        ],
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/6f62c691-5780-11ec-8572-005056acd597"
                }
            },
            "uuid": "6f62c691-5780-11ec-8572-005056acd597",
        },
        "name": "Subnet-002",
        "total_count": 113,
        "uuid": "451d8d99-582c-11ec-8572-005056acd597",
        "used_count": 0,
        "_links": {
            "self": {
                "href": "/api/network/ip/subnets/451d8d99-582c-11ec-8572-005056acd597?fields=**"
            }
        },
        "available_count": 113,
        "available_ip_ranges": [
            {"end": "10.2.1.22", "family": "ipv4", "start": "10.2.1.10"},
            {"end": "10.2.1.200", "family": "ipv4", "start": "10.2.1.101"},
        ],
        "subnet": {"netmask": "24", "family": "ipv4", "address": "10.2.1.0"},
        "gateway": "10.2.1.1",
    }
)

```
</div>
</div>

---
## Creating IP subnets
You can use the IP subnets POST API to create IP subnets as shown in the following examples.
<br/>
---
## Examples
### Creating an IP subnet using the minimum number of parameters.
The following example shows the record returned after the creation of an IP subnet.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpSubnet()
    resource.name = "Subnet-003"
    resource.broadcast_domain = {"uuid": "6577524b-5863-11ec-8981-005056a7077f"}
    resource.subnet = {"address": "10.3.0.0", "netmask": "16"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Creating an IP subnet using all parameters.
The following example shows the record returned after the creation of an IP subnet setting all parameters.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpSubnet()
    resource.name = "Subnet-004"
    resource.ipspace = {
        "name": "Default",
        "uuid": "36569d0f-5863-11ec-8981-005056a7077f",
    }
    resource.broadcast_domain = {
        "name": "Default",
        "uuid": "6577524b-5863-11ec-8981-005056a7077f",
    }
    resource.subnet = {"address": "10.4.1.0", "netmask": "24"}
    resource.gateway = "10.4.1.1"
    resource.ip_ranges = [
        {"start": "10.4.1.30", "end": "10.4.1.39"},
        {"start": "10.4.1.150", "end": "10.4.1.229"},
    ]
    resource.fail_if_lifs_conflict = False
    resource.post(hydrate=True)
    print(resource)

```

---
## Updating IP subnets
You can use the IP subnets PATCH API to update the attributes of an IP subnet.
<br/>
---
## Examples
### Updating the name of an IP subnet
The following example shows how the PATCH request changes the name.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpSubnet(uuid="0e0a19e7-59ba-11ec-8981-005056a7077f")
    resource.name = "Subnet-004-NewName"
    resource.patch()

```

---
### Updating the ip_ranges of an IP subnet
The following example shows how the PATCH request updates the ip_ranges.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpSubnet(uuid="0e0a19e7-59ba-11ec-8981-005056a7077f")
    resource.ip_ranges = [{"start": "10.4.1.20", "end": "10.4.1.239"}]
    resource.patch()

```

---
## Deleting IP subnets
You can use the IP subnets DELETE API to delete an IP subnet.
<br/>
---
## Example
### Deleting an IP subnet
The following DELETE request deletes a specific network IP subnet.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpSubnet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpSubnet(uuid="0e0a19e7-59ba-11ec-8981-005056a7077f")
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


__all__ = ["IpSubnet", "IpSubnetSchema"]
__pdoc__ = {
    "IpSubnetSchema.resource": False,
    "IpSubnetSchema.opts": False,
}


class IpSubnetSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpSubnet object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ip_subnet."""

    available_count = Size(
        data_key="available_count",
        allow_none=True,
    )
    r""" The available_count field of the ip_subnet."""

    available_ip_ranges = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ip_address_range.IpAddressRangeSchema", unknown=EXCLUDE, allow_none=True), data_key="available_ip_ranges", allow_none=True)
    r""" IP address range"""

    broadcast_domain = marshmallow_fields.Nested("netapp_ontap.models.broadcast_domain_svm.BroadcastDomainSvmSchema", data_key="broadcast_domain", unknown=EXCLUDE, allow_none=True)
    r""" The broadcast_domain field of the ip_subnet."""

    fail_if_lifs_conflict = marshmallow_fields.Boolean(
        data_key="fail_if_lifs_conflict",
        allow_none=True,
    )
    r""" This action will fail if any existing interface is using an IP address in the ranges provided. Set this to false to associate any manually addressed interfaces with the subnet and allow the action to succeed."""

    gateway = marshmallow_fields.Str(
        data_key="gateway",
        allow_none=True,
    )
    r""" The IP address of the gateway for this subnet.

Example: 10.1.1.1"""

    ip_ranges = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ip_address_range.IpAddressRangeSchema", unknown=EXCLUDE, allow_none=True), data_key="ip_ranges", allow_none=True)
    r""" IP address range"""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the ip_subnet."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Subnet name

Example: subnet1"""

    subnet = marshmallow_fields.Nested("netapp_ontap.models.ip_info.IpInfoSchema", data_key="subnet", unknown=EXCLUDE, allow_none=True)
    r""" IP information"""

    total_count = Size(
        data_key="total_count",
        allow_none=True,
    )
    r""" The total_count field of the ip_subnet."""

    used_count = Size(
        data_key="used_count",
        allow_none=True,
    )
    r""" The used_count field of the ip_subnet."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID that uniquely identifies the subnet.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return IpSubnet

    gettable_fields = [
        "links",
        "available_count",
        "available_ip_ranges",
        "broadcast_domain.links",
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "gateway",
        "ip_ranges",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "name",
        "subnet",
        "total_count",
        "used_count",
        "uuid",
    ]
    """links,available_count,available_ip_ranges,broadcast_domain.links,broadcast_domain.name,broadcast_domain.uuid,gateway,ip_ranges,ipspace.links,ipspace.name,ipspace.uuid,name,subnet,total_count,used_count,uuid,"""

    patchable_fields = [
        "fail_if_lifs_conflict",
        "gateway",
        "ip_ranges",
        "name",
        "subnet",
    ]
    """fail_if_lifs_conflict,gateway,ip_ranges,name,subnet,"""

    postable_fields = [
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "fail_if_lifs_conflict",
        "gateway",
        "ip_ranges",
        "ipspace.name",
        "ipspace.uuid",
        "name",
        "subnet",
    ]
    """broadcast_domain.name,broadcast_domain.uuid,fail_if_lifs_conflict,gateway,ip_ranges,ipspace.name,ipspace.uuid,name,subnet,"""

class IpSubnet(Resource):
    """Allows interaction with IpSubnet objects on the host"""

    _schema = IpSubnetSchema
    _path = "/api/network/ip/subnets"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves details for all subnets.
### Related ONTAP Commands
* `network subnet show`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all IpSubnet resources that match the provided query"""
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
        """Returns a list of RawResources that represent IpSubnet resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["IpSubnet"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an IP subnet.
### Related ONTAP commands
* `network subnet modify`
* `network subnet rename`
* `network subnet add-ranges`
* `network subnet remove-ranges`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["IpSubnet"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IpSubnet"], NetAppResponse]:
        r"""Creates a new named subnet.
### Required properties
* `name` - Name of the subnet to create.
* `broadcast_domain` - Broadcast domain containing the subnet.
* `ipspace` - IPspace containing the subnet. Required only if `broadcast_domain.uuid` is not provided.
* `subnet.address` - IP address for the subnet.
* `subnet.netmask` - IP netmask of the subnet.
### Recommended property values
### Default property values
If not specified in POST, the following default property values are assigned:
* `gateway` - no gateway
* `ip_ranges` - empty
* `fail_if_lifs_conflict` - _true_
### Related ONTAP commands
* `network subnet create`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["IpSubnet"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an IP subnet.
### Related ONTAP commands
* `network subnet delete`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves details for all subnets.
### Related ONTAP Commands
* `network subnet show`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details for a specific IP subnet.
### Related ONTAP commands
* `network subnet show`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
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
        r"""Creates a new named subnet.
### Required properties
* `name` - Name of the subnet to create.
* `broadcast_domain` - Broadcast domain containing the subnet.
* `ipspace` - IPspace containing the subnet. Required only if `broadcast_domain.uuid` is not provided.
* `subnet.address` - IP address for the subnet.
* `subnet.netmask` - IP netmask of the subnet.
### Recommended property values
### Default property values
If not specified in POST, the following default property values are assigned:
* `gateway` - no gateway
* `ip_ranges` - empty
* `fail_if_lifs_conflict` - _true_
### Related ONTAP commands
* `network subnet create`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
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
        r"""Updates an IP subnet.
### Related ONTAP commands
* `network subnet modify`
* `network subnet rename`
* `network subnet add-ranges`
* `network subnet remove-ranges`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
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
        r"""Deletes an IP subnet.
### Related ONTAP commands
* `network subnet delete`

### Learn more
* [`DOC /network/ip/subnets`](#docs-networking-network_ip_subnets)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


