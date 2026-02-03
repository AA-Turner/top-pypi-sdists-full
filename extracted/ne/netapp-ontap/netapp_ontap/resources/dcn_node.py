r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use these API endpoints to update node configuration, delete node configuration, and retrieve the node status.
## Adding a node to a compute cluster
A node can be added to an existing compute cluster by issuing a POST request on /dcn/cluster/nodes. If a compute cluster does not already exist, the API returns a 400 Bad Request error.
## Examples
### Adding a single node to a cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNode

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnNode()
    resource.serial_number = "4048820-60-9"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
DcnNode({"serial_number": "4048820-60-9"})

```
</div>
</div>

### Adding multiple nodes to a cluster
Multiple nodes can be added by sending a "records" array containing each node to the API.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNode

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnNode()
    resource.records = [
        {"serial_number": "4048820-60-9", "name": "node1"},
        {"serial_number": "4048820-55-7", "name": "node2"},
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
DcnNode({})

```
</div>
</div>

## Discover available compute nodes
Available nodes eligible to join or create a compute cluster can be discovered by issuing a GET request on /dcn/cluster/nodes. If a compute cluster already exists, the query parameter "membership=available" must be used to discover nodes not already in the cluster. If there is no compute cluster, the query parameter is optional. When a compute cluster already exists and the membership query parameter is not sent, the API only returns information about nodes already participating in the cluster.
## Examples
### Discover available nodes to join
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNode

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(DcnNode.get_collection(membership="available")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    DcnNode(
        {
            "serial_number": "4048820-32-5",
            "name": "node1",
            "membership": "available",
            "uuid": "f8b16514-cb03-44e0-8efd-9feec9c3fb3e",
        }
    ),
    DcnNode(
        {
            "serial_number": "4048820-47-2",
            "name": "node2",
            "membership": "available",
            "uuid": "f8b16514-cb03-44e0-8efd-9feec9c3fb3f",
        }
    ),
]

```
</div>
</div>

### Retrieve membership for each node in the cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNode

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(DcnNode.get_collection(fields="membership")))

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    DcnNode(
        {
            "name": "dcn-01",
            "membership": "member",
            "_links": {
                "self": {
                    "href": "/api/dcn/cluster/nodes/f8b16514-cb03-44e0-8efd-9feec9c3fb3e"
                }
            },
            "uuid": "f8b16514-cb03-44e0-8efd-9feec9c3fb3e",
        }
    ),
    DcnNode(
        {
            "name": "dcn-02",
            "membership": "member",
            "_links": {
                "self": {
                    "href": "/api/dcn/cluster/nodes/f8b16514-cb03-44e0-8efd-9feec9c3fb3f"
                }
            },
            "uuid": "f8b16514-cb03-44e0-8efd-9feec9c3fb3f",
        }
    ),
]

```
</div>
</div>


### Delete a node from the cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNode

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnNode(uuid="1152414e-2eb2-48b7-a960-4aa2cba312b6")
    resource.delete()

```

### Retrieving statistics and metrics for a node
In this example, the API returns the statistics and metric properties.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnNode

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(DcnNode.get_collection(fields="statistics,metric")))

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    DcnNode(
        {
            "name": "example_node_name",
            "metric": {
                "cpu": {"memory_used": 1024000000, "processor_utilization": 3},
                "timestamp": "2019-12-19T15:50:45+00:00",
                "gpu": {"memory_used": 1024000000, "processor_utilization": 3},
                "status": "ok",
                "duration": "PT15S",
            },
            "statistics": {
                "status": "ok",
                "gpu": {
                    "processor_utilization_base": 35042835393,
                    "memory_used": 1024000000,
                    "processor_utilization_raw": 2514992973,
                },
                "cpu": {
                    "processor_utilization_base": 35046206957,
                    "memory_used": 1024000000,
                    "processor_utilization_raw": 2569086312,
                },
                "timestamp": "2019-12-19T15:50:48+00:00",
            },
            "uuid": "6b29327b-21ca-11ea-99aa-005056bb420b",
        }
    )
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
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["DcnNode", "DcnNodeSchema"]
__pdoc__ = {
    "DcnNodeSchema.resource": False,
    "DcnNodeSchema.opts": False,
}

class DcnNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNode object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the dcn_node."""

    date = ImpreciseDateTime(
        data_key="date",
        allow_none=True,
    )
    r""" The current or "wall clock" time of the node in ISO-8601 date, time, and time zone format.
The ISO-8601 date and time are localized based on the ONTAP cluster's timezone setting.


Example: 2019-04-17T15:49:26.000+0000"""

    error = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.dcn_node_error", "DcnNodeErrorSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="error",
                allow_none=True
            )
    r""" DCN node error information."""

    hardware = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_hardware", "DcnHardwareSchema"),
                data_key="hardware",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Hardware information."""

    location = marshmallow_fields.Str(
        data_key="location",
        allow_none=True,
    )
    r""" The location field of the dcn_node.

Example: rack 2 row 5"""

    membership = marshmallow_fields.Str(
        data_key="membership",
        validate=enum_validation(['available', 'joining', 'member']),
        allow_none=True,
    )
    r""" Possible values:

* <i>available</i> - A node is detected on the network and can be added to the compute cluster. Nodes that have a membership of "available" are not returned when a GET request is called when the cluster exists. Provide a query on the "membership" property for <i>available</i> to scan for nodes on the network. Nodes that have a membership of "available" are returned automatically before a cluster is created.
* <i>joining</i> - Joining nodes are in the process of being added to the cluster. The node might be progressing through the steps to become a member or might have failed. The job to add the node or create the cluster provides details on the current progress of the node.
* <i>member</i> - Nodes that are members have successfully joined the cluster.


Valid choices:

* available
* joining
* member"""

    metric = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.dcn_node_metrics", "DcnNodeMetricsSchema"),
                data_key="metric",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" CPU and GPU performance metrics for the nodes. It provides detailed insights into the utilization and memory usage of the processors over specified time durations."""

    model = marshmallow_fields.Str(
        data_key="model",
        allow_none=True,
    )
    r""" The model field of the dcn_node.

Example: FAS3070"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The node's hostname.

Example: node1"""

    network = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_network", "DcnNodeNetworkSchema"),
                data_key="network",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The network field of the dcn_node."""

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
    r""" The serial_number field of the dcn_node.

Example: 4048820-60-9"""

    software = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_software", "DcnNodeSoftwareSchema"),
                data_key="software",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The software information of the node."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'down', 'degraded']),
        allow_none=True,
    )
    r""" State of the node:

* <i>up</i> - Node is up and operational.
* <i>down</i> - Node has stopped or is dumping core.
* <i>degraded</i> - Node has one or more critical services offline.


Valid choices:

* up
* down
* degraded"""

    statistics = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_statistics", "DcnNodeStatisticsSchema"),
                data_key="statistics",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Detailed CPU and GPU performance metrics for the nodes. It provides raw utilization and memory usage data, enabling precise calculations of processor performance."""

    system_id = marshmallow_fields.Str(
        data_key="system_id",
        allow_none=True,
    )
    r""" The system_id field of the dcn_node.

Example: 0537035403"""

    uptime = Size(
        data_key="uptime",
        allow_none=True,
    )
    r""" The total time that the node has been up, in seconds.

Example: 300536"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the dcn_node.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    vendor_serial_number = marshmallow_fields.Str(
        data_key="vendor_serial_number",
        allow_none=True,
    )
    r""" OEM vendor serial number.

Example: 791603000068"""

    @property
    def resource(self):
        return DcnNode

    gettable_fields = [
        "links",
        "date",
        "error",
        "hardware",
        "location",
        "membership",
        "metric",
        "model",
        "name",
        "network",
        "owner",
        "serial_number",
        "software",
        "state",
        "statistics",
        "system_id",
        "uptime",
        "uuid",
        "vendor_serial_number",
    ]
    """links,date,error,hardware,location,membership,metric,model,name,network,owner,serial_number,software,state,statistics,system_id,uptime,uuid,vendor_serial_number,"""

    patchable_fields = [
        "location",
        "name",
        "network",
        "owner",
    ]
    """location,name,network,owner,"""

    postable_fields = [
        "location",
        "name",
        "network",
        "owner",
        "serial_number",
    ]
    """location,name,network,owner,serial_number,"""

class DcnNode(Resource):
    r""" Compute node information. """

    _schema = DcnNodeSchema
    _path = "/api/dcn/cluster/nodes"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of data compute nodes.

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all DcnNode resources that match the provided query"""
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
        """Returns a list of RawResources that represent DcnNode resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["DcnNode"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies a compute node.
### Required properties
* `uuid` - UUID for the compute node instance

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["DcnNode"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DcnNode"], NetAppResponse]:
        r"""Adds one or more compute nodes to the compute cluster.
### Required properties
* `serial_number`
### Optional properties
* `name`
If a name is not provided it is automatically generated.

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["DcnNode"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the node.  This is effectively a factory reset.

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of data compute nodes.

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the node configuration and status.

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
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
        r"""Adds one or more compute nodes to the compute cluster.
### Required properties
* `serial_number`
### Optional properties
* `name`
If a name is not provided it is automatically generated.

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
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
        r"""Modifies a compute node.
### Required properties
* `uuid` - UUID for the compute node instance

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
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
        r"""Deletes the node.  This is effectively a factory reset.

### Learn more
* [`DOC /dcn/cluster/nodes`](#docs-dcn-dcn_cluster_nodes)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


