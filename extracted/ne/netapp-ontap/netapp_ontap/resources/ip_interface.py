r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The following operations are supported:

* Creation: POST network/ip/interfaces
* Collection Get: GET network/ip/interfaces
* Instance Get: GET network/ip/interfaces/{uuid}
* Instance Patch: PATCH network/ip/interfaces/{uuid}
* Instance Delete: DELETE network/ip/interfaces/{uuid}
## Retrieving network interface information
The IP interfaces GET API retrieves and displays relevant information pertaining to the interfaces configured in the cluster. The response can contain a list of multiple interfaces or a specific interface. The fields returned in the response vary for different interfaces and configurations.
## Examples
### Retrieving all interfaces in the cluster
The following example shows the list of all interfaces configured in a cluster.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(IpInterface.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    IpInterface(
        {
            "name": "user-cluster-01_mgmt1",
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/14531286-59fc-11e8-ba55-005056b4340f"
                }
            },
            "uuid": "14531286-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "name": "user-cluster-01_clus2",
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/145318ba-59fc-11e8-ba55-005056b4340f"
                }
            },
            "uuid": "145318ba-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "name": "user-cluster-01_clus1",
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/14531e45-59fc-11e8-ba55-005056b4340f"
                }
            },
            "uuid": "14531e45-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "name": "cluster_mgmt",
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
                }
            },
            "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "name": "lif1",
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/c670707c-5a11-11e8-8fcb-005056b4340f"
                }
            },
            "uuid": "c670707c-5a11-11e8-8fcb-005056b4340f",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific Cluster-scoped interface
The following example shows the response when a specific Cluster-scoped interface is requested. The system returns an error when there is no interface with the requested UUID. SVM information is not returned for Cluster-scoped interfaces.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="245979de-59fc-11e8-ba55-005056b4340f")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
IpInterface(
    {
        "name": "cluster_mgmt",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
            }
        },
        "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
        "location": {
            "auto_revert": False,
            "node": {
                "name": "user-cluster-01-a",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                    }
                },
                "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
            },
            "is_home": True,
            "failover": "broadcast_domain_only",
            "home_node": {
                "name": "user-cluster-01-a",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                    }
                },
                "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
            },
            "port": {
                "name": "e0d",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                    }
                },
                "node": {"name": "user-cluster-01-a"},
                "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
            },
            "home_port": {
                "name": "e0d",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                    }
                },
                "node": {"name": "user-cluster-01-a"},
                "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
            },
        },
        "state": "up",
        "ip": {"netmask": "18", "family": "ipv4", "address": "10.63.41.6"},
        "scope": "cluster",
        "ipspace": {
            "name": "Default",
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/114ecfb5-59fc-11e8-ba55-005056b4340f"
                }
            },
            "uuid": "114ecfb5-59fc-11e8-ba55-005056b4340f",
        },
        "service_policy": {
            "name": "default-management",
            "uuid": "9e0f4151-141b-11e9-851e-005056ac1ce0",
        },
        "vip": False,
        "services": ["management_core", "management_autosupport", "management_access"],
    }
)

```
</div>
</div>

---
### Retrieving a specific SVM-scoped interface using a filter
The following example shows the response when a specific SVM-scoped interface is requested. The SVM object is only included for SVM-scoped interfaces.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(IpInterface.get_collection(name="lif1", fields="*")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    IpInterface(
        {
            "name": "lif1",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/c670707c-5a11-11e8-8fcb-005056b4340f"
                }
            },
            "svm": {
                "name": "user_vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/c2134665-5a11-11e8-8fcb-005056b4340f"
                    }
                },
                "uuid": "c2134665-5a11-11e8-8fcb-005056b4340f",
            },
            "uuid": "c670707c-5a11-11e8-8fcb-005056b4340f",
            "location": {
                "auto_revert": False,
                "node": {
                    "name": "user-cluster-01-a",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                        }
                    },
                    "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
                },
                "is_home": True,
                "failover": "broadcast_domain_only",
                "home_node": {
                    "name": "user-cluster-01-a",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                        }
                    },
                    "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
                },
                "port": {
                    "name": "e0d",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                        }
                    },
                    "node": {"name": "user-cluster-01-a"},
                    "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
                },
                "home_port": {
                    "name": "e0d",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                        }
                    },
                    "node": {"name": "user-cluster-01-a"},
                    "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
                },
            },
            "state": "up",
            "ip": {"netmask": "24", "family": "ipv4", "address": "10.10.10.11"},
            "scope": "svm",
            "ipspace": {
                "name": "Default",
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/114ecfb5-59fc-11e8-ba55-005056b4340f"
                    }
                },
                "uuid": "114ecfb5-59fc-11e8-ba55-005056b4340f",
            },
            "service_policy": {
                "name": "default-data-files",
                "uuid": "9e53525f-141b-11e9-851e-005056ac1ce0",
            },
            "vip": False,
            "services": ["data_core", "data_nfs", "data_cifs", "data_flexcache"],
        }
    )
]

```
</div>
</div>

---
### Retrieving specific fields and limiting the output using filters
The following example shows the response when a filter is applied (location.home_port.name=e0a) and only certain fields are requested. Filtered fields are in the output in addition to the default fields and requested fields.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            IpInterface.get_collection(
                fields="location.home_node.name,service_policy.name,ip.address,enabled",
                **{"location.home_port.name": "e0a"}
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
    IpInterface(
        {
            "name": "user-cluster-01-a_clus1",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/1d1c9dc8-4f17-11e9-9553-005056ac918a"
                }
            },
            "uuid": "1d1c9dc8-4f17-11e9-9553-005056ac918a",
            "location": {
                "home_node": {"name": "user-cluster-01-a"},
                "home_port": {"name": "e0a"},
            },
            "ip": {"address": "192.168.170.24"},
            "service_policy": {"name": "default-cluster"},
        }
    ),
    IpInterface(
        {
            "name": "user-cluster-01-b_clus1",
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/d07782c1-4f16-11e9-86e7-005056ace7ee"
                }
            },
            "uuid": "d07782c1-4f16-11e9-86e7-005056ace7ee",
            "location": {
                "home_node": {"name": "user-cluster-01-b"},
                "home_port": {"name": "e0a"},
            },
            "ip": {"address": "192.168.170.22"},
            "service_policy": {"name": "default-cluster"},
        }
    ),
]

```
</div>
</div>

---
## Creating IP interfaces
You can use the IP interfaces POST API to create IP interfaces as shown in the following examples.
<br/>
---
## Examples
### Creating a Cluster-scoped IP interface using names
The following example shows the record returned after the creation of an IP interface on "e0d".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "cluster_mgmt"
    resource.ip = {"address": "10.63.41.6", "netmask": "18"}
    resource.enabled = True
    resource.scope = "cluster"
    resource.ipspace = {"name": "Default"}
    resource.location = {
        "auto_revert": False,
        "failover": "broadcast_domain_only",
        "home_port": {"name": "e0d", "node": {"name": "user-cluster-01-a"}},
    }
    resource.service_policy = {"name": "default-management"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
IpInterface(
    {
        "name": "cluster_mgmt",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
            }
        },
        "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
        "location": {
            "auto_revert": False,
            "failover": "broadcast_domain_only",
            "home_port": {"name": "e0d", "node": {"name": "user-cluster-01-a"}},
        },
        "ip": {"netmask": "18", "address": "10.63.41.6"},
        "scope": "cluster",
        "ipspace": {"name": "Default"},
        "service_policy": {"name": "default-management"},
    }
)

```
</div>
</div>

---
### Creating a SVM-scoped IP interface using a mix of parameter types
The following example shows the record returned after the creation of a IP interface by specifying a broadcast domain as the location.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "Data1"
    resource.ip = {"address": "10.234.101.116", "netmask": "255.255.240.0"}
    resource.enabled = True
    resource.scope = "svm"
    resource.svm = {"uuid": "137f3618-1e89-11e9-803e-005056a7646a"}
    resource.location = {"auto_revert": True, "broadcast_domain": {"name": "Default"}}
    resource.service_policy = {"name": "default-data-files"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
IpInterface(
    {
        "name": "Data1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/80d271c9-1f43-11e9-803e-005056a7646a"
            }
        },
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/137f3618-1e89-11e9-803e-005056a7646a"}
            },
            "uuid": "137f3618-1e89-11e9-803e-005056a7646a",
        },
        "uuid": "80d271c9-1f43-11e9-803e-005056a7646a",
        "location": {"auto_revert": True},
        "ip": {"netmask": "20", "address": "10.234.101.116"},
        "scope": "svm",
        "service_policy": {"name": "default-data-files"},
    }
)

```
</div>
</div>

---
### Creating a Cluster-scoped IP interface without specifying the scope parameter
The following example shows the record returned after creating an IP interface on "e0d" without specifying the scope parameter. The scope is "cluster" if an "svm" is not specified.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "cluster_mgmt"
    resource.ip = {"address": "10.63.41.6", "netmask": "18"}
    resource.enabled = True
    resource.ipspace = {"name": "Default"}
    resource.location = {
        "auto_revert": False,
        "home_port": {"name": "e0d", "node": {"name": "user-cluster-01-a"}},
    }
    resource.service_policy = {"name": "default-management"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
IpInterface(
    {
        "name": "cluster_mgmt",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
            }
        },
        "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
        "location": {
            "auto_revert": False,
            "home_port": {"name": "e0d", "node": {"name": "user-cluster-01-a"}},
        },
        "ip": {"netmask": "18", "address": "10.63.41.6"},
        "scope": "cluster",
        "ipspace": {"name": "Default"},
        "service_policy": {"name": "default-management"},
    }
)

```
</div>
</div>

---
### Creating an SVM-scoped IP interface without specifying the scope parameter
The following example shows the record returned after creating an IP interface on "e0d" without specifying the scope parameter. The scope is "svm" if the "svm" field is specified.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "Data1"
    resource.ip = {"address": "10.234.101.116", "netmask": "255.255.240.0"}
    resource.enabled = True
    resource.svm = {"uuid": "137f3618-1e89-11e9-803e-005056a7646a"}
    resource.location = {"auto_revert": True, "broadcast_domain": {"name": "Default"}}
    resource.service_policy = {"name": "default-data-files"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
IpInterface(
    {
        "name": "Data1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/80d271c9-1f43-11e9-803e-005056a7646a"
            }
        },
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svms/137f3618-1e89-11e9-803e-005056a7646a"}
            },
            "uuid": "137f3618-1e89-11e9-803e-005056a7646a",
        },
        "uuid": "80d271c9-1f43-11e9-803e-005056a7646a",
        "location": {"auto_revert": True},
        "ip": {"netmask": "20", "address": "10.234.101.116"},
        "scope": "svm",
        "service_policy": {"name": "default-data-files"},
    }
)

```
</div>
</div>

---
### Creating an SVM-scoped IP interface using a subnet
The following example shows the record returned after the creation of a IP interface by allocating an IP address from a subnet.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "Data1"
    resource.subnet = {"name": "Subnet10"}
    resource.enabled = True
    resource.scope = "svm"
    resource.svm = {"uuid": "137f3618-1e89-11e9-803e-005056a7646a"}
    resource.location = {"auto_revert": True, "broadcast_domain": {"name": "Default"}}
    resource.service_policy = {"name": "default-data-files"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
IpInterface(
    {
        "name": "Data1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/80d271c9-1f43-11e9-803e-005056a7646a"
            }
        },
        "svm": {
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/137f3618-1e89-11e9-803e-005056a7646a"}
            },
            "uuid": "137f3618-1e89-11e9-803e-005056a7646a",
        },
        "uuid": "80d271c9-1f43-11e9-803e-005056a7646a",
        "location": {"auto_revert": True},
        "subnet": {"name": "testSubnet"},
        "scope": "svm",
        "service_policy": {"name": "default-data-files"},
    }
)

```
</div>
</div>

---
## Updating IP interfaces
You can use the IP interfaces PATCH API to update the attributes of an IP interface.
<br/>
---
## Examples
### Updating the auto revert flag of an IP interface
The following example shows how the PATCH request changes the auto revert flag to 'false'.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.location = {"auto_revert": "false"}
    resource.patch()

```

---
### Updating the service policy of an IP interface
The following example shows how the PATCH request changes the service policy to 'default-management'.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.service_policy = {"name": "default-management"}
    resource.patch()

```

---
## Deleting IP interfaces
You can use the IP interfaces DELETE API to delete an IP interface in the cluster.
<br/>
---
## Example
### Deleting an IP Interface
The following DELETE request deletes a network IP interface.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
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


__all__ = ["IpInterface", "IpInterfaceSchema"]
__pdoc__ = {
    "IpInterfaceSchema.resource": False,
    "IpInterfaceSchema.opts": False,
}


class IpInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ip_interface."""

    ddns_enabled = marshmallow_fields.Boolean(
        data_key="ddns_enabled",
        allow_none=True,
    )
    r""" Indicates whether or not dynamic DNS updates are enabled. Defaults to true if the interface supports "data_nfs" or "data_cifs" services, otherwise false."""

    dns_zone = marshmallow_fields.Str(
        data_key="dns_zone",
        allow_none=True,
    )
    r""" Fully qualified DNS zone name

Example: storage.company.com"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The administrative state of the interface."""

    fail_if_subnet_conflicts = marshmallow_fields.Boolean(
        data_key="fail_if_subnet_conflicts",
        allow_none=True,
    )
    r""" This command fails if the specified IP address falls within the address range of a named subnet. Set this value to false to use the specified IP address and to assign the subnet owning that address to the interface."""

    ip = marshmallow_fields.Nested("netapp_ontap.models.ip_info.IpInfoSchema", data_key="ip", unknown=EXCLUDE, allow_none=True)
    r""" IP information"""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the ip_interface."""

    location = marshmallow_fields.Nested("netapp_ontap.models.ip_interface_location.IpInterfaceLocationSchema", data_key="location", unknown=EXCLUDE, allow_none=True)
    r""" Current or home location can be modified. Specifying a port implies a node. Specifying a node allows an appropriate port to be automatically selected. Ports are not valid and not shown for VIP interfaces. For POST, broadcast_domain can be specified alone or with home_node.  For PATCH, set is_home to true to revert a LIF back to its home port."""

    metric = marshmallow_fields.Nested("netapp_ontap.models.interface_metrics_data.InterfaceMetricsDataSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Throughput performance for the interfaces."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Interface name

Example: dataLif1"""

    probe_port = Size(
        data_key="probe_port",
        allow_none=True,
    )
    r""" Probe port for Cloud load balancer

Example: 64001"""

    rdma_protocols = marshmallow_fields.List(marshmallow_fields.Str, data_key="rdma_protocols", allow_none=True)
    r""" Supported RDMA offload protocols"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster"""

    service_policy = marshmallow_fields.Nested("netapp_ontap.resources.ip_service_policy.IpServicePolicySchema", data_key="service_policy", unknown=EXCLUDE, allow_none=True)
    r""" The service_policy field of the ip_interface."""

    services = marshmallow_fields.List(marshmallow_fields.Str, data_key="services", allow_none=True)
    r""" The services associated with the interface."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'down']),
        allow_none=True,
    )
    r""" The operational state of the interface.

Valid choices:

* up
* down"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.interface_statistics.InterfaceStatisticsSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" These are the total throughput raw performance data for the interface."""

    subnet = marshmallow_fields.Nested("netapp_ontap.resources.ip_subnet.IpSubnetSchema", data_key="subnet", unknown=EXCLUDE, allow_none=True)
    r""" Use this field to allocate an interface address from a subnet. If needed, a default route is created for this subnet."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ip_interface."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID that uniquely identifies the interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    vip = marshmallow_fields.Boolean(
        data_key="vip",
        allow_none=True,
    )
    r""" True for a VIP interface, whose location is announced via BGP."""

    @property
    def resource(self):
        return IpInterface

    gettable_fields = [
        "links",
        "ddns_enabled",
        "dns_zone",
        "enabled",
        "ip",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "location",
        "metric",
        "name",
        "probe_port",
        "rdma_protocols",
        "scope",
        "service_policy.links",
        "service_policy.name",
        "service_policy.uuid",
        "services",
        "state",
        "statistics",
        "subnet.links",
        "subnet.name",
        "subnet.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "vip",
    ]
    """links,ddns_enabled,dns_zone,enabled,ip,ipspace.links,ipspace.name,ipspace.uuid,location,metric,name,probe_port,rdma_protocols,scope,service_policy.links,service_policy.name,service_policy.uuid,services,state,statistics,subnet.links,subnet.name,subnet.uuid,svm.links,svm.name,svm.uuid,uuid,vip,"""

    patchable_fields = [
        "ddns_enabled",
        "dns_zone",
        "enabled",
        "fail_if_subnet_conflicts",
        "ip",
        "location",
        "name",
        "rdma_protocols",
        "service_policy.name",
        "service_policy.uuid",
        "subnet.name",
        "subnet.uuid",
    ]
    """ddns_enabled,dns_zone,enabled,fail_if_subnet_conflicts,ip,location,name,rdma_protocols,service_policy.name,service_policy.uuid,subnet.name,subnet.uuid,"""

    postable_fields = [
        "ddns_enabled",
        "dns_zone",
        "enabled",
        "fail_if_subnet_conflicts",
        "ip",
        "ipspace.name",
        "ipspace.uuid",
        "location",
        "name",
        "probe_port",
        "rdma_protocols",
        "scope",
        "service_policy.name",
        "service_policy.uuid",
        "subnet.name",
        "subnet.uuid",
        "svm.name",
        "svm.uuid",
        "vip",
    ]
    """ddns_enabled,dns_zone,enabled,fail_if_subnet_conflicts,ip,ipspace.name,ipspace.uuid,location,name,probe_port,rdma_protocols,scope,service_policy.name,service_policy.uuid,subnet.name,subnet.uuid,svm.name,svm.uuid,vip,"""

class IpInterface(Resource):
    """Allows interaction with IpInterface objects on the host"""

    _schema = IpInterfaceSchema
    _path = "/api/network/ip/interfaces"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the details of all IP interfaces.
### Related ONTAP Commands
* `network interface show`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all IpInterface resources that match the provided query"""
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
        """Returns a list of RawResources that represent IpInterface resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["IpInterface"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an IP interface.
### Related ONTAP commands
* `network interface migrate`
* `network interface modify`
* `network interface rename`
* `network interface revert`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["IpInterface"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IpInterface"], NetAppResponse]:
        r"""Creates a new Cluster-scoped or SVM-scoped interface.<br/>
### Required properties
* `name` - Name of the interface to create.
* `ip` or `subnet`
  * `ip.address` - IP address for the interface.
  * `ip.netmask` - IP subnet of the interface.
  * `subnet.uuid` or `subnet.name`
* `ipspace.name` or `ipspace.uuid`
  * Required for Cluster-scoped interfaces.
  * Optional for SVM-scoped interfaces.
* `svm.name` or `svm.uuid`
  * Required for an SVM-scoped interface.
  * Invalid for a Cluster-scoped interface.
* If a LIF in the subnet of the specified IP address does not already exist, a location.home_port, a location.home_node, or a location.broadcast_domain needs to be provided.
### Recommended property values
* `service_policy`
  * `for SVM scoped interfaces`
    * _default-data-files_ for interfaces carrying file-oriented NAS data traffic
    * _default-data-blocks_ for interfaces carrying block-oriented SAN data traffic
    * _default-data-iscsi_ for interfaces carrying iSCSI data traffic
    * _default-management_ for interfaces carrying SVM management requests
  * `for Cluster scoped interfaces`
    * _default-intercluster_ for interfaces carrying cluster peering traffic
    * _default-management_ for interfaces carrying system management requests
    * _default-route-announce_ for interfaces carrying BGP peer connections
### Default property values
If not specified in POST, the following default property values are assigned:
* `scope`
  * _svm_ if svm parameter is specified.
  * _cluster_ if svm parameter is not specified
* `enabled` - _true_
* `location.auto_revert` - _true_
* `service_policy`
  * **Unified ONTAP**: _default-data-files_ if scope is `svm`
  * **ASA r2**: _default-data-blocks_ if scope is `svm`
  * _default-management_ if scope is `cluster` and IPspace is not `Cluster`
  * _default-cluster_ if scope is `cluster` and IPspace is `Cluster`
* `failover` - Selects the least restrictive failover policy supported by all the services in the service policy.
* `ddns_enabled`
  * _true_ if the interface supports _data_nfs_ or _data_cifs_ services
  * _false_ otherwise
* `fail_if_subnet_conflicts` - _true_
### Related ONTAP commands
* `network interface create`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["IpInterface"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an IP interface.
### Related ONTAP commands
* `network interface delete`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the details of all IP interfaces.
### Related ONTAP Commands
* `network interface show`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details for a specific IP interface.
### Related ONTAP commands
* `network interface show`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
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
        r"""Creates a new Cluster-scoped or SVM-scoped interface.<br/>
### Required properties
* `name` - Name of the interface to create.
* `ip` or `subnet`
  * `ip.address` - IP address for the interface.
  * `ip.netmask` - IP subnet of the interface.
  * `subnet.uuid` or `subnet.name`
* `ipspace.name` or `ipspace.uuid`
  * Required for Cluster-scoped interfaces.
  * Optional for SVM-scoped interfaces.
* `svm.name` or `svm.uuid`
  * Required for an SVM-scoped interface.
  * Invalid for a Cluster-scoped interface.
* If a LIF in the subnet of the specified IP address does not already exist, a location.home_port, a location.home_node, or a location.broadcast_domain needs to be provided.
### Recommended property values
* `service_policy`
  * `for SVM scoped interfaces`
    * _default-data-files_ for interfaces carrying file-oriented NAS data traffic
    * _default-data-blocks_ for interfaces carrying block-oriented SAN data traffic
    * _default-data-iscsi_ for interfaces carrying iSCSI data traffic
    * _default-management_ for interfaces carrying SVM management requests
  * `for Cluster scoped interfaces`
    * _default-intercluster_ for interfaces carrying cluster peering traffic
    * _default-management_ for interfaces carrying system management requests
    * _default-route-announce_ for interfaces carrying BGP peer connections
### Default property values
If not specified in POST, the following default property values are assigned:
* `scope`
  * _svm_ if svm parameter is specified.
  * _cluster_ if svm parameter is not specified
* `enabled` - _true_
* `location.auto_revert` - _true_
* `service_policy`
  * **Unified ONTAP**: _default-data-files_ if scope is `svm`
  * **ASA r2**: _default-data-blocks_ if scope is `svm`
  * _default-management_ if scope is `cluster` and IPspace is not `Cluster`
  * _default-cluster_ if scope is `cluster` and IPspace is `Cluster`
* `failover` - Selects the least restrictive failover policy supported by all the services in the service policy.
* `ddns_enabled`
  * _true_ if the interface supports _data_nfs_ or _data_cifs_ services
  * _false_ otherwise
* `fail_if_subnet_conflicts` - _true_
### Related ONTAP commands
* `network interface create`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
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
        r"""Updates an IP interface.
### Related ONTAP commands
* `network interface migrate`
* `network interface modify`
* `network interface rename`
* `network interface revert`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
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
        r"""Deletes an IP interface.
### Related ONTAP commands
* `network interface delete`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


