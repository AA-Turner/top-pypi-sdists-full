r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Fibre Channel (FC) ports are the physical ports of FC adapters on ONTAP cluster nodes that can be connected to FC networks to provide FC network connectivity. An FC port defines the location of an FC interface within the ONTAP cluster.<br/>
The Fibre Channel port REST API allows you to discover FC ports, obtain status information for FC ports, and configure FC port properties. POST and DELETE requests are not supported. You must physically add and remove FC adapters to ONTAP nodes to create and remove ports from the ONTAP cluster.
## Performance monitoring
Performance of an FC port can be monitored by observing the `metric.*` and `statistics.*` properties. These properties show the performance of an FC port in terms of IOPS, latency, and throughput. The `metric.*` properties denote an average, whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
## Examples
### Retrieving all FC ports
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcPort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcPort.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    FcPort(
        {
            "name": "0a",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "uuid": "931b20f8-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b20f8-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "0b",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "uuid": "931b23f7-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b23f7-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "0c",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "uuid": "931b25ba-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b25ba-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "0d",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "uuid": "931b2748-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b2748-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "0e",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "uuid": "931b28c2-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b28c2-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "0f",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "uuid": "931b2a7b-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b2a7b-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "1b",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "uuid": "931b2e2b-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b2e2b-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving all FC ports with state _online_
The `state` query parameter is used to perform the query.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcPort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcPort.get_collection(state="online")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    FcPort(
        {
            "name": "0a",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "state": "online",
            "uuid": "931b20f8-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b20f8-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "0b",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "state": "online",
            "uuid": "931b23f7-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b23f7-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
    FcPort(
        {
            "name": "0c",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/3c768e01-1abc-4b3b-b7c0-629ceb62a497"
                    }
                },
                "uuid": "3c768e01-1abc-4b3b-b7c0-629ceb62a497",
            },
            "state": "online",
            "uuid": "931b25ba-b047-11e8-9af3-005056bb838e",
            "_links": {
                "self": {
                    "href": "/api/network/fc/ports/931b25ba-b047-11e8-9af3-005056bb838e"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving an FC port
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcPort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcPort(uuid="931b20f8-b047-11e8-9af3-005056bb838e")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
FcPort(
    {
        "metric": {
            "status": "ok",
            "iops": {"total": 0, "write": 0, "other": 0, "read": 0},
            "latency": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:15+00:00",
            "throughput": {"total": 0, "write": 0, "read": 0},
            "duration": "PT15S",
        },
        "supported_protocols": ["fcp"],
        "description": "Fibre Channel Target Adapter 0a (ACME Fibre Channel Adapter, rev. 1.0.0, 8G)",
        "statistics": {
            "status": "ok",
            "iops_raw": {"total": 3, "write": 0, "other": 3, "read": 0},
            "latency_raw": {"total": 38298, "write": 0, "other": 38298, "read": 0},
            "throughput_raw": {"total": 0, "write": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:42+00:00",
        },
        "fabric": {
            "connected": True,
            "port_address": "52100",
            "name": "55:0e:b1:a0:20:40:80:00",
            "switch_port": "ssan-g620-03:1",
            "connected_speed": 8,
        },
        "name": "0a",
        "speed": {"configured": "auto", "maximum": "8"},
        "node": {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/5a534a72-b047-11e8-9af3-005056bb838e"
                }
            },
            "uuid": "5a534a72-b047-11e8-9af3-005056bb838e",
        },
        "state": "online",
        "enabled": True,
        "uuid": "931b20f8-b047-11e8-9af3-005056bb838e",
        "_links": {
            "self": {
                "href": "/api/network/fc/ports/931b20f8-b047-11e8-9af3-005056bb838e"
            }
        },
        "wwpn": "50:0a:09:82:bb:83:8e:00",
        "physical_protocol": "fibre_channel",
        "wwnn": "50:0a:09:80:bb:83:8e:00",
        "transceiver": {
            "form_factor": "SFP",
            "manufacturer": "ACME",
            "part_number": "1000",
            "capabilities": [4, 8],
        },
    }
)

```
</div>
</div>

---
### Disabling an FC port
If an active FC interface exists on an FC port, the port cannot be disabled.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcPort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcPort(uuid="931b20f8-b047-11e8-9af3-005056bb838e")
    resource.enabled = False
    resource.patch()

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


__all__ = ["FcPort", "FcPortSchema"]
__pdoc__ = {
    "FcPortSchema.resource": False,
    "FcPortSchema.opts": False,
}


class FcPortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcPort object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the fc_port."""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" A description of the FC port.


Example: Fibre Channel Target Adapter 0a (ACME Fibre Channel Adapter, rev. 1.0.0, 8G)"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The administrative state of the FC port. If this property is set to _false_, all FC connectivity to FC interfaces are blocked. Optional in PATCH."""

    fabric = marshmallow_fields.Nested("netapp_ontap.models.fc_port_fabric.FcPortFabricSchema", data_key="fabric", unknown=EXCLUDE, allow_none=True)
    r""" Properties of the fabric to which the FC port is attached."""

    interface_count = Size(
        data_key="interface_count",
        allow_none=True,
    )
    r""" The number of FC interfaces currently provisioned on this port. This property is not supported in an SVM context."""

    metric = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_reduced_throughput.PerformanceMetricReducedThroughputSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The FC port name.


Example: 0a"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the fc_port."""

    physical_protocol = marshmallow_fields.Str(
        data_key="physical_protocol",
        validate=enum_validation(['fibre_channel', 'ethernet']),
        allow_none=True,
    )
    r""" The physical network protocol of the FC port.


Valid choices:

* fibre_channel
* ethernet"""

    speed = marshmallow_fields.Nested("netapp_ontap.models.fc_port_speed.FcPortSpeedSchema", data_key="speed", unknown=EXCLUDE, allow_none=True)
    r""" The physical device speed related properties of the FC port."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['startup', 'link_not_connected', 'online', 'link_disconnected', 'offlined_by_user', 'offlined_by_system', 'node_offline', 'unknown']),
        allow_none=True,
    )
    r""" The operational state of the FC port.
- startup - The port is booting up.
- link_not_connected - The port has finished initialization, but a link with the fabric is not established.
- online - The port is initialized and a link with the fabric has been established.
- link_disconnected - The link was present at one point on this port but is currently not established.
- offlined_by_user - The port is administratively disabled.
- offlined_by_system - The port is set to offline by the system. This happens when the port encounters too many errors.
- node_offline - The state information for the port cannot be retrieved. The node is offline or inaccessible.


Valid choices:

* startup
* link_not_connected
* online
* link_disconnected
* offlined_by_user
* offlined_by_system
* node_offline
* unknown"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_reduced_throughput.PerformanceMetricRawReducedThroughputSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" These are raw performance numbers, such as IOPS latency and throughput. These numbers are aggregated across all nodes in the cluster and increase with the uptime of the cluster."""

    supported_protocols = marshmallow_fields.List(marshmallow_fields.Str, data_key="supported_protocols", allow_none=True)
    r""" The network protocols supported by the FC port."""

    transceiver = marshmallow_fields.Nested("netapp_ontap.models.fc_port_transceiver.FcPortTransceiverSchema", data_key="transceiver", unknown=EXCLUDE, allow_none=True)
    r""" Properties of the transceiver connected to the FC port."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the FC port.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    wwnn = marshmallow_fields.Str(
        data_key="wwnn",
        allow_none=True,
    )
    r""" The base world wide node name (WWNN) for the FC port.


Example: 20:00:00:50:56:b4:13:a8"""

    wwpn = marshmallow_fields.Str(
        data_key="wwpn",
        allow_none=True,
    )
    r""" The base world wide port name (WWPN) for the FC port.


Example: 20:00:00:50:56:b4:13:a8"""

    @property
    def resource(self):
        return FcPort

    gettable_fields = [
        "links",
        "description",
        "enabled",
        "fabric",
        "interface_count",
        "metric",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "physical_protocol",
        "speed",
        "state",
        "statistics",
        "supported_protocols",
        "transceiver",
        "uuid",
        "wwnn",
        "wwpn",
    ]
    """links,description,enabled,fabric,interface_count,metric,name,node.links,node.name,node.uuid,physical_protocol,speed,state,statistics,supported_protocols,transceiver,uuid,wwnn,wwpn,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""

class FcPort(Resource):
    r""" A Fibre Channel (FC) port is the physical port of an FC adapter on an ONTAP cluster node that can be connected to an FC network to provide FC network connectivity. An FC port defines the location of an FC interface within the ONTAP cluster. """

    _schema = FcPortSchema
    _path = "/api/network/fc/ports"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FC ports.<br/>
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `fabric.name`
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `network fcp adapter show`
### Learn more
* [`DOC /network/fc/ports`](#docs-networking-network_fc_ports)
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
        """Returns a count of all FcPort resources that match the provided query"""
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
        """Returns a list of RawResources that represent FcPort resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FcPort"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an FC port.
### Related ONTAP commands
* `network fcp adapter modify`
### Learn more
* [`DOC /network/fc/ports`](#docs-networking-network_fc_ports)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FC ports.<br/>
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `fabric.name`
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `network fcp adapter show`
### Learn more
* [`DOC /network/fc/ports`](#docs-networking-network_fc_ports)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an FC port.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `fabric.name`
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `network fcp adapter show`
### Learn more
* [`DOC /network/fc/ports`](#docs-networking-network_fc_ports)
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
        r"""Updates an FC port.
### Related ONTAP commands
* `network fcp adapter modify`
### Learn more
* [`DOC /network/fc/ports`](#docs-networking-network_fc_ports)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



