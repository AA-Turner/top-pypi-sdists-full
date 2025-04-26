r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this API to add nodes to a cluster, update node-specific configurations, and retrieve the current node configuration details.
## Adding a node to a cluster
You can add a node to a cluster by issuing a POST /cluster/nodes request to a node currently in the cluster. All nodes must be running the same version of ONTAP to use this API. Mixed version joins are not supported in this release. You can provide properties as fields in the body of the POST request to configure node-specific settings. On a successful request, POST /cluster/nodes returns a status code of 202 and job information in the body of the request. You can use the /cluster/jobs APIs to track the status of the node add job.
### Fields used for adding a node
Fields used for the /cluster/nodes APIs fall into the following categories:

* Required node fields
* Optional fields
* Network interface fields
* Records field
### Required node fields
The following field is required for any POST /cluster/nodes request:

* cluster_interface.ip.address
### Optional fields
All of the following fields are used to set up additional cluster-wide configurations:

* name
* location
* records
### Network interface fields
You can set a node-specific configuration for each node by using the POST /cluster/nodes API. If you provide a field in the body of a node, provide it for all nodes in the POST body.
You can provide the node management interface for each node if all node management interfaces in the cluster use the same subnet mask. If the node management interfaces use different subnet masks, use the /network/ip/interfaces API to configure the node management interfaces.
### The records field
To add multiple nodes to the cluster in one request, provide an array named "records" with multiple node entries. Each node entry in "records" must follow the required and optional fields listed previously. When only adding a single node, you do not need a "records" field. See "Examples" for an example of how to use the "records" field.
### Create recommended aggregates parameter
When you set the "create_recommended_aggregates" parameter to "true", aggregates based on an optimal layout recommended by the system are created on each of the nodes being added to the cluster. The default setting is "false".
<br/>
---
## Modifying node configurations
The following fields can be used to modify a node configuration:

* name
* location
<br/>
---
## Modifying service processor configurations
When modifying the "service_processor" properties, the job returns success immediately if valid network information is passed in. The values remain in their old state until the network information changes have taken effect on the service processor. You can poll the modified properties until the values are updated.
<br/>
---
## Deleting a node from a cluster
You can delete a node from the cluster. Before deleting a node from the cluster, shut down all of the node's shared resources, such as virtual interfaces to clients. If any of the node's shared resources are still active, the command fails.
You can use the "force" flag to forcibly remove a node that is down and cannot be brought online to remove its shared resources. This flag is set to "false" by default.
<br/>
---
## Node state
The node "state" field in the /cluster/nodes API represents the current operational state of individual nodes.
Note that the state of a node is a transient value and can change depending on the current condition of the node, especially during reboot, takeover, and giveback.
Possible values for the node state are:

* <i>up</i> - Node is fully operational and is able to accept and handle management requests. It is connected to a majority of healthy (up) nodes in the cluster through the cluster interconnect and all critical services are online.
* <i>booting</i> - Node is starting up and is not yet fully functional. It might not yet be accessible through the management interface or cluster interconnect. One or more critical services are offline on the node and the node is not taken over. The HA partner reports the node's firmware state as "SF_BOOTING", "SF_BOOTED", or "SF_CLUSTERWAIT".
* <i>down</i> - Node is known to be down.  It cannot be reached through the management interface or cluster interconnect. The HA partner can be reached and reports that the node is halted/rebooted without takeover. Or, the HA partner cannot be reached (or no SFO configured) but the node shutdown request has been recorded by the quorum change coordinator. The state is reported by the node's HA partner.
* <i>taken_over</i> - Node is taken over by its HA partner. The state is reported by the node's HA partner.
* <i>waiting_for_giveback</i> - Node is taken over by its HA partner and is now ready and waiting for giveback. To bring the node up, either issue the "giveback" command to the HA partner node or wait for auto-giveback, if enabled. The state is reported by the node's HA partner.
* <i>degraded</i> - Node is known to be up but is not yet fully functional. The node can be reached through the cluster interconnect but one or more critical services are offline. Or, the node is not reachable but the node's HA partner can be reached and reports that the node is up with firmware state "SF_UP".
* <i>unknown</i> - Node state cannot be determined.
<br/>
---
## HA
The "ha" field in the /cluster/nodes API shows the takeover and giveback states of the node along with the current values of the HA fields "enabled"and "auto_giveback".
You can modify the HA fields "enabled" and "auto_giveback", which will change the HA states of the node.
### Takeover
The takeover "state" field shows the different takeover states of the node. When the state is "failed", the "code" and "message" fields display.
Possible values for takeover states are:

* <i>not_attempted</i> - Takeover operation is not started and takeover is possible.
* <i>not_possible</i> - Takeover operation is not possible. Check the failure message.
* <i>in_progress</i> - Takeover operation is in progress. The node is taking over its partner.
* <i>in_takeover</i> - Takeover operation is complete.
* <i>failed</i> - Takeover operation failed. Check the failure message.
###
Possible values for takeover failure code and messages are:

* <i>code</i>: 852130 <i>message</i>: Failed to initiate takeover. Run the \"storage failover show-takeover\" command for more information.
* <i>code</i>: 852131 <i>message</i>: Takeover cannot be completed. Reason: disabled.
### Giveback
The giveback "state" field shows the different giveback states of the node. When the state is "failed", the "code" and "message" fields display.
Possible values for giveback states are:

* <i>nothing_to_giveback</i> - Node does not have partner aggregates to giveback.
* <i>not_attempted</i> - Giveback operation is not started.
* <i>in_progress</i> - Giveback operation is in progress.
* <i>failed</i> - Giveback operation failed. Check the failure message.
###
Possible values for giveback failure codes and messages are:

* <i>code</i>: 852126 <i>message</i>: Failed to initiate giveback. Run the \"storage failover show-giveback\" command for more information.
<br/>
---
## Performance monitoring
Performance of a node can be monitored by observing the `metric.*` and `statistics.*` properties. These properties show the performance of a node in terms of cpu utilization. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
<br/>
---
## Examples
The following examples show how to add nodes to a cluster, update node properties, shutdown and reboot a node, and remove a node from the cluster.
### Adding a single node with a minimal configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Node()
    resource.cluster_interface = {"ip": {"address": "1.1.1.1"}}
    resource.post(hydrate=True)
    print(resource)

```

---
### Adding multiple nodes in the same request and creating recommended aggregates
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Node()
    resource.records = [
        {"name": "node1", "cluster_interface": {"ip": {"address": "1.1.1.1"}}},
        {"name": "node2", "cluster_interface": {"ip": {"address": "2.2.2.2"}}},
    ]
    resource.post(hydrate=True, create_recommended_aggregates=True)
    print(resource)

```

---
### Modifying a cluster-wide configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Node()
    resource.name = "renamedNode"
    resource.location = "newLocation"
    resource.patch()

```

---
### Shutting down a node
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Node(uuid="{uuid}")
    resource.patch(hydrate=True, action="shutdown")

```

### Powering off a node using SP assistance
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Node(uuid="{uuid}")
    resource.patch(hydrate=True, action="power_off")

```

---
### Deleting a node from a cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Node(uuid="{uuid}")
    resource.delete()

```

### Force a node deletion from a cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Node(uuid="{uuid}")
    resource.delete(force=True)

```

---
### Retrieving the state of all nodes in a cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Node.get_collection(fields="state")))

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
[
    Node(
        {
            "name": "node2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/54440ec3-6127-11e9-a959-005056bb76f9"
                }
            },
            "uuid": "54440ec3-6127-11e9-a959-005056bb76f9",
            "state": "up",
        }
    ),
    Node(
        {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/e02dbef1-6126-11e9-b8fb-005056bb9ce4"
                }
            },
            "uuid": "e02dbef1-6126-11e9-b8fb-005056bb9ce4",
            "state": "up",
        }
    ),
]

```
</div>
</div>

---
### Retrieving nodes that are in the spare low condition in a cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Node.get_collection(fields="is_spares_low")))

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
[
    Node(
        {
            "name": "node2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/54440ec3-6127-11e9-a959-005056bb76f9"
                }
            },
            "uuid": "54440ec3-6127-11e9-a959-005056bb76f9",
        }
    ),
    Node(
        {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/e02dbef1-6126-11e9-b8fb-005056bb9ce4"
                }
            },
            "uuid": "e02dbef1-6126-11e9-b8fb-005056bb9ce4",
        }
    ),
]

```
</div>
</div>

---
### Retrieving statistics and metric for a node
In this example, the API returns the "statistics" and "metric" properties.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Node.get_collection(fields="statistics,metric")))

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
[
    Node(
        {
            "name": "example_node_name",
            "metric": {
                "status": "ok",
                "processor_utilization": 3,
                "timestamp": "2019-12-19T15:50:45+00:00",
                "duration": "PT15S",
            },
            "uuid": "6b29327b-21ca-11ea-99aa-005056bb420b",
            "statistics": {
                "status": "ok",
                "processor_utilization_raw": 6409411622,
                "processor_utilization_base": 74330229886,
                "timestamp": "2019-12-19T15:50:48+00:00",
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving takeover and giveback failure codes and messages
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Node.get_collection(fields="ha")))

```
<div class="try_it_out">
<input id="example10_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example10_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example10_result" class="try_it_out_content">
```
[
    Node(
        {
            "ha": {
                "auto_giveback": False,
                "ports": [{}, {}],
                "takeover": {
                    "failure": {
                        "message": "Takeover cannot be completed. Reason: disabled.",
                        "code": 852131,
                    },
                    "state": "not_possible",
                },
                "enabled": False,
                "partners": [
                    {"name": "node1", "uuid": "e02dbef1-6126-11e9-b8fb-005056bb9ce4"}
                ],
                "giveback": {"state": "nothing_to_giveback"},
            },
            "name": "node2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/54440ec3-6127-11e9-a959-005056bb76f9"
                }
            },
            "uuid": "54440ec3-6127-11e9-a959-005056bb76f9",
        }
    ),
    Node(
        {
            "ha": {
                "auto_giveback": False,
                "ports": [{}, {}],
                "takeover": {
                    "failure": {
                        "message": "Takeover cannot be completed. Reason: disabled.",
                        "code": 852131,
                    },
                    "state": "not_possible",
                },
                "enabled": False,
                "partners": [
                    {"name": "node2", "uuid": "54440ec3-6127-11e9-a959-005056bb76f9"}
                ],
                "giveback": {"state": "nothing_to_giveback"},
            },
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/e02dbef1-6126-11e9-b8fb-005056bb9ce4"
                }
            },
            "uuid": "e02dbef1-6126-11e9-b8fb-005056bb9ce4",
        }
    ),
]

```
</div>
</div>

---
### Retrieving external cache information for a node
In this example, the API returns the external_cache property.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Node

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Node.get_collection(fields="external_cache")))

```
<div class="try_it_out">
<input id="example11_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example11_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example11_result" class="try_it_out_content">
```
[
    Node(
        {
            "name": "node2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/71af8235-bea9-11eb-874a-005056bbab13"
                }
            },
            "external_cache": {
                "pcs_size": 256,
                "is_hya_enabled": True,
                "is_rewarm_enabled": False,
                "is_enabled": False,
            },
            "uuid": "71af8235-bea9-11eb-874a-005056bbab13",
        }
    ),
    Node(
        {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/8c4cbf08-bea9-11eb-b8ae-005056bb16aa"
                }
            },
            "external_cache": {
                "pcs_size": 256,
                "is_hya_enabled": True,
                "is_rewarm_enabled": False,
                "is_enabled": False,
            },
            "uuid": "8c4cbf08-bea9-11eb-b8ae-005056bb16aa",
        }
    ),
]

```
</div>
</div>
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


__all__ = ["Node", "NodeSchema"]
__pdoc__ = {
    "NodeSchema.resource": False,
    "NodeSchema.opts": False,
}


class NodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Node object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the node."""

    anti_ransomware_version = marshmallow_fields.Str(
        data_key="anti_ransomware_version",
        allow_none=True,
    )
    r""" Anti ransomware version.

Example: 1.0"""

    cluster_interface = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_cluster_interface.ClusterNodesClusterInterfaceSchema", data_key="cluster_interface", unknown=EXCLUDE, allow_none=True)
    r""" The cluster network IP address of the node to be added."""

    cluster_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_management_interfaces.ClusterNodesManagementInterfacesSchema", unknown=EXCLUDE, allow_none=True), data_key="cluster_interfaces", allow_none=True)
    r""" Network interface"""

    controller = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_controller.ClusterNodesControllerSchema", data_key="controller", unknown=EXCLUDE, allow_none=True)
    r""" Controller information"""

    date = ImpreciseDateTime(
        data_key="date",
        allow_none=True,
    )
    r""" The current or "wall clock" time of the node in ISO-8601 date, time, and time zone format.
The ISO-8601 date and time are localized based on the ONTAP cluster's timezone setting.


Example: 2019-04-17T15:49:26.000+0000"""

    external_cache = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_external_cache.ClusterNodesExternalCacheSchema", data_key="external_cache", unknown=EXCLUDE, allow_none=True)
    r""" Cache used for buffer management."""

    ha = marshmallow_fields.Nested("netapp_ontap.models.node_ha.NodeHaSchema", data_key="ha", unknown=EXCLUDE, allow_none=True)
    r""" The ha field of the node."""

    hw_assist = marshmallow_fields.Nested("netapp_ontap.models.hw_assist.HwAssistSchema", data_key="hw_assist", unknown=EXCLUDE, allow_none=True)
    r""" The hardware assist information."""

    is_spares_low = marshmallow_fields.Boolean(
        data_key="is_spares_low",
        allow_none=True,
    )
    r""" Specifies whether or not the node is in spares low condition."""

    location = marshmallow_fields.Str(
        data_key="location",
        allow_none=True,
    )
    r""" The location field of the node.

Example: rack 2 row 5"""

    management_interface = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_management_interface.ClusterNodesManagementInterfaceSchema", data_key="management_interface", unknown=EXCLUDE, allow_none=True)
    r""" The management interface of the node to be added. The subnet mask is set based on the management interface of the cluster or the management interfaces of other nodes."""

    management_interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_management_interfaces.ClusterNodesManagementInterfacesSchema", unknown=EXCLUDE, allow_none=True), data_key="management_interfaces", allow_none=True)
    r""" Network interface"""

    membership = marshmallow_fields.Str(
        data_key="membership",
        validate=enum_validation(['available', 'joining', 'member']),
        allow_none=True,
    )
    r""" Possible values:

* <i>available</i> - A node is detected on the internal cluster network and can be added to the cluster.  Nodes that have a membership of "available" are not returned when a GET request is called when the cluster exists. Provide a query on the "membership" property for <i>available</i> to scan for nodes on the cluster network. Nodes that have a membership of "available" are returned automatically before a cluster is created.
* <i>joining</i> - Joining nodes are in the process of being added to the cluster. The node might be progressing through the steps to become a member or might have failed. The job to add the node or create the cluster provides details on the current progress of the node.
* <i>member</i> - Nodes that are members have successfully joined the cluster.


Valid choices:

* available
* joining
* member"""

    metric = marshmallow_fields.Nested("netapp_ontap.resources.node_metrics.NodeMetricsSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" CPU performance for the nodes."""

    metrocluster = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_metrocluster.ClusterNodesMetroclusterSchema", data_key="metrocluster", unknown=EXCLUDE, allow_none=True)
    r""" Metrocluster"""

    model = marshmallow_fields.Str(
        data_key="model",
        allow_none=True,
    )
    r""" The model field of the node.

Example: FAS3070"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name field of the node.

Example: node-01"""

    nvram = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_nvram.ClusterNodesNvramSchema", data_key="nvram", unknown=EXCLUDE, allow_none=True)
    r""" The nvram field of the node."""

    owner = marshmallow_fields.Str(
        data_key="owner",
        allow_none=True,
    )
    r""" Owner of the node.

Example: Example Corp"""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        allow_none=True,
    )
    r""" The serial_number field of the node.

Example: 4048820-60-9"""

    service_processor = marshmallow_fields.Nested("netapp_ontap.models.service_processor.ServiceProcessorSchema", data_key="service_processor", unknown=EXCLUDE, allow_none=True)
    r""" The service_processor field of the node."""

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_snaplock.ClusterNodesSnaplockSchema", data_key="snaplock", unknown=EXCLUDE, allow_none=True)
    r""" SnapLock-related properties."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'booting', 'down', 'taken_over', 'waiting_for_giveback', 'degraded', 'unknown']),
        allow_none=True,
    )
    r""" State of the node:

* <i>up</i> - Node is up and operational.
* <i>booting</i> - Node is booting up.
* <i>down</i> - Node has stopped or is dumping core.
* <i>taken_over</i> - Node has been taken over by its HA partner and is not yet waiting for giveback.
* <i>waiting_for_giveback</i> - Node has been taken over by its HA partner and is waiting for the HA partner to giveback disks.
* <i>degraded</i> - Node has one or more critical services offline.
* <i>unknown</i> - Node or its HA partner cannot be contacted and there is no information on the node's state.


Valid choices:

* up
* booting
* down
* taken_over
* waiting_for_giveback
* degraded
* unknown"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.node_statistics.NodeStatisticsSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" Raw CPU performance for the nodes."""

    storage_availability_zones = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_storage_availability_zones.ClusterNodesStorageAvailabilityZonesSchema", unknown=EXCLUDE, allow_none=True), data_key="storage_availability_zones", allow_none=True)
    r""" Storage availability zones associated with the node."""

    storage_configuration = marshmallow_fields.Str(
        data_key="storage_configuration",
        validate=enum_validation(['unknown', 'single_path', 'multi_path', 'mixed_path', 'quad_path', 'single_path_ha', 'multi_path_ha', 'mixed_path_ha', 'quad_path_ha', 'tri_path', 'tri_path_ha', 'virtual']),
        allow_none=True,
    )
    r""" The storage configuration in the system. Possible values:

* <i>mixed_path</i>
* <i>single_path</i>
* <i>multi_path</i>
* <i>tri_path</i>
* <i>quad_path</i>
* <i>mixed_path_ha</i>
* <i>single_path_ha</i>
* <i>multi_path_ha</i>
* <i>tri_path_ha</i>
* <i>quad_path_ha</i>
* <i>unknown</i>
* <i>virtual</i>


Valid choices:

* unknown
* single_path
* multi_path
* mixed_path
* quad_path
* single_path_ha
* multi_path_ha
* mixed_path_ha
* quad_path_ha
* tri_path
* tri_path_ha
* virtual"""

    system_aggregate = marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", data_key="system_aggregate", unknown=EXCLUDE, allow_none=True)
    r""" The system_aggregate field of the node."""

    system_id = marshmallow_fields.Str(
        data_key="system_id",
        allow_none=True,
    )
    r""" The system_id field of the node.

Example: 92027651"""

    system_machine_type = marshmallow_fields.Str(
        data_key="system_machine_type",
        allow_none=True,
    )
    r""" OEM system machine type.

Example: 7Y56-CTOWW1"""

    uptime = Size(
        data_key="uptime",
        allow_none=True,
    )
    r""" The total time, in seconds, that the node has been up.

Example: 300536"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the node.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    vendor_serial_number = marshmallow_fields.Str(
        data_key="vendor_serial_number",
        allow_none=True,
    )
    r""" OEM vendor serial number.

Example: 791603000068"""

    version = marshmallow_fields.Nested("netapp_ontap.models.version.VersionSchema", data_key="version", unknown=EXCLUDE, allow_none=True)
    r""" This returns the cluster version information.  When the cluster has more than one node, the cluster version is equivalent to the lowest of generation, major, and minor versions on all nodes."""

    vm = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_vm.ClusterNodesVmSchema", data_key="vm", unknown=EXCLUDE, allow_none=True)
    r""" The vm field of the node."""

    @property
    def resource(self):
        return Node

    gettable_fields = [
        "links",
        "anti_ransomware_version",
        "cluster_interfaces.links",
        "cluster_interfaces.ip",
        "cluster_interfaces.name",
        "cluster_interfaces.uuid",
        "controller",
        "date",
        "external_cache",
        "ha",
        "hw_assist",
        "is_spares_low",
        "location",
        "management_interfaces.links",
        "management_interfaces.ip",
        "management_interfaces.name",
        "management_interfaces.uuid",
        "membership",
        "metric",
        "metrocluster",
        "model",
        "name",
        "nvram",
        "owner",
        "serial_number",
        "service_processor",
        "snaplock",
        "state",
        "statistics",
        "storage_availability_zones.links",
        "storage_availability_zones.name",
        "storage_availability_zones.uuid",
        "storage_configuration",
        "system_aggregate.links",
        "system_aggregate.name",
        "system_aggregate.uuid",
        "system_id",
        "system_machine_type",
        "uptime",
        "uuid",
        "vendor_serial_number",
        "version",
        "vm",
    ]
    """links,anti_ransomware_version,cluster_interfaces.links,cluster_interfaces.ip,cluster_interfaces.name,cluster_interfaces.uuid,controller,date,external_cache,ha,hw_assist,is_spares_low,location,management_interfaces.links,management_interfaces.ip,management_interfaces.name,management_interfaces.uuid,membership,metric,metrocluster,model,name,nvram,owner,serial_number,service_processor,snaplock,state,statistics,storage_availability_zones.links,storage_availability_zones.name,storage_availability_zones.uuid,storage_configuration,system_aggregate.links,system_aggregate.name,system_aggregate.uuid,system_id,system_machine_type,uptime,uuid,vendor_serial_number,version,vm,"""

    patchable_fields = [
        "ha",
        "location",
        "name",
        "owner",
        "service_processor",
        "system_aggregate.name",
        "system_aggregate.uuid",
    ]
    """ha,location,name,owner,service_processor,system_aggregate.name,system_aggregate.uuid,"""

    postable_fields = [
        "cluster_interface",
        "ha",
        "location",
        "management_interface",
        "name",
        "owner",
        "service_processor",
        "system_aggregate.name",
        "system_aggregate.uuid",
    ]
    """cluster_interface,ha,location,management_interface,name,owner,service_processor,system_aggregate.name,system_aggregate.uuid,"""

class Node(Resource):
    r""" Complete node information """

    _schema = NodeSchema
    _path = "/api/cluster/nodes"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the nodes in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `system node show`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Node resources that match the provided query"""
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
        """Returns a list of RawResources that represent Node resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Node"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the node information or performs shutdown/reboot actions on a node.
### Related ONTAP commands
* `cluster ha modify`
* `storage failover modify`
* `system node modify`
* `system node reboot`
* `system node power off`
* `system node power on`
* `system service-processor network modify`
* `system service-processor reboot-sp`
* `system service-processor image modify`
* `system service-processor network auto-configuration enable`
* `system service-processor network auto-configuration disable`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Node"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Node"], NetAppResponse]:
        r"""Adds a node or nodes to the cluster.
### Required properties
* `cluster_interface.ip.address`
### Related ONTAP commands
* `cluster add-node`
* `network interface create`
* `storage aggregate auto-provision`
* `system node modify`
* `system service-processor network modify`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Node"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a node from the cluster.
Note that before deleting a node from the cluster, you must shut down all of the node's shared resources, such as virtual interfaces to clients. If any of the node's shared resources are still active, the command fails.
### Optional parameters:
* `force` - Forcibly removes a node that is down and cannot be brought online to remove its shared resources. This flag is set to "false" by default.
### Related ONTAP commands
* `cluster remove-node`
### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the nodes in the cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `system node show`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information for the node.
### Related ONTAP commands
* `cluster add-node-status`
* `cluster date show`
* `cluster ha show`
* `network interface show`
* `network port show`
* `storage failover show`
* `system controller show`
* `system node show`
* `system node show-discovered`
* `system service-processor network show`
* `system service-processor show`
* `system service-processor ssh show`
* `system service-processor image show`
* `version`
* `system service-processor api-service show`
* `system service-processor network auto-configuration show`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
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
        r"""Adds a node or nodes to the cluster.
### Required properties
* `cluster_interface.ip.address`
### Related ONTAP commands
* `cluster add-node`
* `network interface create`
* `storage aggregate auto-provision`
* `system node modify`
* `system service-processor network modify`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
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
        r"""Updates the node information or performs shutdown/reboot actions on a node.
### Related ONTAP commands
* `cluster ha modify`
* `storage failover modify`
* `system node modify`
* `system node reboot`
* `system node power off`
* `system node power on`
* `system service-processor network modify`
* `system service-processor reboot-sp`
* `system service-processor image modify`
* `system service-processor network auto-configuration enable`
* `system service-processor network auto-configuration disable`

### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)"""
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
        r"""Deletes a node from the cluster.
Note that before deleting a node from the cluster, you must shut down all of the node's shared resources, such as virtual interfaces to clients. If any of the node's shared resources are still active, the command fails.
### Optional parameters:
* `force` - Forcibly removes a node that is down and cannot be brought online to remove its shared resources. This flag is set to "false" by default.
### Related ONTAP commands
* `cluster remove-node`
### Learn more
* [`DOC /cluster/nodes`](#docs-cluster-cluster_nodes)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


