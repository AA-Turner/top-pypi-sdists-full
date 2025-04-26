r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A port is a physical or virtual Ethernet network device. Physical ports may be combined into Link Aggregation Groups (LAGs or ifgrps), or divided into Virtual LANs (VLANs).<br/>
GET (collection), GET (instance), and PATCH APIs are available for all port types. POST and DELETE APIs are available for "lag" (ifgrp) and "vlan" port types.<br/>
## Retrieving network port information
The network ports GET API retrieves and displays relevant information pertaining to the ports configured in the cluster. The API retrieves the list of all ports configured in the cluster, or specifically requested ports. The fields returned in the response vary for different ports and configurations.
## Examples
### Retrieving all ports in the cluster
The following output displays the UUID, name, and port type for all ports configured in a 2-node cluster. The port types are physical, vlan, lag (ifgrp), and p-vlan (available in select environments only).
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Port.get_collection(fields="uuid,name,type")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Port(
        {
            "name": "e0a",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d2c90c0-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "uuid": "2d2c90c0-f70d-11e8-b145-005056bb5b8e",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0b",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d3004da-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "uuid": "2d3004da-f70d-11e8-b145-005056bb5b8e",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0c",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d34a2cb-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "uuid": "2d34a2cb-f70d-11e8-b145-005056bb5b8e",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0d",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d37189f-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "uuid": "2d37189f-f70d-11e8-b145-005056bb5b8e",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0a",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35de5d8b-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "uuid": "35de5d8b-f70d-11e8-abdf-005056bb7fc8",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0b",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35de78cc-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "uuid": "35de78cc-f70d-11e8-abdf-005056bb7fc8",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0c",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35dead3c-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "uuid": "35dead3c-f70d-11e8-abdf-005056bb7fc8",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0d",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35deda90-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "uuid": "35deda90-f70d-11e8-abdf-005056bb7fc8",
            "type": "physical",
        }
    ),
    Port(
        {
            "name": "e0c-100",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/42e25145-f97d-11e8-ade9-005056bb7fc8"
                }
            },
            "uuid": "42e25145-f97d-11e8-ade9-005056bb7fc8",
            "type": "vlan",
        }
    ),
    Port(
        {
            "name": "a0a",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/569e0abd-f97d-11e8-ade9-005056bb7fc8"
                }
            },
            "uuid": "569e0abd-f97d-11e8-ade9-005056bb7fc8",
            "type": "lag",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific physical port
The following output displays the response when a specific physical port is requested. The system returns an error when there is no port with the requested UUID. Also, the "speed" field for the physical port is set only if the state of the port is up.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="2d37189f-f70d-11e8-b145-005056bb5b8e")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Port(
    {
        "reachability": "not_repairable",
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "name": "Default",
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
        },
        "name": "e0d",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/2d37189f-f70d-11e8-b145-005056bb5b8e"
            }
        },
        "mtu": 1500,
        "reachable_broadcast_domains": [
            {
                "ipspace": {"name": "Default"},
                "name": "Default",
                "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                    }
                },
            },
            {
                "ipspace": {"name": "Default"},
                "name": "Default-1",
                "uuid": "df640ccf-72c4-11ea-b31d-005056bbfb29",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/df640ccf-72c4-11ea-b31d-005056bbfb29"
                    }
                },
            },
        ],
        "speed": 1000,
        "node": {
            "name": "user-cluster-01",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/faa56898-f70c-11e8-b145-005056bb5b8e"
                }
            },
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
        },
        "uuid": "2d37189f-f70d-11e8-b145-005056bb5b8e",
        "mac_address": "00:50:56:bb:62:2d",
        "state": "up",
        "type": "physical",
    }
)

```
</div>
</div>

---
### Retrieving a specific VLAN port
The following output displays the response when a specific VLAN port is requested. The system returns an error when there is no port with the requested UUID. Also, the "speed" field for a VLAN port is always set to zero if the state of the port is up. If the state of the port is down, the "speed" field is unset and not reported back.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="42e25145-f97d-11e8-ade9-005056bb7fc8")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Port(
    {
        "reachability": "ok",
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "name": "Default",
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
        },
        "name": "e0e-100",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/42e25145-f97d-11e8-ade9-005056bb7fc8"
            }
        },
        "mtu": 1500,
        "reachable_broadcast_domains": [
            {
                "ipspace": {"name": "Default"},
                "name": "Default",
                "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                    }
                },
            }
        ],
        "speed": 0,
        "node": {
            "name": "user-cluster-02",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/6042cf47-f70c-11e8-abdf-005056bb7fc8"
                }
            },
            "uuid": "6042cf47-f70c-11e8-abdf-005056bb7fc8",
        },
        "uuid": "42e25145-f97d-11e8-ade9-005056bb7fc8",
        "mac_address": "00:50:56:bb:52:2f",
        "state": "up",
        "vlan": {
            "base_port": {
                "name": "e0e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/35deff03-f70d-11e8-abdf-005056bb7fc8"
                    }
                },
                "node": {"name": "user-cluster-02"},
                "uuid": "35deff03-f70d-11e8-abdf-005056bb7fc8",
            },
            "tag": 100,
        },
        "type": "vlan",
    }
)

```
</div>
</div>

---
### Retrieving a specific LAG port
The following output displays the response when a specific LAG port is requested. The system returns an error when there is no port with the requested UUID. The "lag.active_ports" field is set only if the state of the port is up. Also, the "speed" field for a LAG port is always set to zero if the state of the port is up. If the state of the port is down, the "speed" field is unset and not reported back.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="569e0abd-f97d-11e8-ade9-005056bb7fc8")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Port(
    {
        "reachability": "repairable",
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "name": "Default",
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
        },
        "name": "a0a",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/569e0abd-f97d-11e8-ade9-005056bb7fc8"
            }
        },
        "mtu": 1500,
        "reachable_broadcast_domains": [
            {
                "ipspace": {"name": "Default"},
                "name": "Default",
                "uuid": "c7934b4f-691f-11ea-87fd-005056bb1ad3",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/c7934b4f-691f-11ea-87fd-005056bb1ad3"
                    }
                },
            }
        ],
        "speed": 0,
        "node": {
            "name": "user-cluster-02",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/6042cf47-f70c-11e8-abdf-005056bb7fc8"
                }
            },
            "uuid": "6042cf47-f70c-11e8-abdf-005056bb7fc8",
        },
        "uuid": "569e0abd-f97d-11e8-ade9-005056bb7fc8",
        "mac_address": "02:50:56:bb:7f:c8",
        "state": "up",
        "lag": {
            "member_ports": [
                {
                    "name": "e0f",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df318d-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "node": {"name": "user-cluster-02"},
                    "uuid": "35df318d-f70d-11e8-abdf-005056bb7fc8",
                },
                {
                    "name": "e0g",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df5bad-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "node": {"name": "user-cluster-02"},
                    "uuid": "35df5bad-f70d-11e8-abdf-005056bb7fc8",
                },
                {
                    "name": "e0h",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df9926-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "node": {"name": "user-cluster-02"},
                    "uuid": "35df9926-f70d-11e8-abdf-005056bb7fc8",
                },
            ],
            "distribution_policy": "mac",
            "active_ports": [
                {
                    "name": "e0f",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df318d-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "uuid": "35df318d-f70d-11e8-abdf-005056bb7fc8",
                }
            ],
            "mode": "singlemode",
        },
        "type": "lag",
    }
)

```
</div>
</div>

---
### Retrieving all LAG (ifgrp) ports in the cluster
This command retrieves all LAG ports in the cluster (that is, all ports with type=LAG). The example shows how to filter a GET collection based on type.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Port.get_collection(
                type="lag",
                fields="name,enabled,speed,mtu",
                **{"node.name": "user-cluster-01"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    Port(
        {
            "name": "a0b",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/0c226db0-4b63-11e9-8113-005056bbe040"
                }
            },
            "mtu": 1500,
            "speed": 0,
            "node": {"name": "user-cluster-01"},
            "uuid": "0c226db0-4b63-11e9-8113-005056bbe040",
            "type": "lag",
        }
    ),
    Port(
        {
            "name": "a0a",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/d3a84153-4b3f-11e9-a00d-005056bbe040"
                }
            },
            "mtu": 1500,
            "speed": 0,
            "node": {"name": "user-cluster-01"},
            "uuid": "d3a84153-4b3f-11e9-a00d-005056bbe040",
            "type": "lag",
        }
    ),
]

```
</div>
</div>

---
## Creating VLAN and LAG ports
You can use the network ports POST API to create VLAN and LAG ports. If you supply the optional broadcast domain property, the specified broadcast domain will be assigned to the new port immediately.  Otherwise, within a few minutes automatic probing will determine the correct broadcast domain and will assign it to the port.  During that period of time, the port will not be capable of hosting interfaces.
<br/>
---
## Examples
### Creating a VLAN port
The following output displays the record returned after the creation of a VLAN port on "e0e" and VLAN tag "100".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port()
    resource.type = "vlan"
    resource.node = {"name": "user-cluster-01"}
    resource.enabled = True
    resource.vlan = {
        "tag": 100,
        "base_port": {"name": "e0e", "node": {"name": "user-cluster-01"}},
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
Port(
    {
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/88b2f682-fa42-11e8-a6d7-005056bb5b8e"
            }
        },
        "node": {
            "name": "user-cluster-01",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/faa56898-f70c-11e8-b145-005056bb5b8e"
                }
            },
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
        },
        "uuid": "88b2f682-fa42-11e8-a6d7-005056bb5b8e",
        "vlan": {
            "base_port": {
                "name": "e0e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/2d39df72-f70d-11e8-b145-005056bb5b8e"
                    }
                },
                "node": {"name": "user-cluster-01"},
                "uuid": "2d39df72-f70d-11e8-b145-005056bb5b8e",
            },
            "tag": 100,
        },
        "type": "vlan",
    }
)

```
</div>
</div>

---
### Creating a VLAN port in a specific broadcast domain
The following output displays the record returned after the creation of a VLAN port on "e0e" and VLAN tag "100". Also, the VLAN port is added to the "Default" broadcast domain in the "Default" IPspace.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port()
    resource.type = "vlan"
    resource.node = {"name": "user-cluster-01"}
    resource.broadcast_domain = {"name": "Default", "ipspace": {"name": "Default    "}}
    resource.enabled = True
    resource.vlan = {
        "tag": 100,
        "base_port": {"name": "e0e", "node": {"name": "user-cluster-01"}},
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Port(
    {
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "name": "Default",
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
        },
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/88b2f682-fa42-11e8-a6d7-005056bb5b8e"
            }
        },
        "node": {
            "name": "user-cluster-01",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/faa56898-f70c-11e8-b145-005056bb5b8e"
                }
            },
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
        },
        "uuid": "88b2f682-fa42-11e8-a6d7-005056bb5b8e",
        "vlan": {
            "base_port": {
                "name": "e0e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/2d39df72-f70d-11e8-b145-005056bb5b8e"
                    }
                },
                "node": {"name": "user-cluster-01"},
                "uuid": "2d39df72-f70d-11e8-b145-005056bb5b8e",
            },
            "tag": 100,
        },
        "type": "vlan",
    }
)

```
</div>
</div>

---
### Creating a LAG (ifgrp) port
The following output displays the record returned after the creation of a LAG port with "e0f", "e0g" and "e0h" as member ports.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port()
    resource.type = "lag"
    resource.node = {"name": "user-cluster-01"}
    resource.enabled = True
    resource.lag = {
        "mode": "singlemode",
        "distribution_policy": "mac",
        "member_ports": [
            {"name": "e0f", "node": {"name": "user-cluster-01"}},
            {"name": "e0g", "node": {"name": "user-cluster-01"}},
            {"name": "e0h", "node": {"name": "user-cluster-01"}},
        ],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
Port(
    {
        "enabled": True,
        "node": {
            "name": "user-cluster-01",
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
        },
        "uuid": "1807772a-fa4d-11e8-a6d7-005056bb5b8e",
        "lag": {
            "member_ports": [
                {
                    "name": "e0f",
                    "node": {"name": "user-cluster-01"},
                    "uuid": "2d3c9adc-f70d-11e8-b145-005056bb5b8e",
                },
                {
                    "name": "e0g",
                    "node": {"name": "user-cluster-01"},
                    "uuid": "2d40b097-f70d-11e8-b145-005056bb5b8e",
                },
                {
                    "name": "e0h",
                    "node": {"name": "user-cluster-01"},
                    "uuid": "2d46d01e-f70d-11e8-b145-005056bb5b8e",
                },
            ],
            "distribution_policy": "mac",
            "mode": "singlemode",
        },
        "type": "lag",
    }
)

```
</div>
</div>

---
### Creating a LAG (ifgrp) port in a specific broadcast domain
The following output displays the record returned after the creation of a LAG port with "e0f", "e0g" and "e0h" as member ports. Also, the LAG port is added to the "Default" broadcast domain in the "Default" IPspace.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port()
    resource.type = "lag"
    resource.node = {"name": "user-cluster-01"}
    resource.broadcast_domain = {"name": "Default", "ipspace": {"name": "Default"}}
    resource.enabled = True
    resource.lag = {
        "mode": "singlemode",
        "distribution_policy": "mac",
        "member_ports": [
            {"name": "e0f", "node": {"name": "user-cluster-01"}},
            {"name": "e0g", "node": {"name": "user-cluster-01"}},
            {"name": "e0h", "node": {"name": "user-cluster-01"}},
        ],
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
Port(
    {
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "name": "Default",
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
        },
        "enabled": True,
        "node": {
            "name": "user-cluster-01",
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
        },
        "uuid": "1807772a-fa4d-11e8-a6d7-005056bb5b8e",
        "lag": {
            "member_ports": [
                {
                    "name": "e0f",
                    "node": {"name": "user-cluster-01"},
                    "uuid": "2d3c9adc-f70d-11e8-b145-005056bb5b8e",
                },
                {
                    "name": "e0g",
                    "node": {"name": "user-cluster-01"},
                    "uuid": "2d40b097-f70d-11e8-b145-005056bb5b8e",
                },
                {
                    "name": "e0h",
                    "node": {"name": "user-cluster-01"},
                    "uuid": "2d46d01e-f70d-11e8-b145-005056bb5b8e",
                },
            ],
            "distribution_policy": "mac",
            "mode": "singlemode",
        },
        "type": "lag",
    }
)

```
</div>
</div>

---
## Updating ports
You can use the network ports PATCH API to update the attributes of ports.
<br/>
---
## Examples
### Updating the broadcast domain of a port
The following PATCH request removes the port from the current broadcast domain and adds it to the specified broadcast domain.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="6867efaf-d702-11e8-994f-005056bbc994")
    resource.broadcast_domain = {"name": "Default", "ipspace": {"name": "Default"}}
    resource.patch()

```

---
### Updating the admin status of a port
The following PATCH request brings the specified port down.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="51d3ab39-d86d-11e8-aca6-005056bbc994")
    resource.enabled = False
    resource.patch()

```

---
### Repairing a port
The following PATCH request repairs a port. Only ports that have reachability as "repairable" can be repaired. The "reachability" parameter cannot be patched in the same request as other parameters that might affect the target port's reachability status.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="51d3ab39-d86d-11e8-aca6-005056bbc994")
    resource.reachability = "ok"
    resource.patch()

```

---
## Deleting ports
You can use the network ports DELETE API to delete VLAN and LAG ports in the cluster. Note that physical ports cannot be deleted.
Deleting a port also removes the port from the broadcast domain.
---
## Example
### Deleting a VLAN port
The network ports DELETE API is used to delete a VLAN port.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="6867efaf-d702-11e8-994f-005056bbc994")
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


__all__ = ["Port", "PortSchema"]
__pdoc__ = {
    "PortSchema.resource": False,
    "PortSchema.opts": False,
}


class PortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Port object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the port."""

    broadcast_domain = marshmallow_fields.Nested("netapp_ontap.resources.broadcast_domain.BroadcastDomainSchema", data_key="broadcast_domain", unknown=EXCLUDE, allow_none=True)
    r""" The broadcast_domain field of the port."""

    discovered_devices = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.device_discovery_data.DeviceDiscoveryDataSchema", unknown=EXCLUDE, allow_none=True), data_key="discovered_devices", allow_none=True)
    r""" Discovered devices"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The enabled field of the port."""

    flowcontrol_admin = marshmallow_fields.Str(
        data_key="flowcontrol_admin",
        validate=enum_validation(['none', 'send', 'receive', 'full', 'pfc']),
        allow_none=True,
    )
    r""" Requested flow control

Valid choices:

* none
* send
* receive
* full
* pfc"""

    interface_count = Size(
        data_key="interface_count",
        allow_none=True,
    )
    r""" Number of interfaces hosted. This field is only applicable for cluster administrators. No value is returned for SVM administrators. If the node hosting a port is not healthy no value will be returned."""

    lag = marshmallow_fields.Nested("netapp_ontap.models.port_lag.PortLagSchema", data_key="lag", unknown=EXCLUDE, allow_none=True)
    r""" The lag field of the port."""

    mac_address = marshmallow_fields.Str(
        data_key="mac_address",
        allow_none=True,
    )
    r""" The mac_address field of the port.

Example: 01:02:03:04:05:06"""

    metric = marshmallow_fields.Nested("netapp_ontap.models.port_metrics_data.PortMetricsDataSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Throughput performance for the Ethernet port."""

    mtu = Size(
        data_key="mtu",
        validate=integer_validation(minimum=68),
        allow_none=True,
    )
    r""" MTU of the port in bytes. Set by broadcast domain.

Example: 1500"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Portname, such as e0a, e1b-100 (VLAN on Ethernet), a0c (LAG/ifgrp), a0d-200 (VLAN on LAG/ifgrp), e0a.pv1 (p-VLAN, in select environments only)

Example: e1b"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the port."""

    pfc_queues_admin = marshmallow_fields.List(Size, data_key="pfc_queues_admin", allow_none=True)
    r""" List of PFC queues"""

    rdma_protocols = marshmallow_fields.List(marshmallow_fields.Str, data_key="rdma_protocols", allow_none=True)
    r""" Supported RDMA offload protocols"""

    reachability = marshmallow_fields.Str(
        data_key="reachability",
        validate=enum_validation(['ok', 'repairable', 'not_repairable']),
        allow_none=True,
    )
    r""" Reachability status of the port. Enum value "ok" is the only acceptable value for a PATCH request to repair a port.

Valid choices:

* ok
* repairable
* not_repairable"""

    reachable_broadcast_domains = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.broadcast_domain.BroadcastDomainSchema", unknown=EXCLUDE, allow_none=True), data_key="reachable_broadcast_domains", allow_none=True)
    r""" Reachable broadcast domains."""

    speed = Size(
        data_key="speed",
        allow_none=True,
    )
    r""" Link speed in Mbps

Example: 1000"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'down', 'degraded']),
        allow_none=True,
    )
    r""" Operational state of the port. The state is set to 'down' if the operational state of the port is down. The state is set to 'up' if the link state of the port is up and the port is healthy. The state is set to 'up' if the link state of the port is up and configured to ignore health status. The state is 'degraded' if the link state of the port is up, and the port is not healthy.

Valid choices:

* up
* down
* degraded"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.port_statistics.PortStatisticsSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" These are raw performance and error counters for the Ethernet port."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['vlan', 'physical', 'lag', 'pvlan']),
        allow_none=True,
    )
    r""" Type of physical or virtual port

Valid choices:

* vlan
* physical
* lag
* pvlan"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Port UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    vlan = marshmallow_fields.Nested("netapp_ontap.models.port_vlan.PortVlanSchema", data_key="vlan", unknown=EXCLUDE, allow_none=True)
    r""" The vlan field of the port."""

    @property
    def resource(self):
        return Port

    gettable_fields = [
        "links",
        "broadcast_domain.links",
        "broadcast_domain.ipspace",
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "discovered_devices",
        "enabled",
        "flowcontrol_admin",
        "interface_count",
        "lag",
        "mac_address",
        "metric",
        "mtu",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "pfc_queues_admin",
        "rdma_protocols",
        "reachability",
        "reachable_broadcast_domains.links",
        "reachable_broadcast_domains.ipspace",
        "reachable_broadcast_domains.name",
        "reachable_broadcast_domains.uuid",
        "speed",
        "state",
        "statistics",
        "type",
        "uuid",
        "vlan",
    ]
    """links,broadcast_domain.links,broadcast_domain.ipspace,broadcast_domain.name,broadcast_domain.uuid,discovered_devices,enabled,flowcontrol_admin,interface_count,lag,mac_address,metric,mtu,name,node.links,node.name,node.uuid,pfc_queues_admin,rdma_protocols,reachability,reachable_broadcast_domains.links,reachable_broadcast_domains.ipspace,reachable_broadcast_domains.name,reachable_broadcast_domains.uuid,speed,state,statistics,type,uuid,vlan,"""

    patchable_fields = [
        "broadcast_domain.ipspace",
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "enabled",
        "flowcontrol_admin",
        "lag",
        "pfc_queues_admin",
        "reachability",
    ]
    """broadcast_domain.ipspace,broadcast_domain.name,broadcast_domain.uuid,enabled,flowcontrol_admin,lag,pfc_queues_admin,reachability,"""

    postable_fields = [
        "broadcast_domain.ipspace",
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "enabled",
        "lag",
        "node.name",
        "node.uuid",
        "type",
        "vlan",
    ]
    """broadcast_domain.ipspace,broadcast_domain.name,broadcast_domain.uuid,enabled,lag,node.name,node.uuid,type,vlan,"""

class Port(Resource):
    """Allows interaction with Port objects on the host"""

    _schema = PortSchema
    _path = "/api/network/ethernet/ports"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of ports (physical, VLAN and LAG) for an entire cluster.
### Related ONTAP commands
* `network port show`
* `network port ifgrp show`
* `network port vlan show`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Port resources that match the provided query"""
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
        """Returns a list of RawResources that represent Port resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Port"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a port.
### Related ONTAP commands
* `network port broadcast-domain add-ports`
* `network port broadcast-domain remove-ports`
* `network port modify`
* `network port ifgrp add-port`
* `network port ifgrp remove-port`
* `network port reachability repair`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Port"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Port"], NetAppResponse]:
        r"""Creates a new VLAN (such as node1:e0a-100) or LAG (ifgrp, such as node2:a0a).
### Required properties
* `node` - Node the port will be created on.
* `vlan` - This field cannot be specified at the same time as `lag`.
  * `vlan.base_port` - Physical port or LAG the VLAN will be created on.
  * `vlan.tag` - Tag used to identify VLAN on the base port.
* `lag` - This field cannot be specified at the same time as `vlan`.
  * `lag.mode` - Policy for the LAG that will be created.
  * `lag.distribution_policy` - Indicates how the packets are distributed between ports.
  * `lag.member_ports` - Set of ports the LAG consists of.
### Optional properties
* `type` - Defines if a VLAN or LAG will be created:
* `broadcast_domain` - The layer-2 broadcast domain the port is associated with. The port will be placed in a broadcast domain if it is not specified.  It may take several minutes for the broadcast domain to be assigned.  During that period the port cannot host interfaces.
### Related ONTAP commands
* `network port ifgrp create`
* `network port vlan create`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Port"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a VLAN or LAG.
### Related ONTAP commands
* `network port ifgrp delete`
* `network port vlan delete`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of ports (physical, VLAN and LAG) for an entire cluster.
### Related ONTAP commands
* `network port show`
* `network port ifgrp show`
* `network port vlan show`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a physical port, VLAN, or LAG.
### Related ONTAP commands
* `network port show`
* `network port ifgrp show`
* `network port vlan show`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
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
        r"""Creates a new VLAN (such as node1:e0a-100) or LAG (ifgrp, such as node2:a0a).
### Required properties
* `node` - Node the port will be created on.
* `vlan` - This field cannot be specified at the same time as `lag`.
  * `vlan.base_port` - Physical port or LAG the VLAN will be created on.
  * `vlan.tag` - Tag used to identify VLAN on the base port.
* `lag` - This field cannot be specified at the same time as `vlan`.
  * `lag.mode` - Policy for the LAG that will be created.
  * `lag.distribution_policy` - Indicates how the packets are distributed between ports.
  * `lag.member_ports` - Set of ports the LAG consists of.
### Optional properties
* `type` - Defines if a VLAN or LAG will be created:
* `broadcast_domain` - The layer-2 broadcast domain the port is associated with. The port will be placed in a broadcast domain if it is not specified.  It may take several minutes for the broadcast domain to be assigned.  During that period the port cannot host interfaces.
### Related ONTAP commands
* `network port ifgrp create`
* `network port vlan create`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
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
        r"""Updates a port.
### Related ONTAP commands
* `network port broadcast-domain add-ports`
* `network port broadcast-domain remove-ports`
* `network port modify`
* `network port ifgrp add-port`
* `network port ifgrp remove-port`
* `network port reachability repair`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
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
        r"""Deletes a VLAN or LAG.
### Related ONTAP commands
* `network port ifgrp delete`
* `network port vlan delete`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


