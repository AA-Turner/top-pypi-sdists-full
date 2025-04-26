r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A broadcast domain is a collection of Ethernet ports that have layer 2 connectivity. They are used to determine which Ethernet ports can host interfaces of various types. The broadcast domain REST API allows you to retrieve, create, modify, and delete broadcast domains. The broadcast domain APIs do not manage port membership. To add a port to a broadcast domain or to move a port to a different broadcast domain, use PATCH /network/ethernet/ports/<uuid>.
## Retrieving network Ethernet broadcast domain information
The broadcast domains GET API retrieves and displays relevant information pertaining to the broadcast domains configured in the cluster. The API retrieves the list of all broadcast domains configured in the cluster, or a specific broadcast domain.
<br/>
---
## Examples
### Retrieving all broadcast domains in the cluster
The following output shows the list of all broadcast domains configured in a cluster.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(BroadcastDomain.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    BroadcastDomain(
        {
            "ipspace": {
                "name": "Cluster",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/6267eff8-f34f-11e8-8373-005056bb6b85"
                    }
                },
                "uuid": "6267eff8-f34f-11e8-8373-005056bb6b85",
            },
            "ports": [
                {
                    "name": "e0a",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/626b4d19-f34f-11e8-8373-005056bb6b85"
                        }
                    },
                    "node": {"name": "examplecluster-node01"},
                    "uuid": "626b4d19-f34f-11e8-8373-005056bb6b85",
                },
                {
                    "name": "e0b",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/626b77b9-f34f-11e8-8373-005056bb6b85"
                        }
                    },
                    "node": {"name": "examplecluster-node01"},
                    "uuid": "626b77b9-f34f-11e8-8373-005056bb6b85",
                },
            ],
            "name": "Cluster",
            "uuid": "6970c2a9-f34f-11e8-8373-005056bb6b85",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/6970c2a9-f34f-11e8-8373-005056bb6b85"
                }
            },
            "mtu": 9000,
        }
    ),
    BroadcastDomain(
        {
            "ipspace": {
                "name": "Default",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/5f650349-f34f-11e8-8373-005056bb6b85"
                    }
                },
                "uuid": "5f650349-f34f-11e8-8373-005056bb6b85",
            },
            "ports": [
                {
                    "name": "e0c",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/626bae19-f34f-11e8-8373-005056bb6b85"
                        }
                    },
                    "node": {"name": "examplecluster-node01"},
                    "uuid": "626bae19-f34f-11e8-8373-005056bb6b85",
                },
                {
                    "name": "e0d",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/626bd677-f34f-11e8-8373-005056bb6b85"
                        }
                    },
                    "node": {"name": "examplecluster-node01"},
                    "uuid": "626bd677-f34f-11e8-8373-005056bb6b85",
                },
            ],
            "name": "Default",
            "uuid": "6972416c-f34f-11e8-8373-005056bb6b85",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/6972416c-f34f-11e8-8373-005056bb6b85"
                }
            },
            "mtu": 1500,
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific broadcast domain
The following output shows the response returned when a specific broadcast domain is requested. The system returns an error if there is no broadcast domain with the requested UUID.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BroadcastDomain(uuid="4475a2c8-f8a0-11e8-8d33-005056bb986f")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
BroadcastDomain(
    {
        "ipspace": {
            "name": "Cluster",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/3e518ed5-f8a0-11e8-8d33-005056bb986f"
                }
            },
            "uuid": "3e518ed5-f8a0-11e8-8d33-005056bb986f",
        },
        "ports": [
            {
                "name": "e0a",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/3e539a62-f8a0-11e8-8d33-005056bb986f"
                    }
                },
                "node": {"name": "examplecluster-node01"},
                "uuid": "3e539a62-f8a0-11e8-8d33-005056bb986f",
            },
            {
                "name": "e0b",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/3e53c94a-f8a0-11e8-8d33-005056bb986f"
                    }
                },
                "node": {"name": "examplecluster-node01"},
                "uuid": "3e53c94a-f8a0-11e8-8d33-005056bb986f",
            },
        ],
        "name": "Cluster",
        "uuid": "4475a2c8-f8a0-11e8-8d33-005056bb986f",
        "_links": {
            "self": {
                "href": "/api/network/ethernet/broadcast-domains/4475a2c8-f8a0-11e8-8d33-005056bb986f/"
            }
        },
        "mtu": 9000,
    }
)

```
</div>
</div>

---
### Retrieving all broadcast domains with a specific name
The following output shows the response returned when broadcast domains with a specific name in any IPspace are requested.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection(
    "10.224.87.121", username="admin", password="password", verify=False
):
    print(list(BroadcastDomain.get_collection(name="bd1")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    BroadcastDomain(
        {
            "name": "bd1",
            "uuid": "66b607e5-4bee-11e9-af6a-005056bb13c0",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/66b607e5-4bee-11e9-af6a-005056bb13c0"
                }
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving the broadcast domains for an IPspace
The following output shows the response returned when the broadcast domains for a specified IPspace are requested.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection(
    "10.224.87.121", username="admin", password="password", verify=False
):
    print(
        list(BroadcastDomain.get_collection(fields="*", **{"ipspace.name": "Cluster"}))
    )

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    BroadcastDomain(
        {
            "ipspace": {
                "name": "Cluster",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/ac466a88-4bed-11e9-af6a-005056bb13c0"
                    }
                },
                "uuid": "ac466a88-4bed-11e9-af6a-005056bb13c0",
            },
            "ports": [
                {
                    "name": "e0a",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/acd67884-4bed-11e9-af6a-005056bb13c0"
                        }
                    },
                    "node": {"name": "examplecluster-node-1"},
                    "uuid": "acd67884-4bed-11e9-af6a-005056bb13c0",
                },
                {
                    "name": "e0b",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/ace1a36f-4bed-11e9-af6a-005056bb13c0"
                        }
                    },
                    "node": {"name": "examplecluster-node-1"},
                    "uuid": "ace1a36f-4bed-11e9-af6a-005056bb13c0",
                },
            ],
            "name": "Cluster",
            "uuid": "ae69070c-4bed-11e9-af6a-005056bb13c0",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/ae69070c-4bed-11e9-af6a-005056bb13c0"
                }
            },
            "mtu": 1500,
        }
    )
]

```
</div>
</div>

---
## Creating network Ethernet broadcast domains
You can use the POST API to create broadcast domains.
<br/>
---
## Example
### Creating a new broadcast domain
The following example shows how to create a broadcast domain with a name of 'bd1' and an MTU of 1500.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BroadcastDomain()
    resource.name = "bd1"
    resource.mtu = 1500
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
BroadcastDomain(
    {
        "name": "bd1",
        "_links": {"self": {"href": "/api/network/ethernet/broadcast-domains/"}},
        "mtu": 1500,
    }
)

```
</div>
</div>

---
## Updating network Ethernet broadcast domains
You can use the PATCH API to update the attributes of broadcast domains.
<br/>
---
## Examples
### Updating the name and MTU of a specific broadcast domain
The following example shows how the PATCH request changes the broadcast domain name to 'bd2' and the broadcast domain MTU to 9000.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BroadcastDomain(uuid="6cde03b2-f8a2-11e8-8d33-005056bb986f")
    resource.name = "bd2"
    resource.mtu = 9000
    resource.patch()

```

---
### Updating the IPspace of a specific broadcast domain
The following example shows how the PATCH request changes the IPspace of a broadcast domain to 'ipspace2'.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BroadcastDomain(uuid="c6fe2541-61f4-11e9-a66e-005056bbe83e")
    resource.ipspace = {"name": "ipspace2"}
    resource.patch()

```

---
## Deleting network Ethernet broadcast domains
You can use the DELETE API to delete a broadcast domain from the cluster configuration.
## Example
### Deleting a specific broadcast domain
The following DELETE request deletes a broadcast domain.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import BroadcastDomain

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = BroadcastDomain(uuid="6cde03b2-f8a2-11e8-8d33-005056bb986f")
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


__all__ = ["BroadcastDomain", "BroadcastDomainSchema"]
__pdoc__ = {
    "BroadcastDomainSchema.resource": False,
    "BroadcastDomainSchema.opts": False,
}


class BroadcastDomainSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BroadcastDomain object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the broadcast_domain."""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the broadcast_domain."""

    mtu = Size(
        data_key="mtu",
        validate=integer_validation(minimum=68),
        allow_none=True,
    )
    r""" Maximum transmission unit, largest packet size on this network

Example: 1500"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the broadcast domain, scoped to its IPspace

Example: bd1"""

    ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.port.PortSchema", unknown=EXCLUDE, allow_none=True), data_key="ports", allow_none=True)
    r""" Ports that belong to the broadcast domain"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Broadcast domain UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return BroadcastDomain

    gettable_fields = [
        "links",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "mtu",
        "name",
        "ports.links",
        "ports.name",
        "ports.node",
        "ports.uuid",
        "uuid",
    ]
    """links,ipspace.links,ipspace.name,ipspace.uuid,mtu,name,ports.links,ports.name,ports.node,ports.uuid,uuid,"""

    patchable_fields = [
        "ipspace.name",
        "ipspace.uuid",
        "mtu",
        "name",
    ]
    """ipspace.name,ipspace.uuid,mtu,name,"""

    postable_fields = [
        "ipspace.name",
        "ipspace.uuid",
        "mtu",
        "name",
    ]
    """ipspace.name,ipspace.uuid,mtu,name,"""

class BroadcastDomain(Resource):
    r""" Set of ports that will receive a broadcast Ethernet packet from any of them """

    _schema = BroadcastDomainSchema
    _path = "/api/network/ethernet/broadcast-domains"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of broadcast domains for the entire cluster.
### Related ONTAP commands
* `network port broadcast-domain show`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all BroadcastDomain resources that match the provided query"""
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
        """Returns a list of RawResources that represent BroadcastDomain resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["BroadcastDomain"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of a broadcast domain.
### Related ONTAP commands
* `network port broadcast-domain modify`
* `network port broadcast-domain rename`
* `network port broadcast-domain move`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["BroadcastDomain"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["BroadcastDomain"], NetAppResponse]:
        r"""Creates a new broadcast domain.<br/>
### Required properties
* `name` - Name of the broadcast-domain to create.
* `mtu` - Maximum transmission unit (MTU) of the broadcast domain.
### Recommended optional properties
* `ipspace.name` or `ipspace.uuid` - IPspace the broadcast domain belongs to.
### Default property values
If not specified in POST, the following default property values are assigned:
* `ipspace` - _Default_
### Related ONTAP commands
* `network port broadcast-domain create`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["BroadcastDomain"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a broadcast domain.
### Related ONTAP commands
* `network port broadcast-domain delete`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of broadcast domains for the entire cluster.
### Related ONTAP commands
* `network port broadcast-domain show`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a broadcast domain.
### Related ONTAP commands
* `network port broadcast-domain show`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
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
        r"""Creates a new broadcast domain.<br/>
### Required properties
* `name` - Name of the broadcast-domain to create.
* `mtu` - Maximum transmission unit (MTU) of the broadcast domain.
### Recommended optional properties
* `ipspace.name` or `ipspace.uuid` - IPspace the broadcast domain belongs to.
### Default property values
If not specified in POST, the following default property values are assigned:
* `ipspace` - _Default_
### Related ONTAP commands
* `network port broadcast-domain create`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
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
        r"""Updates the properties of a broadcast domain.
### Related ONTAP commands
* `network port broadcast-domain modify`
* `network port broadcast-domain rename`
* `network port broadcast-domain move`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
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
        r"""Deletes a broadcast domain.
### Related ONTAP commands
* `network port broadcast-domain delete`

### Learn more
* [`DOC /network/ethernet/broadcast-domains`](#docs-networking-network_ethernet_broadcast-domains)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


