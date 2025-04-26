r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Use this API to retrieve the status for a specific automatic package update.<p/>
This API supports GET and PATCH calls. PATCH can be used to perform an action on an automatic update.
---
## Examples
### Retrieving the status of an update
The following example shows how to retrieve the status of an automatic update:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutoUpdateStatus

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutoUpdateStatus(uuid="440ae2e4-fd8f-4225-9bee-94e2da3f8d9d")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AutoUpdateStatus(
    {
        "expiry_time": "2021-06-01T09:12:03+00:00",
        "last_state_change_time": "2020-12-01T09:12:23+00:00",
        "status": {
            "message": "Get-url request to AutoSupport OnDemand Server failed. Error: Couldn't connect to server.",
            "code": "8650878",
        },
        "description": "disk_fw version 3.0",
        "creation_time": "2020-12-01T09:12:03+00:00",
        "package_id": "572361f3-e769-439d-9c04-2ba48a08ff47",
        "start_time": "2020-12-01T09:12:23+00:00",
        "state": "downloading",
        "uuid": "440ae2e4-fd8f-4225-9bee-94e2da3f8d9d",
        "content_type": "disk_fw",
        "_links": {"self": {}},
        "percent_complete": 25,
        "remaining_time": "PT1M30S",
        "content_category": "Firmware",
    }
)

```
</div>
</div>

---
### Updating the state of an automatic update
The following example shows how to trigger an automatic update that is waiting for user confirmation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutoUpdateStatus

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutoUpdateStatus(uuid="440ae2e4-fd8f-4225-9bee-94e2da3f8d9d")
    resource.patch(hydrate=True, action="schedule_now")

```

The following example shows how to dismiss an automatic update that is waiting for user confirmation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutoUpdateStatus

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutoUpdateStatus(uuid="440ae2e4-fd8f-4225-9bee-94e2da3f8d9d")
    resource.patch(hydrate=True, action="dismiss")

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


__all__ = ["AutoUpdateStatus", "AutoUpdateStatusSchema"]
__pdoc__ = {
    "AutoUpdateStatusSchema.resource": False,
    "AutoUpdateStatusSchema.opts": False,
}


class AutoUpdateStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AutoUpdateStatus object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.application_nvme_access_subsystem_map_subsystem_hosts_links.ApplicationNvmeAccessSubsystemMapSubsystemHostsLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the auto_update_status."""

    action = marshmallow_fields.Str(
        data_key="action",
        validate=enum_validation(['cancel_schedule', 'dismiss', 'schedule', 'schedule_now', 'abort', 'undismiss']),
        allow_none=True,
    )
    r""" Action to be applied to the automatic update.

Valid choices:

* cancel_schedule
* dismiss
* schedule
* schedule_now
* abort
* undismiss"""

    content_category = marshmallow_fields.Str(
        data_key="content_category",
        allow_none=True,
    )
    r""" Category of the update

Example: Firmware"""

    content_type = marshmallow_fields.Str(
        data_key="content_type",
        allow_none=True,
    )
    r""" Image or package type.

Example: disk_fw"""

    creation_time = ImpreciseDateTime(
        data_key="creation_time",
        allow_none=True,
    )
    r""" The date and time at which the update request was received.

Example: 2020-12-01T09:12:23.000+0000"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description of the update.

Example: disk_fw version 3.0"""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" The date and time at which the update request processing ended.

Example: 2020-12-01T09:12:23.000+0000"""

    expiry_time = ImpreciseDateTime(
        data_key="expiry_time",
        allow_none=True,
    )
    r""" The date and time at which the update request will expire.

Example: 2021-06-01T09:12:23.000+0000"""

    last_state_change_time = ImpreciseDateTime(
        data_key="last_state_change_time",
        allow_none=True,
    )
    r""" The date and time at which the state of the update changed last.

Example: 2020-12-01T09:12:23.000+0000"""

    package_id = marshmallow_fields.Str(
        data_key="package_id",
        allow_none=True,
    )
    r""" Unique identifier provided by the back-end.

Example: 572361f3-e769-439d-9c04-2ba48a08ff47"""

    percent_complete = Size(
        data_key="percent_complete",
        allow_none=True,
    )
    r""" Percentage of update completed

Example: 85"""

    remaining_time = marshmallow_fields.Str(
        data_key="remaining_time",
        allow_none=True,
    )
    r""" The time remaining for the update processing to complete in an ISO-8601 duration formatted string.

Example: PT1H45M13S"""

    schedule_time = ImpreciseDateTime(
        data_key="schedule_time",
        allow_none=True,
    )
    r""" Date and time when an automatic update action is scheduled.
This field is required when the action field is set to "schedule".


Example: 2020-12-20T21:00:00.000+0000"""

    scheduled_time = ImpreciseDateTime(
        data_key="scheduled_time",
        allow_none=True,
    )
    r""" The date and time at which the update request is currently scheduled for.

Example: 2020-12-05T09:12:23.000+0000"""

    start_time = ImpreciseDateTime(
        data_key="start_time",
        allow_none=True,
    )
    r""" The date and time at which the update request processing started.

Example: 2020-12-01T09:12:23.000+0000"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['pending_confirmation', 'downloading', 'applying', 'applied', 'dismissed', 'scheduled', 'failed', 'aborted']),
        allow_none=True,
    )
    r""" Current state of the update.

Valid choices:

* pending_confirmation
* downloading
* applying
* applied
* dismissed
* scheduled
* failed
* aborted"""

    status = marshmallow_fields.Nested("netapp_ontap.models.error.ErrorSchema", data_key="status", unknown=EXCLUDE, allow_none=True)
    r""" The status field of the auto_update_status."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for this update.

Example: 440ae2e4-fd8f-4225-9bee-94e2da3f9d8d"""

    @property
    def resource(self):
        return AutoUpdateStatus

    gettable_fields = [
        "links",
        "content_category",
        "content_type",
        "creation_time",
        "description",
        "end_time",
        "expiry_time",
        "last_state_change_time",
        "package_id",
        "percent_complete",
        "remaining_time",
        "scheduled_time",
        "start_time",
        "state",
        "status",
        "uuid",
    ]
    """links,content_category,content_type,creation_time,description,end_time,expiry_time,last_state_change_time,package_id,percent_complete,remaining_time,scheduled_time,start_time,state,status,uuid,"""

    patchable_fields = [
        "action",
        "schedule_time",
    ]
    """action,schedule_time,"""

    postable_fields = [
    ]
    """"""

class AutoUpdateStatus(Resource):
    """Allows interaction with AutoUpdateStatus objects on the host"""

    _schema = AutoUpdateStatusSchema
    _path = "/api/support/auto-update/updates"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the status of all updates.

### Learn more
* [`DOC /support/auto-update/updates`](#docs-support-support_auto-update_updates)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all AutoUpdateStatus resources that match the provided query"""
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
        """Returns a list of RawResources that represent AutoUpdateStatus resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["AutoUpdateStatus"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Perform an action on the update.

### Learn more
* [`DOC /support/auto-update/updates/{uuid}`](#docs-support-support_auto-update_updates_{uuid})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the status of all updates.

### Learn more
* [`DOC /support/auto-update/updates`](#docs-support-support_auto-update_updates)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the status of an update.

### Learn more
* [`DOC /support/auto-update/updates/{uuid}`](#docs-support-support_auto-update_updates_{uuid})"""
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
        r"""Perform an action on the update.

### Learn more
* [`DOC /support/auto-update/updates/{uuid}`](#docs-support-support_auto-update_updates_{uuid})"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



