r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The Fibre Channel (FC) fabric REST APIs provide read-only access to FC network information. This includes:

* the connections between the ONTAP cluster and the FC fabric,
* the switches that comprise the fabric, and
* the zones of the active zoneset of the fabric.
## Caching
Obtaining this information from the FC fabric can be time consuming. To allow the REST API to be more responsive, the APIs always return data from a cache that is updated asynchronously, but only on demand. Cache updates are triggered when the age of cached data exceeds the caller-specified maximum age as specified by the query parameter `cache.maximum_age`.</br>
When a GET request initiates a cache refresh, the API attempts to wait for the update to complete before returning. If the cache cannot be updated before the return timeout (see query parameter `return_timeout`), the GET returns the currently cached data, but the cache update continues asynchronously. The caller may examine the returned property `cache.update_time` or `cache.age` to determine if the returned information is sufficiently fresh. If not, the caller should wait several seconds, then make a GET request again until the returned information is updated.
## Examples
Fibre Channel fabric data is typically large. The numbers of rows returned in the following examples has been edited to simplify reading.
### Retrieving the Fibre Channel fabrics to which the cluster is connected
This example retrieves the names of the cluster's connected Fibre Channel fabrics. It also retrieves the cache timestamp properties so that the caller can verify the currency of the data.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Fabric

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Fabric.get_collection(fields="cache")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Fabric(
        {
            "name": "10:00:aa:bb:cc:dd:ee:ff",
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10%3A00%3Aaa%3Abb%3Acc%3Add%3Aee%3Aff"
                }
            },
            "cache": {
                "age": "PT1M16S",
                "is_current": True,
                "update_time": "2022-02-07T21:21:29+00:00",
            },
        }
    ),
    Fabric(
        {
            "name": "10:00:ff:ee:dd:cc:bb:aa",
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10%3A00%3Aff%3Aee%3Add%3Acc%3Abb%3Aaa"
                }
            },
            "cache": {
                "age": "PT1M16S",
                "is_current": True,
                "update_time": "2022-02-07T21:21:29+00:00",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving all switches of a Fibre Channel fabric
This example retrieves the switches of Fibre Channel fabric `10:00:aa:bb:cc:dd:ee:ff`.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcSwitch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcSwitch.get_collection("10:00:aa:bb:cc:dd:ee:ff", fields="cache")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    FcSwitch(
        {
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/switches/10:00:1a:1b:1c:1d:1e:1f"
                }
            },
            "cache": {
                "age": "PT45S",
                "is_current": True,
                "update_time": "2022-02-07T21:22:00+00:00",
            },
            "wwn": "10:00:1a:1b:1c:1d:1e:1f",
        }
    ),
    FcSwitch(
        {
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/switches/10:00:2a:2b:2c:2d:2e:1f"
                }
            },
            "cache": {
                "age": "PT45S",
                "is_current": True,
                "update_time": "2022-02-07T21:22:00+00:00",
            },
            "wwn": "10:00:2a:2b:2c:2d:2e:1f",
        }
    ),
    FcSwitch(
        {
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/switches/10:00:3a:3b:3c:3d:3e:3f"
                }
            },
            "cache": {
                "age": "PT45S",
                "is_current": True,
                "update_time": "2022-02-07T21:22:00+00:00",
            },
            "wwn": "10:00:3a:3b:3c:3d:3e:3f",
        }
    ),
    FcSwitch(
        {
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/switches/10:00:4a:4b:4c:4d:4e:4f"
                }
            },
            "cache": {
                "age": "PT45S",
                "is_current": True,
                "update_time": "2022-02-07T21:22:00+00:00",
            },
            "wwn": "10:00:4a:4b:4c:4d:4e:4f",
        }
    ),
    FcSwitch(
        {
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/switches/10:00:5a:5b:1a:5c:5d:5e"
                }
            },
            "cache": {
                "age": "PT45S",
                "is_current": True,
                "update_time": "2022-02-07T21:22:00+00:00",
            },
            "wwn": "10:00:5a:5b:1a:5c:5d:5e",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all zones of the active zoneset of a Fibre Channel fabric
This example retrieves the zone of the active set of Fibre Channel fabric `10:00:aa:bb:cc:dd:ee:ff`.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcZone

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcZone.get_collection("10:00:aa:bb:cc:dd:ee:ff", fields="cache")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    FcZone(
        {
            "name": "zone1",
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/zones/zone1"
                }
            },
            "cache": {
                "age": "PT1H17M54S",
                "is_current": True,
                "update_time": "2022-02-07T20:17:06+00:00",
            },
        }
    ),
    FcZone(
        {
            "name": "zone2",
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/zones/zone2"
                }
            },
            "cache": {
                "age": "PT1H17M54S",
                "is_current": True,
                "update_time": "2022-02-07T20:17:06+00:00",
            },
        }
    ),
    FcZone(
        {
            "name": "zone3",
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/zones/zone3"
                }
            },
            "cache": {
                "age": "PT1H17M54S",
                "is_current": True,
                "update_time": "2022-02-07T20:17:06+00:00",
            },
        }
    ),
    FcZone(
        {
            "name": "zone4",
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/zones/zone4"
                }
            },
            "cache": {
                "age": "PT1H17M54S",
                "is_current": True,
                "update_time": "2022-02-07T20:17:06+00:00",
            },
        }
    ),
]

```
</div>
</div>

---
### Searching all Fibre Channel fabrics for a specific attached device identified by its WWPN
This example finds the Fibre Channel fabric, switch, and switch port to which the device with WWPN `50:0a:2a:2b:2c:2d:2e:2f` is attached. Note the use of the wildcard character in place of a fabric WWN in order to search all Fibre Channel fabrics.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcSwitch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FcSwitch.get_collection(
                "*",
                fields="ports,cache",
                **{"ports.attached_device.wwpn": "50:0a:2a:2b:2c:2d:2e:2f"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    FcSwitch(
        {
            "ports": [
                {
                    "slot": "0",
                    "attached_device": {
                        "wwpn": "50:0a:1a:1b:1c:1d:1e:1f",
                        "port_id": "0x999000",
                    },
                    "state": "online",
                    "wwpn": "20:00:1a:1b:1c:1d:1e:1f",
                    "type": "f_port",
                },
                {
                    "slot": "1",
                    "attached_device": {
                        "wwpn": "50:0a:2a:2b:2c:2d:2e:2f",
                        "port_id": "0x999100",
                    },
                    "state": "online",
                    "wwpn": "20:01:2a:2b:1c:2d:2e:2f",
                    "type": "f_port",
                },
                {
                    "slot": "2",
                    "state": "offline",
                    "wwpn": "20:02:3a:3b:3c:3d:3e:3f",
                    "type": "none",
                },
                {
                    "slot": "3",
                    "attached_device": {
                        "wwpn": "50:0a:4a:4b:4c:4d:4e:4f",
                        "port_id": "0x999300",
                    },
                    "state": "offline",
                    "wwpn": "20:03:4a:4b:4c:4d:4e:4f",
                    "type": "f_port",
                },
                {
                    "slot": "4",
                    "attached_device": {
                        "wwpn": "50:0a:5a:5b:5c:5d:5e:5f",
                        "port_id": "0x999400",
                    },
                    "state": "online",
                    "wwpn": "20:04:5a:5b:5c:5d:5e:5f",
                    "type": "f_port",
                },
            ],
            "fabric": {
                "name": "10:00:aa:bb:cc:dd:ee:ff",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/fabrics/10%3A00%3Aaa%3Abb%3Acc%3Add%3Aee%3Aff"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/network/fc/fabrics/10:00:aa:bb:cc:dd:ee:ff/switches/10:00:6a:6b:6c:6d:6e:6f"
                }
            },
            "cache": {
                "age": "PT4M49S",
                "is_current": True,
                "update_time": "2022-02-07T21:57:29+00:00",
            },
            "wwn": "10:00:6a:6b:6c:6d:6e:6f",
        }
    )
]

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


__all__ = ["Fabric", "FabricSchema"]
__pdoc__ = {
    "FabricSchema.resource": False,
    "FabricSchema.opts": False,
}


class FabricSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Fabric object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the fabric."""

    cache = marshmallow_fields.Nested("netapp_ontap.models.fabric_cache.FabricCacheSchema", data_key="cache", unknown=EXCLUDE, allow_none=True)
    r""" Properties of Fibre Chanel fabric cache."""

    connections = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.fabric_connections.FabricConnectionsSchema", unknown=EXCLUDE, allow_none=True), data_key="connections", allow_none=True)
    r""" An array of the connections between the cluster and the switches Fibre Channel fabric."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The world wide name (WWN) of the primary switch of the Fibre Channel (FC) fabric. This is used as a unique identifier for the FC fabric.


Example: 10:00:c1:c2:c3:c4:c5:c6"""

    zoneset = marshmallow_fields.Nested("netapp_ontap.models.fabric_zoneset.FabricZonesetSchema", data_key="zoneset", unknown=EXCLUDE, allow_none=True)
    r""" The active Fibre Channel zoneset in the fabric."""

    @property
    def resource(self):
        return Fabric

    gettable_fields = [
        "links",
        "cache",
        "connections",
        "name",
        "zoneset",
    ]
    """links,cache,connections,name,zoneset,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class Fabric(Resource):
    r""" A Fibre Channel (FC) fabric REST object provides information about an FC network (fabric) connected to the cluster. Logically, the FC fabric also contains FC switches and the FC zones that comprise the active zoneset of the fabric. FC switch and zone information is not reported directly in the FC fabric REST object for reasons of scale and flexibility; they are found by querying the FC switches and FC zones REST endpoints. """

    _schema = FabricSchema
    _path = "/api/network/fc/fabrics"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Fibre Channel fabrics.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connections`
* `zoneset`
### Related ONTAP commands
* `network fcp topology show`
* `network fcp zone show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
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
        """Returns a count of all Fabric resources that match the provided query"""
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
        """Returns a list of RawResources that represent Fabric resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Fibre Channel fabrics.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connections`
* `zoneset`
### Related ONTAP commands
* `network fcp topology show`
* `network fcp zone show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a Fibre Channel fabric.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connections`
* `zoneset`
### Related ONTAP commands
* `network fcp topology show`
* `network fcp zone show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





