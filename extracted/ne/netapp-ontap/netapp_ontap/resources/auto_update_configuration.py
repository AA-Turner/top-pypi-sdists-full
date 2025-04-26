r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Use this API to query and retrieve a specific automatic package update configuration.<p/>
This API supports GET and PATCH calls. PATCH enables the `action` field to be updated for the specified configuration.
---
## Examples
### Retrieving settings for a specific automatic update
The following example shows how to retrieve configuration settings for an automatic update category:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutoUpdateConfiguration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutoUpdateConfiguration(uuid="440ae2e4-fd8f-4225-9bee-94e2da3f8d9d")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AutoUpdateConfiguration(
    {
        "action": "confirm",
        "description": {"message": "SP/BMC Firmware", "code": "131072402"},
        "uuid": "440ae2e4-fd8f-4225-9bee-94e2da3f8d9d",
        "category": "firmware",
    }
)

```
</div>
</div>

---
### Updating the settings for a specific automatic update
The following example shows how to modify configuration settings for an automatic update:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutoUpdateConfiguration

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutoUpdateConfiguration(uuid="440ae2e4-fd8f-4225-9bee-94e2da3f8d9d")
    resource.action = "confirm"
    resource.patch()

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


__all__ = ["AutoUpdateConfiguration", "AutoUpdateConfigurationSchema"]
__pdoc__ = {
    "AutoUpdateConfigurationSchema.resource": False,
    "AutoUpdateConfigurationSchema.opts": False,
}


class AutoUpdateConfigurationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AutoUpdateConfiguration object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the auto_update_configuration."""

    action = marshmallow_fields.Str(
        data_key="action",
        validate=enum_validation(['confirm', 'dismiss', 'automatic']),
        allow_none=True,
    )
    r""" The action to be taken by the alert source as specified by the user.

Valid choices:

* confirm
* dismiss
* automatic"""

    category = marshmallow_fields.Str(
        data_key="category",
        allow_none=True,
    )
    r""" Category for the configuration row.

Example: disk_fw"""

    description = marshmallow_fields.Nested("netapp_ontap.models.error_arguments.ErrorArgumentsSchema", data_key="description", unknown=EXCLUDE, allow_none=True)
    r""" The description field of the auto_update_configuration."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier for the configuration row.

Example: 572361f3-e769-439d-9c04-2ba48a08ff47"""

    @property
    def resource(self):
        return AutoUpdateConfiguration

    gettable_fields = [
        "links",
        "action",
        "category",
        "description",
        "uuid",
    ]
    """links,action,category,description,uuid,"""

    patchable_fields = [
        "action",
    ]
    """action,"""

    postable_fields = [
    ]
    """"""

class AutoUpdateConfiguration(Resource):
    """Allows interaction with AutoUpdateConfiguration objects on the host"""

    _schema = AutoUpdateConfigurationSchema
    _path = "/api/support/auto-update/configurations"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the configuration for automatic updates.

### Learn more
* [`DOC /support/auto-update/configurations`](#docs-support-support_auto-update_configurations)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all AutoUpdateConfiguration resources that match the provided query"""
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
        """Returns a list of RawResources that represent AutoUpdateConfiguration resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["AutoUpdateConfiguration"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the configuration for a specified automatic update.

### Learn more
* [`DOC /support/auto-update/configurations/{uuid}`](#docs-support-support_auto-update_configurations_{uuid})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the configuration for automatic updates.

### Learn more
* [`DOC /support/auto-update/configurations`](#docs-support-support_auto-update_configurations)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the configuration for a specified automatic update.

### Learn more
* [`DOC /support/auto-update/configurations/{uuid}`](#docs-support-support_auto-update_configurations_{uuid})"""
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
        r"""Updates the configuration for a specified automatic update.

### Learn more
* [`DOC /support/auto-update/configurations/{uuid}`](#docs-support-support_auto-update_configurations_{uuid})"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



