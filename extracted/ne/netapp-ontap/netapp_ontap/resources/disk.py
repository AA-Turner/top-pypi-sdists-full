r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Retrieving storage disk information
The storage disk GET API retrieves all of the disks in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of disks from the cluster.
#### The following example shows the response with a list of disks in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Disk.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Disk({"name": "1.24.4"}),
    Disk({"name": "1.24.3"}),
    Disk({"name": "1.24.5"}),
    Disk({"name": "1.24.0"}),
    Disk({"name": "1.24.2"}),
    Disk({"name": "1.24.1"}),
]

```
</div>
</div>

---
### 2) Retrieve a specific disk from the cluster.
#### The following example shows the response of the requested disk. If there is no disk with the requested name, an error is returned:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk(name="1.24.3")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Disk(
    {
        "physical_size": 438804988000,
        "bytes_per_sector": 512,
        "name": "1.24.3",
        "shelf": {"uid": "10318311901725526608"},
        "error": [
            {
                "type": "notallflashdisk",
                "reason": {
                    "message": '"The node is configured with All-Flash Optimized personality and this disk is not an SSD. The disk needs to be removed from the system."',
                    "code": "721082",
                },
            }
        ],
        "aggregates": [
            {
                "name": "node_2_SAS_1",
                "_links": {
                    "self": {
                        "href": "/api/storage/aggregates/3fd9c345-ba91-4949-a7b1-6e2b898d74e3"
                    }
                },
                "uuid": "3fd9c345-ba91-4949-a7b1-6e2b898d74e3",
            }
        ],
        "sector_count": 1172123568,
        "firmware_version": "NA02",
        "uid": "50000394:0808AA88:00000000:00000000:00000000:00000000:00000000:00000000:00000000:00000000",
        "right_size_sector_count": 5579776,
        "paths": [
            {
                "port_type": "sas",
                "initiator": "3a",
                "port_name": "B",
                "wwpn": "5000cca02f0e676a",
                "wwnn": "5000cca02f0e6768",
            },
            {
                "port_type": "sas",
                "initiator": "3d",
                "port_name": "A",
                "wwpn": "5000cca02f0e6769",
                "wwnn": "5000cca02f0e6768",
            },
            {
                "port_type": "sas",
                "initiator": "3d",
                "port_name": "A",
                "wwpn": "5000cca02f0e6769",
                "wwnn": "5000cca02f0e6768",
            },
            {
                "port_type": "sas",
                "initiator": "3a",
                "port_name": "B",
                "wwpn": "5000cca02f0e676a",
                "wwnn": "5000cca02f0e6768",
            },
        ],
        "node": {
            "name": "node-2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/3a89ed49-8c6d-11e8-93bc-00a0985a64b6"
                }
            },
            "uuid": "3a89ed49-8c6d-11e8-93bc-00a0985a64b6",
        },
        "outage": {
            "persistently_failed": True,
            "reason": {
                "message": 'Failed disk. Reason: "admin failed".',
                "code": "721081",
            },
        },
        "stats": {
            "iops_total": 12854,
            "path_error_count": 0,
            "throughput": 1957888,
            "average_latency": 6,
            "power_on_hours": 11797,
        },
        "model": "X421_FAL12450A10",
        "bay": 3,
        "class": "performance",
        "pool": "pool0",
        "state": "present",
        "effective_type": "sas",
        "rpm": 10000,
        "local": True,
        "container_type": "aggregate",
        "serial_number": "EC47PC5021SW",
        "home_node": {
            "name": "node-2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/3a89ed49-8c6d-11e8-93bc-00a0985a64b6"
                }
            },
            "uuid": "3a89ed49-8c6d-11e8-93bc-00a0985a64b6",
        },
        "vendor": "NETAPP",
        "usable_size": 438304768000,
        "type": "sas",
    }
)

```
</div>
</div>

---
### 3) Retrieving a specific disk from the hypervisor
#### The following example shows the response of the requested disk. If there is no disk with the requested name, an error is returned:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk(name="NET-3.2")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Disk(
    {
        "physical_size": 204808,
        "bytes_per_sector": 512,
        "name": "NET-3.2",
        "sector_count": 204808,
        "firmware_version": "0001",
        "uid": "32343637:65386464:00000000:00000000:00000000:00000000:00000000:00000000:00000000:00000000",
        "right_size_sector_count": 5579776,
        "paths": [
            {
                "port_type": "sas",
                "vmdisk_hypervisor_file_name": "LUN 4.0",
                "initiator": "0f",
                "port_name": "A",
                "wwpn": "53059d50444f5476",
                "wwnn": "53059d50444f5476",
            },
            {
                "port_type": "sas",
                "vmdisk_hypervisor_file_name": "LUN 2.0",
                "initiator": "0f",
                "port_name": "A",
                "wwpn": "53059d50444f5476",
                "wwnn": "53059d50444f5476",
            },
        ],
        "node": {
            "name": "example_node_name",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/f4cb78ba-5841-11ec-80c4-916f62b4cd44"
                }
            },
            "uuid": "f4cb78ba-5841-11ec-80c4-916f62b4cd44",
        },
        "outage": {
            "persistently_failed": False,
            "reason": {"message": 'Failed disk. Reason: "".', "code": "721081"},
        },
        "stats": {
            "iops_total": 1,
            "path_error_count": 0,
            "throughput": 4096,
            "average_latency": 2157188883,
            "power_on_hours": 0,
        },
        "model": "PHA-DISK",
        "class": "virtual",
        "fips_certified": False,
        "pool": "pool0",
        "local": True,
        "container_type": "mediator",
        "serial_number": "3234363765386464",
        "self_encrypting": False,
        "home_node": {
            "name": "example_node_name",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/f4cb78ba-5841-11ec-80c4-916f62b4cd44"
                }
            },
            "uuid": "f4cb78ba-5841-11ec-80c4-916f62b4cd44",
        },
        "vendor": "NETAPP",
        "type": "vmdisk",
    }
)

```
</div>
</div>

---
## Modifying storage disk
The storage disk PATCH API modifies disk ownership, unfails a disk, updates encrypting drive authentication keys (AKs), sanitizes encrypting drives, or sanitizes non-encrypting spare drives in the cluster.
The storage disk API currently supports patching one attribute at a time.
### Updating the disk ownership for a specified disk. Disk ownership cannot be updated on the ASA r2 platform.
### 1. When the disk is not assigned
When the disk is a spare (or unowned) disk and node name is specified, the PATCH operation assigns the disk to the specified node.
Optionally, pool name can also be specified along with node name. Accepted pool names are: pool0, pool1.
### 2. When the disk is already assigned
When the disk is already assigned (already has a owner), and a new node is specified, the PATCH operation changes the ownership to the new node.
Optionally, pool name can also be specified along with node name. Accepted pool names are: pool0, pool1.
### Removing the disk ownership for a specified disk
When the disk is already assigned, and node name is specified as null (no-quotes), the PATCH operation removes the owner.
<br/>
---
## Examples
### 1. Update the disk ownership for an unowned disk
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.node = {"name": "node-name"}
    resource.patch(hydrate=True, name="<disk-name>")

```

---
### 2. Update the disk ownership for an already owned disk
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.node = {"name": "node-name"}
    resource.patch(hydrate=True, name="<disk-name>")

```

---
### 3. Update the disk pool for a disk (can be either owned or unowned).
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.node = {"name": "node-name"}
    resource.pool = "pool0"
    resource.patch(hydrate=True, name="<disk-name>")

```

---
### 4. Rekey the data authentication key (AK) of all encrypting drives to an authentication key (AK) selected automatically by the system
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.patch(hydrate=True, name="*", encryption_operation="rekey_data_auto_id")

```

---
### 5. Cryptographically sanitize a spare or broken disk
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.patch(
        hydrate=True, name="<disk-name>", encryption_operation="sanitize_disk"
    )

```

---
### 6. Unfailing a disk to a spare.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.state = "spare"
    resource.patch(hydrate=True, name="<disk-name>")

```

---
### 7. Unfailing a disk and attempting to reassimilate filesystem labels.
### If unable or unnecessary to reassimilate filesystem labels, the disk will be set as spare.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.state = "present"
    resource.patch(hydrate=True, name="<disk-name>")

```

---
### 8. Sanitize spare disks (non-cryptographically)
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.sanitize_spare = True
    resource.patch(hydrate=True, name="<disk-name>")

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


__all__ = ["Disk", "DiskSchema"]
__pdoc__ = {
    "DiskSchema.resource": False,
    "DiskSchema.opts": False,
}


class DiskSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Disk object"""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" List of aggregates sharing this disk"""

    bay = Size(
        data_key="bay",
        allow_none=True,
    )
    r""" Disk shelf bay

Example: 1"""

    bytes_per_sector = Size(
        data_key="bytes_per_sector",
        allow_none=True,
    )
    r""" Bytes per sector.

Example: 520"""

    class_ = marshmallow_fields.Str(
        data_key="class",
        validate=enum_validation(['unknown', 'capacity', 'performance', 'archive', 'solid_state', 'array', 'virtual']),
        allow_none=True,
    )
    r""" Disk class

Valid choices:

* unknown
* capacity
* performance
* archive
* solid_state
* array
* virtual"""

    compliance_standard = marshmallow_fields.Str(
        data_key="compliance_standard",
        allow_none=True,
    )
    r""" Security standard that the device is certified to.

Example: FIPS 140-2"""

    container_type = marshmallow_fields.Str(
        data_key="container_type",
        validate=enum_validation(['aggregate', 'broken', 'foreign', 'labelmaint', 'maintenance', 'shared', 'spare', 'unassigned', 'unknown', 'unsupported', 'remote', 'mediator']),
        allow_none=True,
    )
    r""" Type of overlying disk container

Valid choices:

* aggregate
* broken
* foreign
* labelmaint
* maintenance
* shared
* spare
* unassigned
* unknown
* unsupported
* remote
* mediator"""

    control_standard = marshmallow_fields.Str(
        data_key="control_standard",
        allow_none=True,
    )
    r""" Standard that the device supports for encryption control.

Example: TCG Enterprise"""

    dr_node = marshmallow_fields.Nested("netapp_ontap.models.dr_node.DrNodeSchema", data_key="dr_node", unknown=EXCLUDE, allow_none=True)
    r""" The dr_node field of the disk."""

    drawer = marshmallow_fields.Nested("netapp_ontap.models.disk_drawer.DiskDrawerSchema", data_key="drawer", unknown=EXCLUDE, allow_none=True)
    r""" The drawer field of the disk."""

    effective_type = marshmallow_fields.Str(
        data_key="effective_type",
        validate=enum_validation(['ata', 'fcal', 'lun', 'msata', 'sas', 'bsas', 'ssd', 'ssd_nvm', 'ssd_zns', 'ssd_cap', 'fsas', 'vmdisk', 'unknown']),
        allow_none=True,
    )
    r""" Effective Disk type

Valid choices:

* ata
* fcal
* lun
* msata
* sas
* bsas
* ssd
* ssd_nvm
* ssd_zns
* ssd_cap
* fsas
* vmdisk
* unknown"""

    encryption_operation = marshmallow_fields.Str(
        data_key="encryption_operation",
        allow_none=True,
    )
    r""" This field should only be set as a query parameter in a PATCH operation. It is input only and won't be returned by a subsequent GET."""

    error = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.disk_error_info.DiskErrorInfoSchema", unknown=EXCLUDE, allow_none=True), data_key="error", allow_none=True)
    r""" List of disk errors information."""

    fips_certified = marshmallow_fields.Boolean(
        data_key="fips_certified",
        allow_none=True,
    )
    r""" The fips_certified field of the disk."""

    firmware_version = marshmallow_fields.Str(
        data_key="firmware_version",
        allow_none=True,
    )
    r""" The firmware_version field of the disk.

Example: NA51"""

    home_node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="home_node", unknown=EXCLUDE, allow_none=True)
    r""" The home_node field of the disk."""

    key_id = marshmallow_fields.Nested("netapp_ontap.models.disk_key_id.DiskKeyIdSchema", data_key="key_id", unknown=EXCLUDE, allow_none=True)
    r""" The key_id field of the disk."""

    local = marshmallow_fields.Boolean(
        data_key="local",
        allow_none=True,
    )
    r""" Indicates if a disk is locally attached versus being remotely attached.
A locally attached disk resides in the same proximity as the host
cluster versus been attached to the remote cluster."""

    location = marshmallow_fields.Str(
        data_key="location",
        allow_none=True,
    )
    r""" Physical location of the disk

Example: node-01"""

    model = marshmallow_fields.Str(
        data_key="model",
        allow_none=True,
    )
    r""" The model field of the disk.

Example: X421_HCOBE450A10"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Cluster-wide disk name

Example: 1.0.1"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the disk."""

    outage = marshmallow_fields.Nested("netapp_ontap.models.disk_outage.DiskOutageSchema", data_key="outage", unknown=EXCLUDE, allow_none=True)
    r""" Indicates if a disk has an entry in the failed disk registry, along with the reason for the failure."""

    overall_security = marshmallow_fields.Str(
        data_key="overall_security",
        allow_none=True,
    )
    r""" Overall Security rating, for FIPS-certified devices.

Example: Level 2"""

    paths = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.disk_path_info.DiskPathInfoSchema", unknown=EXCLUDE, allow_none=True), data_key="paths", allow_none=True)
    r""" List of paths to a disk"""

    physical_size = Size(
        data_key="physical_size",
        allow_none=True,
    )
    r""" Physical size, in units of bytes

Example: 228930"""

    pool = marshmallow_fields.Str(
        data_key="pool",
        validate=enum_validation(['pool0', 'pool1', 'failed', 'none']),
        allow_none=True,
    )
    r""" Pool to which disk is assigned

Valid choices:

* pool0
* pool1
* failed
* none"""

    protection_mode = marshmallow_fields.Str(
        data_key="protection_mode",
        validate=enum_validation(['open', 'data', 'part', 'full', 'miss']),
        allow_none=True,
    )
    r""" Mode of drive data protection and FIPS compliance. Possible values are:
- _open_ - Data is unprotected
- _data_ - Data protection only, without FIPS compliance
- _part_ - Data is unprotected; other FIPS compliance settings present
- _full_ - Full data and FIPS compliance protection
- _miss_ - Protection mode information is not available


Valid choices:

* open
* data
* part
* full
* miss"""

    rated_life_used_percent = Size(
        data_key="rated_life_used_percent",
        allow_none=True,
    )
    r""" Percentage of rated life used

Example: 10"""

    right_size_sector_count = Size(
        data_key="right_size_sector_count",
        allow_none=True,
    )
    r""" Number of usable disk sectors that remain after subtracting the right-size adjustment for this disk.

Example: 1172123568"""

    rpm = Size(
        data_key="rpm",
        allow_none=True,
    )
    r""" Revolutions per minute

Example: 15000"""

    sanitize_spare = marshmallow_fields.Boolean(
        data_key="sanitize_spare",
        allow_none=True,
    )
    r""" Confirms spare disk sanitization (non-cryptographically)."""

    sector_count = Size(
        data_key="sector_count",
        allow_none=True,
    )
    r""" Number of sectors on the disk.

Example: 1172123568"""

    self_encrypting = marshmallow_fields.Boolean(
        data_key="self_encrypting",
        allow_none=True,
    )
    r""" The self_encrypting field of the disk."""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        allow_none=True,
    )
    r""" The serial_number field of the disk.

Example: KHG2VX8R"""

    shelf = marshmallow_fields.Nested("netapp_ontap.resources.shelf.ShelfSchema", data_key="shelf", unknown=EXCLUDE, allow_none=True)
    r""" The shelf field of the disk."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['broken', 'copy', 'maintenance', 'partner', 'pending', 'present', 'reconstructing', 'removed', 'spare', 'unfail', 'zeroing']),
        allow_none=True,
    )
    r""" State

Valid choices:

* broken
* copy
* maintenance
* partner
* pending
* present
* reconstructing
* removed
* spare
* unfail
* zeroing"""

    stats = marshmallow_fields.Nested("netapp_ontap.models.disk_stats.DiskStatsSchema", data_key="stats", unknown=EXCLUDE, allow_none=True)
    r""" The stats field of the disk."""

    storage_availability_zone = marshmallow_fields.Nested("netapp_ontap.resources.storage_availability_zone.StorageAvailabilityZoneSchema", data_key="storage_availability_zone", unknown=EXCLUDE, allow_none=True)
    r""" The storage_availability_zone field of the disk."""

    storage_pool = marshmallow_fields.Nested("netapp_ontap.resources.storage_pool.StoragePoolSchema", data_key="storage_pool", unknown=EXCLUDE, allow_none=True)
    r""" The storage_pool field of the disk."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['ata', 'bsas', 'fcal', 'fsas', 'lun', 'sas', 'msata', 'ssd', 'vmdisk', 'unknown', 'ssd_cap', 'ssd_nvm', 'ssd_zns']),
        allow_none=True,
    )
    r""" Disk interface type

Valid choices:

* ata
* bsas
* fcal
* fsas
* lun
* sas
* msata
* ssd
* vmdisk
* unknown
* ssd_cap
* ssd_nvm
* ssd_zns"""

    uid = marshmallow_fields.Str(
        data_key="uid",
        allow_none=True,
    )
    r""" The unique identifier for a disk

Example: 002538E5:71B00B2F:00000000:00000000:00000000:00000000:00000000:00000000:00000000:00000000"""

    usable_size = Size(
        data_key="usable_size",
        allow_none=True,
    )
    r""" The usable_size field of the disk.

Example: 959934889984"""

    vendor = marshmallow_fields.Str(
        data_key="vendor",
        allow_none=True,
    )
    r""" The vendor field of the disk.

Example: NETAPP"""

    virtual = marshmallow_fields.Nested("netapp_ontap.models.disk_virtual.DiskVirtualSchema", data_key="virtual", unknown=EXCLUDE, allow_none=True)
    r""" Information about backing storage for disks on cloud platforms."""

    @property
    def resource(self):
        return Disk

    gettable_fields = [
        "aggregates.links",
        "aggregates.name",
        "aggregates.uuid",
        "bay",
        "bytes_per_sector",
        "class_",
        "compliance_standard",
        "container_type",
        "control_standard",
        "dr_node.name",
        "dr_node.uuid",
        "drawer",
        "effective_type",
        "error",
        "fips_certified",
        "firmware_version",
        "home_node.links",
        "home_node.name",
        "home_node.uuid",
        "key_id",
        "local",
        "location",
        "model",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "outage",
        "overall_security",
        "paths",
        "physical_size",
        "pool",
        "protection_mode",
        "rated_life_used_percent",
        "right_size_sector_count",
        "rpm",
        "sector_count",
        "self_encrypting",
        "serial_number",
        "shelf.links",
        "shelf.uid",
        "state",
        "stats",
        "storage_availability_zone.links",
        "storage_availability_zone.name",
        "storage_availability_zone.uuid",
        "storage_pool.links",
        "storage_pool.name",
        "storage_pool.uuid",
        "type",
        "uid",
        "usable_size",
        "vendor",
        "virtual",
    ]
    """aggregates.links,aggregates.name,aggregates.uuid,bay,bytes_per_sector,class_,compliance_standard,container_type,control_standard,dr_node.name,dr_node.uuid,drawer,effective_type,error,fips_certified,firmware_version,home_node.links,home_node.name,home_node.uuid,key_id,local,location,model,name,node.links,node.name,node.uuid,outage,overall_security,paths,physical_size,pool,protection_mode,rated_life_used_percent,right_size_sector_count,rpm,sector_count,self_encrypting,serial_number,shelf.links,shelf.uid,state,stats,storage_availability_zone.links,storage_availability_zone.name,storage_availability_zone.uuid,storage_pool.links,storage_pool.name,storage_pool.uuid,type,uid,usable_size,vendor,virtual,"""

    patchable_fields = [
        "encryption_operation",
        "node.name",
        "node.uuid",
        "outage",
        "pool",
        "sanitize_spare",
        "state",
        "stats",
        "virtual",
    ]
    """encryption_operation,node.name,node.uuid,outage,pool,sanitize_spare,state,stats,virtual,"""

    postable_fields = [
        "outage",
        "state",
        "stats",
        "virtual",
    ]
    """outage,state,stats,virtual,"""

class Disk(Resource):
    """Allows interaction with Disk objects on the host"""

    _schema = DiskSchema
    _path = "/api/storage/disks"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of disks.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
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
        """Returns a count of all Disk resources that match the provided query"""
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
        """Returns a list of RawResources that represent Disk resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Disk"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates disk ownership, changes authentication keys, sanitizes encrypting disks, or sanitizes non-encrypting spare disks.
### Related ONTAP commands
* `storage disk assign`
* `storage disk removeowner`
* `storage encryption disk modify -data-key-id`
* `storage encryption disk sanitize`
* `security key-manager key query -key-type NSE-AK`
* `storage disk unfail`
* `storage disk sanitize-spare`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of disks.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific disk.
### Related ONTAP commands
* `storage disk show`
* `storage encryption disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





