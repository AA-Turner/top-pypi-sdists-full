r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to retrieve and manage netgroups cache settings.
## Examples
### Retrieving a netgroup cache setting
---
The following example shows how to use the cache netgroup settings GET endpoint to retrieve netgroup cache settings.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetgroupsSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NetgroupsSettings.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NetgroupsSettings(
        {
            "negative_cache_enabled_byhost": True,
            "ttl_byhost": "P1D",
            "negative_ttl_byhost": "PT30M",
            "ttl_for_members": "PT30M",
            "enabled": True,
            "svm": {"name": "vs43", "uuid": "8a1a8730-2036-11ec-8457-005056bbcfdb"},
        }
    ),
    NetgroupsSettings(
        {
            "negative_cache_enabled_byhost": True,
            "ttl_byhost": "PT2H",
            "negative_ttl_byhost": "PT30M",
            "ttl_for_members": "PT30M",
            "enabled": True,
            "svm": {"name": "vs34", "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving a netgroup cache setting for a given SVM
---
The following example shows how to use the cache netgroup settings GET endpoint to retrieve netgroup cache settings for a given SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetgroupsSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetgroupsSettings(**{"svm.uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
NetgroupsSettings(
    {
        "negative_cache_enabled_byhost": True,
        "ttl_byhost": "P1D",
        "negative_ttl_byhost": "PT30M",
        "ttl_for_members": "PT30M",
        "enabled": True,
        "svm": {"name": "vs34", "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"},
    }
)

```
</div>
</div>

---
### Updating a netgroup cache setting
---
The following example shows how to use the cache netgroup settings PATCH endpoint to update netgroup cache settings.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetgroupsSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetgroupsSettings(**{"svm.uuid": "02c9e252-41be-11e9-81d5-00a0986138f9"})
    resource.ttl_byhost = "PT2H"
    resource.negative_ttl_byhost = "PT2M"
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


__all__ = ["NetgroupsSettings", "NetgroupsSettingsSchema"]
__pdoc__ = {
    "NetgroupsSettingsSchema.resource": False,
    "NetgroupsSettingsSchema.opts": False,
}


class NetgroupsSettingsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NetgroupsSettings object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the netgroups_settings."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether or not the cache is enabled."""

    negative_cache_enabled_byhost = marshmallow_fields.Boolean(
        data_key="negative_cache_enabled_byhost",
        allow_none=True,
    )
    r""" Indicates whether or not the negative cache is enabled."""

    negative_ttl_byhost = marshmallow_fields.Str(
        data_key="negative_ttl_byhost",
        allow_none=True,
    )
    r""" Specifies negative Time to Live by host, in ISO 8601 format.


Example: PT2M5S"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the netgroups_settings."""

    ttl_byhost = marshmallow_fields.Str(
        data_key="ttl_byhost",
        allow_none=True,
    )
    r""" Specifies Time to Live by host, in ISO 8601 format.


Example: PT24H"""

    ttl_for_members = marshmallow_fields.Str(
        data_key="ttl_for_members",
        allow_none=True,
    )
    r""" Specifies Time to Live for netgroup members, in ISO 8601 format.


Example: PT2M"""

    @property
    def resource(self):
        return NetgroupsSettings

    gettable_fields = [
        "links",
        "enabled",
        "negative_cache_enabled_byhost",
        "negative_ttl_byhost",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "ttl_byhost",
        "ttl_for_members",
    ]
    """links,enabled,negative_cache_enabled_byhost,negative_ttl_byhost,svm.links,svm.name,svm.uuid,ttl_byhost,ttl_for_members,"""

    patchable_fields = [
        "enabled",
        "negative_cache_enabled_byhost",
        "negative_ttl_byhost",
        "ttl_byhost",
        "ttl_for_members",
    ]
    """enabled,negative_cache_enabled_byhost,negative_ttl_byhost,ttl_byhost,ttl_for_members,"""

    postable_fields = [
        "enabled",
        "negative_cache_enabled_byhost",
        "negative_ttl_byhost",
        "ttl_byhost",
        "ttl_for_members",
    ]
    """enabled,negative_cache_enabled_byhost,negative_ttl_byhost,ttl_byhost,ttl_for_members,"""

class NetgroupsSettings(Resource):
    r""" Netgroups cache setting. """

    _schema = NetgroupsSettingsSchema
    _path = "/api/name-services/cache/netgroup/settings"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves netgroups cache settings.
### Related ONTAP commands
* `vserver services name-service cache netgroups settings show`
### Learn more
* [`DOC /name-services/cache/netgroup/settings`](#docs-name-services-name-services_cache_netgroup_settings)
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
        """Returns a count of all NetgroupsSettings resources that match the provided query"""
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
        """Returns a list of RawResources that represent NetgroupsSettings resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NetgroupsSettings"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a netgroup cache setting.
### Important notes
  - svm.uuid field cannot be empty.
  - Returns success in case no values are provided for update.
### Related ONTAP commands
* `vserver services name-service cache netgroups settings modify`
### Learn more
* [`DOC /name-services/cache/netgroup/settings`](#docs-name-services-name-services_cache_netgroup_settings)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves netgroups cache settings.
### Related ONTAP commands
* `vserver services name-service cache netgroups settings show`
### Learn more
* [`DOC /name-services/cache/netgroup/settings`](#docs-name-services-name-services_cache_netgroup_settings)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a netgroup cache setting for a given SVM.
### Related ONTAP commands
* `vserver services name-service cache netgroups settings show`
### Learn more
* [`DOC /name-services/cache/netgroup/settings`](#docs-name-services-name-services_cache_netgroup_settings)
"""
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
        r"""Updates a netgroup cache setting.
### Important notes
  - svm.uuid field cannot be empty.
  - Returns success in case no values are provided for update.
### Related ONTAP commands
* `vserver services name-service cache netgroups settings modify`
### Learn more
* [`DOC /name-services/cache/netgroup/settings`](#docs-name-services-name-services_cache_netgroup_settings)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



