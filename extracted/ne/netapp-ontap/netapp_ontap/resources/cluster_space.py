r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Retrieves cluster-wide storage details across the different tiers.
Storage details include storage efficiency, block storage and cloud storage information.
---
Example
### Retrieving cluster-wide storage details
The following example shows the details returned for a GET request on cluster-wide storage:
<personalities supports=unified>
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterSpace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterSpace()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
ClusterSpace(
    {
        "efficiency": {
            "ratio": 1.134099616858238,
            "savings": 143360,
            "logical_used": 1212416,
        },
        "efficiency_without_snapshots_flexclones": {
            "ratio": 1.0,
            "savings": 0,
            "logical_used": 167936,
        },
        "efficiency_without_snapshots": {
            "ratio": 1.0,
            "savings": 0,
            "logical_used": 167936,
        },
        "block_storage": {
            "used": 6269812736,
            "inactive_data": 0,
            "size": 56125612032,
            "available": 49855799296,
            "medias": [
                {
                    "efficiency": {"ratio": 1.0, "savings": 0, "logical_used": 0},
                    "efficiency_without_snapshots_flexclones": {
                        "ratio": 1.0,
                        "savings": 0,
                        "logical_used": 0,
                    },
                    "used": 6163390464,
                    "size": 9891430400,
                    "efficiency_without_snapshots": {
                        "ratio": 1.0,
                        "savings": 0,
                        "logical_used": 0,
                    },
                    "available": 3728039936,
                    "type": "ssd",
                    "physical_used": 1832886272,
                },
                {
                    "efficiency": {
                        "ratio": 1.303964757709251,
                        "savings": 282624,
                        "logical_used": 1212416,
                    },
                    "efficiency_without_snapshots_flexclones": {
                        "ratio": 1.0,
                        "savings": 0,
                        "logical_used": 167936,
                    },
                    "used": 106422272,
                    "size": 46234181632,
                    "efficiency_without_snapshots": {
                        "ratio": 1.0,
                        "savings": 0,
                        "logical_used": 167936,
                    },
                    "available": 46127759360,
                    "type": "vmdisk",
                    "physical_used": 5398528,
                },
            ],
            "physical_used": 1838284800,
        },
    }
)

```
</div>
</div>

---
</personalities>
<personalities supports=asar2>
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterSpace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterSpace()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
ClusterSpace(
    {
        "efficiency_without_snapshots": {
            "ratio": 1.0,
            "savings": 73728,
            "logical_used": 73728,
        },
        "block_storage": {
            "delayed_frees": 57139200,
            "total_metadata_used": 58679865344,
            "full_threshold_percent": 98,
            "nearly_full_threshold_percent": 85,
            "physical_used_percent": 46,
            "size": 125357654016,
            "available": 66677788672,
            "physical_used": 58679865344,
        },
    }
)

```
</div>
</div>

---
### Updating the threshold value for a cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterSpace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterSpace()
    resource.block_storage.nearly_full_threshold_percent = "85"
    resource.patch()

```

---
</personalities>"""

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


__all__ = ["ClusterSpace", "ClusterSpaceSchema"]
__pdoc__ = {
    "ClusterSpaceSchema.resource": False,
    "ClusterSpaceSchema.opts": False,
}


class ClusterSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterSpace object"""

    block_storage = marshmallow_fields.Nested("netapp_ontap.models.cluster_space_block_storage.ClusterSpaceBlockStorageSchema", data_key="block_storage", unknown=EXCLUDE, allow_none=True)
    r""" Configuration information for the locally attached portion of the storage across the cluster. When a cloud store is also used by the storage, this is referred to as the performance tier."""

    cloud_storage = marshmallow_fields.Nested("netapp_ontap.models.cluster_space_cloud_storage.ClusterSpaceCloudStorageSchema", data_key="cloud_storage", unknown=EXCLUDE, allow_none=True)
    r""" Configuration information for the cloud storage portion of all the aggregates across the cluster. This is referred to as the capacity tier."""

    efficiency = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency", unknown=EXCLUDE, allow_none=True)
    r""" The efficiency field of the cluster_space."""

    efficiency_without_snapshots = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency_without_snapshots", unknown=EXCLUDE, allow_none=True)
    r""" The efficiency_without_snapshots field of the cluster_space."""

    efficiency_without_snapshots_flexclones = marshmallow_fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency_without_snapshots_flexclones", unknown=EXCLUDE, allow_none=True)
    r""" The efficiency_without_snapshots_flexclones field of the cluster_space."""

    @property
    def resource(self):
        return ClusterSpace

    gettable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,"""

    patchable_fields = [
        "block_storage",
    ]
    """block_storage,"""

    postable_fields = [
        "block_storage",
    ]
    """block_storage,"""

class ClusterSpace(Resource):
    r""" Provides information on cluster-wide storage details across the different tiers. Storage details include storage efficiency, block storage and cloud storage information. """

    _schema = ClusterSpaceSchema
    _path = "/api/storage/cluster"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves cluster-wide storage details across the different tiers. By default, this endpoint returns all fields.
Storage details include storage efficiency, block storage and cloud storage information.
Supports the following roles: admin, and readonly.

### Learn more
* [`DOC /storage/cluster`](#docs-storage-storage_cluster)"""
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
        r"""Updates full_threshold_percent and nearly_full_threshold_percent for the complete cluster.

### Learn more
* [`DOC /storage/cluster`](#docs-storage-storage_cluster)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



