r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API controls what is logged to the audit log files. All operations that make changes are always logged and cannot be disabled. The PATCH request updates administrative audit settings for GET requests. All fields are optional for a PATCH request. A GET request retrieves administrative audit settings for GET requests.
<br />
---
## Examples
### Retrieving administrative audit settings for GET requests
The following example shows the administrative audit settings for GET requests.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAudit

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = SecurityAudit()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecurityAudit(
    {
        "cli": False,
        "_links": {"self": {"href": "/api/security/audit"}},
        "http": False,
        "ontapi": False,
    }
)

```
</div>
</div>

---
### Updating administrative audit settings for GET requests
The following example updates the administrative audit settings for GET requests
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAudit

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = SecurityAudit()
    resource.cli = False
    resource.http = True
    resource.ontapi = True
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


__all__ = ["SecurityAudit", "SecurityAuditSchema"]
__pdoc__ = {
    "SecurityAuditSchema.resource": False,
    "SecurityAuditSchema.opts": False,
}


class SecurityAuditSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityAudit object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_audit."""

    cli = marshmallow_fields.Boolean(
        data_key="cli",
        allow_none=True,
    )
    r""" Enable auditing of CLI GET Operations. Valid in PATCH"""

    http = marshmallow_fields.Boolean(
        data_key="http",
        allow_none=True,
    )
    r""" Enable auditing of HTTP GET Operations. Valid in PATCH"""

    ontapi = marshmallow_fields.Boolean(
        data_key="ontapi",
        allow_none=True,
    )
    r""" Enable auditing of ONTAP API GET operations. Valid in PATCH"""

    @property
    def resource(self):
        return SecurityAudit

    gettable_fields = [
        "links",
        "cli",
        "http",
        "ontapi",
    ]
    """links,cli,http,ontapi,"""

    patchable_fields = [
        "cli",
        "http",
        "ontapi",
    ]
    """cli,http,ontapi,"""

    postable_fields = [
        "cli",
        "http",
        "ontapi",
    ]
    """cli,http,ontapi,"""

class SecurityAudit(Resource):
    """Allows interaction with SecurityAudit objects on the host"""

    _schema = SecurityAuditSchema
    _path = "/api/security/audit"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves administrative audit settings for GET requests.
### Learn more
* [`DOC /security/audit`](#docs-security-security_audit)"""
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
        r"""Updates administrative audit settings for GET requests.
All of the fields are optional. An empty body will make no changes.

### Learn more
* [`DOC /security/audit`](#docs-security-security_audit)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



