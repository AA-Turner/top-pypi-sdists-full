r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Vscan On-Demand scanning is used to check files for viruses on a schedule. For example, it can be used to run scans only in off-peak hours, or to scan very large files that are excluded from an on-access scan. Vscan On-Demand scanning can be used for any path in the SVM namespace.<p/>
Vscan On-Demand policy configurations define the scope of a Vscan On-Demand scan. The schedule parameter in the On-Demand policy configuration decides when to execute the task. Schedule can be created using the /api/clusters/schedule endpoint and can be assigned on policy create or policy modify. This API is used to retrieve and manage Vscan On-Demand policy configurations. It is also used to schedule the Vscan On-Demand scan.
## Examples
### Retrieving all fields for all policies of an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnDemand

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(VscanOnDemand.get_collection("{svm.uuid}", fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    VscanOnDemand(
        {
            "schedule": {
                "name": "schedule",
                "uuid": "f6d0843e-f159-11e8-8e22-0050568e0945",
                "_links": {
                    "self": {
                        "href": "/api/cluster/schedules/f6d0843e-f159-11e8-8e22-0050568e0945"
                    }
                },
            },
            "name": "on-demand-policy1",
            "log_path": "/vol0/report_dir",
            "scan_paths": ["/vol1/", "/vol2/cifs/"],
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/86fbc414-f140-11e8-8e22-0050568e0945"
                    }
                },
                "uuid": "86fbc414-f140-11e8-8e22-0050568e0945",
            },
            "scope": {
                "exclude_paths": ["/vol1/cold-files/", "/vol1/cifs/names"],
                "scan_without_extension": False,
                "include_extensions": ["vmdk", "mp*"],
                "max_file_size": 10737418240,
                "exclude_extensions": ["mp3", "mp4"],
            },
        }
    ),
    VscanOnDemand(
        {
            "name": "on-demand-policy2",
            "log_path": "/report",
            "scan_paths": ["/vol1/", "/vol2/cifs/"],
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/86fbc414-f140-11e8-8e22-0050568e0945"
                    }
                },
                "uuid": "86fbc414-f140-11e8-8e22-0050568e0945",
            },
            "scope": {
                "scan_without_extension": True,
                "include_extensions": ["mp*"],
                "max_file_size": 10737418240,
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific On-Demand policy associated with a specified SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnDemand

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnDemand(
        "86fbc414-f140-11e8-8e22-0050568e0945", name="on-demand-task"
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
VscanOnDemand(
    {
        "name": "on-demand-policy",
        "log_path": "/report",
        "scan_paths": ["/vol1/cifs"],
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/86fbc414-f140-11e8-8e22-0050568e0945"}
            },
            "uuid": "86fbc414-f140-11e8-8e22-0050568e0945",
        },
        "scope": {
            "scan_without_extension": True,
            "include_extensions": ["vmdk", "mp*"],
            "max_file_size": 10737418240,
        },
    }
)

```
</div>
</div>

---
### Creating a Vscan On-Demand policy
The Vscan On-Demand policy POST endpoint creates an On-Demand policy for the specified SVM. Specify the schedule parameter to schedule an On-Demand scan.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnDemand

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnDemand("86fbc414-f140-11e8-8e22-0050568e0945")
    resource.log_path = "/vol0/report_dir"
    resource.name = "on-demand-policy"
    resource.scan_paths = ["/vol1/", "/vol2/cifs/"]
    resource.schedule = {
        "name": "weekly",
        "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412",
    }
    resource.scope = {
        "exclude_extensions": ["mp3"],
        "exclude_paths": ["/vol/cold-files/"],
        "include_extensions": ["vmdk", "mp*"],
        "max_file_size": 1073741824,
        "scan_without_extension": True,
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
VscanOnDemand(
    {
        "schedule": {"name": "weekly"},
        "name": "on-demand-policy",
        "log_path": "/vol0/report_dir",
        "scan_paths": ["/vol1/", "/vol2/cifs/"],
        "svm": {"name": "vs1"},
        "scope": {
            "exclude_paths": ["/vol/cold-files/"],
            "scan_without_extension": True,
            "include_extensions": ["vmdk", "mp*"],
            "max_file_size": 1073741824,
            "exclude_extensions": ["mp3"],
        },
    }
)

```
</div>
</div>

---
### Creating a Vscan On-Demand policy where a number of optional fields are not specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnDemand

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnDemand("86fbc414-f140-11e8-8e22-0050568e0945")
    resource.log_path = "/report"
    resource.name = "on-demand-policy"
    resource.scan_paths = ["/vol1/cifs/"]
    resource.scope = {"include_extensions": ["mp*"], "scan_without_extension": True}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
VscanOnDemand(
    {
        "name": "on-demand-policy",
        "log_path": "/report",
        "scan_paths": ["vol1/cifs/"],
        "svm": {"name": "vs1"},
        "scope": {
            "scan_without_extension": True,
            "include_extensions": ["vmdk", "mp*"],
            "max_file_size": 10737418240,
        },
    }
)

```
</div>
</div>

---
### Updating a Vscan On-Demand policy
The policy being modified is identified by the UUID of the SVM and the policy name.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnDemand

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnDemand(
        "86fbc414-f140-11e8-8e22-0050568e0945", name="on-demand-policy"
    )
    resource.schedule = {"name": "weekly"}
    resource.scope = {
        "exclude_extensions": ["mp3"],
        "exclude_paths": ["/vol/"],
        "include_extensions": ["vmdk", "mp3"],
        "scan_without_extension": True,
    }
    resource.patch()

```

---
### Deleting a Vscan On-Demand policy
The policy to be deleted is identified by the UUID of the SVM and the policy name.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnDemand

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnDemand(
        "86fbc414-f140-11e8-8e22-0050568e0945", name="on-demand-policy"
    )
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


__all__ = ["VscanOnDemand", "VscanOnDemandSchema"]
__pdoc__ = {
    "VscanOnDemandSchema.resource": False,
    "VscanOnDemandSchema.opts": False,
}


class VscanOnDemandSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanOnDemand object"""

    log_path = marshmallow_fields.Str(
        data_key="log_path",
        allow_none=True,
    )
    r""" The path from the Vserver root where the task report is created.

Example: /vol0/report_dir"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=256),
        allow_none=True,
    )
    r""" On-Demand task name

Example: task-1"""

    scan_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="scan_paths", allow_none=True)
    r""" List of paths that need to be scanned.

Example: ["/vol1/","/vol2/cifs/"]"""

    schedule = marshmallow_fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", data_key="schedule", unknown=EXCLUDE, allow_none=True)
    r""" The schedule field of the vscan_on_demand."""

    scope = marshmallow_fields.Nested("netapp_ontap.models.vscan_on_demand_scope.VscanOnDemandScopeSchema", data_key="scope", unknown=EXCLUDE, allow_none=True)
    r""" The scope field of the vscan_on_demand."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the vscan_on_demand."""

    @property
    def resource(self):
        return VscanOnDemand

    gettable_fields = [
        "log_path",
        "name",
        "scan_paths",
        "schedule.links",
        "schedule.name",
        "schedule.uuid",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """log_path,name,scan_paths,schedule.links,schedule.name,schedule.uuid,scope,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "log_path",
        "scan_paths",
        "schedule.name",
        "schedule.uuid",
        "scope",
    ]
    """log_path,scan_paths,schedule.name,schedule.uuid,scope,"""

    postable_fields = [
        "log_path",
        "name",
        "scan_paths",
        "schedule.name",
        "schedule.uuid",
        "scope",
    ]
    """log_path,name,scan_paths,schedule.name,schedule.uuid,scope,"""

class VscanOnDemand(Resource):
    r""" Use On-Demand scanning to check files for viruses on a schedule. An On-Demand policy defines the scope of an On-Demand scan. """

    _schema = VscanOnDemandSchema
    _path = "/api/protocols/vscan/{svm[uuid]}/on-demand-policies"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the Vscan On-Demand policy.
### Related ONTAP commands
* `vserver vscan on-demand-task show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
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
        """Returns a count of all VscanOnDemand resources that match the provided query"""
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
        """Returns a list of RawResources that represent VscanOnDemand resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["VscanOnDemand"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the Vscan On-Demand policy configuration of an SVM. Use schedule name or schedule UUID to schedule an On-Demand scan.
### Related ONTAP commands
* `vserver vscan on-demand-task modify`
* `vserver vscan on-demand-task schedule`
* `vserver vscan on-demand-task unschedule`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["VscanOnDemand"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["VscanOnDemand"], NetAppResponse]:
        r"""Creates a Vscan On-Demand policy. Created only on a data SVM.
</br> Important notes:
  * Only one policy can be scheduled at a time on an SVM. Use schedule name or schedule uuid to schedule an On-Demand policy.
  * Scanning must be enabled on the SVM before the policy is scheduled to run.
  * The exclude_extensions setting overrides the include_extensions setting. Set scan_without_extension to true to scan files without extensions.
### Required properties
* `svm.uuid` - Existing SVM in which to create the Vscan On-Demand policy.
* `name` - Name of the Vscan On-Demand policy. Maximum length is 256 characters.
* `log_path` - Path from the Vserver root where the On-Demand policy report is created.
* `scan_paths` - List of paths that need to be scanned.
### Recommended optional properties
* `schedule` - Scan schedule. It is recommended to set the schedule property, as it dictates when to scan for viruses.
### Default property values
If not specified in POST, the following default property values are assigned:
* `include_extensions` - _*_
* `max_file_size` - _10737418240_
* `scan_without_extension` - _true_
### Related ONTAP commands
* `vserver vscan on-demand-task create`
* `vserver vscan on-demand-task schedule`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
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
        records: Iterable["VscanOnDemand"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the Vscan On-Demand configuration.
### Related ONTAP commands
* `vserver vscan on-demand-task delete`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the Vscan On-Demand policy.
### Related ONTAP commands
* `vserver vscan on-demand-task show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Vscan On-Demand configuration of an SVM.
### Related ONTAP commands
* `vserver vscan on-demand-task show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
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
        r"""Creates a Vscan On-Demand policy. Created only on a data SVM.
</br> Important notes:
  * Only one policy can be scheduled at a time on an SVM. Use schedule name or schedule uuid to schedule an On-Demand policy.
  * Scanning must be enabled on the SVM before the policy is scheduled to run.
  * The exclude_extensions setting overrides the include_extensions setting. Set scan_without_extension to true to scan files without extensions.
### Required properties
* `svm.uuid` - Existing SVM in which to create the Vscan On-Demand policy.
* `name` - Name of the Vscan On-Demand policy. Maximum length is 256 characters.
* `log_path` - Path from the Vserver root where the On-Demand policy report is created.
* `scan_paths` - List of paths that need to be scanned.
### Recommended optional properties
* `schedule` - Scan schedule. It is recommended to set the schedule property, as it dictates when to scan for viruses.
### Default property values
If not specified in POST, the following default property values are assigned:
* `include_extensions` - _*_
* `max_file_size` - _10737418240_
* `scan_without_extension` - _true_
### Related ONTAP commands
* `vserver vscan on-demand-task create`
* `vserver vscan on-demand-task schedule`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
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
        r"""Updates the Vscan On-Demand policy configuration of an SVM. Use schedule name or schedule UUID to schedule an On-Demand scan.
### Related ONTAP commands
* `vserver vscan on-demand-task modify`
* `vserver vscan on-demand-task schedule`
* `vserver vscan on-demand-task unschedule`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
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
        r"""Deletes the Vscan On-Demand configuration.
### Related ONTAP commands
* `vserver vscan on-demand-task delete`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-demand-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-demand-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


