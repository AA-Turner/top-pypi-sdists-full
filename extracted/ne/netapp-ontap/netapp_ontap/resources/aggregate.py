r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Updating storage aggregates
The PATCH operation is used to modify properties of the aggregate. There are several properties that can be modified on an aggregate. Only one property can be modified for each PATCH request.
PATCH operations on the aggregate's disk count will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.</br>
Aggregates are automatically managed in the ASA r2 system. Therefore, PATCH and DELETE operations are not supported in ASA r2.</br>
The following is a list of properties that can be modified using the PATCH operation including a brief description for each:

* name - This property can be changed to rename the aggregate.
* node.name and node.uuid - Either property can be updated in order to relocate the aggregate to a different node in the cluster.
* state - This property can be changed to 'online' or 'offline'. Setting an aggregate 'offline' would automatically offline all the volumes currently hosted on the aggregate.
* block_storage.mirror.enabled - This property can be changed from 'false' to 'true' in order to mirror the aggregate, if the system is capable of doing so.
* block_storage.primary.disk_count - This property can be updated to increase the number of disks in an aggregate.
* block_storage.primary.raid_size - This property can be updated to set the desired RAID size.
* block_storage.primary.raid_type - This property can be updated to set the desired RAID type.
* cloud_storage.tiering_fullness_threshold - This property can be updated to set the desired tiering fullness threshold if using FabricPool.
* cloud_storage.migrate_threshold - This property can be updated to set the desired migrate threshold if using FabricPool.
* data_encryption.software_encryption_enabled - This property enables or disables NAE on the aggregate.
* block_storage.hybrid_cache.storage_pools.allocation_units_count - This property can be updated to add a storage pool to the aggregate specifying the number of allocation units.
* block_storage.hybrid_cache.storage_pools.name - This property can be updated to add a storage pool to the aggregate specifying the storage pool name. block_storage.hybrid_cache.storage_pools.uuid or this field must be specified with block_storage.hybrid_cache.storage_pools.allocation_units_count.
* block_storage.hybrid_cache.storage_pools.uuid - This property can be updated to add a storage pool to the aggregate specifying the storage pool uuid. block_storage.hybrid_cache.storage_pools.name or this field must be specified with block_storage.hybrid_cache.storage_pools.allocation_units_count.
* block_storage.hybrid_cache.raid_size - This property can be updated to set the desired RAID size. This property can also be specified on the first time addition of a storage pool to the aggregate.
* block_storage.hybrid_cache.raid_type - This property can be updated to set the desired RAID type of a physical SSD Flash Pool. This property can also be specified on the first time addition of a storage pool to the aggregate. When specifying a raidtype of raid4, the node is required to have spare SSDs for the storage pool as well.
* block_storage.hybrid_cache.disk_count - This property can be specified on the first time addition of physical SSD cache to the aggregate. It can also be updated to increase the number of disks in the physical SSD cache of a hybrid aggregate.
### Aggregate expansion
The PATCH operation also supports automatically expanding an aggregate based on the spare disks which are present within the system. Running PATCH with the query "auto_provision_policy" set to "expand" starts the recommended expansion job. In order to see the expected change in capacity before starting the job, call GET on an aggregate instance with the query "auto_provision_policy" set to "expand".
### Manual simulated aggregate expansion
The PATCH operation also supports simulated manual expansion of an aggregate.
Running PATCH with the query "simulate" set to "true" and "block_storage.primary.disk_count" set to the final disk count will start running the prechecks associated with expanding the aggregate to the proposed size.
The response body will include information on how many disks the aggregate can be expanded to, any associated warnings, along with the proposed final size of the aggregate.
## Deleting storage aggregates
If volumes exist on an aggregate, they must be deleted or moved before the aggregate can be deleted.
See the /storage/volumes API for details on moving or deleting volumes.
## Adding a storage pool to an aggregate
A storage pool can be added to an aggregate by patching the field "block_storage.hybrid_cache.storage_pools.allocation_units_count" while also specifying the specific storage pool using the
"block_storage.hybrid_cache.storage_pools.name" or "block_storage.hybrid_cache.storage_pools.uuid". Subsequent patches to the aggregate can be completed to increase allocation unit counts
or adding additional storage pools. On the first time addition of a storage pool to the aggregate, the raidtype can be optionally specified using the "block_storage.hybrid_cache.raid_type" field.
## Adding physical SSD cache capacity to an aggregate
The PATCH operation supports addition of a new physical SSD cache to an aggregate. It also supports expansion of existing physical SSD cache in the hybrid aggregate.
Running PATCH with "block_storage.hybrid_cache.disk_count" set to the final disk count will expand the physical SSD cache of the hybrid aggregate to the proposed size.
The RAID type can be optionally specified using the "block_storage.hybrid_cache.raid_type" field.
The RAID size can be optionally specified using the "block_storage.hybrid_cache.raid_size" field.
These operations can also be simulated by setting the query "simulate" to "true".
---
## Examples
### Retrieving a specific aggregate from the cluster
The following example shows the response of the requested aggregate. If there is no aggregate with the requested UUID, an error is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="870dd9f2-bdfa-4167-b692-57d1cec874d4")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Aggregate(
    {
        "name": "test1",
        "data_encryption": {
            "drive_protection_enabled": False,
            "software_encryption_enabled": False,
        },
        "block_storage": {
            "uses_partitions": False,
            "mirror": {"enabled": False, "state": "unmirrored"},
            "primary": {
                "raid_type": "raid_dp",
                "disk_class": "solid_state",
                "disk_count": 6,
                "checksum_style": "block",
                "raid_size": 24,
                "disk_type": "ssd",
            },
            "storage_type": "vmdisk",
            "hybrid_cache": {"enabled": False},
            "plexes": [{"name": "plex0"}],
        },
        "inode_attributes": {
            "files_total": 31136,
            "max_files_used": 97,
            "files_used": 97,
            "used_percent": 5,
            "max_files_possible": 2844525,
            "max_files_available": 31136,
        },
        "node": {"name": "node-1", "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1"},
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
        "volume-count": 0,
        "create_time": "2018-12-04T15:40:38-05:00",
        "state": "online",
        "cloud_storage": {"attach_eligible": False},
        "snapshot": {
            "files_total": 10,
            "max_files_available": 5,
            "max_files_used": 50,
            "files_used": 3,
        },
        "snaplock_type": "non_snaplock",
        "space": {
            "efficiency": {
                "ratio": 6.908119720880661,
                "cross_volume_inline_dedupe": False,
                "cross_volume_dedupe_savings": True,
                "enable_workload_informed_tsse": True,
                "cross_volume_background_dedupe": True,
                "savings": 1408029,
                "logical_used": 1646350,
                "wise_tsse_min_used_capacity_pct": 2,
                "auto_adaptive_compression_savings": False,
            },
            "efficiency_without_snapshots_flexclones": {
                "ratio": 2.0,
                "savings": 5000,
                "logical_used": 10000,
            },
            "cloud_storage": {"used": 0},
            "snapshot": {
                "used": 3000,
                "used_percent": 45,
                "total": 5000,
                "reserve_percent": 20,
                "available": 2000,
            },
            "efficiency_without_snapshots": {
                "ratio": 1.0,
                "savings": 0,
                "logical_used": 737280,
            },
            "block_storage": {
                "used_including_snapshot_reserve_percent": 35,
                "aggregate_metadata": 2655,
                "physical_used": 5271552,
                "data_compaction_space_saved_percent": 47,
                "volume_footprints_percent": 14,
                "physical_used_percent": 1,
                "aggregate_metadata_percent": 8,
                "used_including_snapshot_reserve": 674685,
                "data_compacted_count": 666666,
                "used": 43061248,
                "volume_deduplication_space_saved": 23765,
                "used_percent": 50,
                "data_compaction_space_saved": 654566,
                "size": 235003904,
                "volume_deduplication_space_saved_percent": 32,
                "full_threshold_percent": 98,
                "available": 191942656,
                "volume_deduplication_shared_count": 567543,
            },
        },
        "home_node": {"name": "node-1", "uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1"},
    }
)

```
</div>
</div>

### Retrieving statistics and metric for an aggregate
In this example, the API returns the "statistics" and "metric" properties for the aggregate requested.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="538bf337-1b2c-11e8-bad0-005056b48388")
    resource.get(fields="statistics,metric")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Aggregate(
    {
        "name": "aggr4",
        "metric": {
            "status": "ok",
            "iops": {"total": 11682, "write": 17, "other": 11663, "read": 1},
            "latency": {"total": 124, "write": 230, "other": 123, "read": 149},
            "timestamp": "2019-07-08T22:16:45+00:00",
            "throughput": {
                "total": 194141115,
                "write": 840226,
                "other": 193293789,
                "read": 7099,
            },
            "duration": "PT15S",
        },
        "uuid": "538bf337-1b2c-11e8-bad0-005056b48388",
        "statistics": {
            "status": "ok",
            "iops_raw": {
                "total": 3052032,
                "write": 1137230,
                "other": 1586535,
                "read": 328267,
            },
            "latency_raw": {
                "total": 844628724,
                "write": 313354426,
                "other": 477201985,
                "read": 54072313,
            },
            "throughput_raw": {
                "total": 213063348224,
                "write": 63771742208,
                "other": 146185560064,
                "read": 3106045952,
            },
            "timestamp": "2019-07-08T22:17:09+00:00",
        },
    }
)

```
</div>
</div>

For more information and examples on viewing historical performance metrics for any given aggregate, see [`DOC /storage/aggregates/{uuid}/metrics`](#docs-storage-storage_aggregates_{uuid}_metrics)
### Simulating aggregate expansion
The following example shows the response for a simulated data aggregate expansion based on the values of the 'block_storage.primary.disk_count' attribute passed in.
The query does not modify the existing aggregate but returns how the aggregate will look after the expansion along with any associated warnings.
Simulated data aggregate expansion will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
This will be reflected in the following attributes:

* space.block_storage.size - Total usable space in bytes, not including WAFL reserve and aggregate snapshot reserve.
* block_storage.primary.disk_count - Number of disks that could be used to create the aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.block_storage = {"primary": {"disk_count": 13}}
    resource.patch(hydrate=True, simulate=True)

```

### Manual aggregate expansion with disk size query
The following example shows the response for aggregate expansion based on the values of the 'block_storage.hybrid_cache.disk_count' attribute based on the disk size passed in.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.block_storage = {"hybrid_cache": {"disk_count": 4}}
    resource.patch(hydrate=True, disk_size=1902379008)

```

### Simulating a manual aggregate expansion with disk size query
The following example shows the response for a manual aggregate expansion based on the values of the 'block_storage.hybrid_cache.disk_count' attribute based on the disk size passed in.
The query internally maps out the appropriate expansion as well as warnings that may be associated for the hybrid enabled aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.block_storage = {"hybrid_cache": {"disk_count": 4}}
    resource.patch(hydrate=True, simulate=True, disk_size=1902379008)

```

### Simulating a manual aggregate expansion with raid group query
The following example shows the response for a manual aggregate expansion based on the values of the 'block_storage.primary.disk_count' attribute passed in.
The query internally maps out the appropriate expansion as well as warnings that may be associated and lays out the new raidgroups in a more detailed view. An additional query can be passed in to specify
raidgroup addition by new raidgroup, all raidgroups or a specific raidgroup.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.block_storage = {"primary": {"disk_count": 24}}
    resource.patch(hydrate=True, simulate=True, raid_group="new")

```

### Retrieving the usable spare information for the cluster
The following example shows the response from retrieving usable spare information for the expansion of this particular aggregate. The output is restricted to only spares that are compatible with this aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Aggregate.get_collection(
                uuid="cae60cfe-deae-42bd-babb-ef437d118314", show_spares=True
            )
        )
    )

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
[]

```
</div>
</div>

### Retrieving the SSD spare count for the cluster
The following example shows the response from retrieving SSD spare count information for the expansion of this particular aggregate's hybrid cache tier. The output is restricted to only spares that are compatible with this aggregate.
```
# The API:
/api/storage/aggregates?show_spares=true&uuid={uuid}&flash_pool_eligible=true
# The response:
{
  "records": [],
  "num_records": 0,
  "spares": [
    {
      "node": {
        "uuid": "c35c5975-cbcb-11ec-a3e1-005056bbdb46",
        "name": "node-2"
      },
      "disk_class": "solid_state",
      "disk_type": "ssd",
      "size": 1902379008,
      "checksum_style": "block",
      "syncmirror_pool": "pool0",
      "is_partition": false,
      "usable": 1,
      "layout_requirements": [
        {
          "raid_type": "raid4",
          "default": true,
          "aggregate_min_disks": 2,
          "raid_group": {
            "min": 2,
            "max": 14,
            "default": 8
          }
        }
      ]
    }
  ]
}
```
### Retrieving a recommendation for an aggregate expansion
The following example shows the response with the recommended data aggregate expansion based on what disks are present within the system.
The query does not modify the existing aggregate but returns how the aggregate will look after the expansion. The recommendation will be reflected in the attributes - 'space.block_storage.size' and 'block_storage.primary.disk_count'.
Recommended data aggregate expansion will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.get(auto_provision_policy="expand")
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
Aggregate(
    {
        "name": "node_2_SSD_1",
        "block_storage": {
            "mirror": {"enabled": False},
            "primary": {
                "raid_type": "raid_dp",
                "simulated_raid_groups": [
                    {
                        "is_partition": False,
                        "data_disk_count": 10,
                        "name": "test/plex0/rg0",
                        "usable_size": 12309487,
                        "parity_disk_count": 2,
                    }
                ],
                "disk_class": "solid_state",
                "disk_count": 12,
                "raid_size": 24,
                "disk_type": "ssd",
            },
            "hybrid_cache": {"enabled": False},
        },
        "node": {"name": "node-2", "uuid": "4046dda8-f802-11e8-8f6d-005056bb2030"},
        "uuid": "cae60cfe-deae-42bd-babb-ef437d118314",
        "space": {"block_storage": {"size": 1116180480}},
    }
)

```
</div>
</div>

### Updating an aggregate in the cluster
The following example shows the workflow of adding disks to the aggregate.<br>
Step 1: Check the current disk count on the aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.get(fields="block_storage.primary.disk_count")
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
Aggregate(
    {
        "name": "test1",
        "block_storage": {"primary": {"disk_count": 6}},
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
    }
)

```
</div>
</div>

Step 2: Update the aggregate with the new disk count in 'block_storage.primary.disk_count'. The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.block_storage = {"primary": {"disk_count": 8}}
    resource.patch()

```

Step 3: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.get(fields="block_storage.primary.disk_count")
    print(resource)

```
<div class="try_it_out">
<input id="example10_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example10_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example10_result" class="try_it_out_content">
```
Aggregate(
    {
        "name": "test1",
        "block_storage": {"primary": {"disk_count": 8}},
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
    }
)

```
</div>
</div>

### Adding a storage pool to an aggregate
The following example shows how to add cache capacity from an existing storage pool to an aggregate.
Step 1: Update the aggregate with the new storage pool allocation unit in 'block_storage.hybrid_cache.storage_pools.allocation_units_count'.
Additionally, specify 'block_storage.hybrid_cache.storage_pools.name' or 'block_storage.hybrid_cache.storage_pools.uuid' to the storage pool.
On the first storage pool, 'block_storage.hybrid_cache.raid_type' can be specified for the raidtype of the hybrid cache.
The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.block_storage = {
        "hybrid_cache": {
            "raid_type": "raid_dp",
            "storage_pools": [
                {"allocation_units_count": 2, "storage_pool": {"name": "sp1"}}
            ],
        }
    }
    resource.patch()

```

Step 2: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.get(fields="block_storage.hybrid_cache")
    print(resource)

```
<div class="try_it_out">
<input id="example12_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example12_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example12_result" class="try_it_out_content">
```
Aggregate({"name": "test1", "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c"})

```
</div>
</div>

### Adding physical SSD cache capacity to an aggregate
The following example shows how to add physical SSD cache capacity to an aggregate.
Step 1: Specify the number of disks to be added to cache in 'block_storage.hybrid_cache.disk_count'.
'block_storage.hybrid_cache.raid_type' can be specified for the RAID type of the hybrid cache.
'block_storage.hybrid_cache.raid_size' can be specified for the RAID size of the hybrid cache.
The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="caa8a9f1-0219-4eaf-bcad-e29c05042fe1")
    resource.block_storage.hybrid_cache.disk_count = 3
    resource.block_storage.hybrid_cache.raid_type = "raid4"
    resource.patch()

```

Step 2: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="caa8a9f1-0219-4eaf-bcad-e29c05042fe1")
    resource.get(fields="block_storage.hybrid_cache")
    print(resource)

```
<div class="try_it_out">
<input id="example14_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example14_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example14_result" class="try_it_out_content">
```
Aggregate({"name": "test1", "uuid": "caa8a9f1-0219-4eaf-bcad-e29c05042fe1"})

```
</div>
</div>

### Simulated addition of physical SSD cache capacity to an aggregate
The following example shows the response for a simulated addition of physical SSD cache capacity to an aggregate based on the values of the
'block_storage.hybrid_cache.disk_count', 'block_storage.hybrid_cache.raid_type' and 'block_storage.hybrid_cache.raid_size' attributes passed in.
The query does not modify the existing aggregate but returns how the aggregate will look after the expansion along with any associated warnings.
Simulated addition of physical SSD cache capacity to an aggregate will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
This will be reflected in the following attributes:

* block_storage.hybrid_cache.size - Total usable cache space in bytes, not including WAFL reserve and aggregate snapshot reserve.
* block_storage.hybrid_cache.disk_count - Number of disks that can be added to the aggregate's cache tier.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="7eb630d1-0e55-4cb6-8d90-957d6f4db54e")
    resource.block_storage.hybrid_cache.disk_count = 6
    resource.block_storage.hybrid_cache.raid_type = "raid4"
    resource.block_storage.hybrid_cache.raid_size = 3
    resource.patch(hydrate=True, simulate=True)

```

The following example shows the workflow to enable software encryption on an aggregate.<br>
Step 1: Check the current software encryption status of the aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.get(fields="data_encryption.software_encryption_enabled")
    print(resource)

```
<div class="try_it_out">
<input id="example16_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example16_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example16_result" class="try_it_out_content">
```
Aggregate(
    {
        "name": "aggr5",
        "data_encryption": {"software_encryption_enabled": False},
        "uuid": "f3aafdc6-be35-4d93-9590-5a402bffbe4b",
    }
)

```
</div>
</div>

Step 2: Update the aggregate with the encryption status in 'data_encryption.software_encryption_enabled'. The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.data_encryption = {"software_encryption_enabled": "true"}
    resource.patch()

```

Step 3: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.get(fields="data_encryption.software_encryption_enabled")
    print(resource)

```
<div class="try_it_out">
<input id="example18_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example18_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example18_result" class="try_it_out_content">
```
Aggregate(
    {
        "name": "aggr5",
        "data_encryption": {"software_encryption_enabled": True},
        "uuid": "f3aafdc6-be35-4d93-9590-5a402bffbe4b",
    }
)

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


__all__ = ["Aggregate", "AggregateSchema"]
__pdoc__ = {
    "AggregateSchema.resource": False,
    "AggregateSchema.opts": False,
}


class AggregateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Aggregate object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the aggregate."""

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="_tags", allow_none=True)
    r""" Tags are an optional way to track the uses of a resource. Tag values must be formatted as key:value strings.

Example: ["team:csi","environment:test"]"""

    block_storage = marshmallow_fields.Nested("netapp_ontap.models.aggregate_block_storage.AggregateBlockStorageSchema", data_key="block_storage", unknown=EXCLUDE, allow_none=True)
    r""" Configuration information for the locally attached portion of the aggregate. When a cloud store is also used by this aggregate, this is referred to as the performance tier."""

    cloud_storage = marshmallow_fields.Nested("netapp_ontap.models.aggregate_cloud_storage.AggregateCloudStorageSchema", data_key="cloud_storage", unknown=EXCLUDE, allow_none=True)
    r""" Configuration information for the cloud storage portion of the aggregate. This is referred to as the capacity tier."""

    create_time = marshmallow_fields.Str(
        data_key="create_time",
        allow_none=True,
    )
    r""" Timestamp of aggregate creation.

Example: 2018-01-01T16:00:00.000+0000"""

    data_encryption = marshmallow_fields.Nested("netapp_ontap.models.aggregate_data_encryption.AggregateDataEncryptionSchema", data_key="data_encryption", unknown=EXCLUDE, allow_none=True)
    r""" The data_encryption field of the aggregate."""

    dr_home_node = marshmallow_fields.Nested("netapp_ontap.models.dr_node.DrNodeSchema", data_key="dr_home_node", unknown=EXCLUDE, allow_none=True)
    r""" The dr_home_node field of the aggregate."""

    home_node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="home_node", unknown=EXCLUDE, allow_none=True)
    r""" The home_node field of the aggregate."""

    inactive_data_reporting = marshmallow_fields.Nested("netapp_ontap.models.aggregate_inactive_data_reporting.AggregateInactiveDataReportingSchema", data_key="inactive_data_reporting", unknown=EXCLUDE, allow_none=True)
    r""" The inactive_data_reporting field of the aggregate."""

    inode_attributes = marshmallow_fields.Nested("netapp_ontap.models.aggregate_inode_attributes.AggregateInodeAttributesSchema", data_key="inode_attributes", unknown=EXCLUDE, allow_none=True)
    r""" The inode_attributes field of the aggregate."""

    is_spare_low = marshmallow_fields.Boolean(
        data_key="is_spare_low",
        allow_none=True,
    )
    r""" Specifies whether the aggregate is in a spares low condition on any of the RAID groups.
This is an advanced property; there is an added computational cost to retrieving its value. The field is not populated for either a collection GET or an instance GET unless it is explicitly requested using the <i>fields</i> query parameter containing either footprint or **.


Example: false"""

    metric = marshmallow_fields.Nested("netapp_ontap.resources.performance_metric.PerformanceMetricSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Aggregate name.

Example: node1_aggr_1"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the aggregate."""

    sidl_enabled = marshmallow_fields.Boolean(
        data_key="sidl_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not SIDL is enabled on the aggregate."""

    snaplock_type = marshmallow_fields.Str(
        data_key="snaplock_type",
        validate=enum_validation(['non_snaplock', 'compliance', 'enterprise']),
        allow_none=True,
    )
    r""" SnapLock type.

Valid choices:

* non_snaplock
* compliance
* enterprise"""

    snapshot = marshmallow_fields.Nested("netapp_ontap.models.aggregate_snapshot.AggregateSnapshotSchema", data_key="snapshot", unknown=EXCLUDE, allow_none=True)
    r""" The snapshot field of the aggregate."""

    space = marshmallow_fields.Nested("netapp_ontap.models.aggregate_space.AggregateSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The space field of the aggregate."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['online', 'onlining', 'offline', 'offlining', 'relocating', 'unmounted', 'restricted', 'inconsistent', 'failed', 'unknown']),
        allow_none=True,
    )
    r""" Operational state of the aggregate.

Valid choices:

* online
* onlining
* offline
* offlining
* relocating
* unmounted
* restricted
* inconsistent
* failed
* unknown"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw.PerformanceMetricRawSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the aggregate."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Aggregate UUID."""

    volume_count = Size(
        data_key="volume-count",
        allow_none=True,
    )
    r""" Number of volumes in the aggregate."""

    @property
    def resource(self):
        return Aggregate

    gettable_fields = [
        "links",
        "tags",
        "block_storage",
        "cloud_storage",
        "create_time",
        "data_encryption",
        "dr_home_node.name",
        "dr_home_node.uuid",
        "home_node.links",
        "home_node.name",
        "home_node.uuid",
        "inactive_data_reporting",
        "inode_attributes",
        "is_spare_low",
        "metric",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "sidl_enabled",
        "snaplock_type",
        "snapshot",
        "space",
        "state",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "uuid",
        "volume_count",
    ]
    """links,tags,block_storage,cloud_storage,create_time,data_encryption,dr_home_node.name,dr_home_node.uuid,home_node.links,home_node.name,home_node.uuid,inactive_data_reporting,inode_attributes,is_spare_low,metric,name,node.links,node.name,node.uuid,sidl_enabled,snaplock_type,snapshot,space,state,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,uuid,volume_count,"""

    patchable_fields = [
        "tags",
        "block_storage",
        "cloud_storage",
        "data_encryption",
        "inactive_data_reporting",
        "name",
        "node.name",
        "node.uuid",
        "sidl_enabled",
        "state",
    ]
    """tags,block_storage,cloud_storage,data_encryption,inactive_data_reporting,name,node.name,node.uuid,sidl_enabled,state,"""

    postable_fields = [
        "tags",
        "block_storage",
        "data_encryption",
        "inactive_data_reporting",
        "name",
        "node.name",
        "node.uuid",
        "sidl_enabled",
        "snaplock_type",
        "state",
    ]
    """tags,block_storage,data_encryption,inactive_data_reporting,name,node.name,node.uuid,sidl_enabled,snaplock_type,state,"""

class Aggregate(Resource):
    """Allows interaction with Aggregate objects on the host"""

    _schema = AggregateSchema
    _path = "/api/storage/aggregates"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of aggregates for the entire cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `metric.*`
* `space.block_storage.inactive_user_data`
* `space.block_storage.inactive_user_data_percent`
* `space.footprint`
* `is_spare_low`
* `statistics.*`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Aggregate resources that match the provided query"""
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
        """Returns a list of RawResources that represent Aggregate resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Aggregate"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the aggregate specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Platform Specifics
* **ASA r2**: PATCH is not supported.
### Related ONTAP commands
* `storage aggregate add-disks`
* `storage aggregate mirror`
* `storage aggregate modify`
* `storage aggregate relocation start`
* `storage aggregate rename`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Aggregate"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Aggregate"], NetAppResponse]:
        r"""Automatically creates aggregates based on an optimal layout recommended by the system. Alternatively, properties can be provided to create an aggregate according to the requested specification. This request starts a job and returns a link to that job.
POST operations will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Required properties
Properties are not required for this API. The following properties are only required if you want to specify properties for aggregate creation:
* `name` - Name of the aggregate.
* `node.name` or `node.uuid` - Node on which the aggregate will be created.
* `block_storage.primary.disk_count` - Number of disks to be used to create the aggregate.
### Default values
If not specified in POST, the following default values are assigned. The remaining unspecified properties will receive system dependent default values.
* `block_storage.mirror.enabled` - _false_
* `snaplock_type` - _non_snaplock_
### Related ONTAP commands
* `storage aggregate auto-provision`
* `storage aggregate create`
### Example:
```
POST /api/storage/aggregates {"node": {"name": "node1"}, "name": "test", "block_storage": {"primary": {"disk_count": "10"}}}
```

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Aggregate"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the aggregate specified by the UUID. This request starts a job and returns a link to that job.
### Platform Specifics
* **ASA r2**: DELETE is not supported.
### Related ONTAP commands
* `storage aggregate delete`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of aggregates for the entire cluster.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `metric.*`
* `space.block_storage.inactive_user_data`
* `space.block_storage.inactive_user_data_percent`
* `space.footprint`
* `is_spare_low`
* `statistics.*`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the aggregate specified by the UUID. The recommend query cannot be used for this operation.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `metric.*`
* `space.block_storage.inactive_user_data`
* `space.block_storage.inactive_user_data_percent`
* `space.footprint`
* `is_spare_low`
* `statistics.*`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
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
        r"""Automatically creates aggregates based on an optimal layout recommended by the system. Alternatively, properties can be provided to create an aggregate according to the requested specification. This request starts a job and returns a link to that job.
POST operations will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
### Platform Specifics
* **ASA r2**: POST is not supported.
### Required properties
Properties are not required for this API. The following properties are only required if you want to specify properties for aggregate creation:
* `name` - Name of the aggregate.
* `node.name` or `node.uuid` - Node on which the aggregate will be created.
* `block_storage.primary.disk_count` - Number of disks to be used to create the aggregate.
### Default values
If not specified in POST, the following default values are assigned. The remaining unspecified properties will receive system dependent default values.
* `block_storage.mirror.enabled` - _false_
* `snaplock_type` - _non_snaplock_
### Related ONTAP commands
* `storage aggregate auto-provision`
* `storage aggregate create`
### Example:
```
POST /api/storage/aggregates {"node": {"name": "node1"}, "name": "test", "block_storage": {"primary": {"disk_count": "10"}}}
```

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
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
        r"""Updates the aggregate specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Platform Specifics
* **ASA r2**: PATCH is not supported.
### Related ONTAP commands
* `storage aggregate add-disks`
* `storage aggregate mirror`
* `storage aggregate modify`
* `storage aggregate relocation start`
* `storage aggregate rename`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
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
        r"""Deletes the aggregate specified by the UUID. This request starts a job and returns a link to that job.
### Platform Specifics
* **ASA r2**: DELETE is not supported.
### Related ONTAP commands
* `storage aggregate delete`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


