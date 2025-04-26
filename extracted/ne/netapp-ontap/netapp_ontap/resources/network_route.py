r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This endpoint supports the following operations: GET (collection and instance), POST, and DELETE.
<br/>
---
## Retrieving network routes
You can use the IP routes GET API to retrieve and display relevant information pertaining to the routes configured in the cluster. The API retrieves the list of all routes configured in the cluster, or a specific route. The fields that are returned in the response will differ with the configuration.
## Examples
### Retrieving all routes in the cluster
The following output shows the list of all routes configured in a cluster.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkRoute

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NetworkRoute.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NetworkRoute(
        {
            "destination": {"netmask": "18", "family": "ipv4", "address": "10.4.3.14"},
            "ipspace": {
                "name": "Default",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
                    }
                },
                "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
            },
            "uuid": "5fdffb0b-62f8-11e8-853d-005056b4c971",
            "_links": {
                "self": {
                    "href": "/api/network/ip/routes/5fdffb0b-62f8-11e8-853d-005056b4c971"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/3243312c-62f8-11e8-853d-005056b4c971"
                    }
                },
                "uuid": "3243312c-62f8-11e8-853d-005056b4c971",
            },
            "gateway": "10.4.3.1",
            "scope": "svm",
        }
    ),
    NetworkRoute(
        {
            "destination": {"netmask": "0", "family": "ipv6", "address": "::"},
            "ipspace": {
                "name": "ips1",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/cc71aadc-62f7-11e8-853d-005056b4c971"
                    }
                },
                "uuid": "cc71aadc-62f7-11e8-853d-005056b4c971",
            },
            "uuid": "84c128d2-62f9-11e8-853d-005056b4c971",
            "_links": {
                "self": {
                    "href": "/api/network/ip/routes/84c128d2-62f9-11e8-853d-005056b4c971"
                }
            },
            "gateway": "fd20:8b1e:b255:814e::1",
            "scope": "cluster",
        }
    ),
    NetworkRoute(
        {
            "destination": {"netmask": "0", "family": "ipv4", "address": "0.0.0.0"},
            "ipspace": {
                "name": "Default",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
                    }
                },
                "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
            },
            "uuid": "8cc72bcd-616c-11e8-a4df-005056b4c971",
            "_links": {
                "self": {
                    "href": "/api/network/ip/routes/8cc72bcd-616c-11e8-a4df-005056b4c971"
                }
            },
            "gateway": "10.224.64.1",
            "scope": "cluster",
        }
    ),
    NetworkRoute(
        {
            "destination": {
                "netmask": "64",
                "family": "ipv6",
                "address": "fd20:8b1e:b255:814e::",
            },
            "ipspace": {
                "name": "Default",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
                    }
                },
                "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
            },
            "uuid": "d63b6eee-62f9-11e8-853d-005056b4c971",
            "_links": {
                "self": {
                    "href": "/api/network/ip/routes/d63b6eee-62f9-11e8-853d-005056b4c971"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/3243312c-62f8-11e8-853d-005056b4c971"
                    }
                },
                "uuid": "3243312c-62f8-11e8-853d-005056b4c971",
            },
            "gateway": "fd20:8b1e:b255:814e::1",
            "scope": "svm",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific Cluster-scoped route
The following output shows the returned response when a specific Cluster-scoped route is requested. The system returns an error if there is no route with the requested UUID. SVM information is not returned for Cluster-scoped routes.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkRoute

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkRoute(uuid="84c128d2-62f9-11e8-853d-005056b4c971")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
NetworkRoute(
    {
        "destination": {"netmask": "0", "family": "ipv6", "address": "::"},
        "ipspace": {
            "name": "ips1",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/cc71aadc-62f7-11e8-853d-005056b4c971"
                }
            },
            "uuid": "cc71aadc-62f7-11e8-853d-005056b4c971",
        },
        "uuid": "84c128d2-62f9-11e8-853d-005056b4c971",
        "_links": {
            "self": {
                "href": "/api/network/ip/routes/84c128d2-62f9-11e8-853d-005056b4c971"
            }
        },
        "gateway": "fd20:8b1e:b255:814e::1",
        "scope": "cluster",
    }
)

```
</div>
</div>

---
### Retrieving a specific SVM-scoped route
The following output shows the returned response when a specific SVM-scoped route is requested. The system returns an error if there is no route with the requested UUID. The SVM object is only included for SVM-scoped routes.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkRoute

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkRoute(uuid="d63b6eee-62f9-11e8-853d-005056b4c971")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
NetworkRoute(
    {
        "destination": {
            "netmask": "64",
            "family": "ipv6",
            "address": "fd20:8b1e:b255:814e::",
        },
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/84f4beb2-616c-11e8-a4df-005056b4c971"
                }
            },
            "uuid": "84f4beb2-616c-11e8-a4df-005056b4c971",
        },
        "uuid": "d63b6eee-62f9-11e8-853d-005056b4c971",
        "_links": {
            "self": {
                "href": "/api/network/ip/routes/d63b6eee-62f9-11e8-853d-005056b4c971"
            }
        },
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/3243312c-62f8-11e8-853d-005056b4c971"}
            },
            "uuid": "3243312c-62f8-11e8-853d-005056b4c971",
        },
        "gateway": "fd20:8b1e:b255:814e::1",
        "scope": "svm",
    }
)

```
</div>
</div>

---
## Creating network routes
You can use the POST API to create an SVM-scoped route by specifying the associated SVM, or a Cluster-scoped route by specifying the associated IPspace.
## Examples
### Creating a Cluster-scoped route
IPspace is required to create a Cluster-scoped route. If the IPspace is not specified, the route will be created in the Default IPspace. The default destination will be set to "0.0.0.0/0" for IPv4 gateway addresses or "::/0" for IPv6 gateway addresses.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkRoute

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkRoute()
    resource.ipspace = {"name": "ips1"}
    resource.gateway = "10.10.10.1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
NetworkRoute(
    {
        "ipspace": {"name": "ips1"},
        "uuid": "ae583c9e-9ac7-11e8-8bc9-005056bbd531",
        "gateway": "10.10.10.1",
    }
)

```
</div>
</div>

---
### Creating an SVM-scoped route
To create an SVM-scoped route, the associated SVM can be identified by either its UUID or name.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkRoute

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkRoute()
    resource.svm = {"name": "vs0"}
    resource.gateway = "10.10.10.1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
NetworkRoute(
    {
        "uuid": "38805a91-9ac9-11e8-8bc9-005056bbd531",
        "svm": {"name": "vs0"},
        "gateway": "10.10.10.1",
    }
)

```
</div>
</div>

---
## Deleting network routes
You can use the DELETE API to delete a specific route identified by its UUID.
## Example
### Deleting a specific route
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkRoute

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkRoute(uuid="38805a91-9ac9-11e8-8bc9-005056bbd531")
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


__all__ = ["NetworkRoute", "NetworkRouteSchema"]
__pdoc__ = {
    "NetworkRouteSchema.resource": False,
    "NetworkRouteSchema.opts": False,
}


class NetworkRouteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NetworkRoute object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the network_route."""

    destination = marshmallow_fields.Nested("netapp_ontap.models.ip_info.IpInfoSchema", data_key="destination", unknown=EXCLUDE, allow_none=True)
    r""" IP information"""

    gateway = marshmallow_fields.Str(
        data_key="gateway",
        allow_none=True,
    )
    r""" The IP address of the gateway router leading to the destination.

Example: 10.1.1.1"""

    interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", unknown=EXCLUDE, allow_none=True), data_key="interfaces", allow_none=True)
    r""" IP interfaces on the same subnet as the gateway."""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the network_route."""

    metric = Size(
        data_key="metric",
        allow_none=True,
    )
    r""" Indicates a preference order between several routes to the same destination.  With typical usage, the default metrics provided are adequate, there is no need to specify a metric in the route creation."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the network_route."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the network_route."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID that uniquely identifies the route.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return NetworkRoute

    gettable_fields = [
        "links",
        "destination",
        "gateway",
        "interfaces.links",
        "interfaces.ip",
        "interfaces.name",
        "interfaces.uuid",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "metric",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,destination,gateway,interfaces.links,interfaces.ip,interfaces.name,interfaces.uuid,ipspace.links,ipspace.name,ipspace.uuid,metric,scope,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "destination",
        "gateway",
        "ipspace.name",
        "ipspace.uuid",
        "metric",
        "scope",
        "svm.name",
        "svm.uuid",
    ]
    """destination,gateway,ipspace.name,ipspace.uuid,metric,scope,svm.name,svm.uuid,"""

    postable_fields = [
        "destination",
        "gateway",
        "ipspace.name",
        "ipspace.uuid",
        "metric",
        "scope",
        "svm.name",
        "svm.uuid",
    ]
    """destination,gateway,ipspace.name,ipspace.uuid,metric,scope,svm.name,svm.uuid,"""

class NetworkRoute(Resource):
    """Allows interaction with NetworkRoute objects on the host"""

    _schema = NetworkRouteSchema
    _path = "/api/network/ip/routes"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of IP routes.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `interfaces.*`
### Related ONTAP commands
* `network route show`
* `network route show-lifs`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all NetworkRoute resources that match the provided query"""
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
        """Returns a list of RawResources that represent NetworkRoute resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["NetworkRoute"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NetworkRoute"], NetAppResponse]:
        r"""Creates a Cluster-scoped or SVM-scoped static route.
### Required properties
* `gateway` - IP address to route packets to.
* SVM-scoped routes
  * `svm.name` or `svm.uuid` - SVM that route is applied to.
* cluster-scoped routes
  * There are no additional required fields for Cluster-scoped routes.
### Default property values
If not specified in POST, the following default property values are assigned:
* `destination` - _0.0.0.0/0_ for IPv4 or _::/0_ for IPv6.
* `ipspace.name`
  * _Default_ for Cluster-scoped routes.
  * Name of the SVM's IPspace for SVM-scoped routes.
* `metric` - 20.
### Related ONTAP commands
* `network route create`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["NetworkRoute"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a specific IP route.
### Related ONTAP commands
* `network route delete`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of IP routes.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `interfaces.*`
### Related ONTAP commands
* `network route show`
* `network route show-lifs`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a specific IP route.
### Related ONTAP commands
* `network route show`
* `network route show-lifs`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
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
        r"""Creates a Cluster-scoped or SVM-scoped static route.
### Required properties
* `gateway` - IP address to route packets to.
* SVM-scoped routes
  * `svm.name` or `svm.uuid` - SVM that route is applied to.
* cluster-scoped routes
  * There are no additional required fields for Cluster-scoped routes.
### Default property values
If not specified in POST, the following default property values are assigned:
* `destination` - _0.0.0.0/0_ for IPv4 or _::/0_ for IPv6.
* `ipspace.name`
  * _Default_ for Cluster-scoped routes.
  * Name of the SVM's IPspace for SVM-scoped routes.
* `metric` - 20.
### Related ONTAP commands
* `network route create`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a specific IP route.
### Related ONTAP commands
* `network route delete`

### Learn more
* [`DOC /network/ip/routes`](#docs-networking-network_ip_routes)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


