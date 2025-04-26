r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Storage units is an aggregated view of LUNs and NVMe namespaces. See [`/storage/luns`](#docs-SAN-storage_luns) or [`/storage/namespaces`](#docs-NVMe-storage_namespaces) to learn more about each storage unit type.<br/>
The storage unit REST API allows you to clone, restore, and discover storage units.<br/>
## Platform Specifics
### Unified ONTAP
This endpoint is not available.
## Examples
### Retrieving storage units
This example retrieves summary information for all online storage units. The `status.state` query parameter is used to find the desired storage units.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageUnit.get_collection(**{"status.state": "online"})))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StorageUnit(
        {
            "name": "lun1",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b"
                }
            },
            "uuid": "9034e72c-1d07-11ef-bd09-005056bbbc7b",
            "status": {"state": "online"},
        }
    ),
    StorageUnit(
        {
            "name": "ns1",
            "_links": {
                "self": {
                    "href": "/api/storage/storage-units/3d9c001f-227e-11ef-97b9-005056bbbc7b"
                }
            },
            "uuid": "3d9c001f-227e-11ef-97b9-005056bbbc7b",
            "status": {"state": "online"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving details for a specific storage unit
In this example, the `fields` query parameter is used to request all fields, including advanced fields, that would not otherwise be returned by default for the storage unit.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnit(uuid="9034e72c-1d07-11ef-bd09-005056bbbc7b")
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
StorageUnit(
    {
        "name": "lun1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/storage/storage-units/9034e72c-1d07-11ef-bd09-005056bbbc7b?fields=**"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/7cb65b79-1a0f-11ef-bd09-005056bbbc7b"}
            },
            "uuid": "7cb65b79-1a0f-11ef-bd09-005056bbbc7b",
        },
        "clone": {"is_flexclone": False},
        "uuid": "9034e72c-1d07-11ef-bd09-005056bbbc7b",
        "class": "regular",
        "create_time": "2024-05-28T11:33:03-04:00",
        "location": {
            "volume": {
                "name": "lun1",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/906d2f70-1d07-11ef-bd09-005056bbbc7b"
                    }
                },
                "uuid": "906d2f70-1d07-11ef-bd09-005056bbbc7b",
            },
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/7925ce48-1a0e-11ef-bd09-005056bbbc7b"
                    }
                },
                "uuid": "7925ce48-1a0e-11ef-bd09-005056bbbc7b",
            },
        },
        "os_type": "linux",
        "status": {
            "read_only": False,
            "state": "online",
            "mapped": False,
            "container_state": "online",
        },
        "serial_number": "z-iC3$WZtL1H",
        "space": {
            "efficiency_ratio": 1.0,
            "physical_used_by_snapshots": 3248128,
            "used": 0,
            "physical_used": 28672,
            "size": 10485760,
        },
        "encryption": {"state": "unencrypted"},
        "type": "lun",
    }
)

```
</div>
</div>

---
### Restoring a storage unit from a snapshot
A snapshot restore operation is initiated by PATCH request to [`/storage/storage-units/{uuid}`](#/SAN/storage_unit_modify). Set `restore_to.snapshot.uuid` or `restore_to.snapshot.name` to identify the source snapshot to restore the storage unit to in order to begin the operation.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnit

with HostConnection("10.63.26.53", username="admin", password="password", verify=False):
    resource = StorageUnit(uuid="eaebc659-237b-11ef-a1bc-005056bbf4ce")
    resource.patch(
        hydrate=True, return_timeout=90, **{"restore_to.snapshot.name": "mySnap"}
    )

```

---
## Cloning storage units
A clone of a storage unit is an independent "copy" of the storage unit that shares unchanged data blocks with the original. As blocks of the source and the clone are modified, unique blocks are written for each. Storage unit clones can be created quickly and consume very little space initially. They can be created for the purpose of back-up, or to replicate data for multiple consumers.<br/>
### Creating a new storage unit clone
You create a new storage unit clone by POST request to [`/storage/storage-units/`](#/SAN/storage_unit_create). Set `clone.source.storage_unit.uuid` or `clone.source.storage_unit.name` to identify the source storage unit from which the clone is created. The storage unit clone and its source must reside on the same SVM.<br/>
The source storage unit can reside in a snapshot, in which case the `clone.source.snapshot.name` field must be used to identify it.<br/>
By default, storage unit clones do not inherit the Quality of Service (QoS) policy of the source storage unit; a QoS policy should be set for the clone by setting the `qos_policy` property by PATCH request to [`/storage/luns/`](#/SAN/lun_modify) or [`/storage/namespaces/`](#/NVMe/nvme_namespace_modify)<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnit()
    resource.clone = {
        "source": {"storage_unit": {"name": "lun1"}, "svm": {"name": "svm1"}}
    }
    resource.svm = {"name": "svm1"}
    resource.name = "lun1Clone1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
StorageUnit(
    {
        "name": "lun1Clone1",
        "svm": {"name": "svm1"},
        "clone": {
            "source": {"svm": {"name": "svm1"}, "storage_unit": {"name": "lun1"}}
        },
    }
)

```
</div>
</div>

---
### Splitting a storage unit clone
A clone split operation is initiated by PATCH request to [`/storage/storage-units/{uuid}`](#/SAN/storage_unit_modify). Set the `clone.split_initiated` property to `true` to initiate the clone split operation. The clone split operation is asynchronous and might take some time to complete. The clone split operation is complete when the `clone.split_initiated` property is set to `false`.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StorageUnit(uuid="9034e72c-1d07-11ef-bd09-005056bbbc7b")
    resource.clone = {"split_initiated": "true"}
    resource.patch()

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


__all__ = ["StorageUnit", "StorageUnitSchema"]
__pdoc__ = {
    "StorageUnitSchema.resource": False,
    "StorageUnitSchema.opts": False,
}


class StorageUnitSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnit object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the storage_unit."""

    class_ = marshmallow_fields.Str(
        data_key="class",
        validate=enum_validation(['regular', 'vvol']),
        allow_none=True,
    )
    r""" The class of LUN.


Valid choices:

* regular
* vvol"""

    clone = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_clone.StorageUnitCloneSchema", data_key="clone", unknown=EXCLUDE, allow_none=True)
    r""" The clone field of the storage_unit."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" A configurable comment available for use by the administrator."""

    consistency_group = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_consistency_group.StorageUnitConsistencyGroupSchema", data_key="consistency_group", unknown=EXCLUDE, allow_none=True)
    r""" The storage unit's consistency group. This property is populated for storage units that are members of a consistency group."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The time the storage unit was created.


Example: 2018-06-04T19:00:00.000+0000"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The enabled state of the storage unit. Storage units can be disabled to prevent access to the storage unit. Certain error conditions also cause the storage unit to become disabled. If the storage unit is disabled, check the `status.state` property to determine if the storage unit is administratively disabled (_offline_) or has become disabled as a result of an error.<br/>
A storage unit in an error condition can be brought online by setting the `enabled` property to _true_ or brought administratively offline by setting the `enabled` property to _false_ using /api/storage/luns or /api/storage/namespaces. Upon creation, a storage unit is enabled by default."""

    encryption = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_encryption.StorageUnitEncryptionSchema", data_key="encryption", unknown=EXCLUDE, allow_none=True)
    r""" The encryption field of the storage_unit."""

    location = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_location.StorageUnitLocationSchema", data_key="location", unknown=EXCLUDE, allow_none=True)
    r""" The location field of the storage_unit."""

    maps = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.storage_unit_maps.StorageUnitMapsSchema", unknown=EXCLUDE, allow_none=True), data_key="maps", allow_none=True)
    r""" Maps between the storage unit and host groups."""

    metric = marshmallow_fields.Nested("netapp_ontap.resources.performance_metric.PerformanceMetricSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput."""

    movement = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_movement.StorageUnitMovementSchema", data_key="movement", unknown=EXCLUDE, allow_none=True)
    r""" The properties of a storage unit move operation from one storage availability zone to another."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the storage unit. The name must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 203 characters or less in length. Valid in POST.


Example: lun1"""

    os_type = marshmallow_fields.Str(
        data_key="os_type",
        validate=enum_validation(['aix', 'hpux', 'hyper_v', 'linux', 'netware', 'openvms', 'solaris', 'solaris_efi', 'vmware', 'windows', 'windows_2008', 'windows_gpt', 'xen']),
        allow_none=True,
    )
    r""" The operating system type of the storage unit.<br/>


Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* solaris_efi
* vmware
* windows
* windows_2008
* windows_gpt
* xen"""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_qos_policy.StorageUnitQosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The QoS policy for the storage unit. Both traditional and adaptive QoS policies are supported."""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        validate=len_validation(minimum=12, maximum=12),
        allow_none=True,
    )
    r""" The LUN serial number. The serial number is generated by ONTAP when the LUN is created."""

    space = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_space.StorageUnitSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The storage space related properties of the storage unit."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw.PerformanceMetricRawSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the storage_unit."""

    status = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_status.StorageUnitStatusSchema", data_key="status", unknown=EXCLUDE, allow_none=True)
    r""" Status information about the storage unit."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the storage_unit."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['lun', 'namespace']),
        allow_none=True,
    )
    r""" The type of storage unit.


Valid choices:

* lun
* namespace"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the storage unit. The UUID is generated by ONTAP when the storage unit is created. The storage unit UUID is the same as the LUN or namespace UUID.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return StorageUnit

    gettable_fields = [
        "links",
        "class_",
        "clone",
        "comment",
        "consistency_group",
        "create_time",
        "enabled",
        "encryption",
        "location",
        "maps",
        "metric",
        "movement",
        "name",
        "os_type",
        "qos_policy",
        "serial_number",
        "space",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "status",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """links,class_,clone,comment,consistency_group,create_time,enabled,encryption,location,maps,metric,movement,name,os_type,qos_policy,serial_number,space,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,status,svm.links,svm.name,svm.uuid,type,uuid,"""

    patchable_fields = [
        "clone",
        "location",
        "movement",
    ]
    """clone,location,movement,"""

    postable_fields = [
        "clone",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """clone,name,svm.name,svm.uuid,"""

class StorageUnit(Resource):
    r""" A storage unit representing either a LUN or a namespace. """

    _schema = StorageUnitSchema
    _path = "/api/storage/storage-units"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves storage units.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `clone.inherited_physical_used`
* `clone.inherited_savings`
* `clone.match_source_storage_tier`
* `clone.source.snapshot.name`
* `clone.source.snapshot.uuid`
* `clone.split_complete_percent`
* `clone.split_estimate`
* `clone.split_initiated`
* `maps.*`
* `metric.*`
* `movement.percent_complete`
* `movement.start_time`
* `space.physical_used_by_snapshots`
* `space.physical_used`
* `statistics.*`
### Learn more
* [`DOC /storage/storage-units`](#docs-SAN-storage_storage-units)
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
        """Returns a count of all StorageUnit resources that match the provided query"""
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
        """Returns a list of RawResources that represent StorageUnit resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["StorageUnit"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modify an existing storage unit.<br/>
Storage unit modification supports the following:
* `restore_to` - Restores the storage unit to a prior snapshot. These properties are specified in the query.
* `clone.split_initiated` - Initiates a clone split operation.
### Learn more
* [`DOC /storage/storage-units`](#docs-SAN-storage_storage-units)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["StorageUnit"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["StorageUnit"], NetAppResponse]:
        r"""Creates a storage unit.<br/>
A storage unit can only be directly created as a clone of an existing storage unit. To create a new storage unit that is not a clone of another, use /api/storage/luns or /api/storage/namespaces.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the storage unit.
* `name` - The name of the storage unit.
* `clone` - Identifiers of the parent storage unit or storage unit snapshot from which to clone a new storage unit.
### Learn more
* [`DOC /storage/storage-units`](#docs-SAN-storage_storage-units)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves storage units.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `clone.inherited_physical_used`
* `clone.inherited_savings`
* `clone.match_source_storage_tier`
* `clone.source.snapshot.name`
* `clone.source.snapshot.uuid`
* `clone.split_complete_percent`
* `clone.split_estimate`
* `clone.split_initiated`
* `maps.*`
* `metric.*`
* `movement.percent_complete`
* `movement.start_time`
* `space.physical_used_by_snapshots`
* `space.physical_used`
* `statistics.*`
### Learn more
* [`DOC /storage/storage-units`](#docs-SAN-storage_storage-units)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a storage unit's properties.<br/>
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `clone.inherited_physical_used`
* `clone.inherited_savings`
* `clone.match_source_storage_tier`
* `clone.source.snapshot.name`
* `clone.source.snapshot.uuid`
* `clone.split_complete_percent`
* `clone.split_estimate`
* `clone.split_initiated`
* `maps.*`
* `metric.*`
* `movement.percent_complete`
* `movement.start_time`
* `space.physical_used_by_snapshots`
* `space.physical_used`
* `statistics.*`
### Learn more
* [`DOC /storage/storage-units`](#docs-SAN-storage_storage-units)
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
        r"""Creates a storage unit.<br/>
A storage unit can only be directly created as a clone of an existing storage unit. To create a new storage unit that is not a clone of another, use /api/storage/luns or /api/storage/namespaces.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the storage unit.
* `name` - The name of the storage unit.
* `clone` - Identifiers of the parent storage unit or storage unit snapshot from which to clone a new storage unit.
### Learn more
* [`DOC /storage/storage-units`](#docs-SAN-storage_storage-units)
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
        r"""Modify an existing storage unit.<br/>
Storage unit modification supports the following:
* `restore_to` - Restores the storage unit to a prior snapshot. These properties are specified in the query.
* `clone.split_initiated` - Initiates a clone split operation.
### Learn more
* [`DOC /storage/storage-units`](#docs-SAN-storage_storage-units)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



