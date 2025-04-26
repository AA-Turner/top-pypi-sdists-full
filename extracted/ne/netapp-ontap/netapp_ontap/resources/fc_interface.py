r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Fibre Channel (FC) interfaces are the logical endpoints for FC network connections to an SVM. An FC interface provides FC access to storage within the interface SVM using either Fibre Channel Protocol (FCP) or NVMe over FC (NVMe/FC).<br/>
The FC interface REST API allows you to create, delete, update, and discover FC interfaces, and obtain status information for FC interfaces.<br/>
An FC interface is created on an FC port which is located on a cluster node. The FC port must be specified to identify the location of the interface for a POST or PATCH request that relocates an interface. You can identify the port by supplying either the node and port names or the port UUID.
## Performance monitoring
Performance of an FC interface can be monitored by observing the `metric.*` and `statistics.*` properties. These properties show the performance of an FC interface in terms of IOPS, latency, and throughput. The `metric.*` properties denote an average, whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
## Interface placement recommendations
The FC interface REST API can also recommend the placement (cluster nodes and FC ports) for FC interfaces for a new or existing SVM as well as evaluate caller-proposed locations for FC interfaces. This functionality is available to cluster administrators only and is accessed using `GET /network/fc/interfaces` with the `recommend` family of query parameters.<br/>
The query parameter `recommend.data_protocol` is required when getting recommendations or evaluating caller-proposed locations for FC interfaces. It identifies the type of FC interfaces to recommend. Other `recommend` query parameters are optional and are used to modify the recommendation algorithm.<br/>
If an SVM is supplied using the query parameter `recommend.svm.name` and/or `recommend.svm.uuid`, existing FC interfaces are considered as part of the overall solution and only additionally recommended interfaces are returned. If no SVM is supplied, recommendations are returned for a new SVM.<br/>
FC fabrics connected to the cluster are discovered by the API. By default, FC interfaces are placed and evaluated for each fabric. The query parameter `recommend.fabrics.name` can be used to identify specific FC fabrics to use.<br/>
Cluster nodes supporting FC fabric connections for the specific data protocol are discovered by the API. By default, FC interfaces are placed all supported cluster nodes. Either query parameter `recommend.nodes.name` or `recommend.nodes.uuid` can be used to identify specific cluster nodes to use.<br/>
FC interfaces for the FC-NVMe data protocol are limited to two (2) interfaces per cluster node with a maximum of four (4) nodes, within a single SVM.<br/>
Placement recommendations are best effort and limited by the information available. In situations where an optimum configuration cannot be produced, the API returns the recommendations it can along with messages describing how the caller might improve the configuration. These messages are produced by evaluating the calculated FC interface layout against best practices.<br/>
The same best practice evaluation can be applied to a caller-proposed configuration by using the query parameter `recommend.proposed.locations.port.uuid` to specify the locations for proposed FC interfaces. When this query parameter is supplied, the best practice evaluation is performed using the proposed interface locations and messages are produced describing how the caller might improve the configuration.
## Examples
### Creating an FC interface using the port node and name to identify the location
This example uses the `return_records` query parameter to retrieve the newly created FC interface in the POST response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcInterface()
    resource.svm = {"name": "svm1"}
    resource.name = "lif1"
    resource.location = {"home_port": {"name": "0a", "home_node": {"name": "node1"}}}
    resource.data_protocol = "fcp"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
FcInterface(
    {
        "data_protocol": "fcp",
        "location": {
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/bafe9b9f-db81-11e8-bd46-005056bba0e0"
                    }
                },
                "uuid": "bafe9b9f-db81-11e8-bd46-005056bba0e0",
            },
            "home_node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/bafe9b9f-db81-11e8-bd46-005056bba0e0"
                    }
                },
                "uuid": "bafe9b9f-db81-11e8-bd46-005056bba0e0",
            },
            "port": {
                "name": "0a",
                "node": {"name": "node1"},
                "uuid": "300c1ae3-db82-11e8-bd46-005056bba0e0",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/ports/300c1ae3-db82-11e8-bd46-005056bba0e0"
                    }
                },
            },
            "home_port": {
                "name": "0a",
                "node": {"name": "node1"},
                "uuid": "300c1ae3-db82-11e8-bd46-005056bba0e0",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/ports/300c1ae3-db82-11e8-bd46-005056bba0e0"
                    }
                },
            },
        },
        "port_address": "9da2cb1",
        "name": "lif1",
        "state": "down",
        "enabled": True,
        "uuid": "f6045b92-dec7-11e8-a733-005056bba0e0",
        "_links": {
            "self": {
                "href": "/api/network/fc/interfaces/f6045b92-dec7-11e8-a733-005056bba0e0"
            }
        },
        "wwpn": "20:04:00:50:56:bb:a0:e0",
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/cf300f5c-db83-11e8-bd46-005056bba0e0"}
            },
            "uuid": "cf300f5c-db83-11e8-bd46-005056bba0e0",
        },
        "wwnn": "20:00:00:50:56:bb:a0:e0",
    }
)

```
</div>
</div>

---
### Creating an FC interface using the port UUID to identify the location
This example uses the `return_records` query parameter to retrieve the newly created FC interface in the POST response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcInterface()
    resource.svm = {"name": "svm3"}
    resource.name = "lif2"
    resource.location = {"home_port": {"uuid": "24bb636a-db83-11e8-9a49-005056bb1ec6"}}
    resource.data_protocol = "fc_nvme"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
FcInterface(
    {
        "data_protocol": "fc_nvme",
        "location": {
            "node": {
                "name": "node3",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/e85aa147-db83-11e8-9a48-005056bb1ec6"
                    }
                },
                "uuid": "e85aa147-db83-11e8-9a48-005056bb1ec6",
            },
            "home_node": {
                "name": "node3",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/e85aa147-db83-11e8-9a48-005056bb1ec6"
                    }
                },
                "uuid": "e85aa147-db83-11e8-9a48-005056bb1ec6",
            },
            "port": {
                "name": "1b",
                "node": {"name": "node3"},
                "uuid": "24bb636a-db83-11e8-9a49-005056bb1ec6",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/ports/24bb636a-db83-11e8-9a49-005056bb1ec6"
                    }
                },
            },
            "home_port": {
                "name": "1b",
                "node": {"name": "node3"},
                "uuid": "24bb636a-db83-11e8-9a49-005056bb1ec6",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/ports/24bb636a-db83-11e8-9a49-005056bb1ec6"
                    }
                },
            },
        },
        "port_address": "612e202b",
        "name": "lif2",
        "state": "down",
        "enabled": True,
        "uuid": "cdeb5591-dec9-11e8-a733-005056bba0e0",
        "_links": {
            "self": {
                "href": "/api/network/fc/interfaces/cdeb5591-dec9-11e8-a733-005056bba0e0"
            }
        },
        "wwpn": "20:05:00:50:56:bb:a0:e0",
        "svm": {
            "name": "svm3",
            "_links": {
                "self": {"href": "/api/svm/svms/a5060466-dbab-11e8-bd46-005056bba0e0"}
            },
            "uuid": "a5060466-dbab-11e8-bd46-005056bba0e0",
        },
        "wwnn": "20:02:00:50:56:bb:a0:e0",
    }
)

```
</div>
</div>

---
### Retrieving all properties for all FC interfaces
This example uses the `fields` query parameter to retrieve all properties.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcInterface.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    FcInterface(
        {
            "data_protocol": "fc_nvme",
            "location": {
                "node": {
                    "name": "node3",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/e85aa147-db83-11e8-9a48-005056bb1ec6"
                        }
                    },
                    "uuid": "e85aa147-db83-11e8-9a48-005056bb1ec6",
                },
                "home_node": {
                    "name": "node3",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/e85aa147-db83-11e8-9a48-005056bb1ec6"
                        }
                    },
                    "uuid": "e85aa147-db83-11e8-9a48-005056bb1ec6",
                },
                "port": {
                    "name": "1b",
                    "node": {"name": "node3"},
                    "uuid": "24bb636a-db83-11e8-9a49-005056bb1ec6",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/ports/24bb636a-db83-11e8-9a49-005056bb1ec6"
                        }
                    },
                },
                "home_port": {
                    "name": "1b",
                    "node": {"name": "node3"},
                    "uuid": "24bb636a-db83-11e8-9a49-005056bb1ec6",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/ports/24bb636a-db83-11e8-9a49-005056bb1ec6"
                        }
                    },
                },
            },
            "port_address": "612e202b",
            "name": "lif2",
            "state": "down",
            "enabled": True,
            "uuid": "cdeb5591-dec9-11e8-a733-005056bba0e0",
            "_links": {
                "self": {
                    "href": "/api/network/fc/interfaces/cdeb5591-dec9-11e8-a733-005056bba0e0"
                }
            },
            "wwpn": "20:05:00:50:56:bb:a0:e0",
            "svm": {
                "name": "svm3",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/a5060466-dbab-11e8-bd46-005056bba0e0"
                    }
                },
                "uuid": "a5060466-dbab-11e8-bd46-005056bba0e0",
            },
            "wwnn": "20:02:00:50:56:bb:a0:e0",
        }
    ),
    FcInterface(
        {
            "data_protocol": "fcp",
            "location": {
                "node": {
                    "name": "node1",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/bafe9b9f-db81-11e8-bd46-005056bba0e0"
                        }
                    },
                    "uuid": "bafe9b9f-db81-11e8-bd46-005056bba0e0",
                },
                "home_node": {
                    "name": "node1",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/bafe9b9f-db81-11e8-bd46-005056bba0e0"
                        }
                    },
                    "uuid": "bafe9b9f-db81-11e8-bd46-005056bba0e0",
                },
                "port": {
                    "name": "0a",
                    "node": {"name": "node1"},
                    "uuid": "300c1ae3-db82-11e8-bd46-005056bba0e0",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/ports/300c1ae3-db82-11e8-bd46-005056bba0e0"
                        }
                    },
                },
                "home_port": {
                    "name": "0a",
                    "node": {"name": "node1"},
                    "uuid": "300c1ae3-db82-11e8-bd46-005056bba0e0",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/ports/300c1ae3-db82-11e8-bd46-005056bba0e0"
                        }
                    },
                },
            },
            "port_address": "9da2cb1",
            "name": "lif1",
            "state": "down",
            "enabled": True,
            "uuid": "f6045b92-dec7-11e8-a733-005056bba0e0",
            "_links": {
                "self": {
                    "href": "/api/network/fc/interfaces/f6045b92-dec7-11e8-a733-005056bba0e0"
                }
            },
            "wwpn": "20:04:00:50:56:bb:a0:e0",
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/cf300f5c-db83-11e8-bd46-005056bba0e0"
                    }
                },
                "uuid": "cf300f5c-db83-11e8-bd46-005056bba0e0",
            },
            "wwnn": "20:00:00:50:56:bb:a0:e0",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a list of selected FC interfaces
This example uses property query parameters to retrieve FC interfaces configured for the FC Protocol that are set to _up_.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FcInterface.get_collection(data_protocol="fcp", state="up")))

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    FcInterface(
        {
            "data_protocol": "fcp",
            "name": "lif1",
            "state": "up",
            "uuid": "f6045b92-dec7-11e8-a733-005056bba0e0",
            "_links": {
                "self": {
                    "href": "/api/network/fc/interfaces/f6045b92-dec7-11e8-a733-005056bba0e0"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/cf300f5c-db83-11e8-bd46-005056bba0e0"
                    }
                },
                "uuid": "cf300f5c-db83-11e8-bd46-005056bba0e0",
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific FC interface
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcInterface(uuid="cdeb5591-dec9-11e8-a733-005056bba0e0")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
FcInterface(
    {
        "data_protocol": "fc_nvme",
        "metric": {
            "status": "ok",
            "iops": {"total": 0, "write": 0, "other": 0, "read": 0},
            "latency": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:15+00:00",
            "throughput": {"total": 0, "write": 0, "read": 0},
            "duration": "PT15S",
        },
        "location": {
            "node": {
                "name": "node3",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/e85aa147-db83-11e8-9a48-005056bb1ec6"
                    }
                },
                "uuid": "e85aa147-db83-11e8-9a48-005056bb1ec6",
            },
            "home_node": {
                "name": "node3",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/e85aa147-db83-11e8-9a48-005056bb1ec6"
                    }
                },
                "uuid": "e85aa147-db83-11e8-9a48-005056bb1ec6",
            },
            "port": {
                "name": "1b",
                "node": {"name": "node3"},
                "uuid": "24bb636a-db83-11e8-9a49-005056bb1ec6",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/ports/24bb636a-db83-11e8-9a49-005056bb1ec6"
                    }
                },
            },
            "home_port": {
                "name": "1b",
                "node": {"name": "node3"},
                "uuid": "24bb636a-db83-11e8-9a49-005056bb1ec6",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/ports/24bb636a-db83-11e8-9a49-005056bb1ec6"
                    }
                },
            },
        },
        "port_address": "612e202b",
        "statistics": {
            "status": "ok",
            "iops_raw": {"total": 3, "write": 0, "other": 3, "read": 0},
            "latency_raw": {"total": 38298, "write": 0, "other": 38298, "read": 0},
            "throughput_raw": {"total": 0, "write": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:42+00:00",
        },
        "name": "lif2",
        "state": "down",
        "enabled": True,
        "uuid": "cdeb5591-dec9-11e8-a733-005056bba0e0",
        "_links": {
            "self": {
                "href": "/api/network/fc/interfaces/cdeb5591-dec9-11e8-a733-005056bba0e0"
            }
        },
        "wwpn": "20:05:00:50:56:bb:a0:e0",
        "svm": {
            "name": "svm3",
            "_links": {
                "self": {"href": "/api/svm/svms/a5060466-dbab-11e8-bd46-005056bba0e0"}
            },
            "uuid": "a5060466-dbab-11e8-bd46-005056bba0e0",
        },
        "wwnn": "20:02:00:50:56:bb:a0:e0",
    }
)

```
</div>
</div>

---
## Disabling an FC interface
When updating certain properties of an FC interface, the interface must first be disabled using the following:
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcInterface(uuid="f6045b92-dec7-11e8-a733-005056bba0e0")
    resource.enabled = False
    resource.patch()

```

---
### Moving an FC interface to a new node and port
To move an FC interface to another node or port, the destination FC port must be specified in a PATCH request. Either the port UUID or node and port names can be used to identify the port.<br/>
Note that only FC interfaces configured for the FC Protocol can be moved. FC interfaces configured for NVMe/FC cannot be moved. The interface must also be set to the disabled state before being moved.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcInterface(uuid="f6045b92-dec7-11e8-a733-005056bba0e0")
    resource.location = {"home_port": {"uuid": "a1dc7aa5-db83-11e8-9ef7-005056bbbbcc"}}
    resource.patch()

```

---
### Deleting an FC interface
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FcInterface(uuid="f6045b92-dec7-11e8-a733-005056bba0e0")
    resource.delete()

```

---
### Recommending interface locations for a new SVM
This example gets recommendations for FCP network interfaces for a new SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FcInterface.get_collection(fields="*", **{"recommend.data_protocol": "fcp"})
        )
    )

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
[
    FcInterface(
        {
            "data_protocol": "fcp",
            "location": {
                "home_port": {
                    "name": "0a",
                    "node": {"name": "node1"},
                    "uuid": "300c1ae3-db82-11e8-bd46-005056bba0e0",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/ports/300c1ae3-db82-11e8-bd46-005056bba0e0"
                        }
                    },
                }
            },
            "comment": "fabric: 55:0e:b1:a0:20:40:80:00",
        }
    ),
    FcInterface(
        {
            "data_protocol": "fcp",
            "location": {
                "home_port": {
                    "name": "0a",
                    "node": {"name": "node2"},
                    "uuid": "ad7d3915-db82-11e8-b36d-005056bb982e",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/ports/ad7d3915-db82-11e8-b36d-005056bb982e"
                        }
                    },
                }
            },
            "comment": "fabric: 55:0e:b1:a0:20:40:80:00",
        }
    ),
    FcInterface(
        {
            "data_protocol": "fcp",
            "location": {
                "home_port": {
                    "name": "0b",
                    "node": {"name": "node1"},
                    "uuid": "300c1dfd-db82-11e8-bd46-005056bba0e0",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/ports/300c1dfd-db82-11e8-bd46-005056bba0e0"
                        }
                    },
                }
            },
            "comment": "fabric: 55:0e:b1:a0:20:40:80:01",
        }
    ),
]

```
</div>
</div>

---
### Proposing interface locations for a new SVM
This example requests that caller-proposed locations for FC-NVMe interfaces on two nodes be evaluated.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FcInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FcInterface.get_collection(
                fields="*",
                **{
                    "recommend.data_protocol": "fc_nvme",
                    "recommend.proposed.locations.port.uuid": "300c2786-db82-11e8-bd46-005056bba0e0,ad7d47d6-db82-11e8-b36d-005056bb982e",
                }
            )
        )
    )

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
[]

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


__all__ = ["FcInterface", "FcInterfaceSchema"]
__pdoc__ = {
    "FcInterfaceSchema.resource": False,
    "FcInterfaceSchema.opts": False,
}


class FcInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the fc_interface."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" A user configurable comment. Optional in POST; valid in PATCH. To clear a prior comment, set the property to an empty string in PATCH."""

    data_protocol = marshmallow_fields.Str(
        data_key="data_protocol",
        validate=enum_validation(['fcp', 'fc_nvme']),
        allow_none=True,
    )
    r""" The data protocol for which the FC interface is configured. Required in POST.


Valid choices:

* fcp
* fc_nvme"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The administrative state of the FC interface. The FC interface can be disabled to block all FC communication with the SVM through this interface. Optional in POST and PATCH; defaults to _true_ (enabled) in POST."""

    location = marshmallow_fields.Nested("netapp_ontap.models.fc_interface_location.FcInterfaceLocationSchema", data_key="location", unknown=EXCLUDE, allow_none=True)
    r""" The location of the FC interface is defined by the location of its port. An FC port is identified by its UUID, or a combination of its cluster node name and port name. Either the UUID or the cluster node name and port name are required for POST. To move an interface, supply either the port UUID or the cluster node name and port name in a PATCH.<br/>
`location.node` and `location.port` refer to the current location of the FC interface. This can be different from `location.home_node` and `location.home_port` in instances where the FC interface has failed over to its HA partner node. The `location.node`, `location.port`, and `location.is_home` properties are not available for interfaces on the inactive side of a MetroCluster relationship."""

    metric = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_reduced_throughput.PerformanceMetricReducedThroughputSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the FC interface. Required in POST; optional in PATCH.


Example: fc_lif1"""

    port_address = marshmallow_fields.Str(
        data_key="port_address",
        allow_none=True,
    )
    r""" The port address of the FC interface. Each FC port in an FC switched fabric has its own unique FC port address for routing purposes. The FC port address is assigned by a switch in the fabric when that port logs in to the fabric. This property refers to the address given by a switch to the FC interface when the SVM performs a port login (PLOGI).<br/>
This is useful for obtaining statistics and diagnostic information from FC switches.<br/>
This is a hexadecimal encoded numeric value.


Example: 5060F"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'down']),
        allow_none=True,
    )
    r""" The current operational state of the FC interface. The state is set to _down_ if the interface is not enabled.<br/>
If the cluster node hosting the port is down or unavailable, no state value is returned.


Valid choices:

* up
* down"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_reduced_throughput.PerformanceMetricRawReducedThroughputSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" These are raw performance numbers, such as IOPS latency and throughput. These numbers are aggregated across all nodes in the cluster and increase with the uptime of the cluster."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the fc_interface."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the FC interface. Required in the URL.


Example: bce9827d-4d8f-60af-c771-6e8e9af2c6f0"""

    wwnn = marshmallow_fields.Str(
        data_key="wwnn",
        allow_none=True,
    )
    r""" The world wide node name (WWNN) of the FC interface SVM. The WWNN is generated by ONTAP when Fibre Channel Protocol or the NVMe service is created for the FC interface SVM.


Example: 20:00:00:50:56:b4:13:01"""

    wwpn = marshmallow_fields.Str(
        data_key="wwpn",
        allow_none=True,
    )
    r""" The world wide port name (WWPN) of the FC interface. The WWPN is generated by ONTAP when the FC interface is created.


Example: 20:00:00:50:56:b4:13:a8"""

    @property
    def resource(self):
        return FcInterface

    gettable_fields = [
        "links",
        "comment",
        "data_protocol",
        "enabled",
        "location",
        "metric",
        "name",
        "port_address",
        "state",
        "statistics",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "wwnn",
        "wwpn",
    ]
    """links,comment,data_protocol,enabled,location,metric,name,port_address,state,statistics,svm.links,svm.name,svm.uuid,uuid,wwnn,wwpn,"""

    patchable_fields = [
        "comment",
        "enabled",
        "location",
        "name",
    ]
    """comment,enabled,location,name,"""

    postable_fields = [
        "comment",
        "data_protocol",
        "enabled",
        "location",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """comment,data_protocol,enabled,location,name,svm.name,svm.uuid,"""

class FcInterface(Resource):
    r""" A Fibre Channel (FC) interface is the logical endpoint for FC network connections to an SVM. An FC interface provides FC access to storage within the interface SVM using either Fibre Channel Protocol or NVMe over Fibre Channel (NVMe/FC).<br/>
An FC interface is created on an FC port which is located on a cluster node. The FC port must be specified to identify the location of the interface for a POST or PATCH operation that relocates an interface. You can identify the port by supplying either the cluster node and port names or the port UUID. """

    _schema = FcInterfaceSchema
    _path = "/api/network/fc/interfaces"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FC interfaces.
### Related ONTAP commands
* `network interface show`
* `vserver fcp interface show`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
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
        """Returns a count of all FcInterface resources that match the provided query"""
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
        """Returns a list of RawResources that represent FcInterface resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FcInterface"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an FC interface.
### Related ONTAP commands
* `network interface modify`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["FcInterface"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FcInterface"], NetAppResponse]:
        r"""Creates an FC interface.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the FC interface.
* `name` - Name of the FC interface.
* `location.port.uuid` or both `location.port.name` and `location.port.node.name` - FC port on which to create the FC interface.
* `data_protocol` - Data protocol for the FC interface.
### Default property values
If not specified in POST, the following default property values are assigned.
* `enabled` - _true_
### Related ONTAP commands
* `network interface create`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
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
        records: Iterable["FcInterface"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an FC interface.
### Related ONTAP commands
* `network interface delete`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FC interfaces.
### Related ONTAP commands
* `network interface show`
* `vserver fcp interface show`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an FC interface.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `network interface show`
* `vserver fcp interface show`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
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
        r"""Creates an FC interface.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the FC interface.
* `name` - Name of the FC interface.
* `location.port.uuid` or both `location.port.name` and `location.port.node.name` - FC port on which to create the FC interface.
* `data_protocol` - Data protocol for the FC interface.
### Default property values
If not specified in POST, the following default property values are assigned.
* `enabled` - _true_
### Related ONTAP commands
* `network interface create`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
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
        r"""Updates an FC interface.
### Related ONTAP commands
* `network interface modify`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
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
        r"""Deletes an FC interface.
### Related ONTAP commands
* `network interface delete`
### Learn more
* [`DOC /network/fc/interfaces`](#docs-networking-network_fc_interfaces)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


