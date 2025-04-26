r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A LUN is the logical representation of storage in a storage area network (SAN).<br/>
The LUN REST API allows you to create, update, delete, and discover LUNs.<br/>
A LUN must be mapped to an initiator group to grant access to the initiator group's initiators (client hosts). Initiators can then access the LUN and perform I/O over a Fibre Channel (FC) fabric using the FC Protocol or a TCP/IP network using iSCSI.<br/>
See the LUN object model to learn more about each of the properties supported by the LUN REST API.
## Platform Specifics
### Unified ONTAP
A LUN is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
LUN names are paths of the form "/vol/\<volume>[/\<qtree>]/\<lun>" where the qtree name is optional.<br/>
A LUN can be created to a specified size using thin or thick provisioning. A LUN can then be renamed, resized, cloned, moved to a different volume and copied. LUNs support the assignment of a QoS policy for performance management or a QoS policy can be assigned to a volume containing one or more LUNs.
### ASA r2
LUN names are simple names that share a namespace with NVMe namespaces within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.<br/>
A LUN can be created to a specified size. A LUN can then be renamed, resized, or cloned. LUNs support the assignment of a QoS policy for performance management.<br/>
**Note**: LUN related REST API examples use the Unified ONTAP form for LUN names. On ASA r2, the ASA r2 format must be used.
## Performance monitoring
Performance of a LUN can be monitored by observing the `metric.*` and `statistics.*` properties. These properties show the space utilization and performance of a LUN in terms of IOPS, latency and throughput. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
## Examples
### Creating a LUN
This example creates a 300 gigabyte, thin-provisioned LUN in SVM _svm1_, volume _vol1_, configured for use by _linux_ initiators. The `return_records` query parameter is used to retrieve properties of the newly created LUN in the POST response.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun()
    resource.svm = {"name": "svm1"}
    resource.os_type = "linux"
    resource.space = {"size": "300G"}
    resource.name = "/vol/vol1/lun1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Lun(
    {
        "name": "/vol/vol1/lun1",
        "enabled": True,
        "_links": {
            "self": {"href": "/api/storage/luns/5a24ae5b-28af-47fb-b129-5adf6cfba0a6"}
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/6bf967fd-2a1c-11e9-b682-005056bbc17d"}
            },
            "uuid": "6bf967fd-2a1c-11e9-b682-005056bbc17d",
        },
        "uuid": "5a24ae5b-28af-47fb-b129-5adf6cfba0a6",
        "class": "regular",
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
            "logical_unit": "lun1",
        },
        "os_type": "linux",
        "status": {"read_only": False, "state": "online", "container_state": "online"},
        "serial_number": "wf0Iq+N4uck3",
        "space": {
            "used": 0,
            "scsi_thin_provisioning_support_enabled": True,
            "guarantee": {"requested": False, "reserved": False},
            "size": 322163441664,
        },
    }
)

```
</div>
</div>

### Updating a LUN
This example sets the `comment` property of a LUN.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="5a24ae5b-28af-47fb-b129-5adf6cfba0a6")
    resource.comment = "Data for the finance department."
    resource.patch()

```

### Retrieving LUNs
This example retrieves summary information for all online LUNs in SVM _svm1_. The `svm.name` and `status.state` query parameters are used to find the desired LUNs.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Lun.get_collection(**{"svm.name": "svm1", "status.state": "online"})))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    Lun(
        {
            "name": "/vol/vol1/lun1",
            "_links": {
                "self": {
                    "href": "/api/storage/luns/5a24ae5b-28af-47fb-b129-5adf6cfba0a6"
                }
            },
            "svm": {"name": "svm1"},
            "uuid": "5a24ae5b-28af-47fb-b129-5adf6cfba0a6",
            "status": {"state": "online"},
        }
    ),
    Lun(
        {
            "name": "/vol/vol1/lun2",
            "_links": {
                "self": {
                    "href": "/api/storage/luns/c903a978-9bac-4ce9-8237-4a3ba8b13f08"
                }
            },
            "svm": {"name": "svm1"},
            "uuid": "c903a978-9bac-4ce9-8237-4a3ba8b13f08",
            "status": {"state": "online"},
        }
    ),
    Lun(
        {
            "name": "/vol/vol2/lun3",
            "_links": {
                "self": {
                    "href": "/api/storage/luns/7faf0a9e-0a47-4876-8318-3638d5da16bf"
                }
            },
            "svm": {"name": "svm1"},
            "uuid": "7faf0a9e-0a47-4876-8318-3638d5da16bf",
            "status": {"state": "online"},
        }
    ),
]

```
</div>
</div>

### Retrieving details for a specific LUN
In this example, the `fields` query parameter is used to request all fields, including advanced fields, that would not otherwise be returned by default for the LUN.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="5a24ae5b-28af-47fb-b129-5adf6cfba0a6")
    resource.get(fields="**")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Lun(
    {
        "name": "/vol/vol1/lun1",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/storage/luns/5a24ae5b-28af-47fb-b129-5adf6cfba0a6?fields=**"
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
            "throughput": {"total": 0, "write": 0, "other": 0, "read": 0},
            "duration": "PT15S",
        },
        "consistency_group": {
            "name": "vol1",
            "_links": {
                "self": {
                    "href": "/api/application/consistency-groups/6d657aaf-b57a-5396-82ea-c01329e46c79"
                }
            },
            "uuid": "6d657aaf-b57a-5396-82ea-c01329e46c79",
        },
        "vvol": {
            "bindings": [
                {
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/vvol-bindings/353c7262-be4b-4176-acf3-f1021faa8b64/5a24ae5b-28af-47fb-b129-5adf6cfba0a6"
                        }
                    },
                    "id": 4304512,
                    "partner": {
                        "name": "/vol/vol1/pelun1",
                        "_links": {
                            "self": {
                                "href": "/api/storage/luns/353c7262-be4b-4176-acf3-f1021faa8b64"
                            }
                        },
                        "uuid": "353c7262-be4b-4176-acf3-f1021faa8b64",
                    },
                }
            ],
            "is_bound": True,
        },
        "uuid": "5a24ae5b-28af-47fb-b129-5adf6cfba0a6",
        "class": "vvol",
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
            "logical_unit": "lun1",
        },
        "os_type": "linux",
        "statistics": {
            "status": "ok",
            "iops_raw": {"total": 3, "write": 0, "other": 3, "read": 0},
            "latency_raw": {"total": 38298, "write": 0, "other": 38298, "read": 0},
            "throughput_raw": {"total": 0, "write": 0, "other": 0, "read": 0},
            "timestamp": "2019-04-09T05:50:42+00:00",
        },
        "comment": "Data for the finance department.",
        "status": {
            "read_only": False,
            "state": "online",
            "mapped": True,
            "container_state": "online",
        },
        "auto_delete": False,
        "serial_number": "wf0Iq+N4uck3",
        "lun_maps": [
            {
                "igroup": {
                    "name": "ig1",
                    "uuid": "2b9d57e1-2a66-11e9-b682-005056bbc17d",
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/2b9d57e1-2a66-11e9-b682-005056bbc17d"
                        }
                    },
                },
                "logical_unit_number": 0,
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/lun-maps/5a24ae5b-28af-47fb-b129-5adf6cfba0a6/2b9d57e1-2a66-11e9-b682-005056bbc17d"
                    }
                },
            }
        ],
        "space": {
            "used": 0,
            "scsi_thin_provisioning_support_enabled": True,
            "guarantee": {"requested": False, "reserved": False},
            "size": 322163441664,
        },
    }
)

```
</div>
</div>

### Deleting a LUN
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="c903a978-9bac-4ce9-8237-4a3ba8b13f08")
    resource.delete()

```

---
## LUN data
The LUN REST API also supports reading data from and writing data to a LUN via the REST API as multipart/form-data.<br/>
Reading data is performed using a GET request on the LUN endpoint. The request header must include `Accept: multipart/form-data`. When this header entry is provided, query parameters `data.offset` and `data.size` are required and used to specify the portion of the LUN's data to read; no other query parameters are allowed. Reads are limited to one megabyte (1MB) per request. Data is returned as `multipart/form-data` content with exactly one form entry containing the data. The form entry has content type `application/octet-stream`.<br/>
Writing data is performed using a PATCH request on the LUN endpoint. The request header must include `Content-Type: multipart/form-data`. When this header entry is provided, query parameter `data.offset` is required and used to specify the location within the LUN at which to write the data; no other query parameters are allowed. The request body must be `multipart/form-data` content with exactly one form entry containing the data to write. The content type entry of the form data is ignored and always treated as `application/octet-stream`. Writes are limited to one megabyte (1MB) per request.
### Reading data from a LUN
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="c903a978-9bac-4ce9-8237-4a3ba8b13f08")
    resource.get(**{"data.offset": "0", "data.size": "9"})
    print(resource)

```

### Writing data to a LUN
This example writes the contents of a file to a LUN starting at offset 1024.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="c903a978-9bac-4ce9-8237-4a3ba8b13f08")
    resource.patch(
        hydrate=True,
        data="@file;type=application/octet-stream",
        **{"data.offset": "1024"}
    )

```

---
## Cloning LUNs
A clone of a LUN is an independent "copy" of the LUN that shares unchanged data blocks with the original. As blocks of the source and clone are modified, unique blocks are written for each. LUN clones can be created quickly and consume very little space initially. They can be created for the purpose of back-up, or to replicate data for multiple consumers.<br/>
Space reservations can be set for the LUN clone independent of the source LUN by setting the `space.guarantee.requested` property in a POST or PATCH request.<br/>
A LUN clone can be set to auto-delete by setting the `auto_delete` property. If the LUN's volume is configured for automatic deletion, LUNs that have auto-delete enabled are deleted when a volume is nearly full to reclaim a target amount of free space in the volume.<br/>
The value of property `space.scsi_thin_provisioning_support_enabled` is not propagated to the destination when a LUN is cloned as a new LUN; it is reset to false. The value of this property is maintained from the destination LUN when a LUN is overwritten as a clone.
### Creating a new LUN clone
You create a new LUN clone as you create any LUN - a POST request to [`/storage/luns`](#/SAN/lun_create). Set `clone.source.uuid` or `clone.source.name` to identify the source LUN from which the clone is created. The LUN clone and its source must reside in the same volume.<br/>
The source LUN can reside in a snapshot, in which case the `clone.source.name` field must be used to identify it. Add `/.snapshot/<snapshot_name>` to the path after the volume name to identify the snapshot. For example `/vol/vol1/.snapshot/snap1/lun1`.<br/>
By default, new LUN clones do not inherit the QoS policy of the source LUN; a QoS policy should be set for the clone by setting the `qos_policy` property.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun()
    resource.svm = {"name": "svm1"}
    resource.name = "/vol/vol1/lun2clone1"
    resource.clone = {"source": {"name": "/vol/vol1/lun2"}}
    resource.qos_policy = {"name": "qos1"}
    resource.post(hydrate=True)
    print(resource)

```

### Over-writing an existing LUN's data as a clone of another
You can overwrite an existing LUN as a clone of another, using a PATCH request to [`/storage/luns/{uuid}`](#/SAN/lun_modify). Set the `clone.source.uuid` or `clone.source.name` property to identify the source LUN from which the clone data is taken. The LUN clone and its source must reside in the same volume.<br/>
When used in a PATCH request, the patched LUN's data is overwritten as a clone of the source. The following properties are preserved from the patched LUN unless otherwise specified as part of the PATCH: `class`, `auto_delete`, `lun_maps`, `vvol`, `serial_number`, `status.state`, and `uuid`.<br/>
Persistent reservations for the updated LUN are also preserved.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="5a24ae5b-28af-47fb-b129-5adf6cfba0a6")
    resource.clone = {"source": {"name": "/vol/vol1/lun2"}}
    resource.patch()

```

---
## Converting an NVMe namespace into a LUN
An existing NVMe namespace can be converted in-place to a LUN with no modification to the data blocks. In other words, there is no additional copy created for the data blocks. There are certain requirements for converting an NVMe namespace to a LUN. For instance, the namespace should not be mapped to an NVMe subsystem. Additionally, the namespace should not have a block size other than 512 bytes.<br/>
The conversion process updates the metadata to the NVMe namespace, making it a LUN. The conversion is both time and space efficient. After conversion, the new LUN behaves as a regular LUN and may be mapped to an initiator group.
### Convert an NVMe namespace into a LUN
You convert an NVMe namespace into a LUN by calling a POST to [`/storage/luns`](#/SAN/lun_create). Set `convert.namespace.uuid` or `convert.namespace.name` to identify the source NVMe namespace which is to be converted in-place into a LUN.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun()
    resource.svm = {"name": "svm1"}
    resource.convert = {"namespace": {"name": "/vol/vol1/namespace1"}}
    resource.post(hydrate=True)
    print(resource)

```

---
## Moving LUNs between volumes
You move a LUN between volumes by using a PATCH request to [`/storage/luns/{uuid}`](#/SAN/lun_modify). Set the volume portion of the fully qualified LUN path `name` property, `path.volume.uuid`, or `path.volume.name` property to a different volume than the LUN's current volume. Moving a LUN between volumes is an asynchronous activity. A successful request returns a response of 200 synchronously, which indicates that the movement has been successfully queued. The LUN object can then be further polled with a GET request to [`/storage/luns/{uuid}`](#lun_get) to monitor the status of the movement.<br/>
The `movement` sub-object of the LUN object is populated while a LUN movement is in progress and for two minutes following completion of a movement.
### Starting a LUN movement
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="7faf0a9e-0a47-4876-8318-3638d5da16bf")
    resource.name = "/vol/vol1/lun3"
    resource.patch()

```

### Checking on the status of the LUN movement
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Lun

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Lun(uuid="7faf0a9e-0a47-4876-8318-3638d5da16bf")
    resource.get(fields="movement")
    print(resource)

```
<div class="try_it_out">
<input id="example11_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example11_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example11_result" class="try_it_out_content">
```
Lun(
    {
        "movement": {
            "paths": {"destination": "/vol/vol1/lun3", "source": "/vol/vol2/lun3"},
            "progress": {
                "volume_snapshot_blocked": False,
                "state": "preparing",
                "percent_complete": 0,
                "elapsed": 1,
            },
        },
        "name": "/vol/vol1/lun3",
        "_links": {
            "self": {"href": "/api/storage/luns/7faf0a9e-0a47-4876-8318-3638d5da16bf"}
        },
        "uuid": "7faf0a9e-0a47-4876-8318-3638d5da16bf",
    }
)

```
</div>
</div>

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


__all__ = ["Lun", "LunSchema"]
__pdoc__ = {
    "LunSchema.resource": False,
    "LunSchema.opts": False,
}


class LunSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Lun object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the lun."""

    attributes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.lun_attributes.LunAttributesSchema", unknown=EXCLUDE, allow_none=True), data_key="attributes", allow_none=True)
    r""" An array of name/value pairs optionally stored with the LUN. Attributes are available to callers to persist small amounts of application-specific metadata. They are in no way interpreted by ONTAP.<br/>
Attribute names and values must be at least one byte and no more than 4091 bytes in length. The sum of the name and value lengths must be no more than 4092 bytes.<br/>
Valid in POST except when creating a LUN clone. A cloned can already have attributes from its source. You can add, modify, and delete the attributes of a LUN clone in separate requests after creation of the LUN.<br/>
Attributes can be added/modified/removed for an existing LUN using the /api/storage/luns/{lun.uuid}/attributes endpoint. For further information, see [`DOC /storage/luns/{lun.uuid}/attributes`](#docs-SAN-storage_luns_{lun.uuid}_attributes).<br/>
There is an added computational cost to retrieving property values for `attributes`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more."""

    auto_delete = marshmallow_fields.Boolean(
        data_key="auto_delete",
        allow_none=True,
    )
    r""" * **Unified ONTAP**:
This property marks the LUN for auto deletion when the volume containing the LUN runs out of space. This is most commonly set on LUN clones.<br/>
When set to _true_, the LUN becomes eligible for automatic deletion when the volume runs out of space. Auto deletion only occurs when the volume containing the LUN is also configured for auto deletion and free space in the volume decreases below a particular threshold.<br/>
This property is optional in POST and PATCH. The default value for a new LUN is _false_.<br/>
There is an added computational cost to retrieving this property's value. It is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.

* **ASA r2**:
This property is not supported. It cannot be set in POST or PATCH and will not be returned by GET."""

    class_ = marshmallow_fields.Str(
        data_key="class",
        validate=enum_validation(['regular', 'protocol_endpoint', 'vvol']),
        allow_none=True,
    )
    r""" The class of LUN.<br/>
Optional in POST.
### Platform Specifics

* **ASA r2**: When set to _protocol_endpoint_, most other properties are not supported in POST, and the operation can be asynchronous. The LUN is provisioned with a generated name. Protocol endpoints are provisioned in a round robin pattern across all nodes in the cluster.<br/>
The following properties are supported in POST:<br/>

* `class`
* `svm`
* `provisioning_options.count`
* `lun_maps`
* `comment`
POST is asynchronous in these cases:<br/>

* There are nodes in the cluster not already hosting a protocol endpoint.
* The request includes either the `lun_maps` or `provisioning_options.count` properties.
* The `records` array is used for bulk provisioning.
<br/>DELETE is asynchronous when calling DELETE on the last protocol endpoint on a node.
<br/>Calling implementations should not attempt to track these conditions. Instead, check the HTTP status code. A 200 or 201 status code indicates the operation is already complete. A 202 status code indicates there is an asynchronous job that can be tracked. If asynchronous requests are always preferred, wrap individual POST and DELETE requests in a `records` array to force the operation to be asynchronous.
<br/>For more details, see [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)


Valid choices:

* regular
* protocol_endpoint
* vvol"""

    clone = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_luns_clone.ConsistencyGroupConsistencyGroupsLunsCloneSchema", data_key="clone", unknown=EXCLUDE, allow_none=True)
    r""" * **Unified ONTAP**:
This sub-object is used in POST to create a new LUN as a clone of an existing LUN, or PATCH to overwrite an existing LUN as a clone of another. Setting a property in this sub-object indicates that a LUN clone is desired. Consider the following other properties when cloning a LUN: `auto_delete`, `qos_policy`, `space.guarantee.requested` and `space.scsi_thin_provisioning_support_enabled`.<br/>
When used in a PATCH, the patched LUN's data is over-written as a clone of the source and the following properties are preserved from the patched LUN unless otherwise specified as part of the PATCH: `class`, `auto_delete`, `lun_maps`, `serial_number`, `status.state`, and `uuid`.<br/>
Persistent reservations for the patched LUN are also preserved.

* **ASA r2**:
This endpoint does not support clones. No properties in this sub-object can be set for POST or PATCH and none will be returned by GET.<br/>
Cloning is supported through the /api/storage/storage-units endpoint. See the [`POST /ap/storage/storage-units`](#/SAN/storage_unit_create) to learn more about cloning LUNs."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" A configurable comment available for use by the administrator. Valid in POST and PATCH."""

    consistency_group = marshmallow_fields.Nested("netapp_ontap.models.lun_consistency_group.LunConsistencyGroupSchema", data_key="consistency_group", unknown=EXCLUDE, allow_none=True)
    r""" The LUN's consistency group. This property is populated for LUNs that are members of a consistency group. If the LUN is a member of a child consistency group, the parent consistency group is reported.
### Platform Specifics

* **Unified ONTAP**: A LUN's consistency group is the consistency group of its containing volume.
* **ASA r2**: A LUN is optionally associated directly with a consistency group."""

    convert = marshmallow_fields.Nested("netapp_ontap.models.lun_convert.LunConvertSchema", data_key="convert", unknown=EXCLUDE, allow_none=True)
    r""" This sub-object is used in POST to convert a valid in-place NVMe namespace to a LUN. Setting a property in this sub-object indicates that a conversion from the specified NVMe namespace to LUN is desired.<br/>"""

    copy = marshmallow_fields.Nested("netapp_ontap.models.lun_copy.LunCopySchema", data_key="copy", unknown=EXCLUDE, allow_none=True)
    r""" * **Unified ONTAP**:
This sub-object applies to LUN copy operations. A LUN can be copied with a POST request that supplies `copy.source` properties.<br/>
Copying a LUN is an asynchronous activity begun by a POST request that specifies the source of the copy in the `copy.source` properties. The data for the LUN is then asynchronously copied from the source to the destination. The time required to complete the copy depends on the size of the LUN and the load on the cluster. The `copy` sub-object is populated while a LUN copy is in progress and for two (2) minutes following completion of a copy.<br/>
While LUNs are being copied, the status of the LUN copy operations can be obtained using a GET of the source or destination LUN that requests the `copy` properties. If the LUN is the source LUN for one or more copy operations, the `copy.destinations` array is populated in GET. If the containing LUN is the destination LUN for a copy operation, the `copy.source` sub-object is populated in GET. The LUN copy operation can be further modified using a PATCH on the properties on the `copy.source` sub-object of the copy destination LUN.<br/>
There is an added computational cost to retrieving property values for `copy`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.

* **ASA r2**:
LUN copies are not supported. No properties in this sub-object can be set in POST or PATCH and none will be returned by GET."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The time the LUN was created.

Example: 2018-06-04T19:00:00.000+0000"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The enabled state of the LUN. LUNs can be disabled to prevent access to the LUN. Certain error conditions also cause the LUN to become disabled. If the LUN is disabled, check the `status.state` property to determine if the LUN is administratively disabled (_offline_) or has become disabled as a result of an error. A LUN in an error condition can be brought online by setting the `enabled` property to _true_ or brought administratively offline by setting the `enabled` property to _false_. Upon creation, a LUN is enabled by default. Valid in PATCH."""

    encryption = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_encryption.StorageUnitEncryptionSchema", data_key="encryption", unknown=EXCLUDE, allow_none=True)
    r""" The encryption field of the lun."""

    location = marshmallow_fields.Nested("netapp_ontap.models.lun_location.LunLocationSchema", data_key="location", unknown=EXCLUDE, allow_none=True)
    r""" The location of the LUN within the ONTAP cluster.
### Platform Specifics

* **Unified ONTAP**:
LUNs support rename and move between volumes. Valid in POST and PATCH.

* **ASA r2**:
The LUN name can be changed by PATCHing the `name` property. The `location` properties are read-only."""

    lun_maps = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.lun_lun_maps.LunLunMapsSchema", unknown=EXCLUDE, allow_none=True), data_key="lun_maps", allow_none=True)
    r""" The LUN maps with which the LUN is associated.<br/>
There is an added computational cost to retrieving property values for `lun_maps`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
### Platform Specifics

* **Unified ONTAP**: These properties are supported for GET only.
* **ASA r2**: These properties are supported for GET and POST. During POST, a new or existing initiator group can be referenced. When referencing an existing initiator group, only the `name` and `uuid` properties are supported."""

    metric = marshmallow_fields.Nested("netapp_ontap.resources.performance_metric.PerformanceMetricSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput."""

    movement = marshmallow_fields.Nested("netapp_ontap.models.lun_movement.LunMovementSchema", data_key="movement", unknown=EXCLUDE, allow_none=True)
    r""" * **Unified ONTAP**:
This sub-object applies to LUN movement between volumes. A LUN can be moved to a new volume with a PATCH request that changes either the volume portion of property `name`, `location.volume.uuid`, or `location.volume.name`. If the volume is changed using more than one of these properties, the supplied properties used must refer to the same volume.<br/>
Moving a LUN between volumes is an asynchronous activity begun by a PATCH request. The data for the LUN is then asynchronously copied from the source volume to the destination volume. The time required to complete the move depends on the size of the LUN and the load on the cluster. The `movement` sub-object is populated while a LUN movement is in progress and for two (2) minutes following completion of a movement.<br/>
While the LUN is being moved, the status of the LUN movement operation can be obtained using a GET for the LUN that requests the `movement` properties. The LUN movement operation can be further modified using a PATCH on the properties on the `movement` sub-object.<br/>
There is an added computational cost to retrieving property values for `movement`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.

* **ASA r2**:
LUN movement is not supported. No properties in this sub-object can be set in POST or PATCH and none will be returned by GET."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the LUN. Valid in POST and PATCH.

* **Unified ONTAP**:
A LUN is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
LUN names are paths of the form "/vol/\<volume>[/\<qtree>]/\<lun>" where the qtree name is optional.<br/>
A PATCH that modifies the qtree and/or base name portion of the LUN path is considered a rename operation.<br/>
A PATCH that modifies the volume portion of the LUN path begins an asynchronous LUN movement operation.

* **ASA r2**:
LUN names are simple names that share a namespace with NVMe namespaces within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.<br/>
A PATCH that modifies the name of the LUN is considered a rename operation.


Example: /vol/volume1/qtree1/lun1"""

    os_type = marshmallow_fields.Str(
        data_key="os_type",
        validate=enum_validation(['aix', 'hpux', 'hyper_v', 'linux', 'netware', 'openvms', 'solaris', 'solaris_efi', 'vmware', 'windows', 'windows_2008', 'windows_gpt', 'xen']),
        allow_none=True,
    )
    r""" The operating system type of the LUN.<br/>
Required in POST when creating a LUN that is not a clone of another. Disallowed in POST when creating a LUN clone.


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

    provisioning_options = marshmallow_fields.Nested("netapp_ontap.models.lun_provisioning_options.LunProvisioningOptionsSchema", data_key="provisioning_options", unknown=EXCLUDE, allow_none=True)
    r""" Options that are applied to the operation."""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.models.lun_qos_policy.LunQosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The QoS policy for the LUN. Both traditional and adaptive QoS policies are supported. If both property `qos_policy.uuid` and `qos_policy.name` are specified in the same request, they must refer to the same QoS policy. To remove the QoS policy from a LUN, leaving it with no QoS policy, set the property `qos_policy.name` to an empty string ("") in a PATCH request. Valid in POST and PATCH.
### Platform Specifics

* **ASA r2**: To remove the QoS policy, set it to `null` in a PATCH request."""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        validate=len_validation(minimum=12, maximum=12),
        allow_none=True,
    )
    r""" The LUN serial number. The serial number is generated by ONTAP when the LUN is created."""

    space = marshmallow_fields.Nested("netapp_ontap.models.lun_space.LunSpaceSchema", data_key="space", unknown=EXCLUDE, allow_none=True)
    r""" The storage space related properties of the LUN."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw.PerformanceMetricRawSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the lun."""

    status = marshmallow_fields.Nested("netapp_ontap.models.lun_status.LunStatusSchema", data_key="status", unknown=EXCLUDE, allow_none=True)
    r""" Status information about the LUN."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the lun."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the LUN. The UUID is generated by ONTAP when the LUN is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    vvol = marshmallow_fields.Nested("netapp_ontap.models.lun_vvol.LunVvolSchema", data_key="vvol", unknown=EXCLUDE, allow_none=True)
    r""" A VMware virtual volume (vVol) binding is an association between a LUN of class `protocol_endpoint` and a LUN of class `vvol`. Class `protocol_endpoint` LUNs are mapped to igroups and granted access using the same configuration as class `regular` LUNs. When a class `vvol` LUN is bound to a mapped class `protocol_endpoint` LUN, VMware can access the class `vvol` LUN through the class `protocol_endpoint` LUN mapping.<br/>
See [`POST /protocols/san/vvol-bindings`](#/SAN/vvol_binding_create) to learn more about creating vVol bindings and [`DELETE /protocols/san/vvol-bindings`](#/SAN/vvol_binding_delete) to learn more about deleting vVol bindings.<br/>
There is an added computational cost to retrieving property values for `vvol`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more."""

    @property
    def resource(self):
        return Lun

    gettable_fields = [
        "links",
        "attributes",
        "auto_delete",
        "class_",
        "comment",
        "consistency_group",
        "copy",
        "create_time",
        "enabled",
        "encryption",
        "location",
        "lun_maps",
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
        "uuid",
        "vvol",
    ]
    """links,attributes,auto_delete,class_,comment,consistency_group,copy,create_time,enabled,encryption,location,lun_maps,metric,movement,name,os_type,qos_policy,serial_number,space,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,status,svm.links,svm.name,svm.uuid,uuid,vvol,"""

    patchable_fields = [
        "auto_delete",
        "clone",
        "comment",
        "copy",
        "enabled",
        "location",
        "movement",
        "name",
        "qos_policy",
        "space",
    ]
    """auto_delete,clone,comment,copy,enabled,location,movement,name,qos_policy,space,"""

    postable_fields = [
        "attributes",
        "auto_delete",
        "class_",
        "clone",
        "comment",
        "convert",
        "copy",
        "location",
        "lun_maps",
        "movement",
        "name",
        "os_type",
        "provisioning_options",
        "qos_policy",
        "space",
        "svm.name",
        "svm.uuid",
    ]
    """attributes,auto_delete,class_,clone,comment,convert,copy,location,lun_maps,movement,name,os_type,provisioning_options,qos_policy,space,svm.name,svm.uuid,"""

class Lun(Resource):
    r""" A LUN is the logical representation of storage in a storage area network (SAN).<br/>
A LUN must be mapped to an initiator group to grant access to the initiator group's initiators (client hosts). Initiators can then access the LUN and perform I/O over a Fibre Channel (FC) fabric using the FC Protocol or a TCP/IP network using iSCSI.<br/>
See the LUN object model to learn more about each of the properties supported by the LUN REST API.
## Platform Specifics
### Unified ONTAP
A LUN is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
LUN names are paths of the form "/vol/\<volume>[/\<qtree>]/\<lun>" where the qtree name is optional.<br/>
A LUN can be created to a specified size using thin or thick provisioning. A LUN can then be renamed, resized, cloned, moved to a different volume and copied. LUNs support the assignment of a QoS policy for performance management or a QoS policy can be assigned to a volume containing one or more LUNs.
### ASA r2
LUN names are simple names that share a namespace with NVMe namespaces within the same SVM. The name must begin with a letter or "\_" and contain only "\_" and alphanumeric characters. In specific cases, an optional snapshot-name can be used of the form "\<name>[@\<snapshot-name>]". The snapshot name must not begin or end with whitespace.<br/>
A LUN can be created to a specified size. A LUN can then be renamed, resized, or cloned. LUNs support the assignment of a QoS policy for performance management.<br/>
**Note**: LUN related REST API examples use the Unified ONTAP form for LUN names. On ASA r2, the ASA r2 format must be used. """

    _schema = LunSchema
    _path = "/api/storage/luns"
    _keys = ["uuid"]
    _patch_form_data_parameters = { 'data':'string', }

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves LUNs.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `attributes.*`
* `auto_delete`
* `copy.*`
* `lun_maps.*`
* `movement.*`
* `space.physical_used`
* `space.physical_used_by_snapshots`
* `space.efficiency_ratio`
* `statistics.*`
* `vvol.bindings.*`
* `metric.*`
### Related ONTAP commands
* `lun bind show`
* `lun copy show`
* `lun mapping show`
* `lun move show`
* `lun show`
* `volume file clone show-autodelete`
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
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
        """Returns a count of all Lun resources that match the provided query"""
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
        """Returns a list of RawResources that represent Lun resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Lun"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an existing LUN in one of several ways:
- Updates the properties of a LUN.
- Writes data to a LUN. LUN data write requests are distinguished by the header entry `Content-Type: multipart/form-data`. When this header entry is provided, query parameter `data.offset` is required and used to specify the location within the LUN at which to write the data; no other query parameters are allowed. The request body must be `multipart/form-data` content with exactly one form entry containing the data to write. The content type entry of the form data is ignored and always treated as `application/octet-stream`. Writes are limited to one megabyte (1MB) per request.
- Overwrites the contents of a LUN as a clone of another.
- Begins the movement of a LUN between volumes. PATCH can also pause and resume the movement of a LUN between volumes that is already in active.
### Related ONTAP commands
* `lun copy modify`
* `lun copy pause`
* `lun copy resume`
* `lun modify`
* `lun move-in-volume`
* `lun move modify`
* `lun move pause`
* `lun move resume`
* `lun move start`
* `lun resize`
* `volume file clone autodelete`
### Platform Specifics
* **ASA r2**: PATCH is asynchronous when modifying `name` or `qos_policy`.
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Lun"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Lun"], NetAppResponse]:
        r"""Creates a LUN.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the LUN.
* `name`, `location.volume.name` or `location.volume.uuid` - Existing volume in which to create the LUN.
* `name` or `location.logical_unit` - Base name of the LUN.
* `os_type` - Operating system from which the LUN will be accessed. Required when creating a non-clone LUN and disallowed when creating a clone of an existing LUN. A clone's `os_type` is taken from the source LUN.
* `space.size` - Size of the LUN. Required when creating a non-clone LUN and disallowed when creating a clone of an existing LUN. A clone's size is taken from the source LUN.
### Recommended optional properties
* `qos_policy.name` or `qos_policy.uuid` - Existing traditional or adaptive QoS policy to be applied to the LUN. All LUNs should be managed by a QoS policy at the volume or LUN level.
### Default property values
If not specified in POST, the follow default property values are assigned.
* `auto_delete` - _false_
### Related ONTAP commands
* `lun create`
* `lun convert-from-namespace`
* `lun copy start`
* `volume file clone autodelete`
* `volume file clone create`
### Platform Specifics
* **ASA r2**: The `name` property is required when creating a new LUN. The name must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 203 characters or less in length. The `location` properties are not supported.
POST is asynchronous when creating a new LUN. It is synchronous when converting a namespace to a LUN via the `convert` property.
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
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
        records: Iterable["Lun"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a LUN.
### Related ONTAP commands
* `lun copy cancel`
* `lun delete`
### Platform Specifics
* **ASA r2**: DELETE is asynchronous.
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves LUNs.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `attributes.*`
* `auto_delete`
* `copy.*`
* `lun_maps.*`
* `movement.*`
* `space.physical_used`
* `space.physical_used_by_snapshots`
* `space.efficiency_ratio`
* `statistics.*`
* `vvol.bindings.*`
* `metric.*`
### Related ONTAP commands
* `lun bind show`
* `lun copy show`
* `lun mapping show`
* `lun move show`
* `lun show`
* `volume file clone show-autodelete`
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a LUN's properties or a LUN's data.<br/>
LUN data read requests are distinguished by the header entry `Accept: multipart/form-data`. When this header entry is provided, query parameters `data.offset` and `data.size` are required and used to specify the portion of the LUN's data to read; no other query parameters are allowed. Reads are limited to one megabyte (1MB) per request. Data is returned as `multipart/form-data` content with exactly one form entry containing the data. The form entry has content type `application/octet-stream`.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `attributes.*`
* `auto_delete`
* `copy.*`
* `lun_maps.*`
* `movement.*`
* `space.physical_used`
* `space.physical_used_by_snapshots`
* `space.efficiency_ratio`
* `statistics.*`
* `vvol.bindings.*`
* `metric.*`
### Related ONTAP commands
* `lun bind show`
* `lun copy show`
* `lun mapping show`
* `lun move show`
* `lun show`
* `volume file clone show-autodelete`
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
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
        r"""Creates a LUN.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the LUN.
* `name`, `location.volume.name` or `location.volume.uuid` - Existing volume in which to create the LUN.
* `name` or `location.logical_unit` - Base name of the LUN.
* `os_type` - Operating system from which the LUN will be accessed. Required when creating a non-clone LUN and disallowed when creating a clone of an existing LUN. A clone's `os_type` is taken from the source LUN.
* `space.size` - Size of the LUN. Required when creating a non-clone LUN and disallowed when creating a clone of an existing LUN. A clone's size is taken from the source LUN.
### Recommended optional properties
* `qos_policy.name` or `qos_policy.uuid` - Existing traditional or adaptive QoS policy to be applied to the LUN. All LUNs should be managed by a QoS policy at the volume or LUN level.
### Default property values
If not specified in POST, the follow default property values are assigned.
* `auto_delete` - _false_
### Related ONTAP commands
* `lun create`
* `lun convert-from-namespace`
* `lun copy start`
* `volume file clone autodelete`
* `volume file clone create`
### Platform Specifics
* **ASA r2**: The `name` property is required when creating a new LUN. The name must start with an alphabetic character (a to z or A to Z) or an underscore (_). The name must be 203 characters or less in length. The `location` properties are not supported.
POST is asynchronous when creating a new LUN. It is synchronous when converting a namespace to a LUN via the `convert` property.
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
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
        r"""Updates an existing LUN in one of several ways:
- Updates the properties of a LUN.
- Writes data to a LUN. LUN data write requests are distinguished by the header entry `Content-Type: multipart/form-data`. When this header entry is provided, query parameter `data.offset` is required and used to specify the location within the LUN at which to write the data; no other query parameters are allowed. The request body must be `multipart/form-data` content with exactly one form entry containing the data to write. The content type entry of the form data is ignored and always treated as `application/octet-stream`. Writes are limited to one megabyte (1MB) per request.
- Overwrites the contents of a LUN as a clone of another.
- Begins the movement of a LUN between volumes. PATCH can also pause and resume the movement of a LUN between volumes that is already in active.
### Related ONTAP commands
* `lun copy modify`
* `lun copy pause`
* `lun copy resume`
* `lun modify`
* `lun move-in-volume`
* `lun move modify`
* `lun move pause`
* `lun move resume`
* `lun move start`
* `lun resize`
* `volume file clone autodelete`
### Platform Specifics
* **ASA r2**: PATCH is asynchronous when modifying `name` or `qos_policy`.
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
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
        r"""Deletes a LUN.
### Related ONTAP commands
* `lun copy cancel`
* `lun delete`
### Platform Specifics
* **ASA r2**: DELETE is asynchronous.
### Learn more
* [`DOC /storage/luns`](#docs-SAN-storage_luns)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


