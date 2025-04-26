r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
These APIs provide information on the multi-admin verification global setting.
The GET API retrieves the object store that contains the global setting values of the multi-admin-verify feature.
The PATCH request is used to modify the multi-admin-verify global setting. All fields are optional for the PATCH request.
Note it is recommended that multi-admin-verify is enabled equally on peered ONTAP clusters.
<br />
---
## Examples
### Retrieving the multi-admin-verify global setting
Retrieves the current multi-admin-verify global setting. If the global setting is not set, default values are returned.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyConfig

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyConfig()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
MultiAdminVerifyConfig(
    {
        "enabled": False,
        "approval_groups": [],
        "required_approvers": 1,
        "execution_expiry": "PT1H",
        "approval_expiry": "PT1H",
    }
)

```
</div>
</div>

---
### Updating the multi-admin-verify global setting
The following example updates the multi-admin-verify global settings.
Note that the approval_groups needs to be available in /security/multi-admin-verify/approval-groups before it is set in the global setting.
Note that the total number of approvers in an approval group must be a positive integer more than the number of required approvers. For example, if there are a total of 10 approvers in a group, the required approvers can be set between 1 and 9.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyConfig

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyConfig()
    resource.required_approvers = "1"
    resource.enabled = True
    resource.execution_expiry = "2h"
    resource.approval_expiry = "3h"
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


__all__ = ["MultiAdminVerifyConfig", "MultiAdminVerifyConfigSchema"]
__pdoc__ = {
    "MultiAdminVerifyConfigSchema.resource": False,
    "MultiAdminVerifyConfigSchema.opts": False,
}


class MultiAdminVerifyConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MultiAdminVerifyConfig object"""

    approval_expiry = marshmallow_fields.Str(
        data_key="approval_expiry",
        allow_none=True,
    )
    r""" Default time for requests to be approved, in ISO-8601 duration format."""

    approval_groups = marshmallow_fields.List(marshmallow_fields.Str, data_key="approval_groups", allow_none=True)
    r""" List of approval groups that are allowed to approve requests for rules that don't have approval groups."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The enabled field of the multi_admin_verify_config."""

    execution_expiry = marshmallow_fields.Str(
        data_key="execution_expiry",
        allow_none=True,
    )
    r""" Default time for requests to be executed once approved, in ISO-8601 duration format."""

    required_approvers = Size(
        data_key="required_approvers",
        allow_none=True,
    )
    r""" The number of required approvers, excluding the user that made the request."""

    @property
    def resource(self):
        return MultiAdminVerifyConfig

    gettable_fields = [
        "approval_expiry",
        "approval_groups",
        "enabled",
        "execution_expiry",
        "required_approvers",
    ]
    """approval_expiry,approval_groups,enabled,execution_expiry,required_approvers,"""

    patchable_fields = [
        "approval_expiry",
        "approval_groups",
        "enabled",
        "execution_expiry",
        "required_approvers",
    ]
    """approval_expiry,approval_groups,enabled,execution_expiry,required_approvers,"""

    postable_fields = [
        "approval_expiry",
        "approval_groups",
        "enabled",
        "execution_expiry",
        "required_approvers",
    ]
    """approval_expiry,approval_groups,enabled,execution_expiry,required_approvers,"""

class MultiAdminVerifyConfig(Resource):
    """Allows interaction with MultiAdminVerifyConfig objects on the host"""

    _schema = MultiAdminVerifyConfigSchema
    _path = "/api/security/multi-admin-verify"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the multi-admin-verify configuration.

### Learn more
* [`DOC /security/multi-admin-verify`](#docs-security-security_multi-admin-verify)"""
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
        r"""Modifies the multi-admin-verify configuration.

### Learn more
* [`DOC /security/multi-admin-verify`](#docs-security-security_multi-admin-verify)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



