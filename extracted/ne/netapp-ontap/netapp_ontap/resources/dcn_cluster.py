r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
This API can be used to create a compute cluster and retrieve the current compute cluster configuration.
## Creating a compute cluster
A compute cluster can be created by issuing a POST request on /dcn/cluster. The following parameters are required:

* nodes
* network_pool
## Nodes field
The nodes field should be populated with a subset of discovered data compute nodes. Available data compute nodes can be found by issuing a GET request on /dcn/cluster/nodes?membership=available. This request returns a list of discovered compute nodes found on the network. The membership=available query parameter is optional if a compute cluster does not already exist. If names are not provided for each node, then a name will be automatically generated.
## Examples
### Creating a compute cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnCluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnCluster()
    resource.nodes = [
        {"serial_number": "4048820-60-9"},
        {"serial_number": "4048820-47-3"},
        {"serial_number": "4048820-53-6"},
    ]
    resource.network_pool = {
        "subnet": {"address": "10.27.0.1", "netmask": "24"},
        "ip_ranges": [{"start": "10.27.0.10", "end": "10.27.0.10"}],
    }
    resource.service_ip = {
        "address": "10.10.10.7",
        "netmask": "255.255.255.0",
        "gateway": "10.1.1.1",
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
DcnCluster(
    {
        "service_ip": {
            "gateway": "10.1.1.1",
            "netmask": "255.255.255.0",
            "address": "10.10.10.7",
        },
        "nodes": [
            {"serial_number": "4048820-60-9"},
            {"serial_number": "4048820-47-3"},
            {"serial_number": "4048820-53-6"},
        ],
        "network_pool": {
            "subnet": {"netmask": "24", "address": "10.27.0.1"},
            "ip_ranges": [{"start": "10.27.0.10", "end": "10.27.0.10"}],
        },
    }
)

```
</div>
</div>

### Modifying the cluster's data platform IP
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnCluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnCluster()
    resource.service_ip = {
        "address": "10.10.10.1",
        "netmask": "255.255.255.0",
        "gateway": "10.1.1.1",
    }
    resource.patch()

```

### Modifying the cluster's network pool
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnCluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnCluster()
    resource.network_pool = {
        "subnet": {"address": "10.27.27.1", "netmask": "24"},
        "ip_ranges": [{"start": "10.27.27.1", "end": "10.27.27.1"}],
    }
    resource.patch()

```

### Delete the cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnCluster

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnCluster()
    resource.delete()

```
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


__all__ = ["DcnCluster", "DcnClusterSchema"]
__pdoc__ = {
    "DcnClusterSchema.resource": False,
    "DcnClusterSchema.opts": False,
}

class DcnClusterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnCluster object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the dcn_cluster."""

    network_pool = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_cluster_network_pool", "DcnClusterNetworkPoolSchema"),
                data_key="network_pool",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Pool of usable IP addresses for the compute cluster network."""

    nodes = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.resources.dcn_node", "DcnNodeSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="nodes",
                allow_none=True
            )
    r""" Compute node information."""

    service_ip = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.ip_interface_and_gateway", "IpInterfaceAndGatewaySchema"),
                data_key="service_ip",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" Object to setup an interface along with its default router."""

    software = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_cluster_software", "DcnClusterSoftwareSchema"),
                data_key="software",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The software information of the DCN cluster."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID of the compute cluster.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return DcnCluster

    gettable_fields = [
        "links",
        "network_pool",
        "nodes",
        "service_ip",
        "software",
        "uuid",
    ]
    """links,network_pool,nodes,service_ip,software,uuid,"""

    patchable_fields = [
        "network_pool",
        "service_ip",
    ]
    """network_pool,service_ip,"""

    postable_fields = [
        "network_pool",
        "nodes",
        "service_ip",
    ]
    """network_pool,nodes,service_ip,"""

class DcnCluster(Resource):
    r""" Compute cluster information. """

    _schema = DcnClusterSchema
    _path = "/api/dcn/cluster"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the compute cluster configuration.
### Learn more
* [`DOC /dcn/cluster`](#docs-dcn-dcn_cluster)"""
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
        r"""Creates a data compute cluster.
### Required properties
* `nodes`
* `network_pool`

### Learn more
* [`DOC /dcn/cluster`](#docs-dcn-dcn_cluster)"""
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
        r"""Modifies a compute cluster.

### Learn more
* [`DOC /dcn/cluster`](#docs-dcn-dcn_cluster)"""
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
        r"""Deletes a compute cluster.

### Learn more
* [`DOC /dcn/cluster`](#docs-dcn-dcn_cluster)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


