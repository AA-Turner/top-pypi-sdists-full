r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to retrieve and manage hosts cache settings.
## Examples
### Retrieving hosts cache settings
---
The following examples shows how to use the cache host settings GET endpoint to retrieve host cache settings.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import HostsSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(HostsSettings.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    HostsSettings(
        {
            "negative_cache_enabled": True,
            "uuid": "8a1a8730-2036-11ec-8457-005056bbcfdb",
            "enabled": True,
            "svm": {"name": "vs43", "uuid": "8a1a8730-2036-11ec-8457-005056bbcfdb"},
            "ttl": "P1D",
            "negative_ttl": "PT1M",
            "dns_ttl_enabled": True,
        }
    ),
    HostsSettings(
        {
            "negative_cache_enabled": True,
            "uuid": "951e8676-2035-11ec-bfe2-005056bb6bef",
            "enabled": True,
            "ttl": "P1D",
            "negative_ttl": "PT1M",
            "dns_ttl_enabled": True,
        }
    ),
    HostsSettings(
        {
            "negative_cache_enabled": True,
            "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef",
            "enabled": True,
            "svm": {"name": "vs34", "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"},
            "ttl": "P1D",
            "negative_ttl": "PT1M",
            "dns_ttl_enabled": True,
        }
    ),
]

```
</div>
</div>

---
### Retrieving host cache settings for a given SVM
---
The following examples shows how to use the cache hosts settings GET endpoint to retrieve hosts cache settings for a specific SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import HostsSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = HostsSettings(uuid="dc458b2f-2035-11ec-bfe2-005056bb6bef")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
HostsSettings(
    {
        "negative_cache_enabled": True,
        "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef",
        "enabled": False,
        "svm": {"name": "vs34", "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"},
        "ttl": "P1D",
        "negative_ttl": "PT1M",
        "dns_ttl_enabled": True,
    }
)

```
</div>
</div>

---
### Updating a hosts cache setting
---
The following example shows how to use the cache host settings PATCH endpoint to update a host cache setting.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import HostsSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = HostsSettings(uuid="02c9e252-41be-11e9-81d5-00a0986138f9")
    resource.ttl = "PT2H"
    resource.negative_ttl = "PT2M"
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


__all__ = ["HostsSettings", "HostsSettingsSchema"]
__pdoc__ = {
    "HostsSettingsSchema.resource": False,
    "HostsSettingsSchema.opts": False,
}


class HostsSettingsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the HostsSettings object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the hosts_settings."""

    dns_ttl_enabled = marshmallow_fields.Boolean(
        data_key="dns_ttl_enabled",
        allow_none=True,
    )
    r""" Specifies whether TTL is based on the DNS or host settings. If enabled, TTL from DNS is used.


Example: true"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether or not the cache is enabled."""

    negative_cache_enabled = marshmallow_fields.Boolean(
        data_key="negative_cache_enabled",
        allow_none=True,
    )
    r""" Indicates whether or not the negative cache is enabled."""

    negative_ttl = marshmallow_fields.Str(
        data_key="negative_ttl",
        allow_none=True,
    )
    r""" Specifies negative Time to Live, in ISO 8601 format.


Example: PT5M"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the hosts_settings."""

    ttl = marshmallow_fields.Str(
        data_key="ttl",
        allow_none=True,
    )
    r""" Specifies Time to Live (TTL), in ISO 8601 format.


Example: PT24H"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" UUID for the host record.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7"""

    @property
    def resource(self):
        return HostsSettings

    gettable_fields = [
        "links",
        "dns_ttl_enabled",
        "enabled",
        "negative_cache_enabled",
        "negative_ttl",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "ttl",
        "uuid",
    ]
    """links,dns_ttl_enabled,enabled,negative_cache_enabled,negative_ttl,svm.links,svm.name,svm.uuid,ttl,uuid,"""

    patchable_fields = [
        "dns_ttl_enabled",
        "enabled",
        "negative_cache_enabled",
        "negative_ttl",
        "ttl",
        "uuid",
    ]
    """dns_ttl_enabled,enabled,negative_cache_enabled,negative_ttl,ttl,uuid,"""

    postable_fields = [
        "dns_ttl_enabled",
        "enabled",
        "negative_cache_enabled",
        "negative_ttl",
        "ttl",
        "uuid",
    ]
    """dns_ttl_enabled,enabled,negative_cache_enabled,negative_ttl,ttl,uuid,"""

class HostsSettings(Resource):
    r""" Hosts cache setting. """

    _schema = HostsSettingsSchema
    _path = "/api/name-services/cache/host/settings"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves host cache settings.
### Related ONTAP commands
* `vserver services name-service cache hosts settings show`
### Learn more
* [`DOC /name-services/cache/host/settings`](#docs-name-services-name-services_cache_host_settings)
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
        """Returns a count of all HostsSettings resources that match the provided query"""
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
        """Returns a list of RawResources that represent HostsSettings resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["HostsSettings"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a host cache setting.
### Important notes
  - UUID field cannot be empty.
  - Returns success in case no values are provided for update.
### Related ONTAP commands
* `vserver services name-service cache hosts settings modify`
### Learn more
* [`DOC /name-services/cache/host/settings`](#docs-name-services-name-services_cache_host_settings)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves host cache settings.
### Related ONTAP commands
* `vserver services name-service cache hosts settings show`
### Learn more
* [`DOC /name-services/cache/host/settings`](#docs-name-services-name-services_cache_host_settings)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a host cache setting for a given SVM.
### Related ONTAP commands
* `vserver services name-service cache hosts settings show`
### Learn more
* [`DOC /name-services/cache/host/settings`](#docs-name-services-name-services_cache_host_settings)
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
        r"""Updates a host cache setting.
### Important notes
  - UUID field cannot be empty.
  - Returns success in case no values are provided for update.
### Related ONTAP commands
* `vserver services name-service cache hosts settings modify`
### Learn more
* [`DOC /name-services/cache/host/settings`](#docs-name-services-name-services_cache_host_settings)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



