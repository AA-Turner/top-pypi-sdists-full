r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

### Overview
Volume efficiency policies specify information about efficiency policies that are applied to the volume.<br/>
## Volume efficiency policy APIs
The following APIs are used to perform operations related to volume efficiency policy information:

* POST      /api/storage/volume-efficiency-policies
* GET       /api/storage/volume-efficiency-policies
* GET       /api/storage/volume-efficiency-policies/{uuid}
* PATCH     /api/storage/volume-efficiency-policies/{uuid}
* DELETE    /api/storage/volume-efficiency-policies/{uuid}
## Examples
### Creating a volume efficiency policy
The POST operation is used to create a volume efficiency policy with the specified attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VolumeEfficiencyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VolumeEfficiencyPolicy()
    resource.name = "new_policy"
    resource.type = "scheduled"
    resource.schedule = {"name": "daily"}
    resource.duration = "2"
    resource.qos_policy = "best_effort"
    resource.enabled = True
    resource.comment = "schedule-policy"
    resource.svm = {"name": "vs1"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
VolumeEfficiencyPolicy(
    {
        "name": "new_policy",
        "schedule": {"name": "daily"},
        "qos_policy": "best_effort",
        "comment": "schedule-policy",
        "uuid": "a69d8173-450c-11e9-aa44-005056bbc848",
        "enabled": True,
        "svm": {"name": "vs1"},
        "type": "scheduled",
        "duration": 2,
    }
)

```
</div>
</div>

### Retrieving volume efficiency policy attributes
The GET operation is used to retrieve volume efficiency policy attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VolumeEfficiencyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(VolumeEfficiencyPolicy.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    VolumeEfficiencyPolicy(
        {
            "name": "default",
            "uuid": "3c112527-2fe8-11e9-b55e-005056bbf1c8",
            "_links": {
                "self": {
                    "href": "/api/storage/volume-efficiency-policies/3c112527-2fe8-11e9-b55e-005056bbf1c8"
                }
            },
        }
    ),
    VolumeEfficiencyPolicy(
        {
            "name": "default-1weekly",
            "uuid": "3c1c1656-2fe8-11e9-b55e-005056bbf1c8",
            "_links": {
                "self": {
                    "href": "/api/storage/volume-efficiency-policies/3c1c1656-2fe8-11e9-b55e-005056bbf1c8"
                }
            },
        }
    ),
    VolumeEfficiencyPolicy(
        {
            "name": "none",
            "uuid": "3c228b82-2fe8-11e9-b55e-005056bbf1c8",
            "_links": {
                "self": {
                    "href": "/api/storage/volume-efficiency-policies/3c228b82-2fe8-11e9-b55e-005056bbf1c8"
                }
            },
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of a specific volume efficiency policy
The GET operation is used to retrieve the attributes of a specific volume efficiency policy.
# The API:
/api/storage/volume-efficiency-policies/{uuid}
# The call:
curl -X GET "https://<mgmt-ip>/api/storage/volume-efficiency-policies/3c112527-2fe8-11e9-b55e-005056bbf1c8" -H "accept: application/hal+json"
# The response:
HTTP/1.1 200 OK
Date: Tue, 12 Mar 2019 21:24:48 GMT
Server: libzapid-httpd
X-Content-Type-Options: nosniff
Cache-Control: no-cache,no-store,must-revalidate
Content-Length: 381
Content-Type: application/json
{
  "uuid": "3c112527-2fe8-11e9-b55e-005056bbf1c8",
  "name": "new_policy",
  "type": "scheduled",
  "schedule": {
    "name": "daily"
  }
  "duration": "2",
  "qos_policy": "best_effort",
  "enabled": "true",
  "comment": "schedule-policy",
  "svm": {
        "name": "vs1"
  }
  "_links": {
    "self": {
      "href": "/api/storage/volume-efficiency-policies/3c112527-2fe8-11e9-b55e-005056bbf1c8"
    }
  }
}
```
### Updating a volume efficiency policy
The PATCH operation is used to update the specific attributes of a volume efficiency policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VolumeEfficiencyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VolumeEfficiencyPolicy(uuid="ae9e65c4-4506-11e9-aa44-005056bbc848")
    resource.duration = "3"
    resource.patch()

```

### Deleting a volume efficiency policy
The DELETE operation is used to delete a volume efficiency policy.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VolumeEfficiencyPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VolumeEfficiencyPolicy(uuid="ae9e65c4-4506-11e9-aa44-005056bbc848")
    resource.delete()

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


__all__ = ["VolumeEfficiencyPolicy", "VolumeEfficiencyPolicySchema"]
__pdoc__ = {
    "VolumeEfficiencyPolicySchema.resource": False,
    "VolumeEfficiencyPolicySchema.opts": False,
}


class VolumeEfficiencyPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeEfficiencyPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the volume_efficiency_policy."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" A comment associated with the volume efficiency policy."""

    duration = Size(
        data_key="duration",
        allow_none=True,
    )
    r""" This field is used with the policy type "scheduled" to indicate the allowed duration for a session, in hours. Possible value is a number between 0 and 999 inclusive. Default is unlimited indicated by value 0."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Is the volume efficiency policy enabled?"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the volume efficiency policy."""

    qos_policy = marshmallow_fields.Str(
        data_key="qos_policy",
        validate=enum_validation(['background', 'best_effort']),
        allow_none=True,
    )
    r""" QoS policy for the sis operation. Possible values are background and best_effort. In background, sis operation will run in background with minimal or no impact on data serving client operations. In best_effort, sis operations may have some impact on data serving client operations.

Valid choices:

* background
* best_effort"""

    schedule = marshmallow_fields.Nested("netapp_ontap.models.volume_efficiency_policy_schedule.VolumeEfficiencyPolicyScheduleSchema", data_key="schedule", unknown=EXCLUDE, allow_none=True)
    r""" The schedule field of the volume_efficiency_policy."""

    start_threshold_percent = Size(
        data_key="start_threshold_percent",
        allow_none=True,
    )
    r""" This field is used with the policy type "threshold" to indicate the threshold percentage for triggering the volume efficiency policy. It is mutually exclusive of the schedule."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the volume_efficiency_policy."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['scheduled', 'threshold']),
        allow_none=True,
    )
    r""" Type of volume efficiency policy.

Valid choices:

* scheduled
* threshold"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of volume efficiency policy."""

    @property
    def resource(self):
        return VolumeEfficiencyPolicy

    gettable_fields = [
        "links",
        "comment",
        "duration",
        "enabled",
        "name",
        "qos_policy",
        "schedule",
        "start_threshold_percent",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """links,comment,duration,enabled,name,qos_policy,schedule,start_threshold_percent,svm.links,svm.name,svm.uuid,type,uuid,"""

    patchable_fields = [
        "comment",
        "duration",
        "enabled",
        "qos_policy",
        "schedule",
        "start_threshold_percent",
        "type",
    ]
    """comment,duration,enabled,qos_policy,schedule,start_threshold_percent,type,"""

    postable_fields = [
        "comment",
        "duration",
        "enabled",
        "name",
        "qos_policy",
        "schedule",
        "start_threshold_percent",
        "svm.name",
        "svm.uuid",
        "type",
    ]
    """comment,duration,enabled,name,qos_policy,schedule,start_threshold_percent,svm.name,svm.uuid,type,"""

class VolumeEfficiencyPolicy(Resource):
    """Allows interaction with VolumeEfficiencyPolicy objects on the host"""

    _schema = VolumeEfficiencyPolicySchema
    _path = "/api/storage/volume-efficiency-policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of volume efficiency policies.
### Related ONTAP commands
* `volume efficiency policy show`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
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
        """Returns a count of all VolumeEfficiencyPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent VolumeEfficiencyPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["VolumeEfficiencyPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a volume efficiency policy.
### Platform Specifics
* **Unified ONTAP**: PATCH must be used to update the attributes of a volume efficiency policy.
* **ASA r2**: PATCH is not supported.
### Related ONTAP commands
* `volume efficiency policy modify`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["VolumeEfficiencyPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["VolumeEfficiencyPolicy"], NetAppResponse]:
        r"""Creates a volume efficiency policy.
### Platform Specifics
* **Unified ONTAP**: POST must be used to create a volume efficiency policy.
* **ASA r2**: POST is not supported.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the volume efficiency policy.
* `name` - Name for the volume efficiency policy.
### Recommended optional properties
* `type` - Type of volume policy.
* `schedule` - Schedule the volume efficiency defined in minutes, hourly, daily and weekly.
* `duration` - Indicates the allowed duration for a session for policy type "scheduled".
* `start_threshold_percent` - Indicates the start threshold percentage for the policy type "threshold". It is mutually exclusive of the schedule.
* `qos_policy` - QoS policy for the sis operation.
* `comment` - A comment associated with the volume efficiency policy.
* `enabled` - Is the volume efficiency policy enabled?
### Default property values
If not specified in POST, the following default property values are assigned:
* `type` - scheduled
* `start_threshold_percent` - 20
* `enabled` - true
* `qos_policy` - best_effort
* `schedule` - daily
### Related ONTAP commands
* `volume efficiency policy create`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
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
        records: Iterable["VolumeEfficiencyPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a volume efficiency policy.
### Platform Specifics
* **Unified ONTAP**: DELETE must be used to delete a volume efficiency policy.
* **ASA r2**: DELETE is not supported.
### Related ONTAP commands
* `volume efficiency policy delete`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of volume efficiency policies.
### Related ONTAP commands
* `volume efficiency policy show`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of the specified volume efficiency policy.
### Related ONTAP commands
* `volume efficiency policy show`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
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
        r"""Creates a volume efficiency policy.
### Platform Specifics
* **Unified ONTAP**: POST must be used to create a volume efficiency policy.
* **ASA r2**: POST is not supported.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the volume efficiency policy.
* `name` - Name for the volume efficiency policy.
### Recommended optional properties
* `type` - Type of volume policy.
* `schedule` - Schedule the volume efficiency defined in minutes, hourly, daily and weekly.
* `duration` - Indicates the allowed duration for a session for policy type "scheduled".
* `start_threshold_percent` - Indicates the start threshold percentage for the policy type "threshold". It is mutually exclusive of the schedule.
* `qos_policy` - QoS policy for the sis operation.
* `comment` - A comment associated with the volume efficiency policy.
* `enabled` - Is the volume efficiency policy enabled?
### Default property values
If not specified in POST, the following default property values are assigned:
* `type` - scheduled
* `start_threshold_percent` - 20
* `enabled` - true
* `qos_policy` - best_effort
* `schedule` - daily
### Related ONTAP commands
* `volume efficiency policy create`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
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
        r"""Updates a volume efficiency policy.
### Platform Specifics
* **Unified ONTAP**: PATCH must be used to update the attributes of a volume efficiency policy.
* **ASA r2**: PATCH is not supported.
### Related ONTAP commands
* `volume efficiency policy modify`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
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
        r"""Deletes a volume efficiency policy.
### Platform Specifics
* **Unified ONTAP**: DELETE must be used to delete a volume efficiency policy.
* **ASA r2**: DELETE is not supported.
### Related ONTAP commands
* `volume efficiency policy delete`
### Learn more
* [`DOC /storage/volume-efficiency-policies`](#docs-storage-storage_volume-efficiency-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


