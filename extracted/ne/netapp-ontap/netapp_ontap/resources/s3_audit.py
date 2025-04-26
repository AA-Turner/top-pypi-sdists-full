r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
S3 events auditing is a security measure that enables you to track and log certain S3 events on storage virtual machines (SVMs). You can track potential security problems and provides evidence of any security breaches.
## Examples
---
### Creating an S3 audit entry with log rotation size and log retention count
To create an S3 audit entry with log rotation size and log retention count, use the following API. Note the <i>return_records=true</i> query parameter is used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Audit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Audit("ec650e97-156e-11e9-abcb-005056bbd0bf")
    resource.enabled = True
    resource.events = {"data": False, "management": False}
    resource.log = {
        "format": "json",
        "retention": {"count": 10},
        "rotation": {"size": 2048000},
    }
    resource.log_path = "/"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
S3Audit(
    {
        "log_path": "/",
        "enabled": True,
        "events": {"data": False, "management": False},
        "log": {
            "rotation": {"size": 2048000},
            "retention": {"duration": "0s", "count": 10},
            "format": "json",
        },
        "svm": {"name": "vs1", "uuid": "ec650e97-156e-11e9-abcb-005056bbd0bf"},
    }
)

```
</div>
</div>

---
### Creating an S3 audit entry with log rotation schedule and log retention duration
To create an S3 audit entry with log rotation schedule and log retention duration, use the following API. Note that the <i>return_records=true</i> query parameter is used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Audit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Audit("a8d64674-13fc-11e9-87b1-005056a7ae7e")
    resource.enabled = False
    resource.events = {"data": True, "management": True}
    resource.log = {
        "format": "json",
        "retention": {"duration": "P4DT12H30M5S"},
        "rotation": {
            "schedule": {
                "days": [1, 5, 10, 15],
                "hours": [0, 1, 6, 12, 18, 23],
                "minutes": [10, 15, 30, 45, 59],
                "months": [0],
                "weekdays": [0, 2, 5],
            }
        },
    }
    resource.log_path = "/"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
S3Audit(
    {
        "log_path": "/",
        "enabled": True,
        "events": {"data": True, "management": True},
        "log": {
            "rotation": {
                "schedule": {
                    "days": [1, 5, 10, 15],
                    "hours": [0, 1, 6, 12, 18, 23],
                    "minutes": [10, 15, 30, 45, 59],
                    "weekdays": [0, 2, 5],
                    "months": [0],
                }
            },
            "retention": {"duration": "P4DT12H30M5S", "count": 0},
            "format": "json",
        },
        "svm": {"name": "vs3", "uuid": "a8d64674-13fc-11e9-87b1-005056a7ae7e"},
    }
)

```
</div>
</div>

---
### Retrieving an S3 audit configuration for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Audit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Audit("*")
    resource.get(fields="*", return_timeout=15)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    S3Audit(
        {
            "log_path": "/",
            "enabled": True,
            "events": {"data": False, "management": False},
            "log": {
                "rotation": {"size": 2048000},
                "retention": {"duration": "0s", "count": 10},
                "format": "json",
            },
            "svm": {"name": "vs1", "uuid": "ec650e97-156e-11e9-abcb-005056bbd0bf"},
        }
    ),
    S3Audit(
        {
            "log_path": "/",
            "enabled": True,
            "events": {"data": True, "management": True},
            "log": {
                "rotation": {
                    "schedule": {
                        "days": [1, 5, 10, 15],
                        "hours": [0, 1, 6, 12, 18, 23],
                        "minutes": [10, 15, 30, 45, 59],
                        "weekdays": [0, 2, 5],
                        "months": [0],
                    }
                },
                "retention": {"duration": "P4DT12H30M5S", "count": 0},
                "format": "json",
            },
            "svm": {"name": "vs3", "uuid": "a8d64674-13fc-11e9-87b1-005056a7ae7e"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving specific entries with event list as data and management event for an SVM
The configuration returned is identified by the events in the list of S3 audit configurations of an SVM.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Audit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Audit("*")
    resource.get(
        return_timeout=15, **{"events.data": "true", "events.management": "true"}
    )
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    S3Audit(
        {
            "events": {"data": True, "management": True},
            "svm": {"name": "vs1", "uuid": "ec650e97-156e-11e9-abcb-005056bbd0bf"},
        }
    ),
    S3Audit(
        {
            "events": {"data": True, "management": True},
            "svm": {"name": "vs3", "uuid": "a8d64674-13fc-11e9-87b1-005056a7ae7e"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific S3 audit configuration of an SVM
The configuration returned is identified by the UUID of its SVM.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Audit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Audit("ec650e97-156e-11e9-abcb-005056bbd0bf")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
S3Audit(
    {
        "log_path": "/",
        "enabled": True,
        "events": {"data": False, "management": False},
        "log": {
            "rotation": {"size": 2048000},
            "retention": {"duration": "0s", "count": 10},
            "format": "json",
        },
        "svm": {"name": "vs1", "uuid": "ec650e97-156e-11e9-abcb-005056bbd0bf"},
    }
)

```
</div>
</div>

---
### Updating a specific S3 audit configuration of an SVM
The configuration is identified by the UUID of its SVM and the provided information is updated.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Audit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Audit("ec650e97-156e-11e9-abcb-005056bbd0bf")
    resource.enabled = False
    resource.patch()

```

---
### Deleting a specific S3 audit configuration of an SVM
The entry to be deleted is identified by the UUID of its SVM.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Audit

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Audit("ec650e97-156e-11e9-abcb-005056bbd0bf")
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


__all__ = ["S3Audit", "S3AuditSchema"]
__pdoc__ = {
    "S3AuditSchema.resource": False,
    "S3AuditSchema.opts": False,
}


class S3AuditSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3Audit object"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies whether or not auditing is enabled on the SVM."""

    events = marshmallow_fields.Nested("netapp_ontap.models.s3_audit_events.S3AuditEventsSchema", data_key="events", unknown=EXCLUDE, allow_none=True)
    r""" The events field of the s3_audit."""

    log = marshmallow_fields.Nested("netapp_ontap.models.s3_log.S3LogSchema", data_key="log", unknown=EXCLUDE, allow_none=True)
    r""" The log field of the s3_audit."""

    log_path = marshmallow_fields.Str(
        data_key="log_path",
        allow_none=True,
    )
    r""" The audit log destination path where consolidated audit logs are stored."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_audit."""

    @property
    def resource(self):
        return S3Audit

    gettable_fields = [
        "enabled",
        "events",
        "log",
        "log_path",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """enabled,events,log,log_path,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "enabled",
        "events",
        "log",
        "log_path",
    ]
    """enabled,events,log,log_path,"""

    postable_fields = [
        "enabled",
        "events",
        "log",
        "log_path",
        "svm.name",
        "svm.uuid",
    ]
    """enabled,events,log,log_path,svm.name,svm.uuid,"""

class S3Audit(Resource):
    r""" Auditing for NAS events is a security measure that enables you to track and log certain S3 events on SVMs. """

    _schema = S3AuditSchema
    _path = "/api/protocols/audit/{svm[uuid]}/object-store"
    _keys = ["svm.uuid"]






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves S3 audit configurations.
### Related ONTAP commands
* `vserver object-store-server audit show`
### Learn more
* [`DOC /protocols/audit/{svm.uuid}/object-store`](#docs-NAS-protocols_audit_{svm.uuid}_object-store)
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
        r"""Creates an S3 audit configuration.
### Required properties
* `log_path` - Path in the owning SVM namespace that is used to store audit logs.
### Default property values
If not specified in POST, the following default property values are assigned:
* `enabled` - _true_
* `events.data` - _true_
* `events.management` - _false_
* `log.format` - _json_
* `log.retention.count` - _0_
* `log.retention.duration` - _PT0S_
* `log.rotation.size` - _100MB_
* `log.rotation.now` - _false_
### Related ONTAP commands
* `vserver object-store-server audit create`
* `vserver object-store-server audit enable`
### Learn more
* [`DOC /protocols/audit/{svm.uuid}/object-store`](#docs-NAS-protocols_audit_{svm.uuid}_object-store)
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
        r"""Updates an S3 audit configuration for an SVM.
### Important notes
* `events` - Not specifying either data or management is equivalent to setting it to false.
### Related ONTAP commands
* `vserver object-store-server audit modify`
### Learn more
* [`DOC /protocols/audit/{svm.uuid}/object-store`](#docs-NAS-protocols_audit_{svm.uuid}_object-store)
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
        r"""Deletes an S3 audit configuration.
### Related ONTAP commands
* `vserver object-store-server audit disable`
* `vserver object-store-server audit delete`
### Learn more
* [`DOC /protocols/audit/{svm.uuid}/object-store`](#docs-NAS-protocols_audit_{svm.uuid}_object-store)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


