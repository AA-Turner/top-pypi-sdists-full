r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An NVMe namespace is a collection of addressable logical blocks presented to hosts connected to the storage virtual machine using the NVMe over Fabrics protocol.<br/>
The NVMe namespace REST API allows you to create, update, delete and discover NVMe namespaces.<br/>
An NVMe namespace must be mapped to an NVMe subsystem to grant access to the subsystem's hosts. Hosts can then access the NVMe namespace and perform I/O using the NVMe over Fabrics protocol.<br/>
See the NVMe namespace object model to learn more about each of the properties supported by the NVMe namespace REST API.
## Platform Specifics
### Unified ONTAP
An NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
NVMe namespace names are paths of the form "/vol/\<volume>[/\<qtree>]/\<namespace>" where the qtree name is optional.<br/>
An NVMe namespace is created to a specified size using thin or thick provisioning as determined by the volume on which it is created. An NVMe namespace can then be resized or cloned. An NVMe namespace cannot be renamed, or moved to a different volume. NVMe namespaces do not support the assignment of a QoS policy for performance management, but a QoS policy can be assigned to the volume containing the namespace.
### ASA r2
NVMe namespace names are simple names that share a namespace with LUNs within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.<br/>
An NVMe namespace can be created to a specified size. An NVMe namespace can then be renamed, resized, or cloned. NVMe namespaces support the assignment of a QoS policy for performance management.<br/>
**Note**: NVMe namespace related REST API examples use the Unified ONTAP form for NVMe namespace names. On ASA r2, the ASA r2 format must be used.
## Performance monitoring
Performance of an NVMe namespace can be monitored by observing the `metric.*` and `statistics.*` properties. These properties show the space utilization and performance of an NVMe namespace in terms of IOPS, latency, and throughput. The `metric.*` properties denote an average, whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
## Examples
### Creating an NVMe namespace
This example creates a 300 gigabyte NVMe namespace, with 4096-byte blocks, in SVM _svm1_, volume _vol1_, configured for use by _linux_ hosts. The `return_records` query parameter is used to retrieve properties of the newly created NVMe namespace in the POST response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeNamespace()
    resource.svm = {"name": "svm1"}
    resource.os_type = "linux"
    resource.space = {"block_size": "4096", "size": "300G"}
    resource.name = "/vol/vol1/namespace1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
NvmeNamespace(
    {
        "name": "/vol/vol1/namespace1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/storage/namespaces/dccdc3e6-cf4e-498f-bec6-f7897f945669"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/6bf967fd-2a1c-11e9-b682-005056bbc17d"}
            },
            "uuid": "6bf967fd-2a1c-11e9-b682-005056bbc17d",
        },
        "uuid": "dccdc3e6-cf4e-498f-bec6-f7897f945669",
        "location": {
            "volume": {
                "name": "vol1",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/71cd0dba-2a1c-11e9-b682-005056bbc17d"
                    }
                },
                "uuid": "71cd0dba-2a1c-11e9-b682-005056bbc17d",
            },
            "namespace": "namespace1",
        },
        "os_type": "linux",
        "status": {"read_only": False, "state": "online", "container_state": "online"},
        "space": {
            "block_size": 4096,
            "used": 0,
            "guarantee": {"requested": False, "reserved": False},
            "size": 322122547200,
        },
    }
)

```
</div>
</div>

---
### Updating an NVMe namespace comment
This example sets the `comment` property of an NVMe namespace.
<br/>
```
# The API:
PATCH /api/storage/namespaces/{uuid}
# The call:
```
### Updating the size of an NVMe namespace
This example increases the size of an NVMe namespace.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeNamespace(uuid="dccdc3e6-cf4e-498f-bec6-f7897f945669")
    resource.space = {"size": "1073741824"}
    resource.patch()

```

---
### Retrieving NVMe namespaces
This example retrieves summary information for all online NVMe namespaces in SVM _svm1_. The `svm.name` and `status.state` query parameters are to find the desired NVMe namespaces.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            NvmeNamespace.get_collection(
                **{"svm.name": "svm1", "status.state": "online"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    NvmeNamespace(
        {
            "name": "/vol/vol1/namespace2",
            "_links": {
                "self": {
                    "href": "/api/storage/namespaces/5c254d22-96a6-42ac-aad8-0cd9ebd126b6"
                }
            },
            "svm": {"name": "svm1"},
            "uuid": "5c254d22-96a6-42ac-aad8-0cd9ebd126b6",
            "status": {"state": "online"},
        }
    ),
    NvmeNamespace(
        {
            "name": "/vol/vol1/namespace1",
            "_links": {
                "self": {
                    "href": "/api/storage/namespaces/dccdc3e6-cf4e-498f-bec6-f7897f945669"
                }
            },
            "svm": {"name": "svm1"},
            "uuid": "dccdc3e6-cf4e-498f-bec6-f7897f945669",
            "status": {"state": "online"},
        }
    ),
    NvmeNamespace(
        {
            "name": "/vol/vol2/namespace3",
            "_links": {
                "self": {
                    "href": "/api/storage/namespaces/be732687-20cf-47d2-a0e2-2a989d15661d"
                }
            },
            "svm": {"name": "svm1"},
            "uuid": "be732687-20cf-47d2-a0e2-2a989d15661d",
            "status": {"state": "online"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving details for a specific NVMe namespace
In this example, the `fields` query parameter is used to request all fields, including advanced fields, that would not otherwise be returned by default for the NVMe namespace.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeNamespace(uuid="dccdc3e6-cf4e-498f-bec6-f7897f945669")
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
NvmeNamespace(
    {
        "name": "/vol/vol1/namespace1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/storage/namespaces/dccdc3e6-cf4e-498f-bec6-f7897f945669?fields=**"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/6bf967fd-2a1c-11e9-b682-005056bbc17d"}
            },
            "uuid": "6bf967fd-2a1c-11e9-b682-005056bbc17d",
        },
        "metric": {
            "status": "ok",
            "iops": {"total": 0, "write": 0, "other": 0, "read": 0},
            "latency": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:15+00:00",
            "throughput": {"total": 0, "write": 0, "read": 0},
            "duration": "PT15S",
        },
        "uuid": "dccdc3e6-cf4e-498f-bec6-f7897f945669",
        "subsystem_map": {
            "subsystem": {
                "name": "subsystem1",
                "uuid": "01f17d05-2be9-11e9-bed2-005056bbc17d",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/01f17d05-2be9-11e9-bed2-005056bbc17d"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-maps/dccdc3e6-cf4e-498f-bec6-f7897f945669/01f17d05-2be9-11e9-bed2-005056bbc17d"
                }
            },
            "nsid": "00000001h",
            "anagrpid": "00000001h",
        },
        "location": {
            "volume": {
                "name": "vol1",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/71cd0dba-2a1c-11e9-b682-005056bbc17d"
                    }
                },
                "uuid": "71cd0dba-2a1c-11e9-b682-005056bbc17d",
            },
            "namespace": "namespace1",
        },
        "os_type": "linux",
        "statistics": {
            "status": "ok",
            "iops_raw": {"total": 3, "write": 0, "other": 3, "read": 0},
            "latency_raw": {"total": 38298, "write": 0, "other": 38298, "read": 0},
            "throughput_raw": {"total": 0, "write": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:42+00:00",
        },
        "comment": "Data for the research department.",
        "status": {
            "read_only": False,
            "state": "online",
            "mapped": True,
            "container_state": "online",
        },
        "auto_delete": False,
        "space": {
            "block_size": 4096,
            "used": 0,
            "guarantee": {"requested": False, "reserved": False},
            "size": 322122547200,
        },
    }
)

```
</div>
</div>

---
## Cloning NVMe namespaces
A clone of an NVMe namespace is an independent "copy" of the namespace that shares unchanged data blocks with the original. As blocks of the source and clone are modified, unique blocks are written for each. NVMe namespace clones can be created quickly and consume very little space initially. They can be created for the purpose of back-up, or to replicate data for multiple consumers.<br/>
An NVMe namespace clone can also be set to auto-delete by setting the `auto_delete` property. If the namespace's volume is configured for automatic deletion, NVMe namespaces that have auto-delete enabled are deleted when a volume is nearly full to reclaim a target amount of free space in the volume.
### Creating a new NVMe namespace clone
You create an NVMe namespace clone as you create any NVMe namespace -- a POST to [`/storage/namespaces`](#/NVMe/nvme_namespace_create). Set `clone.source.uuid` or `clone.source.name` to identify the source NVMe namespace from which the clone is created. The NVMe namespace clone and its source must reside in the same volume.
<br/>
The source NVMe namespace can reside in a snapshot, in which case, the `clone.source.name` field must be used to identify it. Add `/.snapshot/<snapshot_name>` to the path after the volume name to identify the snapshot. For example `/vol/vol1/.snapshot/snap1/namespace1`.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeNamespace()
    resource.svm = {"name": "svm1"}
    resource.name = "/vol/vol1/namespace2clone1"
    resource.clone = {"source": {"name": "/vol/vol1/namespace2"}}
    resource.post(hydrate=True)
    print(resource)

```

---
### Over-writing an existing NVMe namespace's data as a clone of another
You can over-write an existing NVMe namespace as a clone of another. You do this as a PATCH on the NVMe namespace to overwrite -- a PATCH to [`/storage/namespaces/{uuid}`](#/NVMe/nvme_namespace_modify). Set the `clone.source.uuid` or `clone.source.name` property to identify the source NVMe namespace from which the clone data is taken. The NVMe namespace clone and its source must reside in the same volume.<br/>
When used in a PATCH, the patched NVMe namespace's data is over-written as a clone of the source and the following properties are preserved from the patched namespace unless otherwise specified as part of the PATCH: `auto_delete`, `subsystem_map`, `status.state`, and `uuid`.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeNamespace(uuid="dccdc3e6-cf4e-498f-bec6-f7897f945669")
    resource.clone = {"source": {"name": "/vol/vol1/namespace2"}}
    resource.patch()

```

---
## Converting a LUN into an NVMe namespace
An existing LUN can be converted in-place to an NVMe namespace with no modification to the data blocks. In other words, there is no additional copy created for the data blocks. There are certain requirements when converting a LUN to an NVMe namespace. For instance, the LUN should not be mapped to an initiator group, or exist as a protocol endpoint LUN, or in a foreign LUN import relationship. If the LUN exists as a VM volume, it should not be bound to a protocol endpoint LUN. Furthermore, only LUN with a supported operating system type for NVMe namespace can be converted.<br/>
The conversion process updates the metadata to the LUN, making it an NVMe namespace. The conversion is both time and space efficient. After conversion, the new namespace behaves as a regular namespace and may be mapped to an NVMe subsystem.
### Convert a LUN into an NVMe namespace
You convert a LUN into an NVMe namespace by calling a POST to [`/storage/namespaces`](#/NVMe/nvme_namespace_create). Set `convert.lun.uuid` or `convert.lun.name` to identify the source LUN which is to be converted in-place into an NVMe namespace.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeNamespace()
    resource.svm = {"name": "svm1"}
    resource.convert = {"lun": {"name": "/vol/vol1/lun1"}}
    resource.post(hydrate=True)
    print(resource)

```

---
## Deleting an NVMe namespace
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeNamespace

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeNamespace(uuid="5c254d22-96a6-42ac-aad8-0cd9ebd126b6")
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


__all__ = ["NvmeNamespace", "NvmeNamespaceSchema"]
__pdoc__ = {
    "NvmeNamespaceSchema.resource": False,
    "NvmeNamespaceSchema.opts": False,
}


class NvmeNamespaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeNamespace object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nvme_namespace."""

    auto_delete = marshmallow_fields.Boolean(
        data_key="auto_delete",
        allow_none=True,
    )
    r""" * **Unified ONTAP**:
This property marks the NVMe namespace for auto deletion when the volume containing the namespace runs out of space. This is most commonly set on namespace clones.<br/>
When set to _true_, the NVMe namespace becomes eligible for automatic deletion when the volume runs out of space. Auto deletion only occurs when the volume containing the namespace is also configured for auto deletion and free space in the volume decreases below a particular threshold.<br/>
This property is optional in POST and PATCH. The default value for a new NVMe namespace is _false_.<br/>
There is an added computational cost to retrieving this property's value. It is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.

* **ASA r2**:
This property is not supported. It cannot be set in POST or PATCH and will not be returned by GET."""

    clone = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_clone.NvmeNamespaceCloneSchema", data_key="clone", unknown=EXCLUDE, allow_none=True)
    r""" * **Unified ONTAP**:
This sub-object is used in POST to create a new NVMe namespace as a clone of an existing namespace, or PATCH to overwrite an existing namespace as a clone of another. Setting a property in this sub-object indicates that a namespace clone is desired.<br/>
When used in a PATCH, the patched NVMe namespace's data is over-written as a clone of the source and the following properties are preserved from the patched namespace unless otherwise specified as part of the PATCH: `auto_delete` (unless specified in the request), `subsystem_map`, `status.state`, and `uuid`.

* **ASA r2**:
This endpoint does not support clones. No properties in this sub-object can be set for POST or PATCH and none will be returned by GET.<br/>
Cloning is supported through the /api/storage/storage-units endpoint. See the [`POST /ap/storage/storage-units`](#/SAN/storage_unit_create) to learn more about cloning NVMe namespaces."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" A configurable comment available for use by the administrator. Valid in POST and PATCH."""

    consistency_group = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_consistency_group.NvmeNamespaceConsistencyGroupSchema", data_key="consistency_group", unknown=EXCLUDE, allow_none=True)
    r""" The namespace's consistency group. This property is populated for namespaces that are members of a consistency group. If the namespace is a member of a child consistency group, the parent consistency group is reported.
### Platform Specifics

* **Unified ONTAP**: A namespace's consistency group is the consistency group of its containing volume.
* **ASA r2**: A namespace is optionally associated directly with a consistency group."""

    convert = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_convert.NvmeNamespaceConvertSchema", data_key="convert", unknown=EXCLUDE, allow_none=True)
    r""" This sub-object is used in POST to convert a valid in-place LUN to an NVMe namespace. Setting a property in this sub-object indicates that a conversion from the specified LUN to NVMe namespace is desired.<br/>"""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The time the NVMe namespace was created.

Example: 2018-06-04T19:00:00.000+0000"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The enabled state of the NVMe namespace. Certain error conditions cause the namespace to become disabled. If the namespace is disabled, check the `status.state` property to determine what error disabled the namespace. An NVMe namespace is enabled automatically when it is created."""

    encryption = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_encryption.StorageUnitEncryptionSchema", data_key="encryption", unknown=EXCLUDE, allow_none=True)
    r""" The encryption field of the nvme_namespace."""

    location = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_location.NvmeNamespaceLocationSchema", data_key="location", unknown=EXCLUDE, allow_none=True)
    r""" The location of the NVMe namespace within the ONTAP cluster.
### Platform Specifics

* **Unified ONTAP**:
NVMe namespaces do not support rename, or movement between volumes. Valid in POST.

* **ASA r2**:
The NVMe namespace name can be changed by PATCHing the `name` property. The `location` properties are read-only."""

    metric = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_reduced_throughput.PerformanceMetricReducedThroughputSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the NVMe namespace.
### Platform Specifics

* **Unified ONTAP**:
An NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
NVMe namespace names are paths of the form "/vol/\<volume>[/\<qtree>]/\<namespace>" where the qtree name is optional.<br/>
Renaming an NVMe namespace is not supported. Valid in POST.

* **ASA r2**:
NVMe namespace names are simple names that share a namespace with LUNs within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.<br/>
Renaming an NVMe namespace is supported. Valid in POST and PATCH.


Example: /vol/volume1/qtree1/namespace1"""

    os_type = marshmallow_fields.Str(
        data_key="os_type",
        validate=enum_validation(['aix', 'linux', 'vmware', 'windows']),
        allow_none=True,
    )
    r""" The operating system type of the NVMe namespace.<br/>
Required in POST when creating an NVMe namespace that is not a clone of another. Disallowed in POST when creating a namespace clone.


Valid choices:

* aix
* linux
* vmware
* windows"""

    provisioning_options = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_provisioning_options.NvmeNamespaceProvisioningOptionsSchema", data_key="provisioning_options", unknown=EXCLUDE, allow_none=True)
    r""" Options that are applied to the operation."""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_qos_policy.NvmeNamespaceQosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The QoS policy for the NVMe namspace. Both traditional and adaptive QoS policies are supported. If both property `qos_policy.uuid` and `qos_policy.name` are specified in the same request, they must refer to the same QoS policy. To remove the QoS policy from an NVMe namspace, leaving it with no QoS policy, set property `qos_policy.name` to an empty string ("") in a PATCH request. Valid in POST and PATCH.
### Platform Specifics

* **Unified ONTAP**: These properties are not available on the NVMe namespace object in the REST API and are not reported for GET requests. You can set a QoS policy on the containing volume.
* **ASA r2**: An NVMe namespace is optionally associated directly with a QoS policy. To remove the QoS policy, set it to `null` in a PATCH request."""

    space = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_space.NvmeNamespaceSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The storage space related properties of the NVMe namespace."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_reduced_throughput.PerformanceMetricRawReducedThroughputSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" These are raw performance numbers, such as IOPS latency and throughput. These numbers are aggregated across all nodes in the cluster and increase with the uptime of the cluster."""

    status = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_status.NvmeNamespaceStatusSchema", data_key="status", unknown=EXCLUDE, allow_none=True)
    r""" Status information about the NVMe namespace."""

    subsystem_map = marshmallow_fields.Nested("netapp_ontap.models.nvme_namespace_subsystem_map.NvmeNamespaceSubsystemMapSchema", data_key="subsystem_map", unknown=EXCLUDE, allow_none=True)
    r""" The NVMe subsystem with which the NVMe namespace is associated. A namespace can be mapped to zero (0) or one (1) subsystems.<br/>
There is an added computational cost to retrieving property values for `subsystem_map`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
### Platform Specifics

* **Unified ONTAP**: These properties are supported only for GET.
* **ASA r2**: These properties are supported for GET and POST. During POST, a new or existing subsystem can be referenced. When referencing an existing subsystem, only the `name` and `uuid` properties are supported."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nvme_namespace."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the NVMe namespace.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return NvmeNamespace

    gettable_fields = [
        "links",
        "auto_delete",
        "comment",
        "consistency_group",
        "create_time",
        "enabled",
        "encryption",
        "location",
        "metric",
        "name",
        "os_type",
        "qos_policy",
        "space",
        "statistics",
        "status",
        "subsystem_map",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,auto_delete,comment,consistency_group,create_time,enabled,encryption,location,metric,name,os_type,qos_policy,space,statistics,status,subsystem_map,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "auto_delete",
        "clone",
        "comment",
        "name",
        "qos_policy",
        "space",
    ]
    """auto_delete,clone,comment,name,qos_policy,space,"""

    postable_fields = [
        "auto_delete",
        "clone",
        "comment",
        "convert",
        "location",
        "name",
        "os_type",
        "provisioning_options",
        "qos_policy",
        "space",
        "subsystem_map",
        "svm.name",
        "svm.uuid",
    ]
    """auto_delete,clone,comment,convert,location,name,os_type,provisioning_options,qos_policy,space,subsystem_map,svm.name,svm.uuid,"""

class NvmeNamespace(Resource):
    r""" An NVMe namespace is a collection of addressable logical blocks presented to hosts connected to the storage virtual machine using the NVMe over Fabrics protocol.<br/>
An NVMe namespace must be mapped to an NVMe subsystem to grant access to the subsystem's hosts. Hosts can then access the NVMe namespace and perform I/O using the NVMe over Fabrics protocol.<br/>
See the NVMe namespace object model to learn more about each of the properties supported by the NVMe namespace REST API.
## Platform Specifics
### Unified ONTAP
An NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
NVMe namespace names are paths of the form "/vol/\<volume>[/\<qtree>]/\<namespace>" where the qtree name is optional.<br/>
An NVMe namespace is created to a specified size using thin or thick provisioning as determined by the volume on which it is created. An NVMe namespace can then be resized or cloned. An NVMe namespace cannot be renamed, or moved to a different volume. NVMe namespaces do not support the assignment of a QoS policy for performance management, but a QoS policy can be assigned to the volume containing the namespace.
### ASA r2
NVMe namespace names are simple names that share a namespace with LUNs within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.<br/>
An NVMe namespace can be created to a specified size. An NVMe namespace can then be renamed, resized, or cloned. NVMe namespaces support the assignment of a QoS policy for performance management.<br/>
**Note**: NVMe namespace related REST API examples use the Unified ONTAP form for NVMe namespace names. On ASA r2, the ASA r2 format must be used. """

    _schema = NvmeNamespaceSchema
    _path = "/api/storage/namespaces"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NVMe namespaces.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `auto_delete`
* `space.physical_used`
* `space.physical_used_by_snapshots`
* `space.efficiency_ratio`
* `subsystem_map.*`
* `status.mapped`
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver nvme namespace show`
* `vserver nvme subsystem map show`
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces) to learn more and examples.
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
        """Returns a count of all NvmeNamespace resources that match the provided query"""
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
        """Returns a list of RawResources that represent NvmeNamespace resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NvmeNamespace"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an NVMe namespace.
### Related ONTAP commands
* `volume file clone autodelete`
* `vserver nvme namespace modify`
### Platform Specifics
* **ASA r2**: PATCH is asynchronous when modifying `name` or `qos_policy`.
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["NvmeNamespace"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NvmeNamespace"], NetAppResponse]:
        r"""Creates an NVMe namespace.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the NVMe namespace.
* `name`, `location.volume.name` or `location.volume.uuid` - Existing volume in which to create the NVMe namespace.
* `name` or `location.namespace` - Base name for the NVMe namespace.
* `os_type` - Operating system from which the NVMe namespace will be accessed. (Not used for clones, which are created based on the `os_type` of the source NVMe namespace.)
* `space.size` - Size for the NVMe namespace. (Not used for clones, which are created based on the size of the source NVMe namespace.)
### Default property values
If not specified in POST, the following default property values are assigned:
* `auto_delete` - _false_
* `space.block_size` - _4096_ ( _512_ when 'os_type' is _vmware_ )
### Related ONTAP commands
* `volume file clone autodelete`
* `volume file clone create`
* `vserver nvme namespace convert-from-lun`
* `vserver nvme namespace create`
### Platform Specifics
* **ASA r2**: The `name` property is required when creating a new namespace. The name must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 203 characters or less in length. The `location` properties are not supported.
POST is asynchronous when creating a new namespace. It is synchronous when converting a LUN to a namespace via the `convert` property.
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["NvmeNamespace"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an NVMe namespace.
### Related ONTAP commands
* `vserver nvme namespace delete`
### Platform Specifics
* **ASA r2**: DELETE is asynchronous.
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NVMe namespaces.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `auto_delete`
* `space.physical_used`
* `space.physical_used_by_snapshots`
* `space.efficiency_ratio`
* `subsystem_map.*`
* `status.mapped`
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver nvme namespace show`
* `vserver nvme subsystem map show`
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces) to learn more and examples.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NVMe namespace.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `auto_delete`
* `space.physical_used`
* `space.physical_used_by_snapshots`
* `space.efficiency_ratio`
* `subsystem_map.*`
* `status.mapped`
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver nvme namespace show`
* `vserver nvme subsystem map show`
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces)
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
        r"""Creates an NVMe namespace.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the NVMe namespace.
* `name`, `location.volume.name` or `location.volume.uuid` - Existing volume in which to create the NVMe namespace.
* `name` or `location.namespace` - Base name for the NVMe namespace.
* `os_type` - Operating system from which the NVMe namespace will be accessed. (Not used for clones, which are created based on the `os_type` of the source NVMe namespace.)
* `space.size` - Size for the NVMe namespace. (Not used for clones, which are created based on the size of the source NVMe namespace.)
### Default property values
If not specified in POST, the following default property values are assigned:
* `auto_delete` - _false_
* `space.block_size` - _4096_ ( _512_ when 'os_type' is _vmware_ )
### Related ONTAP commands
* `volume file clone autodelete`
* `volume file clone create`
* `vserver nvme namespace convert-from-lun`
* `vserver nvme namespace create`
### Platform Specifics
* **ASA r2**: The `name` property is required when creating a new namespace. The name must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 203 characters or less in length. The `location` properties are not supported.
POST is asynchronous when creating a new namespace. It is synchronous when converting a LUN to a namespace via the `convert` property.
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces)
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
        r"""Updates an NVMe namespace.
### Related ONTAP commands
* `volume file clone autodelete`
* `vserver nvme namespace modify`
### Platform Specifics
* **ASA r2**: PATCH is asynchronous when modifying `name` or `qos_policy`.
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces)
"""
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
        r"""Deletes an NVMe namespace.
### Related ONTAP commands
* `vserver nvme namespace delete`
### Platform Specifics
* **ASA r2**: DELETE is asynchronous.
### Learn more
* [`DOC /storage/namespaces`](#docs-NVMe-storage_namespaces)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


