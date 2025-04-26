r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to retrieve and manage group-membership cache settings.
## Examples
### Retrieving group-membership cache settings
---
The following example shows how to use the cache group-membership settings GET endpoint to retrieve group-membership cache settings.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GroupMembershipSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(GroupMembershipSettings.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    GroupMembershipSettings(
        {
            "enabled": True,
            "svm": {"name": "vs43", "uuid": "8a1a8730-2036-11ec-8457-005056bbcfdb"},
            "ttl": "PT1H",
        }
    ),
    GroupMembershipSettings(
        {
            "enabled": True,
            "svm": {"name": "vs34", "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"},
            "ttl": "PT5M",
        }
    ),
]

```
</div>
</div>

---
### Retrieving group-membership cache settings for a given SVM
---
The following example shows how to use the cache group-membership settings GET endpoint to retrieve group-membership cache settings for a given SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GroupMembershipSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GroupMembershipSettings(
        **{"svm.uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
GroupMembershipSettings(
    {
        "enabled": True,
        "svm": {"name": "vs34", "uuid": "dc458b2f-2035-11ec-bfe2-005056bb6bef"},
        "ttl": "PT1H",
    }
)

```
</div>
</div>

---
### Updating a group-membership cache setting
---
The following example shows how to use the cache group-membership settings PATCH endpoint to update a group-membership setting.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUserSettings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixUserSettings(**{"svm.uuid": "02c9e252-41be-11e9-81d5-00a0986138f9"})
    resource.enabled = False
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


__all__ = ["GroupMembershipSettings", "GroupMembershipSettingsSchema"]
__pdoc__ = {
    "GroupMembershipSettingsSchema.resource": False,
    "GroupMembershipSettingsSchema.opts": False,
}


class GroupMembershipSettingsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupMembershipSettings object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the group_membership_settings."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies whether or not the cache is enabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the group_membership_settings."""

    ttl = marshmallow_fields.Str(
        data_key="ttl",
        allow_none=True,
    )
    r""" Specifies Time to Live for list of group members, in ISO 8601 format.


Example: PT2H30M"""

    @property
    def resource(self):
        return GroupMembershipSettings

    gettable_fields = [
        "links",
        "enabled",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "ttl",
    ]
    """links,enabled,svm.links,svm.name,svm.uuid,ttl,"""

    patchable_fields = [
        "enabled",
        "ttl",
    ]
    """enabled,ttl,"""

    postable_fields = [
        "enabled",
        "ttl",
    ]
    """enabled,ttl,"""

class GroupMembershipSettings(Resource):
    r""" Group membership cache setting. """

    _schema = GroupMembershipSettingsSchema
    _path = "/api/name-services/cache/group-membership/settings"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves group-membership cache settings.
### Related ONTAP commands
* `vserver services name-service cache group-membership settings show`
### Learn more
* [`DOC /name-services/cache/group-membership/settings`](#docs-name-services-name-services_cache_group-membership_settings)
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
        """Returns a count of all GroupMembershipSettings resources that match the provided query"""
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
        """Returns a list of RawResources that represent GroupMembershipSettings resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["GroupMembershipSettings"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a group-membership cache setting.
### Important notes
  - svm.uuid field cannot be empty.
  - Returns success in case no values are provided for update.
### Related ONTAP commands
* `vserver services name-service cache group-membership settings modify`
### Learn more
* [`DOC /name-services/cache/group-membership/settings`](#docs-name-services-name-services_cache_group-membership_settings)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves group-membership cache settings.
### Related ONTAP commands
* `vserver services name-service cache group-membership settings show`
### Learn more
* [`DOC /name-services/cache/group-membership/settings`](#docs-name-services-name-services_cache_group-membership_settings)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a group-membership cache setting for a given SVM.
### Related ONTAP commands
* `vserver services name-service cache group-membership settings show`
### Learn more
* [`DOC /name-services/cache/group-membership/settings`](#docs-name-services-name-services_cache_group-membership_settings)
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
        r"""Updates a group-membership cache setting.
### Important notes
  - svm.uuid field cannot be empty.
  - Returns success in case no values are provided for update.
### Related ONTAP commands
* `vserver services name-service cache group-membership settings modify`
### Learn more
* [`DOC /name-services/cache/group-membership/settings`](#docs-name-services-name-services_cache_group-membership_settings)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



