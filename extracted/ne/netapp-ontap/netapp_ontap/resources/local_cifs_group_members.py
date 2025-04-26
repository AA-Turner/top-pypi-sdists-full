r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to display local group members and to add or delete local users, Active Directory users and/or Active Directory groups to a local group of an SVM.
## Examples
### Retrieving the members of a specific local group
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroupMembers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            LocalCifsGroupMembers.get_collection(
                "S-1-5-21-256008430-3394229847-3930036330-1257"
            )
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    LocalCifsGroupMembers({"name": "CIFS_SERVER1\\user1"}),
    LocalCifsGroupMembers({"name": "CIFS_SERVER1\\user2"}),
]

```
</div>
</div>

## Adding members to a local group
The local group members POST endpoint adds local users, Active Directory users and/or Active Directory groups to the specified local group and the SVM.
### Adding local users to a group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroupMembers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalCifsGroupMembers("S-1-5-21-256008430-3394229847-3930036330-1001")
    resource.records = [{"name": "user1"}, {"name": "user2"}]
    resource.post(hydrate=True)
    print(resource)

```

## Deleting local users from the local group of a specific SVM
## Example
### Delete the local users 'user1' and 'user2' from the specified local group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroupMembers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalCifsGroupMembers("S-1-5-21-256008430-3394229847-3930036330-1001")
    resource.delete(body={"records": [{"name": "user1"}, {"name": "user2"}]})

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


__all__ = ["LocalCifsGroupMembers", "LocalCifsGroupMembersSchema"]
__pdoc__ = {
    "LocalCifsGroupMembersSchema.resource": False,
    "LocalCifsGroupMembersSchema.opts": False,
}


class LocalCifsGroupMembersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalCifsGroupMembers object"""

    local_cifs_group = marshmallow_fields.Nested("netapp_ontap.models.local_cifs_group_members_local_cifs_group.LocalCifsGroupMembersLocalCifsGroupSchema", data_key="local_cifs_group", unknown=EXCLUDE, allow_none=True)
    r""" The local_cifs_group field of the local_cifs_group_members."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Local user, Active Directory user, or Active Directory group which is a member of the specified local group."""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.local_cifs_group_members1.LocalCifsGroupMembers1Schema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of local users, Active Directory users, and Active Directory groups specified to add or delete multiple members to or from a local group in a single API call.
Not allowed when the `name` property is used."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the local_cifs_group_members."""

    @property
    def resource(self):
        return LocalCifsGroupMembers

    gettable_fields = [
        "local_cifs_group",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """local_cifs_group,name,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "records",
    ]
    """records,"""

    postable_fields = [
        "name",
        "records",
    ]
    """name,records,"""

class LocalCifsGroupMembers(Resource):
    """Allows interaction with LocalCifsGroupMembers objects on the host"""

    _schema = LocalCifsGroupMembersSchema
    _path = "/api/protocols/cifs/local-groups/{svm[uuid]}/{local_cifs_group[sid]}/members"
    _keys = ["svm.uuid", "local_cifs_group.sid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves local users, Active Directory users and Active Directory groups which are members of the specified local group and SVM.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group show-members`
### Learn more
* [`DOC /protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members`](#docs-NAS-protocols_cifs_local-groups_{svm.uuid}_{local_cifs_group.sid}_members)
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
        """Returns a count of all LocalCifsGroupMembers resources that match the provided query"""
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
        """Returns a list of RawResources that represent LocalCifsGroupMembers resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["LocalCifsGroupMembers"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["LocalCifsGroupMembers"], NetAppResponse]:
        r"""Adds local users, Active Directory users and Active Directory groups to the specified local group and SVM.
### Important note
* Specified members are appended to the existing list of members.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM for which members are added to local group.
* `local_cifs_group.sid` -  Security ID of the local group to which members are added.
* `name` or `records` - Local users, Active Directory users, or Active Directory groups to be added to a particular local group.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group add-members`
### Learn more
* [`DOC /protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members`](#docs-NAS-protocols_cifs_local-groups_{svm.uuid}_{local_cifs_group.sid}_members)
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
        records: Iterable["LocalCifsGroupMembers"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the local user, Active Directory user and/or Active Directory group from the specified local group and SVM.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group remove-members`
### Learn more
* [`DOC /protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members`](#docs-NAS-protocols_cifs_local-groups_{svm.uuid}_{local_cifs_group.sid}_members)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves local users, Active Directory users and Active Directory groups which are members of the specified local group and SVM.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group show-members`
### Learn more
* [`DOC /protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members`](#docs-NAS-protocols_cifs_local-groups_{svm.uuid}_{local_cifs_group.sid}_members)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves local user, Active Directory user and Active Directory group which is member of the specified local group and SVM.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group show-members`
### Learn more
* [`DOC /protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members`](#docs-NAS-protocols_cifs_local-groups_{svm.uuid}_{local_cifs_group.sid}_members)
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
        r"""Adds local users, Active Directory users and Active Directory groups to the specified local group and SVM.
### Important note
* Specified members are appended to the existing list of members.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM for which members are added to local group.
* `local_cifs_group.sid` -  Security ID of the local group to which members are added.
* `name` or `records` - Local users, Active Directory users, or Active Directory groups to be added to a particular local group.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group add-members`
### Learn more
* [`DOC /protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members`](#docs-NAS-protocols_cifs_local-groups_{svm.uuid}_{local_cifs_group.sid}_members)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the local user, Active Directory user and/or Active Directory group from the specified local group and SVM.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group remove-members`
### Learn more
* [`DOC /protocols/cifs/local-groups/{svm.uuid}/{local_cifs_group.sid}/members`](#docs-NAS-protocols_cifs_local-groups_{svm.uuid}_{local_cifs_group.sid}_members)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


