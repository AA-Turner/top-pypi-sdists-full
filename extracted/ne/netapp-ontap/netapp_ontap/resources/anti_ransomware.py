r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API displays and manages the anti-ransomware version.
## Examples
### Retrieving the anti-ransomware versions of all nodes in the cluster.
The following example shows how to retrieve anti-ransomware versions.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AntiRansomware

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AntiRansomware()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AntiRansomware(
    {
        "nodes": [
            {"version": "1.0", "name": "sti11-vsim-ucs573i"},
            {"version": "1.0", "name": "sti11-vsim-ucs573j"},
        ]
    }
)

```
</div>
</div>

---
### Updating the anti-ransomware package
The following example shows how to update the anti-ransomware package on the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AntiRansomware

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AntiRansomware()
    resource.uri = "http://server/package"
    resource.patch()

```

---
The call to update the anti-ransomware package returns the job UUID, including a HAL link to retrieve details about the job. The job object includes a `state` field and a message to indicate the progress of the job. When the job is complete and the application is fully created, the message indicates success and the job `state` field is set to `success`.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Job

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Job(uuid="74d0faef-3e1a-11ef-af89-005056ac6d8a")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Job(
    {
        "description": "PATCH /api/security/anti-ransomware",
        "code": 0,
        "message": "success",
        "state": "success",
        "uuid": "74d0faef-3e1a-11ef-af89-005056ac6d8a",
        "_links": {
            "self": {"href": "/api/cluster/jobs/74d0faef-3e1a-11ef-af89-005056ac6d8a"}
        },
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


__all__ = ["AntiRansomware", "AntiRansomwareSchema"]
__pdoc__ = {
    "AntiRansomwareSchema.resource": False,
    "AntiRansomwareSchema.opts": False,
}


class AntiRansomwareSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomware object"""

    nodes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.anti_ransomware_node.AntiRansomwareNodeSchema", unknown=EXCLUDE, allow_none=True), data_key="nodes", allow_none=True)
    r""" The nodes field of the anti_ransomware."""

    uri = marshmallow_fields.Str(
        data_key="uri",
        allow_none=True,
    )
    r""" URI of the anti-ransomware package through a server

Example: http://server/package"""

    @property
    def resource(self):
        return AntiRansomware

    gettable_fields = [
        "nodes",
    ]
    """nodes,"""

    patchable_fields = [
        "uri",
    ]
    """uri,"""

    postable_fields = [
    ]
    """"""

class AntiRansomware(Resource):
    """Allows interaction with AntiRansomware objects on the host"""

    _schema = AntiRansomwareSchema
    _path = "/api/security/anti-ransomware"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the anti-ransomware version of the nodes in the cluster.
### Related ONTAP commands
* `security anti-ransomware show`

### Learn more
* [`DOC /security/anti-ransomware`](#docs-security-security_anti-ransomware)"""
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
        r"""Updates the anti-ransomware package on the cluster.
### Required properties
* `uri` - URI of the anti-ransomware package
### Related ONTAP commands
* `security anti-ransomware update-package-from-uri`

### Learn more
* [`DOC /security/anti-ransomware`](#docs-security-security_anti-ransomware)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



