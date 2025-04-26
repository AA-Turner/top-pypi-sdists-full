r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve and display relevant information pertaining to MetroCluster interconnect status. The ```/cluster/metrocluster/interconnects``` endpoint returns a list of all the interconnects in MetroCluster and their status. Each individual interconnect can be queried individually using the ```/cluster/metrocluster/interconnects/{node.uuid}/{partner_type}/{adapter}``` endpoint. You can also use this API to modify relevant information related to MetroCluster interconnect. These include address, netmask, and gateway. Modify a MetroCluster interconnect using the ```/cluster/metrocluster/interconnects/{node.uuid}/{partner_type}/{adapter}``` endpoint.
####
---
### Examples
### Retrieving MetroCluster interconnects
```
GET https://<mgmt-ip>/api/cluster/metrocluster/interconnects
{
    "records": [
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/ha/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/ha/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/dr/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/dr/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/aux/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/aux/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/ha/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/ha/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/dr/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/dr/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/aux/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/aux/e0g"
                }
            }
        }
    ],
    "num_records": 12,
    "_links": {
        "self": {
            "href": "/api/cluster/metrocluster/interconnects"
        }
    }
}
```
### Retrieves information about a specific MetroCluster interconnect
```
https://<mgmt-ip>/api/cluster/metrocluster/interconnects/774b4fbc-86f9-11e9-9051-005056825c71/aux/e0f
{
    "node": {
        "name": "cluster1_01",
        "uuid": "46147363-9857-11e9-9a55-005056828eb9",
        "_links": {
            "self": {
                "href": "/api/cluster/nodes/46147363-9857-11e9-9a55-005056828eb9"
            }
        }
    },
    "partner_type": "aux",
    "adapter": "e0f",
    "state": "up",
    "type": "iwarp",
    "interfaces": [
      {
        "address": "10.2.3.5",
        "netmask": "255.255.255.0"
      }
    ],
    "mirror": {
        "state": "online",
        "enabled": true
    },
    "multipath_policy": "static_map",
    "_links": {
        "self": {
            "href": "/api/cluster/metrocluster/interconnects/46147363-9857-11e9-9a55-005056828eb9/ha/e0f"
        }
    }
}
```
### This example shows how to modify the network address assigned to the home port. Fields required: address.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterInterconnect

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = MetroclusterInterconnect(
        adapter="e0g",
        partner_type="ha",
        **{"node.uuid": "3e1bfd38-ffd2-11eb-bcb7-005056aceaa9"}
    )
    resource.interfaces = [{"address": "1.2.3.4"}]
    resource.patch()

```

#### PATCH Response
```
HTTP/1.1 200 OK
Cache-Control: no-cache,no-store,must-revalidate
Connection: close
Date: Fri, 20 Aug 2021 21:58:36 GMT
Server: libzapid-httpd
Content-Length: 3
Content-Type: application/hal+json
X-Content-Type-Options: nosniff
{
}
```
### This example shows how to modify the netmask assigned to the interface. Be sure to change to a valid subnet. Fields required: netmask.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterInterconnect

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = MetroclusterInterconnect(
        adapter="e0g",
        partner_type="ha",
        **{"node.uuid": "3e1bfd38-ffd2-11eb-bcb7-005056aceaa9"}
    )
    resource.interfaces = [{"netmask": "2.2.2.2"}]
    resource.patch()

```

#### PATCH Response
```
HTTP/1.1 200 OK
Cache-Control: no-cache,no-store,must-revalidate
Connection: close
Date: Fri, 20 Aug 2021 22:11:35 GMT
Server: libzapid-httpd
Content-Length: 3
Content-Type: application/hal+json
X-Content-Type-Options: nosniff
{
}
```
### This example shows how to modify the gateway assigned to the interface. Please make sure to update it on the switch/router first. Assuming it is a new one, the new gateway and IP address must reside in the same subnet range as the interface IP address. Fields required: gateway.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MetroclusterInterconnect

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = MetroclusterInterconnect(
        adapter="e0g",
        partner_type="ha",
        **{"node.uuid": "3e1bfd38-ffd2-11eb-bcb7-005056aceaa9"}
    )
    resource.interfaces = [{"gateway": "1.2.3.4"}]
    resource.patch()

```

#### PATCH Response
```
HTTP/1.1 200 OK
Cache-Control: no-cache,no-store,must-revalidate
Connection: close
Date: Fri, 20 Aug 2021 22:11:35 GMT
Server: libzapid-httpd
Content-Length: 3
Content-Type: application/hal+json
X-Content-Type-Options: nosniff
{
}
```"""

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


__all__ = ["MetroclusterInterconnect", "MetroclusterInterconnectSchema"]
__pdoc__ = {
    "MetroclusterInterconnectSchema.resource": False,
    "MetroclusterInterconnectSchema.opts": False,
}


class MetroclusterInterconnectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterInterconnect object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the metrocluster_interconnect."""

    adapter = marshmallow_fields.Str(
        data_key="adapter",
        allow_none=True,
    )
    r""" Adapter"""

    interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ip_interface_and_gateway.IpInterfaceAndGatewaySchema", unknown=EXCLUDE, allow_none=True), data_key="interfaces", allow_none=True)
    r""" List of objects which contain interface information such as its IP address, netmask and gateway."""

    mirror = marshmallow_fields.Nested("netapp_ontap.models.metrocluster_interconnect_mirror.MetroclusterInterconnectMirrorSchema", data_key="mirror", unknown=EXCLUDE, allow_none=True)
    r""" The mirror field of the metrocluster_interconnect."""

    multipath_policy = marshmallow_fields.Str(
        data_key="multipath_policy",
        validate=enum_validation(['no_mp', 'static_map', 'dynamic_map', 'round_robin']),
        allow_none=True,
    )
    r""" Displays the NVRAM mirror multipath policy for the nodes configured in a MetroCluster.

Valid choices:

* no_mp
* static_map
* dynamic_map
* round_robin"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the metrocluster_interconnect."""

    partner_type = marshmallow_fields.Str(
        data_key="partner_type",
        validate=enum_validation(['aux', 'dr', 'ha']),
        allow_none=True,
    )
    r""" Partner type

Valid choices:

* aux
* dr
* ha"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['down', 'up']),
        allow_none=True,
    )
    r""" Adapter status

Valid choices:

* down
* up"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['roce', 'iwarp', 'unknown']),
        allow_none=True,
    )
    r""" Adapter type

Valid choices:

* roce
* iwarp
* unknown"""

    vlan_id = Size(
        data_key="vlan_id",
        validate=integer_validation(minimum=1, maximum=4095),
        allow_none=True,
    )
    r""" VLAN ID"""

    @property
    def resource(self):
        return MetroclusterInterconnect

    gettable_fields = [
        "links",
        "adapter",
        "interfaces",
        "mirror",
        "multipath_policy",
        "node.links",
        "node.name",
        "node.uuid",
        "partner_type",
        "state",
        "type",
        "vlan_id",
    ]
    """links,adapter,interfaces,mirror,multipath_policy,node.links,node.name,node.uuid,partner_type,state,type,vlan_id,"""

    patchable_fields = [
        "interfaces",
        "mirror",
        "node.name",
        "node.uuid",
    ]
    """interfaces,mirror,node.name,node.uuid,"""

    postable_fields = [
        "interfaces",
        "mirror",
        "node.name",
        "node.uuid",
    ]
    """interfaces,mirror,node.name,node.uuid,"""

class MetroclusterInterconnect(Resource):
    r""" Data for a MetroCluster interconnect. REST: /api/cluster/metrocluster/interconnects """

    _schema = MetroclusterInterconnectSchema
    _path = "/api/cluster/metrocluster/interconnects"
    _keys = ["node.uuid", "partner_type", "adapter"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of interconnect adapter information for nodes in the MetroCluster.
### Related ONTAP Commands
* `metrocluster interconnect show`
### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)
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
        """Returns a count of all MetroclusterInterconnect resources that match the provided query"""
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
        """Returns a list of RawResources that represent MetroclusterInterconnect resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["MetroclusterInterconnect"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a MetroCluster interconnect interface.
### Related ONTAP commands
* `metrocluster configuration-settings interface modify`

### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of interconnect adapter information for nodes in the MetroCluster.
### Related ONTAP Commands
* `metrocluster interconnect show`
### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information about a MetroCluster Interconnect for a specific partner type and adapter.
### Related ONTAP Commands
* `metrocluster interconnect show`

### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)"""
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
        r"""Updates a MetroCluster interconnect interface.
### Related ONTAP commands
* `metrocluster configuration-settings interface modify`

### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



