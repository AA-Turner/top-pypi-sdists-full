r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API endpoint retrieves the username, role, and permissions information for the logged-in user.
## Examples
### Retrieves the username, role, and permissions information for the logged-in user.
Retrieves the username, role, and permissions information for the logged-in user.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Whoami

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Whoami()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Whoami(
    {
        "privileges": [{"access": "all", "path": "/api"}],
        "_links": {"self": {"href": "/api/security/login/whoami"}},
        "username": "admin",
    }
)

```
</div>
</div>
"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["Whoami", "WhoamiSchema"]
__pdoc__ = {
    "WhoamiSchema.resource": False,
    "WhoamiSchema.opts": False,
}

class WhoamiSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Whoami object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the whoami."""

    privileges = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.whoami_privileges", "WhoamiPrivilegesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="privileges",
                allow_none=True
            )
    r""" List of privileges"""

    roles = marshmallow_fields.List(marshmallow_fields.Str, data_key="roles", allow_none=True)
    r""" Role name or names"""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" User name

Example: tom"""

    @property
    def resource(self):
        return Whoami

    gettable_fields = [
        "links",
        "privileges",
        "roles",
        "username",
    ]
    """links,privileges,roles,username,"""

    patchable_fields = [
        "privileges",
        "roles",
        "username",
    ]
    """privileges,roles,username,"""

    postable_fields = [
        "privileges",
        "roles",
        "username",
    ]
    """privileges,roles,username,"""

class Whoami(Resource):
    """Allows interaction with Whoami objects on the host"""

    _schema = WhoamiSchema
    _path = "/api/security/login/whoami"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the username, role, and permissions information for the logged-in user.
### Related ONTAP commands
* `security login whoami`

### Learn more
* [`DOC /security/login/whoami`](#docs-security-security_login_whoami)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





