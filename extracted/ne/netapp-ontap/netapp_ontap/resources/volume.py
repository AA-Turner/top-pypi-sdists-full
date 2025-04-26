r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
FlexVol volumes are logical containers used by ONTAP to serve data to clients.  They contain file systems in a NAS environment and LUNs in a SAN environment.<br/>
A FlexGroup volume is a scale-out NAS container that provides high performance along with automatic load distribution and scalability. A FlexGroup volume contains several constituents that automatically and transparently share the traffic.</br>
FlexClone volumes are writable, point-in-time copies of a FlexVol volume. At this time, FlexClones of FlexGroups are not supported.<br/>
Volumes with SnapLock type Compliance or Enterprise, are referred to as SnapLock volumes. It is possible to create a SnapLock volume by specifying SnapLock parameters.<br/>
ONTAP storage APIs allow you to create, modify, and monitor volumes and aggregates.<br/>
## Storage efficiency
Storage efficiency is used to remove duplicate blocks in the data and to compress the data. Efficiency has deduplication, compression, cross volume deduplication, compaction, policy-name, enabled, application_io_size, compression_type and storage_efficiency_mode options. On All Flash systems, all efficiencies are enabled by default, on volume creation. Options such as "background/inline/both" are treated as both, which means both background and inline are enabled for any efficiency option. The option "none"  disables both background and inline efficiency. Application-io-size and compression-type decides type of compression behavior in the system. Storage efficiency mode decides if the system is to run in default/efficient mode. Detailed information about each field is available under efficiency object for storage efficiency fields.<br/>
To enable any efficiency option on all-flash or FAS systems, background deduplication is always enabled.<br/>
## Quotas
Quotas provide a way to restrict or track the files and space usage by a user, group, or qtree. Quotas are enabled for a specific FlexVol or a FlexGroup volume.<br/>
The following APIs can be used to enable or disable and obtain quota state for a FlexVol or a FlexGroup volume:

* PATCH  /api/storage/volumes/{uuid} -d '{"quota.enabled":"true"}'
* PATCH  /api/storage/volumes/{uuid} -d '{"quota.enabled":"false"}'
* GET    /api/storage/volumes/{uuid}/?fields=quota.state
## File System Analytics
File system analytics (FSA) provide a quick method for obtaining information summarizing properties of all files within any directory tree of a volume. For more information on FSA, see [`DOC /storage/volumes{volume.uuid}/files/{path}`](#docs-storage-storage_volumes_{volume.uuid}_files_{path}). Analytics can be enabled or disabled on individual volumes.<br/>
The following APIs can be used to enable or disable and obtain analytics state for a FlexVol volume or a FlexGroup volume:

* PATCH  /api/storage/volumes/{uuid} -d '{"analytics.state":"on"}'
* PATCH  /api/storage/volumes/{uuid} -d '{"analytics.state":"off"}'
* GET    /api/storage/volumes/{uuid}/?fields=analytics<br/>
If the `analytics.state` field is "initializing" or "initialization_paused" and is set to "off", the FSA initialization scan is cancelled. If FSA is turned on again, the initialization scan restarts.<br/>
## QoS
QoS policy and settings enforce Service Level Objectives (SLO) on a volume. SLO can be set by specifying qos.max_throughput_iops and/or qos.max_throughput_mbps or qos.min_throughput_iops and/or qos.min_throughput_mbps. Specifying min_throughput_iops or min_throughput_mbps is only supported on volumes hosted on a node that is flash optimized. A pre-created QoS policy can also be used by specifying qos.name or qos.uuid property. <br/>
## Performance monitoring
Performance of a volume can be monitored by the `metric.*` and `statistics.*` fields. These show the performance of the volume in terms of IOPS, latency and throughput. The `metric.*` fields denote an average whereas `statistics.*` fields denote a real-time monotonically increasing value aggregated across all nodes. <br/>
## Rebalancing
Non-disruptive capacity rebalancing of a FlexGroup volume is configured by the `rebalancing.*` fields. If not explicitly set, default values are provided. To initiate a capacity rebalancing operation, `rebalancing.state` is set to 'starting'. The `rebalancing.max_runtime` can be optionally set, which is the maximum length of time you want the capacity rebalancing to run for. You can stop capacity rebalancing by setting `rebalancing.state` to 'stopping'. You can also modify the configurations `rebalancing.max_runtime`, `rebalancing.max_threshold`, `rebalancing.min_threshold`, `rebalancing.max_file_moves`, `rebalancing.min_file_size`, and `rebalancing.exclude_snapshots`. When a new capacity rebalancing operation is started on a FlexGroup volume, it uses the current configuration values. Once the operation is started, changes to the configuration are not allowed, until the capacity rebalanding operations stops, either by exceeding their maximum runtime or by being stopped. To see runtime information about each constituent, for a running rebalancing operation, use the 'rebalancing.engine.*' fields.<br/>
## Volume APIs
The following APIs are used to perform operations related with FlexVol volumes and FlexGroup volumes:

* POST      /api/storage/volumes
* GET       /api/storage/volumes
* GET       /api/storage/volumes/{uuid}
* PATCH     /api/storage/volumes/{uuid}
* DELETE    /api/storage/volumes/{uuid}
## Examples
### Creating a volume
The POST request is used to create a new volume and to specify its properties.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume()
    resource.name = "vol1"
    resource.aggregates = [{"name": "aggr1"}]
    resource.svm = {"name": "vs1"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Volume({"name": "vol1", "svm": {"name": "vs1"}, "aggregates": [{"name": "aggr1"}]})

```
</div>
</div>

### Creating a SnapLock volume and specifying its properties using POST
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume()
    resource.name = "vol1"
    resource.aggregates = [{"name": "aggr1"}]
    resource.svm = {"name": "vs1"}
    resource.snaplock = {"retention": {"default": "P20Y"}, "type": "compliance"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Volume(
    {
        "name": "vol1",
        "svm": {"name": "vs1"},
        "aggregates": [{"name": "aggr1"}],
        "snaplock": {"type": "compliance", "retention": {"default": "P20Y"}},
    }
)

```
</div>
</div>

### Creating a FlexGroup volume and specifying its properties using POST
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume()
    resource.name = "vol1"
    resource.state = "online"
    resource.type = "RW"
    resource.aggregates = [{"name": "aggr1"}, {"name": "aggr2"}, {"name": "aggr3"}]
    resource.constituents_per_aggregate = "1"
    resource.svm = {"name": "vs1"}
    resource.size = "240MB"
    resource.encryption = {"enabled": "False"}
    resource.efficiency = {"compression": "both"}
    resource.autosize = {"maximum": "500MB", "minimum": "240MB"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Volume(
    {
        "efficiency": {"compression": "both"},
        "name": "vol1",
        "svm": {"name": "vs1"},
        "aggregates": [{"name": "aggr1"}, {"name": "aggr2"}, {"name": "aggr3"}],
        "type": "RW",
        "constituents_per_aggregate": 1,
        "autosize": {"minimum": 251658240, "maximum": 524288000},
        "state": "online",
        "size": 251658240,
        "encryption": {"enabled": False},
    }
)

```
</div>
</div>

### Creating a FlexGroup volume and specifying its properties using POST when the Performance_NAS license is installed.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume()
    resource.name = "vol1"
    resource.state = "online"
    resource.type = "RW"
    resource.svm = {"name": "vs1"}
    resource.size = "240TB"
    resource.encryption = {"enabled": "False"}
    resource.efficiency = {"compression": "both"}
    resource.autosize = {"maximum": "500TB", "minimum": "240TB"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Volume(
    {
        "efficiency": {"compression": "both"},
        "name": "vol1",
        "svm": {"name": "vs1"},
        "type": "RW",
        "autosize": {"minimum": 263882790666240, "maximum": 549755813888000},
        "state": "online",
        "size": 263882790666240,
        "encryption": {"enabled": False},
    }
)

```
</div>
</div>

### Creating a FlexClone and specifying its properties using POST
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume()
    resource.name = "vol1_clone"
    resource.clone = {"parent_volume": {"name": "vol1"}, "is_flexclone": "true"}
    resource.svm = {"name": "vs0"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
Volume(
    {
        "name": "vol1_clone",
        "svm": {"name": "vs0"},
        "clone": {"is_flexclone": True, "parent_volume": {"name": "vol1"}},
    }
)

```
</div>
</div>

## Volumes reported in the GET REST API
### The following types of volumes are reported:

*  RW, DP and LS volumes
*  FlexGroup volume
*  FlexCache volume
*  FlexClone volume
*  FlexGroup constituent
<br/>
### The following volumes are not reported:

*  DEL and TMP type volume
*  Node Root volume
*  System Vserver volume
*  FlexCache constituent
## Examples
### Retrieving the list of volumes
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Volume.get_collection()))

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    Volume(
        {
            "name": "vsdata_root",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/2d1167cc-c3f2-495a-a23f-8f50b071b9b8"
                }
            },
            "uuid": "2d1167cc-c3f2-495a-a23f-8f50b071b9b8",
        }
    ),
    Volume(
        {
            "name": "vsfg_root",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/3969be7e-78b4-4b4c-82a4-fa86331f03df"
                }
            },
            "uuid": "3969be7e-78b4-4b4c-82a4-fa86331f03df",
        }
    ),
    Volume(
        {
            "name": "svm_root",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/59c03ac5-e708-4ce8-a676-278dc249fda2"
                }
            },
            "uuid": "59c03ac5-e708-4ce8-a676-278dc249fda2",
        }
    ),
    Volume(
        {
            "name": "fgvol",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/6802635b-8036-11e8-aae5-0050569503ac"
                }
            },
            "uuid": "6802635b-8036-11e8-aae5-0050569503ac",
        }
    ),
    Volume(
        {
            "name": "datavol",
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/d0c3359c-5448-4a9b-a077-e3295a7e9057"
                }
            },
            "uuid": "d0c3359c-5448-4a9b-a077-e3295a7e9057",
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of a volume
The GET request is used to retrieve the attributes of a volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Volume(
    {
        "name": "datavol",
        "svm": {"name": "vsdata", "uuid": "d61b69f5-7458-11e8-ad3f-0050569503ac"},
        "aggregates": [
            {
                "name": "data",
                "_links": {"self": {"href": "/api/cluster/aggregates/data"}},
                "uuid": "aa742322-36bc-4d98-bbc4-0a827534c035",
            }
        ],
        "language": "en_us",
        "metric": {
            "status": "ok",
            "iops": {"total": 0, "write": 0, "other": 0, "read": 0},
            "latency": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:15+00:00",
            "throughput": {"total": 0, "write": 0, "other": 0, "read": 0},
            "flexcache": {
                "status": "ok",
                "bandwidth_savings": 0,
                "cache_miss_percent": 0,
                "timestamp": "2019-04-09T05:50:15+00:00",
                "duration": "PT1D",
            },
            "duration": "PT15S",
            "cloud": {
                "status": "ok",
                "iops": {"total": 0, "write": 0, "other": 0, "read": 0},
                "latency": {"total": 0, "write": 0, "other": 0, "read": 0},
                "timestamp": "2019-04-09T05:50:15+00:00",
                "duration": "PT15S",
            },
        },
        "type": "rw",
        "nas": {
            "junction_parent": {
                "name": "vol1",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/a2564f80-25fb-41e8-9b49-44de2600991f"
                    }
                },
                "uuid": "a2564f80-25fb-41e8-9b49-44de2600991f",
            },
            "export_policy": {"name": "default", "id": 8589934593},
            "uid": 1357,
            "gid": 2468,
            "security_style": "unix",
            "unix_permissions": 4755,
        },
        "qos": {
            "policy": {"name": "pg1", "uuid": "228454af-5a8b-11e9-bd5b-005056ac6f1f"}
        },
        "uuid": "d0c3359c-5448-4a9b-a077-e3295a7e9057",
        "create_time": "2018-07-05T14:56:44+05:30",
        "statistics": {
            "status": "ok",
            "iops_raw": {"total": 3, "write": 0, "other": 3, "read": 0},
            "latency_raw": {"total": 38298, "write": 0, "other": 38298, "read": 0},
            "flexcache_raw": {
                "status": "ok",
                "client_requested_blocks": 0,
                "cache_miss_blocks": 0,
                "timestamp": "2019-04-09T05:50:15+00:00",
            },
            "throughput_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:42+00:00",
            "cloud": {
                "status": "ok",
                "iops_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
                "latency_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
                "timestamp": "2019-04-09T05:50:42+00:00",
            },
        },
        "comment": "This is a data volume",
        "state": "online",
        "snaplock": {
            "expiry_time": "2038-01-19T08:44:28+05:30",
            "is_audit_log": False,
            "compliance_clock_time": "2019-05-24T10:59:00+05:30",
            "type": "enterprise",
            "privileged_delete": "disabled",
            "append_mode_enabled": False,
            "retention": {"minimum": "P0Y", "default": "P0Y", "maximum": "P30Y"},
            "litigation_count": 0,
            "autocommit_period": "none",
        },
        "snapshot_policy": {"name": "default"},
        "size": 20971520,
        "files": {"used": 96, "maximum": 566},
        "style": "flexvol",
        "encryption": {"state": "none", "enabled": False, "type": "none", "key_id": ""},
        "error_state": {"is_inconsistent": False, "has_bad_blocks": False},
    }
)

```
</div>
</div>

### Retrieving the quota state of a FlexVol or a FlexGroup volume
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="cb20da45-4f6b-11e9-9a71-005056a7f717")
    resource.get(fields="quota.state")
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
Volume(
    {
        "name": "fv",
        "_links": {
            "self": {
                "href": "/api/storage/volumes/cb20da45-4f6b-11e9-9a71-005056a7f717/"
            }
        },
        "uuid": "cb20da45-4f6b-11e9-9a71-005056a7f717",
        "quota": {"state": "on"},
    }
)

```
</div>
</div>

### Retrieving the constituents of a FlexGroup volume
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Volume.get_collection(
                is_constituent=True,
                **{"flexgroup.uuid": "fd87d06f-8876-11ec-94a3-005056a7484f"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
[
    Volume(
        {
            "name": "fg__0001",
            "flexgroup": {"uuid": "fd87d06f-8876-11ec-94a3-005056a7484f"},
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/fd877f7c-8876-11ec-94a3-005056a7484f?is_constituent=true"
                }
            },
            "uuid": "fd877f7c-8876-11ec-94a3-005056a7484f",
        }
    ),
    Volume(
        {
            "name": "fg__0002",
            "flexgroup": {"uuid": "fd87d06f-8876-11ec-94a3-005056a7484f"},
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/fea631d6-8876-11ec-94a3-005056a7484f?is_constituent=true"
                }
            },
            "uuid": "fea631d6-8876-11ec-94a3-005056a7484f",
        }
    ),
    Volume(
        {
            "name": "fg__0003",
            "flexgroup": {"uuid": "fd87d06f-8876-11ec-94a3-005056a7484f"},
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/ff38a34e-8876-11ec-94a3-005056a7484f?is_constituent=true"
                }
            },
            "uuid": "ff38a34e-8876-11ec-94a3-005056a7484f",
        }
    ),
    Volume(
        {
            "name": "fg__0004",
            "flexgroup": {"uuid": "fd87d06f-8876-11ec-94a3-005056a7484f"},
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/ffdbbd1f-8876-11ec-94a3-005056a7484f?is_constituent=true"
                }
            },
            "uuid": "ffdbbd1f-8876-11ec-94a3-005056a7484f",
        }
    ),
]

```
</div>
</div>

### Retrieving the efficiency attributes of volume
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="5f098ebc-32c8-11eb-8dde-005056ace228")
    resource.get(fields="efficiency")
    print(resource)

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
Volume(
    {
        "efficiency": {
            "dedupe": "background",
            "progress": "Idle for 00:10:37",
            "compaction": "none",
            "schedule": "sun-sat@0",
            "compression": "both",
            "policy": {"name": "-"},
            "last_op_state": "Success",
            "state": "enabled",
            "last_op_size": 0,
            "cross_volume_dedupe": "none",
            "type": "regular",
        },
        "name": "vol1",
        "_links": {
            "self": {
                "href": "/api/storage/volumes/5f098ebc-32c8-11eb-8dde-005056ace228"
            }
        },
        "uuid": "5f098ebc-32c8-11eb-8dde-005056ace228",
    }
)

```
</div>
</div>

## Updating the attributes of a volume
## Examples
### Updating the attributes of a volume
The PATCH request is used to update the attributes of a volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.size = 26214400
    resource.nas = {"security_style": "mixed"}
    resource.comment = "This is a data volume"
    resource.patch()

```

### Updating the attributes of a FlexClone using PATCH
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.clone = {"split_initiated": "true"}
    resource.patch()

```

### Stopping a volume clone split operation on a FlexClone using PATCH.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.clone = {"split_initiated": "false"}
    resource.patch()

```

### Enabling quotas for a FlexVol or a FlexGroup volume using PATCH
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.quota = {"enabled": "true"}
    resource.patch()

```

### Disabling quotas for a FlexVol or a FlexGroup volume using PATCH
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.quota = {"enabled": "false"}
    resource.patch()

```

### Starting non-disruptive volume capacity rebalancing for a FlexGroup volume using PATCH
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.rebalancing = {"state": "starting", "max_runtime": "PT6H"}
    resource.patch()

```

### Starting a scheduled non-disruptive volume capacity rebalancing for a FlexGroup volume using PATCH
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.rebalancing = {
        "state": "starting",
        "start_time": "2022-12-21T15:30:00-05:00",
    }
    resource.patch()

```

### Stopping non-disruptive volume capacity rebalancing OR scheduled rebalancing for a FlexGroup volume using PATCH. This works for scheduled or on-going rebalancing.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.rebalancing = {"state": "stopping"}
    resource.patch()

```

### Modifying non-disruptive volume capacity rebalancing configurations for a FlexGroup volume
The following example shows how to use a PATCH request to modify non-disruptive volume capacity rebalancing configurations for a FlexGroup volume:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.rebalancing = {
        "start_time": "2023-03-18T15:30:00-05:00",
        "max_threshold": 20,
        "min_threshold": 5,
        "max_file_moves": 15,
        "min_file_size": "100MB",
        "exclude_snapshots": "false",
        "max_runtime": "PT6H",
    }
    resource.patch()

```

### Retrieving non-disruptive volume capacity rebalancing engine runtime information for a FlexGroup volume
The following example shows how to use a GET request to retrieve non-disruptive volume capacity rebalancing engine runtime information for a FlexGroup volume:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Volume.get_collection(
                fields="rebalancing.engine",
                is_constituent=True,
                **{"flexgroup.uuid": "d0c3359c-5448-4a9b-a077-e3295a7e9057"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example19_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example19_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example19_result" class="try_it_out_content">
```
[
    Volume(
        {
            "name": "fg__0001",
            "flexgroup": {"uuid": "2b3323db-b916-11ec-b103-005056a79638"},
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/2b32fdf1-b916-11ec-b103-005056a79638?is_constituent=true"
                }
            },
            "uuid": "2b32fdf1-b916-11ec-b103-005056a79638",
            "rebalancing": {
                "engine": {
                    "scanner": {
                        "files_skipped": {
                            "too_large": 199,
                            "metadata": 85449,
                            "other": 336,
                            "incompatible": 9377,
                            "too_small": 3812,
                            "in_snapshot": 77499,
                            "efficiency_percent": 355,
                            "write_fenced": 28,
                            "footprint_invalid": 12,
                            "fast_truncate": 22,
                            "efficiency_blocks": 1823,
                            "remote_cache": 1912,
                            "on_demand_destination": 87,
                        },
                        "blocks_skipped": {
                            "too_large": 865000,
                            "metadata": 85673000,
                            "other": 187000,
                            "incompatible": 2287000,
                            "too_small": 8744000,
                            "in_snapshot": 7749000,
                            "efficiency_percent": 366000,
                            "write_fenced": 19000,
                            "footprint_invalid": 98000,
                            "fast_truncate": 54000,
                            "efficiency_blocks": 1472000,
                            "remote_cache": 9914000,
                            "on_demand_destination": 66000,
                        },
                        "blocks_scanned": 1542675000,
                        "files_scanned": 3522915,
                    },
                    "movement": {
                        "most_recent_start_time": "2022-02-15T12:56:07-05:00",
                        "last_error": {
                            "destination": 1089,
                            "file_id": 88,
                            "code": 60,
                            "time": "2022-02-15T09:09:27-05:00",
                        },
                        "file_moves_started": 9833,
                    },
                }
            },
        }
    ),
    Volume(
        {
            "name": "fg__0002",
            "flexgroup": {"uuid": "2b3323db-b916-11ec-b103-005056a79638"},
            "_links": {
                "self": {
                    "href": "/api/storage/volumes/2cc5da55-b916-11ec-b103-005056a79638?is_constituent=true"
                }
            },
            "uuid": "2cc5da55-b916-11ec-b103-005056a79638",
            "rebalancing": {
                "engine": {
                    "scanner": {
                        "files_skipped": {
                            "too_large": 188,
                            "metadata": 85449,
                            "other": 336,
                            "incompatible": 9377,
                            "too_small": 3812,
                            "in_snapshot": 77499,
                            "efficiency_percent": 355,
                            "write_fenced": 28,
                            "footprint_invalid": 12,
                            "fast_truncate": 25,
                            "efficiency_blocks": 1823,
                            "remote_cache": 1912,
                            "on_demand_destination": 87,
                        },
                        "blocks_skipped": {
                            "too_large": 865000,
                            "metadata": 85673000,
                            "other": 187000,
                            "incompatible": 2287000,
                            "too_small": 8744000,
                            "in_snapshot": 7749000,
                            "efficiency_percent": 366000,
                            "write_fenced": 19000,
                            "footprint_invalid": 98000,
                            "fast_truncate": 54000,
                            "efficiency_blocks": 1472000,
                            "remote_cache": 9914000,
                            "on_demand_destination": 66000,
                        },
                        "blocks_scanned": 1542675000,
                        "files_scanned": 3522915,
                    },
                    "movement": {
                        "most_recent_start_time": "2022-02-15T12:56:07-05:00",
                        "last_error": {
                            "destination": 1089,
                            "file_id": 88,
                            "code": 60,
                            "time": "2022-02-15T08:09:27-05:00",
                        },
                        "file_moves_started": 9833,
                    },
                }
            },
        }
    ),
]

```
</div>
</div>

## Add tiering object tags for a FlexVol volume
The following example shows how to use a PATCH request to add tiering object tags for a FlexVol volume:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.tiering.object_tags = ["key1=val1", "key2=val2"]
    resource.patch()

```

### Remove tiering object tags for a FlexVol using PATCH
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="d0c3359c-5448-4a9b-a077-e3295a7e9057")
    resource.tiering.object_tags = []
    resource.patch()

```

## Deleting a volume
## Example
### Deleting a volume
The DELETE request is used to delete a volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="{uuid}")
    resource.delete()

```

### Deleting a volume and bypassing the recovery queue
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Volume(uuid="{uuid}")
    resource.delete(force=True)

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


__all__ = ["Volume", "VolumeSchema"]
__pdoc__ = {
    "VolumeSchema.resource": False,
    "VolumeSchema.opts": False,
}


class VolumeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Volume object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the volume."""

    tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="_tags", allow_none=True)
    r""" Tags are an optional way to track the uses of a resource. Tag values must be formatted as key:value strings.

Example: ["team:csi","environment:test"]"""

    access_time_enabled = marshmallow_fields.Boolean(
        data_key="access_time_enabled",
        allow_none=True,
    )
    r""" Indicates whether or not access time updates are enabled on the volume."""

    activity_tracking = marshmallow_fields.Nested("netapp_ontap.models.volume_activity_tracking.VolumeActivityTrackingSchema", data_key="activity_tracking", unknown=EXCLUDE, allow_none=True)
    r""" The activity_tracking field of the volume."""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.svm_migration_volume_placement_aggregates.SvmMigrationVolumePlacementAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" Aggregate hosting the volume. Required on POST."""

    aggressive_readahead_mode = marshmallow_fields.Str(
        data_key="aggressive_readahead_mode",
        validate=enum_validation(['none', 'file_prefetch', 'sequential_read', 'cross_file_sequential_read']),
        allow_none=True,
    )
    r""" Specifies the `aggressive_readahead_mode` enabled on the volume. When set to _file_prefetch_, on a file read, the system aggressively issues readaheads for all of the blocks in the file and retains those blocks in a cache for a finite period of time. When the option is set to _sequential_read_, the system aggressively prefetches the file completely, or to a certain length based on the file size limit, and continues as the read makes progress. If the option is set to _cross_file_sequential_read_, then the system aggressively prefetches multiple files completely, or to a certain length, and continues as the read makes progress.

Valid choices:

* none
* file_prefetch
* sequential_read
* cross_file_sequential_read"""

    analytics = marshmallow_fields.Nested("netapp_ontap.models.volume_analytics.VolumeAnalyticsSchema", data_key="analytics", unknown=EXCLUDE, allow_none=True)
    r""" The analytics field of the volume."""

    anti_ransomware = marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_volume.AntiRansomwareVolumeSchema", data_key="anti_ransomware", unknown=EXCLUDE, allow_none=True)
    r""" Anti-ransomware properties of volumes."""

    application = marshmallow_fields.Nested("netapp_ontap.models.volume_application.VolumeApplicationSchema", data_key="application", unknown=EXCLUDE, allow_none=True)
    r""" The application field of the volume."""

    asynchronous_directory_delete = marshmallow_fields.Nested("netapp_ontap.models.volume_asynchronous_directory_delete.VolumeAsynchronousDirectoryDeleteSchema", data_key="asynchronous_directory_delete", unknown=EXCLUDE, allow_none=True)
    r""" Configuration for asynchronous directory delete from the client. This is only supported on Flexible volumes and FlexGroup volumes."""

    autosize = marshmallow_fields.Nested("netapp_ontap.models.volume_autosize.VolumeAutosizeSchema", data_key="autosize", unknown=EXCLUDE, allow_none=True)
    r""" The autosize field of the volume."""

    clone = marshmallow_fields.Nested("netapp_ontap.models.volume_clone.VolumeCloneSchema", data_key="clone", unknown=EXCLUDE, allow_none=True)
    r""" The clone field of the volume."""

    cloud_retrieval_policy = marshmallow_fields.Str(
        data_key="cloud_retrieval_policy",
        validate=enum_validation(['default', 'on_read', 'never', 'promote']),
        allow_none=True,
    )
    r""" This parameter specifies the cloud retrieval policy for the volume. This policy determines which tiered out blocks to retrieve from the capacity tier to the performance tier. The available cloud retrieval policies are
"default" policy retrieves tiered data based on the underlying tiering policy. If the tiering policy is 'auto', tiered data is retrieved only for random client driven data reads. If the tiering policy is 'none' or 'snapshot_only', tiered data is retrieved for random and sequential client driven data reads. If the tiering policy is 'all', tiered data is not retrieved.
"on_read" policy retrieves tiered data for all client driven data reads.
"never" policy never retrieves tiered data.
"promote" policy retrieves all eligible tiered data automatically during the next scheduled scan. It is only supported when the tiering policy is 'none' or 'snapshot_only'. If the tiering policy is 'snapshot_only', the only data brought back is the data in the AFS. Data that is only in a snapshot copy stays in the cloud and if tiering policy is 'none' then all data is retrieved.


Valid choices:

* default
* on_read
* never
* promote"""

    cloud_write_enabled = marshmallow_fields.Boolean(
        data_key="cloud_write_enabled",
        allow_none=True,
    )
    r""" Indicates whether or not cloud writes are enabled on the volume. NFS writes to this volume are sent to the cloud directly instead of the local performance tier.
This feature is only available on volumes in FabricPools."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=1023),
        allow_none=True,
    )
    r""" A comment for the volume. Valid in POST or PATCH."""

    consistency_group = marshmallow_fields.Nested("netapp_ontap.models.volume_consistency_group.VolumeConsistencyGroupSchema", data_key="consistency_group", unknown=EXCLUDE, allow_none=True)
    r""" Consistency group the volume is part of."""

    constituents = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.volume_constituents.VolumeConstituentsSchema", unknown=EXCLUDE, allow_none=True), data_key="constituents", allow_none=True)
    r""" FlexGroup volume constituents. FlexGroup volume constituents can be retrieved more efficiently by specifying "is_constituent=true" or "is_constituent=true&flexgroup.uuid=<flexgroup.uuid>" as query parameters."""

    constituents_per_aggregate = Size(
        data_key="constituents_per_aggregate",
        validate=integer_validation(minimum=1, maximum=1000),
        allow_none=True,
    )
    r""" Specifies the number of times to iterate over the aggregates listed with the "aggregates.name" or "aggregates.uuid" when creating or expanding a FlexGroup volume. If a volume is being created on a single aggregate, the system creates a flexible volume if the "constituents_per_aggregate" field is not specified, or a FlexGroup volume if it is specified. If a volume is being created on multiple aggregates, the system always creates a FlexGroup volume. If a volume is being created on multiple aggregates and the "constituents_per_aggregate" field is not specified, the default value of the "constituents_per_aggregate" field is 4. The root constituent of a FlexGroup volume is always placed on the first aggregate in the list, unless 'optimize_aggregates' is specified as 'true'. If the "aggregates.name" or "aggregates.uuid" is specified in a PATCH request to expand an existing FlexGroup volume, the default value of the "constituents_per_aggregate" field is 1. The volume expand operation is only supported on FlexGroup volumes."""

    convert_unicode = marshmallow_fields.Boolean(
        data_key="convert_unicode",
        allow_none=True,
    )
    r""" Specifies whether directory Unicode format conversion is enabled when directories are accessed by NFS clients."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Creation time of the volume. This field is generated when the volume is created.

Example: 2018-06-04T19:00:00.000+0000"""

    efficiency = marshmallow_fields.Nested("netapp_ontap.models.volume_efficiency.VolumeEfficiencySchema", data_key="efficiency", unknown=EXCLUDE, allow_none=True)
    r""" The efficiency field of the volume."""

    encryption = marshmallow_fields.Nested("netapp_ontap.models.volume_encryption.VolumeEncryptionSchema", data_key="encryption", unknown=EXCLUDE, allow_none=True)
    r""" The encryption field of the volume."""

    error_state = marshmallow_fields.Nested("netapp_ontap.models.volume_error_state.VolumeErrorStateSchema", data_key="error_state", unknown=EXCLUDE, allow_none=True)
    r""" The error_state field of the volume."""

    files = marshmallow_fields.Nested("netapp_ontap.models.volume_files.VolumeFilesSchema", data_key="files", unknown=EXCLUDE, allow_none=True)
    r""" The files field of the volume."""

    flash_pool = marshmallow_fields.Nested("netapp_ontap.models.volume_flash_pool.VolumeFlashPoolSchema", data_key="flash_pool", unknown=EXCLUDE, allow_none=True)
    r""" The flash_pool field of the volume."""

    flexcache_endpoint_type = marshmallow_fields.Str(
        data_key="flexcache_endpoint_type",
        validate=enum_validation(['none', 'cache', 'origin']),
        allow_none=True,
    )
    r""" FlexCache endpoint type. <br>none &dash; The volume is neither a FlexCache nor origin of any FlexCache. <br>cache &dash; The volume is a FlexCache volume. <br>origin &dash; The volume is origin of a FlexCache volume.

Valid choices:

* none
* cache
* origin"""

    flexgroup = marshmallow_fields.Nested("netapp_ontap.models.volume_flexgroup.VolumeFlexgroupSchema", data_key="flexgroup", unknown=EXCLUDE, allow_none=True)
    r""" The flexgroup field of the volume."""

    granular_data = marshmallow_fields.Boolean(
        data_key="granular_data",
        allow_none=True,
    )
    r""" State of granular data on the volume. This setting is `true` by default when creating an AWS S3 FlexGroup volume via a POST request and `false` by default for creating any other type of FlexGroup volume via a POST request. On FlexVol volumes, the setting is always `false`, as only FlexGroup volumes support this feature. Once enabled, this setting can only be disabled by restoring a snapshot. Earlier versions of ONTAP (pre 9.12) are not compatible with this feature. Therefore, reverting to an earlier version of ONTAP is not possible unless this volume is deleted or restored to a snapshot that was taken before the setting was enabled."""

    granular_data_mode = marshmallow_fields.Str(
        data_key="granular_data_mode",
        validate=enum_validation(['disabled', 'basic', 'advanced']),
        allow_none=True,
    )
    r""" Mode of granular data on the volume. This setting defaults to `basic` when the `granular_data` parameter is set to `true`, but can be specified at the time of creation via a POST request. Earlier versions of ONTAP (pre 9.12) are not compatible with the `basic` setting. Therefore, when set to `basic`, reverting to an earlier version of ONTAP is not possible unless this volume is deleted or restored to a snapshot that was taken before the `basic` mode was enabled. Earlier versions of ONTAP (pre 9.16) are not compatible with the `advanced` setting. Therefore, when set to `advanced`, reverting to an earlier version of ONTAP is not possible unless this volume is deleted or restored to a snapshot that was taken before the `advanced` mode was enabled.

Valid choices:

* disabled
* basic
* advanced"""

    guarantee = marshmallow_fields.Nested("netapp_ontap.models.volume_guarantee.VolumeGuaranteeSchema", data_key="guarantee", unknown=EXCLUDE, allow_none=True)
    r""" The guarantee field of the volume."""

    is_object_store = marshmallow_fields.Boolean(
        data_key="is_object_store",
        allow_none=True,
    )
    r""" Specifies whether the volume is provisioned for an object store server."""

    is_svm_root = marshmallow_fields.Boolean(
        data_key="is_svm_root",
        allow_none=True,
    )
    r""" Specifies whether the volume is a root volume of the SVM it belongs to."""

    language = marshmallow_fields.Str(
        data_key="language",
        validate=enum_validation(['ar', 'ar.utf_8', 'c', 'c.utf_8', 'cs', 'cs.utf_8', 'da', 'da.utf_8', 'de', 'de.utf_8', 'en', 'en.utf_8', 'en_us', 'en_us.utf_8', 'es', 'es.utf_8', 'fi', 'fi.utf_8', 'fr', 'fr.utf_8', 'he', 'he.utf_8', 'hr', 'hr.utf_8', 'hu', 'hu.utf_8', 'it', 'it.utf_8', 'ja', 'ja.utf_8', 'ja_jp.932', 'ja_jp.932.utf_8', 'ja_jp.pck', 'ja_jp.pck.utf_8', 'ja_jp.pck_v2', 'ja_jp.pck_v2.utf_8', 'ja_v1', 'ja_v1.utf_8', 'ko', 'ko.utf_8', 'nl', 'nl.utf_8', 'no', 'no.utf_8', 'pl', 'pl.utf_8', 'pt', 'pt.utf_8', 'ro', 'ro.utf_8', 'ru', 'ru.utf_8', 'sk', 'sk.utf_8', 'sl', 'sl.utf_8', 'sv', 'sv.utf_8', 'tr', 'tr.utf_8', 'utf8mb4', 'zh', 'zh.gbk', 'zh.gbk.utf_8', 'zh.utf_8', 'zh_tw', 'zh_tw.big5', 'zh_tw.big5.utf_8', 'zh_tw.utf_8']),
        allow_none=True,
    )
    r""" Language encoding setting for volume. If no language is specified, the volume inherits its SVM language encoding setting.

Valid choices:

* ar
* ar.utf_8
* c
* c.utf_8
* cs
* cs.utf_8
* da
* da.utf_8
* de
* de.utf_8
* en
* en.utf_8
* en_us
* en_us.utf_8
* es
* es.utf_8
* fi
* fi.utf_8
* fr
* fr.utf_8
* he
* he.utf_8
* hr
* hr.utf_8
* hu
* hu.utf_8
* it
* it.utf_8
* ja
* ja.utf_8
* ja_jp.932
* ja_jp.932.utf_8
* ja_jp.pck
* ja_jp.pck.utf_8
* ja_jp.pck_v2
* ja_jp.pck_v2.utf_8
* ja_v1
* ja_v1.utf_8
* ko
* ko.utf_8
* nl
* nl.utf_8
* no
* no.utf_8
* pl
* pl.utf_8
* pt
* pt.utf_8
* ro
* ro.utf_8
* ru
* ru.utf_8
* sk
* sk.utf_8
* sl
* sl.utf_8
* sv
* sv.utf_8
* tr
* tr.utf_8
* utf8mb4
* zh
* zh.gbk
* zh.gbk.utf_8
* zh.utf_8
* zh_tw
* zh_tw.big5
* zh_tw.big5.utf_8
* zh_tw.utf_8"""

    max_dir_size = Size(
        data_key="max_dir_size",
        allow_none=True,
    )
    r""" Maximum directory size. This value sets maximum size, in bytes, to which a directory can grow. The default maximum directory size for FlexVol volumes is model-dependent, and optimized for the size of system memory. Before increasing the maximum directory size, involve technical support."""

    metric = marshmallow_fields.Nested("netapp_ontap.resources.volume_metrics.VolumeMetricsSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS, latency and throughput."""

    movement = marshmallow_fields.Nested("netapp_ontap.models.volume_movement.VolumeMovementSchema", data_key="movement", unknown=EXCLUDE, allow_none=True)
    r""" Volume movement. All attributes are modify, that is, not writable through POST. Set PATCH state to destination_aggregate to initiate a volume move operation. Volume movement on FlexGroup volume constituents are not supported."""

    msid = Size(
        data_key="msid",
        allow_none=True,
    )
    r""" The volume's Master Set ID."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=203),
        allow_none=True,
    )
    r""" Volume name. The name of volume must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 197 or fewer characters in length for FlexGroup volumes, and 203 or fewer characters in length for all other types of volumes. Volume names must be unique within an SVM. Required on POST.

Example: vol_cs_dept"""

    nas = marshmallow_fields.Nested("netapp_ontap.models.volume_nas.VolumeNasSchema", data_key="nas", unknown=EXCLUDE, allow_none=True)
    r""" The nas field of the volume."""

    optimize_aggregates = marshmallow_fields.Boolean(
        data_key="optimize_aggregates",
        allow_none=True,
    )
    r""" Specifies whether to create the constituents of the FlexGroup volume on the aggregates specified in the order they are specified, or whether the system should optimize the ordering of the aggregates. If this value is 'true', the system optimizes the ordering of the aggregates specified. If this value is false, the order of the aggregates is unchanged. The default value is 'false'."""

    qos = marshmallow_fields.Nested("netapp_ontap.models.volume_qos.VolumeQosSchema", data_key="qos", unknown=EXCLUDE, allow_none=True)
    r""" QoS information"""

    queue_for_encryption = marshmallow_fields.Boolean(
        data_key="queue_for_encryption",
        allow_none=True,
    )
    r""" Specifies whether the volume is queued for encryption."""

    quota = marshmallow_fields.Nested("netapp_ontap.models.volume_quota.VolumeQuotaSchema", data_key="quota", unknown=EXCLUDE, allow_none=True)
    r""" Quotas track the space or file usage of a user, group, or qtree in a FlexVol volume or a FlexGroup volume."""

    rebalancing = marshmallow_fields.Nested("netapp_ontap.models.volume_rebalancing.VolumeRebalancingSchema", data_key="rebalancing", unknown=EXCLUDE, allow_none=True)
    r""" Configuration and runtime properties involving non-disruptive volume capacity rebalancing for a FlexGroup volume."""

    scheduled_snapshot_naming_scheme = marshmallow_fields.Str(
        data_key="scheduled_snapshot_naming_scheme",
        validate=enum_validation(['create_time', 'ordinal']),
        allow_none=True,
    )
    r""" Naming Scheme for automatic snapshots:

* create_time - Automatic snapshots are saved as per the start of their current date and time.
* ordinal - Latest automatic snapshot copy is saved as <scheduled_frequency>.0 and subsequent copies will follow the create_time naming convention.


Valid choices:

* create_time
* ordinal"""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" Physical size of the volume, in bytes. The minimum size for a FlexVol volume is 20MB and the minimum size for a FlexGroup volume is 200MB per constituent. The recommended size for a FlexGroup volume is a minimum of 100GB per constituent. For all volumes, the default size is equal to the minimum size."""

    snaplock = marshmallow_fields.Nested("netapp_ontap.models.volume_snaplock.VolumeSnaplockSchema", data_key="snaplock", unknown=EXCLUDE, allow_none=True)
    r""" The snaplock field of the volume."""

    snapmirror = marshmallow_fields.Nested("netapp_ontap.models.volume_snapmirror.VolumeSnapmirrorSchema", data_key="snapmirror", unknown=EXCLUDE, allow_none=True)
    r""" Specifies attributes for SnapMirror protection."""

    snapshot_count = Size(
        data_key="snapshot_count",
        validate=integer_validation(minimum=0, maximum=1023),
        allow_none=True,
    )
    r""" Number of snapshots in the volume."""

    snapshot_directory_access_enabled = marshmallow_fields.Boolean(
        data_key="snapshot_directory_access_enabled",
        allow_none=True,
    )
    r""" This field, if true, enables the visible ".snapshot" directory from the client. The ".snapshot" directory will be available in every directory on the volume."""

    snapshot_locking_enabled = marshmallow_fields.Boolean(
        data_key="snapshot_locking_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not snapshot copy locking is enabled on the volume."""

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", data_key="snapshot_policy", unknown=EXCLUDE, allow_none=True)
    r""" The snapshot_policy field of the volume."""

    space = marshmallow_fields.Nested("netapp_ontap.models.volume_space.VolumeSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The space field of the volume."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['error', 'mixed', 'offline', 'online', 'restricted']),
        allow_none=True,
    )
    r""" Volume state. Client access is supported only when volume is online and junctioned. Taking volume to offline or restricted state removes its junction path and blocks client access. When volume is in restricted state some operations like parity reconstruction and iron on commit are allowed. The 'mixed' state applies to FlexGroup volumes only and cannot be specified as a target state. An 'error' state implies that the volume is not in a state to serve data.

Valid choices:

* error
* mixed
* offline
* online
* restricted"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.volume_statistics.VolumeStatisticsSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the volume."""

    status = marshmallow_fields.List(marshmallow_fields.Str, data_key="status", allow_none=True)
    r""" Describes the current status of a volume."""

    style = marshmallow_fields.Str(
        data_key="style",
        validate=enum_validation(['flexvol', 'flexgroup', 'flexgroup_constituent']),
        allow_none=True,
    )
    r""" The style of the volume. If "style" is not specified, the volume type is determined based on the specified aggregates or license. Specifying a single aggregate, without "constituents_per_aggregate", creates a flexible volume. Specifying multiple aggregates, or a single aggregate with "constituents_per_aggregate", creates a FlexGroup volume. When the UDO License is installed, and no aggregates are specified, the system automatically provisions a FlexGroup volume on system selected aggregates. Specifying a volume "style" creates a volume of that type. For example, if the style is "flexvol", you must specify a single aggregate. If the style is "flexgroup", the system either uses the specified aggregates or automatically provisions aggregates if there are no specified aggregates. The style "flexgroup_constituent" is not supported when creating a volume.<br>flexvol &dash; flexible volumes and FlexClone volumes<br>flexgroup &dash; FlexGroup volumes<br>flexgroup_constituent &dash; FlexGroup volume constituents.

Valid choices:

* flexvol
* flexgroup
* flexgroup_constituent"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the volume."""

    tiering = marshmallow_fields.Nested("netapp_ontap.models.volume_tiering.VolumeTieringSchema", data_key="tiering", unknown=EXCLUDE, allow_none=True)
    r""" The tiering field of the volume."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['rw', 'dp', 'ls']),
        allow_none=True,
    )
    r""" Type of the volume.<br>rw &dash; read-write volume.<br>dp &dash; data-protection volume.<br>ls &dash; load-sharing `dp` volume. Valid in GET.

Valid choices:

* rw
* dp
* ls"""

    use_mirrored_aggregates = marshmallow_fields.Boolean(
        data_key="use_mirrored_aggregates",
        allow_none=True,
    )
    r""" Specifies whether mirrored aggregates are selected when provisioning a FlexGroup without specifying "aggregates.name" or "aggregates.uuid". Only mirrored aggregates are used if this parameter is set to 'true' and only unmirrored aggregates are used if this parameter is set to 'false'. Aggregate level mirroring for a FlexGroup volume can be changed by moving all of the constituents to the required aggregates. The default value is 'true' for a MetroCluster configuration and is 'false' for a non-MetroCluster configuration."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for the volume. This corresponds to the instance-uuid that is exposed in the CLI and ONTAPI. It does not change due to a volume move.

Example: 028baa66-41bd-11e9-81d5-00a0986138f7"""

    validate_only = marshmallow_fields.Boolean(
        data_key="validate_only",
        allow_none=True,
    )
    r""" Validate the volume move or volume conversion operations and their parameters, without actually performing the operation."""

    @property
    def resource(self):
        return Volume

    gettable_fields = [
        "links",
        "tags",
        "access_time_enabled",
        "activity_tracking",
        "aggregates.links",
        "aggregates.name",
        "aggregates.uuid",
        "aggressive_readahead_mode",
        "analytics",
        "anti_ransomware",
        "application",
        "asynchronous_directory_delete",
        "autosize",
        "clone",
        "cloud_retrieval_policy",
        "cloud_write_enabled",
        "comment",
        "consistency_group",
        "constituents",
        "convert_unicode",
        "create_time",
        "efficiency",
        "encryption",
        "error_state",
        "files",
        "flash_pool",
        "flexcache_endpoint_type",
        "flexgroup",
        "granular_data",
        "granular_data_mode",
        "guarantee",
        "is_object_store",
        "is_svm_root",
        "language",
        "max_dir_size",
        "metric",
        "movement",
        "msid",
        "name",
        "nas",
        "qos",
        "queue_for_encryption",
        "quota",
        "rebalancing",
        "scheduled_snapshot_naming_scheme",
        "size",
        "snaplock",
        "snapmirror",
        "snapshot_count",
        "snapshot_directory_access_enabled",
        "snapshot_locking_enabled",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "state",
        "statistics.cifs_ops_raw",
        "statistics.cloud",
        "statistics.flexcache_raw",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.nfs_ops_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "status",
        "style",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tiering",
        "type",
        "uuid",
        "validate_only",
    ]
    """links,tags,access_time_enabled,activity_tracking,aggregates.links,aggregates.name,aggregates.uuid,aggressive_readahead_mode,analytics,anti_ransomware,application,asynchronous_directory_delete,autosize,clone,cloud_retrieval_policy,cloud_write_enabled,comment,consistency_group,constituents,convert_unicode,create_time,efficiency,encryption,error_state,files,flash_pool,flexcache_endpoint_type,flexgroup,granular_data,granular_data_mode,guarantee,is_object_store,is_svm_root,language,max_dir_size,metric,movement,msid,name,nas,qos,queue_for_encryption,quota,rebalancing,scheduled_snapshot_naming_scheme,size,snaplock,snapmirror,snapshot_count,snapshot_directory_access_enabled,snapshot_locking_enabled,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,space,state,statistics.cifs_ops_raw,statistics.cloud,statistics.flexcache_raw,statistics.iops_raw,statistics.latency_raw,statistics.nfs_ops_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,status,style,svm.links,svm.name,svm.uuid,tiering,type,uuid,validate_only,"""

    patchable_fields = [
        "tags",
        "access_time_enabled",
        "activity_tracking",
        "aggregates.name",
        "aggregates.uuid",
        "aggressive_readahead_mode",
        "analytics",
        "anti_ransomware",
        "application",
        "asynchronous_directory_delete",
        "autosize",
        "clone",
        "cloud_retrieval_policy",
        "cloud_write_enabled",
        "comment",
        "consistency_group",
        "constituents",
        "constituents_per_aggregate",
        "convert_unicode",
        "efficiency",
        "encryption",
        "error_state",
        "files",
        "flash_pool",
        "flexgroup",
        "granular_data",
        "granular_data_mode",
        "guarantee",
        "max_dir_size",
        "movement",
        "msid",
        "name",
        "nas",
        "qos",
        "queue_for_encryption",
        "quota",
        "rebalancing",
        "scheduled_snapshot_naming_scheme",
        "size",
        "snaplock",
        "snapmirror",
        "snapshot_directory_access_enabled",
        "snapshot_locking_enabled",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "state",
        "style",
        "tiering",
        "validate_only",
    ]
    """tags,access_time_enabled,activity_tracking,aggregates.name,aggregates.uuid,aggressive_readahead_mode,analytics,anti_ransomware,application,asynchronous_directory_delete,autosize,clone,cloud_retrieval_policy,cloud_write_enabled,comment,consistency_group,constituents,constituents_per_aggregate,convert_unicode,efficiency,encryption,error_state,files,flash_pool,flexgroup,granular_data,granular_data_mode,guarantee,max_dir_size,movement,msid,name,nas,qos,queue_for_encryption,quota,rebalancing,scheduled_snapshot_naming_scheme,size,snaplock,snapmirror,snapshot_directory_access_enabled,snapshot_locking_enabled,snapshot_policy.name,snapshot_policy.uuid,space,state,style,tiering,validate_only,"""

    postable_fields = [
        "tags",
        "activity_tracking",
        "aggregates.name",
        "aggregates.uuid",
        "aggressive_readahead_mode",
        "analytics",
        "anti_ransomware",
        "application",
        "asynchronous_directory_delete",
        "autosize",
        "clone",
        "cloud_retrieval_policy",
        "cloud_write_enabled",
        "comment",
        "consistency_group",
        "constituents",
        "constituents_per_aggregate",
        "convert_unicode",
        "efficiency",
        "encryption",
        "error_state",
        "files",
        "flash_pool",
        "flexgroup",
        "granular_data",
        "granular_data_mode",
        "guarantee",
        "language",
        "max_dir_size",
        "movement",
        "msid",
        "name",
        "nas",
        "optimize_aggregates",
        "qos",
        "quota",
        "rebalancing",
        "scheduled_snapshot_naming_scheme",
        "size",
        "snaplock",
        "snapmirror",
        "snapshot_directory_access_enabled",
        "snapshot_locking_enabled",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "state",
        "style",
        "svm.name",
        "svm.uuid",
        "tiering",
        "type",
        "use_mirrored_aggregates",
        "validate_only",
    ]
    """tags,activity_tracking,aggregates.name,aggregates.uuid,aggressive_readahead_mode,analytics,anti_ransomware,application,asynchronous_directory_delete,autosize,clone,cloud_retrieval_policy,cloud_write_enabled,comment,consistency_group,constituents,constituents_per_aggregate,convert_unicode,efficiency,encryption,error_state,files,flash_pool,flexgroup,granular_data,granular_data_mode,guarantee,language,max_dir_size,movement,msid,name,nas,optimize_aggregates,qos,quota,rebalancing,scheduled_snapshot_naming_scheme,size,snaplock,snapmirror,snapshot_directory_access_enabled,snapshot_locking_enabled,snapshot_policy.name,snapshot_policy.uuid,space,state,style,svm.name,svm.uuid,tiering,type,use_mirrored_aggregates,validate_only,"""

class Volume(Resource):
    """Allows interaction with Volume objects on the host"""

    _schema = VolumeSchema
    _path = "/api/storage/volumes"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves volumes.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `is_svm_root`
* `aggressive_readahead_mode`
* `analytics.*`
* `anti_ransomware.*`
* `application.*`
* `encryption.*`
* `queue_for_encryption`
* `convert_unicode`
* `clone.parent_snapshot.name`
* `clone.parent_snapshot.uuid`
* `clone.parent_svm.name`
* `clone.parent_svm.uuid`
* `clone.parent_volume.name`
* `clone.parent_volume.uuid`
* `clone.split_complete_percent`
* `clone.split_estimate`
* `clone.split_initiated`
* `efficiency.*`
* `error_state.*`
* `files.*`
* `max_dir_size`
* `nas.export_policy.id`
* `nas.gid`
* `nas.path`
* `nas.security_style`
* `nas.uid`
* `nas.unix_permissions`
* `nas.junction_parent.name`
* `nas.junction_parent.uuid`
* `snaplock.*`
* `restore_to.*`
* `snapshot_policy.uuid`
* `quota.*`
* `qos.*`
* `flexcache_endpoint_type`
* `space.block_storage_inactive_user_data`
* `space.capacity_tier_footprint`
* `space.performance_tier_footprint`
* `space.local_tier_footprint`
* `space.footprint`
* `space.over_provisioned`
* `space.metadata`
* `space.total_footprint`
* `space.dedupe_metafiles_footprint`
* `space.dedupe_metafiles_temporary_footprint`
* `space.delayed_free_footprint`
* `space.file_operation_metadata`
* `space.snapmirror_destination_footprint`
* `space.volume_guarantee_footprint`
* `space.cross_volume_dedupe_metafiles_footprint`
* `space.cross_volume_dedupe_metafiles_temporary_footprint`
* `space.snapshot_reserve_unusable`
* `space.snapshot_spill`
* `space.user_data`
* `space.logical_space.*`
* `space.snapshot.*`
* `space.used_by_afs`
* `space.afs_total`
* `space.available_percent`
* `space.full_threshold_percent`
* `space.nearly_full_threshold_percent`
* `space.overwrite_reserve`
* `space.overwrite_reserve_used`
* `space.size_available_for_snapshots`
* `space.percent_used`
* `space.fractional_reserve`
* `space.block_storage_inactive_user_data_percent`
* `space.physical_used`
* `space.physical_used_percent`
* `space.expected_available`
* `space.filesystem_size`
* `space.filesystem_size_fixed`
* `guarantee.*`
* `autosize.*`
* `movement.*`
* `statistics.*`
* `constituents.name`
* `constituents.space.size`
* `constituents.space.available`
* `constituents.space.used`
* `constituents.space.available_percent`
* `constituents.space.used_percent`
* `constituents.space.block_storage_inactive_user_data`
* `constituents.space.capacity_tier_footprint`
* `constituents.space.performance_tier_footprint`
* `constituents.space.local_tier_footprint`
* `constituents.space.footprint`
* `constituents.space.over_provisioned`
* `constituents.space.metadata`
* `constituents.space.total_footprint`
* `constituents.space.logical_space.reporting`
* `constituents.space.logical_space.enforcement`
* `constituents.space.logical_space.used_by_afs`
* `constituents.space.logical_space.available`
* `constituents.space.snapshot.used`
* `constituents.space.snapshot.reserve_percent`
* `constituents.space.snapshot.autodelete_enabled`
* `constituents.space.large_size_enabled`
* `constituents.space.max_size`
* `constituents.space.total_metadata`
* `constituents.space.total_metadata_footprint`
* `constituents.aggregates.name`
* `constituents.aggregates.uuid`
* `constituents.movement.destination_aggregate.name`
* `constituents.movement.destination_aggregate.uuid`
* `constituents.movement.state`
* `constituents.movement.percent_complete`
* `constituents.movement.cutover_window`
* `constituents.movement.tiering_policy`
* `asynchronous_directory_delete.*`
* `rebalancing.*`
* `metric.*`
* `cloud_write_enabled`
### Related ONTAP commands
* `volume show`
* `volume clone show`
* `volume efficiency show`
* `volume encryption show`
* `volume flexcache show`
* `volume flexgroup show`
* `volume move show`
* `volume quota show`
* `volume show-space`
* `volume snaplock show`
* `volume rebalance show`
* `security anti-ransomware volume show`
* `security anti-ransomware volume space show`
* `volume file async-delete client show`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all Volume resources that match the provided query"""
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
        """Returns a list of RawResources that represent Volume resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Volume"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the attributes of a volume. For movement, use the "validate_only" field on the request to validate but not perform the operation. The PATCH API can be used to enable or disable quotas for a FlexVol or a FlexGroup volume. The PATCH API can also be used to start or stop non-disruptive volume capacity rebalancing for FlexGroup volumes in addition to modifying capacity rebalancing properties. An empty path in PATCH deactivates and unmounts the volume. Taking a volume offline removes its junction path.
<br>A PATCH request for volume encryption performs conversion/rekey operations asynchronously. You can retrieve the conversion/rekey progress details by calling a GET request on the corresponding volume endpoint.
### Platform Specifics
**Unified ONTAP**: PATCH must be used to update the attributes of a volume.
**ASA r2**: PATCH is not supported for the following immutable properties.
* `autosize.maximum`
* `autosize.minimum`
* `autosize.grow_threshold`
* `autosize.shrink_threshold`
* `autosize.mode`
* `size`
* `space.size`
* `space.large_size_enabled`
* `space.max_size`
* `qos.policy.min-throughput-iops`
* `qos.policy.max-throughput-iops`
* `qos.policy.max-throughput-mbps`
* `qos.policy.min-throughput-mbps`
* `qos.policy.uuid`
* `qos.policy.name`
* `tiering.policy`
* `tiering.min_cooling_days`
* `tiering.object_tags`
* `tiering.storage_class`
* `anti_ransomware`
* `nas.uid`
* `nas.gid`
* `nas.unix_permissions`
* `state`
* `space.snapshot.autodelete_enabled`
* `snapshot_policy.name`
* `snapshot_policy.uuid`
* `guarantee.type`
* `clone.split_initiated`
* `clone.match_parent_storage_tier`
* `efficiency.application_io_size`
* `efficiency.compression_type`
* `efficiency.compression`
* `efficiency.storage_efficiency_mode`
* `efficiency.dedupe`
* `efficiency.cross_volume_dedupe`
* `efficiency.compaction`
* `efficiency.policy.name`
* `efficiency.enable_all`
* `efficiency.disable_all`
* `efficiency.state`
* `efficiency.scanner.state`
* `efficiency.scanner.scan_old_data`
* `efficiency.scanner.compression`
* `efficiency.scanner.dedupe`
* `efficiency.idcs_scanner.operation_state`
* `efficiency.idcs_scanner.inactive_days`
* `efficiency.idcs_scanner.mode`
* `encryption.enabled`
* `encryption.rekey`
* `encryption.action`
* `queue_for_encryption`
### Optional properties
* `queue_for_encryption` - Queue volumes for encryption when `encryption.enabled=true`.  If this option is not provided or is false, conversion of volumes starts immediately. When there are volumes in the queue and less than four encryptions are running, volumes are encrypted in the order in which they are queued.
* `encryption.action` - You can pause an ongoing rekey/conversion operation or resume a paused rekey/conversion operation using this field.  The following actions are supported for this field: &dash; conversion_pause - Pause an encryption conversion operation currently in progress &dash; conversion_resume - Resume a paused encryption conversion operation &dash; rekey_pause - Pause an encryption rekey operation currently in progress &dash; rekey_resume - Resume a paused encryption rekey operation
### Related ONTAP commands
* `volume unmount`
* `volume mount`
* `volume online`
* `volume offline`
* `volume modify`
* `volume clone modify`
* `volume efficiency modify`
* `volume quota on`
* `volume quota off`
* `volume snaplock modify`
* `volume encryption conversion start`
* `volume encryption conversion pause`
* `volume encryption conversion resume`
* `volume encryption rekey start`
* `volume encryption rekey pause`
* `volume encryption rekey resume`
* `volume rebalance start`
* `volume rebalance stop`
* `volume rebalance modify`
* `security anti-ransomware volume enable`
* `security anti-ransomware volume disable`
* `security anti-ransomware volume dry-run`
* `security anti-ransomware volume pause`
* `security anti-ransomware volume resume`
* `volume file async-delete client disable`
* `volume file async-delete client enable`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Volume"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Volume"], NetAppResponse]:
        r"""Creates a volume on a specified SVM and storage aggregates.
### Platform Specifics
* **Unified ONTAP**: POST must be used to create a volume.
* **ASA r2**: POST is not supported.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the volume.
* `name` - Name of the volume.
* `aggregates.name` or `aggregates.uuid` - Existing aggregates in which to create the volume.
### Default property values
* `state` -  _online_
* `size` - _20MB_
* `style` - _flexvol_
* `type` - _rw_
* `encryption.enabled` - _false_
* `snapshot_policy.name` - _default_
* `guarantee.type` - _volume_
* `anti_ransomware.state` - _default_
### Related ONTAP commands
* `volume create`
* `volume clone create`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["Volume"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a volume. If the UUID belongs to a volume, all of its blocks are freed and returned to its containing aggregate. If a volume is online, it is offlined before deletion. If a volume is mounted, unmount the volume by specifying the nas.path as empty before deleting it using the DELETE operation.
### Platform Specifics
* **Unified ONTAP**: DELETE must be used to delete a volume.
* **ASA r2**: DELETE is not supported.
### Optional parameters:
* `force` - Bypasses the recovery-queue and completely removes the volume from the aggregate making it non-recoverable. By default, this flag is set to "false".
### Related ONTAP commands
* `volume delete`
* `volume clone delete`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves volumes.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `is_svm_root`
* `aggressive_readahead_mode`
* `analytics.*`
* `anti_ransomware.*`
* `application.*`
* `encryption.*`
* `queue_for_encryption`
* `convert_unicode`
* `clone.parent_snapshot.name`
* `clone.parent_snapshot.uuid`
* `clone.parent_svm.name`
* `clone.parent_svm.uuid`
* `clone.parent_volume.name`
* `clone.parent_volume.uuid`
* `clone.split_complete_percent`
* `clone.split_estimate`
* `clone.split_initiated`
* `efficiency.*`
* `error_state.*`
* `files.*`
* `max_dir_size`
* `nas.export_policy.id`
* `nas.gid`
* `nas.path`
* `nas.security_style`
* `nas.uid`
* `nas.unix_permissions`
* `nas.junction_parent.name`
* `nas.junction_parent.uuid`
* `snaplock.*`
* `restore_to.*`
* `snapshot_policy.uuid`
* `quota.*`
* `qos.*`
* `flexcache_endpoint_type`
* `space.block_storage_inactive_user_data`
* `space.capacity_tier_footprint`
* `space.performance_tier_footprint`
* `space.local_tier_footprint`
* `space.footprint`
* `space.over_provisioned`
* `space.metadata`
* `space.total_footprint`
* `space.dedupe_metafiles_footprint`
* `space.dedupe_metafiles_temporary_footprint`
* `space.delayed_free_footprint`
* `space.file_operation_metadata`
* `space.snapmirror_destination_footprint`
* `space.volume_guarantee_footprint`
* `space.cross_volume_dedupe_metafiles_footprint`
* `space.cross_volume_dedupe_metafiles_temporary_footprint`
* `space.snapshot_reserve_unusable`
* `space.snapshot_spill`
* `space.user_data`
* `space.logical_space.*`
* `space.snapshot.*`
* `space.used_by_afs`
* `space.afs_total`
* `space.available_percent`
* `space.full_threshold_percent`
* `space.nearly_full_threshold_percent`
* `space.overwrite_reserve`
* `space.overwrite_reserve_used`
* `space.size_available_for_snapshots`
* `space.percent_used`
* `space.fractional_reserve`
* `space.block_storage_inactive_user_data_percent`
* `space.physical_used`
* `space.physical_used_percent`
* `space.expected_available`
* `space.filesystem_size`
* `space.filesystem_size_fixed`
* `guarantee.*`
* `autosize.*`
* `movement.*`
* `statistics.*`
* `constituents.name`
* `constituents.space.size`
* `constituents.space.available`
* `constituents.space.used`
* `constituents.space.available_percent`
* `constituents.space.used_percent`
* `constituents.space.block_storage_inactive_user_data`
* `constituents.space.capacity_tier_footprint`
* `constituents.space.performance_tier_footprint`
* `constituents.space.local_tier_footprint`
* `constituents.space.footprint`
* `constituents.space.over_provisioned`
* `constituents.space.metadata`
* `constituents.space.total_footprint`
* `constituents.space.logical_space.reporting`
* `constituents.space.logical_space.enforcement`
* `constituents.space.logical_space.used_by_afs`
* `constituents.space.logical_space.available`
* `constituents.space.snapshot.used`
* `constituents.space.snapshot.reserve_percent`
* `constituents.space.snapshot.autodelete_enabled`
* `constituents.space.large_size_enabled`
* `constituents.space.max_size`
* `constituents.space.total_metadata`
* `constituents.space.total_metadata_footprint`
* `constituents.aggregates.name`
* `constituents.aggregates.uuid`
* `constituents.movement.destination_aggregate.name`
* `constituents.movement.destination_aggregate.uuid`
* `constituents.movement.state`
* `constituents.movement.percent_complete`
* `constituents.movement.cutover_window`
* `constituents.movement.tiering_policy`
* `asynchronous_directory_delete.*`
* `rebalancing.*`
* `metric.*`
* `cloud_write_enabled`
### Related ONTAP commands
* `volume show`
* `volume clone show`
* `volume efficiency show`
* `volume encryption show`
* `volume flexcache show`
* `volume flexgroup show`
* `volume move show`
* `volume quota show`
* `volume show-space`
* `volume snaplock show`
* `volume rebalance show`
* `security anti-ransomware volume show`
* `security anti-ransomware volume space show`
* `volume file async-delete client show`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a volume. The GET API can be used to retrieve the quota state for a FlexVol or a FlexGroup volume.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `is_svm_root`
* `analytics.*`
* `anti_ransomware.*`
* `application.*`
* `encryption.*`
* `convert_unicode`
* `clone.parent_snapshot.name`
* `clone.parent_snapshot.uuid`
* `clone.parent_svm.name`
* `clone.parent_svm.uuid`
* `clone.parent_volume.name`
* `clone.parent_volume.uuid`
* `clone.split_complete_percent`
* `clone.split_estimate`
* `clone.split_initiated`
* `efficiency.*`
* `error_state.*`
* `files.*`
* `max_dir_size`
* `nas.export_policy.id`
* `nas.gid`
* `nas.path`
* `nas.security_style`
* `nas.uid`
* `nas.unix_permissions`
* `nas.junction_parent.name`
* `nas.junction_parent.uuid`
* `snaplock.*`
* `restore_to.*`
* `snapshot_policy.uuid`
* `quota.*`
* `qos.*`
* `flexcache_endpoint_type`
* `space.block_storage_inactive_user_data`
* `space.capacity_tier_footprint`
* `space.performance_tier_footprint`
* `space.local_tier_footprint`
* `space.footprint`
* `space.over_provisioned`
* `space.metadata`
* `space.total_footprint`
* `space.dedupe_metafiles_footprint`
* `space.dedupe_metafiles_temporary_footprint`
* `space.delayed_free_footprint`
* `space.file_operation_metadata`
* `space.snapmirror_destination_footprint`
* `space.volume_guarantee_footprint`
* `space.cross_volume_dedupe_metafiles_footprint`
* `space.cross_volume_dedupe_metafiles_temporary_footprint`
* `space.auto_adaptive_compression_footprint_data_reduction`
* `space.capacity_tier_footprint_data_reduction`
* `space.compaction_footprint_data_reduction`
* `space.effective_total_footprint`
* `space.snapshot_reserve_unusable`
* `space.snapshot_spill`
* `space.user_data`
* `space.logical_space.*`
* `space.snapshot.*`
* `space.used_by_afs`
* `space.afs_total`
* `space.available_percent`
* `space.full_threshold_percent`
* `space.nearly_full_threshold_percent`
* `space.overwrite_reserve`
* `space.overwrite_reserve_used`
* `space.size_available_for_snapshots`
* `space.percent_used`
* `space.fractional_reserve`
* `space.block_storage_inactive_user_data_percent`
* `space.physical_used`
* `space.physical_used_percent`
* `space.expected_available`
* `space.filesystem_size`
* `space.filesystem_size_fixed`
* `guarantee.*`
* `autosize.*`
* `movement.*`
* `statistics.*`
* `asynchronous_directory_delete.*`
* `rebalancing.*`
* `metric.*`
* `cloud_write_enabled`
### Related ONTAP commands
* `volume show`
* `volume clone show`
* `volume efficiency show`
* `volume encryption show`
* `volume flexcache show`
* `volume flexgroup show`
* `volume move show`
* `volume quota show`
* `volume show-space`
* `volume snaplock show`
* `volume rebalance show`
* `security anti-ransomware volume show`
* `security anti-ransomware volume attack generate-report`
* `security anti-ransomware volume space show`
* `volume file async-delete client show`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
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
        r"""Creates a volume on a specified SVM and storage aggregates.
### Platform Specifics
* **Unified ONTAP**: POST must be used to create a volume.
* **ASA r2**: POST is not supported.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the volume.
* `name` - Name of the volume.
* `aggregates.name` or `aggregates.uuid` - Existing aggregates in which to create the volume.
### Default property values
* `state` -  _online_
* `size` - _20MB_
* `style` - _flexvol_
* `type` - _rw_
* `encryption.enabled` - _false_
* `snapshot_policy.name` - _default_
* `guarantee.type` - _volume_
* `anti_ransomware.state` - _default_
### Related ONTAP commands
* `volume create`
* `volume clone create`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
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
        r"""Updates the attributes of a volume. For movement, use the "validate_only" field on the request to validate but not perform the operation. The PATCH API can be used to enable or disable quotas for a FlexVol or a FlexGroup volume. The PATCH API can also be used to start or stop non-disruptive volume capacity rebalancing for FlexGroup volumes in addition to modifying capacity rebalancing properties. An empty path in PATCH deactivates and unmounts the volume. Taking a volume offline removes its junction path.
<br>A PATCH request for volume encryption performs conversion/rekey operations asynchronously. You can retrieve the conversion/rekey progress details by calling a GET request on the corresponding volume endpoint.
### Platform Specifics
**Unified ONTAP**: PATCH must be used to update the attributes of a volume.
**ASA r2**: PATCH is not supported for the following immutable properties.
* `autosize.maximum`
* `autosize.minimum`
* `autosize.grow_threshold`
* `autosize.shrink_threshold`
* `autosize.mode`
* `size`
* `space.size`
* `space.large_size_enabled`
* `space.max_size`
* `qos.policy.min-throughput-iops`
* `qos.policy.max-throughput-iops`
* `qos.policy.max-throughput-mbps`
* `qos.policy.min-throughput-mbps`
* `qos.policy.uuid`
* `qos.policy.name`
* `tiering.policy`
* `tiering.min_cooling_days`
* `tiering.object_tags`
* `tiering.storage_class`
* `anti_ransomware`
* `nas.uid`
* `nas.gid`
* `nas.unix_permissions`
* `state`
* `space.snapshot.autodelete_enabled`
* `snapshot_policy.name`
* `snapshot_policy.uuid`
* `guarantee.type`
* `clone.split_initiated`
* `clone.match_parent_storage_tier`
* `efficiency.application_io_size`
* `efficiency.compression_type`
* `efficiency.compression`
* `efficiency.storage_efficiency_mode`
* `efficiency.dedupe`
* `efficiency.cross_volume_dedupe`
* `efficiency.compaction`
* `efficiency.policy.name`
* `efficiency.enable_all`
* `efficiency.disable_all`
* `efficiency.state`
* `efficiency.scanner.state`
* `efficiency.scanner.scan_old_data`
* `efficiency.scanner.compression`
* `efficiency.scanner.dedupe`
* `efficiency.idcs_scanner.operation_state`
* `efficiency.idcs_scanner.inactive_days`
* `efficiency.idcs_scanner.mode`
* `encryption.enabled`
* `encryption.rekey`
* `encryption.action`
* `queue_for_encryption`
### Optional properties
* `queue_for_encryption` - Queue volumes for encryption when `encryption.enabled=true`.  If this option is not provided or is false, conversion of volumes starts immediately. When there are volumes in the queue and less than four encryptions are running, volumes are encrypted in the order in which they are queued.
* `encryption.action` - You can pause an ongoing rekey/conversion operation or resume a paused rekey/conversion operation using this field.  The following actions are supported for this field: &dash; conversion_pause - Pause an encryption conversion operation currently in progress &dash; conversion_resume - Resume a paused encryption conversion operation &dash; rekey_pause - Pause an encryption rekey operation currently in progress &dash; rekey_resume - Resume a paused encryption rekey operation
### Related ONTAP commands
* `volume unmount`
* `volume mount`
* `volume online`
* `volume offline`
* `volume modify`
* `volume clone modify`
* `volume efficiency modify`
* `volume quota on`
* `volume quota off`
* `volume snaplock modify`
* `volume encryption conversion start`
* `volume encryption conversion pause`
* `volume encryption conversion resume`
* `volume encryption rekey start`
* `volume encryption rekey pause`
* `volume encryption rekey resume`
* `volume rebalance start`
* `volume rebalance stop`
* `volume rebalance modify`
* `security anti-ransomware volume enable`
* `security anti-ransomware volume disable`
* `security anti-ransomware volume dry-run`
* `security anti-ransomware volume pause`
* `security anti-ransomware volume resume`
* `volume file async-delete client disable`
* `volume file async-delete client enable`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
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
        r"""Deletes a volume. If the UUID belongs to a volume, all of its blocks are freed and returned to its containing aggregate. If a volume is online, it is offlined before deletion. If a volume is mounted, unmount the volume by specifying the nas.path as empty before deleting it using the DELETE operation.
### Platform Specifics
* **Unified ONTAP**: DELETE must be used to delete a volume.
* **ASA r2**: DELETE is not supported.
### Optional parameters:
* `force` - Bypasses the recovery-queue and completely removes the volume from the aggregate making it non-recoverable. By default, this flag is set to "false".
### Related ONTAP commands
* `volume delete`
* `volume clone delete`

### Learn more
* [`DOC /storage/volumes`](#docs-storage-storage_volumes)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


