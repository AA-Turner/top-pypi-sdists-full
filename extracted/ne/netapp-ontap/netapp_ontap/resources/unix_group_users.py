r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve, add or delete UNIX users for an SVM's UNIX group.
## Retrieving UNIX users from an SVM's UNIX group
The UNIX group users GET endpoint retrieves UNIX users of the specified UNIX group and the SVM.
## Examples
### Retrieving all users from the group 'pcuser'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroupUsers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(UnixGroupUsers.get_collection("pcuser")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    UnixGroupUsers(
        {
            "unix_group": {"name": "pcuser"},
            "name": "user1",
            "_links": {
                "self": {
                    "href": "/api/name-services/unix-groups/f06686a2-c901-11eb-94b4-0050568e9f2c/pcuser/users/user1"
                }
            },
            "svm": {"name": "svm1", "uuid": "f06686a2-c901-11eb-94b4-0050568e9f2c"},
        }
    )
]

```
</div>
</div>

### Retrieving user 'user1' from the group 'pcuser'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroupUsers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixGroupUsers("pcuser", name="user1")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
UnixGroupUsers(
    {
        "unix_group": {"name": "pcuser"},
        "name": "user1",
        "_links": {
            "self": {
                "href": "/api/name-services/unix-groups/f06686a2-c901-11eb-94b4-0050568e9f2c/pcuser/users/user1"
            }
        },
        "svm": {"name": "svm1", "uuid": "f06686a2-c901-11eb-94b4-0050568e9f2c"},
    }
)

```
</div>
</div>

## Adding users to a UNIX group
The UNIX group users POST endpoint adds UNIX users to the specified UNIX group and the SVM.
Multiple users can be added in a single call using the "records" parameter.
## Examples
### Adding a single user to the group 'group1'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroupUsers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixGroupUsers("group1")
    resource.name = "user4"
    resource.post(hydrate=True)
    print(resource)

```

### Adding multiple users to the group 'group1' in a single REST call
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroupUsers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixGroupUsers("group1")
    resource.records = [{"name": "user1"}, {"name": "user2"}, {"name": "user3"}]
    resource.post(hydrate=True)
    print(resource)

```

## Deleting a user from a group of a specific SVM
## Example
### Delete the user 'user1' from group 'group1' in SVM 'vs1'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroupUsers

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixGroupUsers("group1", name="user1")
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


__all__ = ["UnixGroupUsers", "UnixGroupUsersSchema"]
__pdoc__ = {
    "UnixGroupUsersSchema.resource": False,
    "UnixGroupUsersSchema.opts": False,
}


class UnixGroupUsersSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the UnixGroupUsers object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the unix_group_users."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" UNIX user who belongs to the specified UNIX group and the SVM."""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.unix_group_users1.UnixGroupUsers1Schema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of UNIX users specified to add multiple users to a UNIX group in a single API call.
Not allowed when the `name` property is used."""

    skip_name_validation = marshmallow_fields.Boolean(
        data_key="skip_name_validation",
        allow_none=True,
    )
    r""" Indicates whether or not the validation for the specified UNIX user names is disabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the unix_group_users."""

    unix_group = marshmallow_fields.Nested("netapp_ontap.models.unix_group_users_unix_group.UnixGroupUsersUnixGroupSchema", data_key="unix_group", unknown=EXCLUDE, allow_none=True)
    r""" The unix_group field of the unix_group_users."""

    @property
    def resource(self):
        return UnixGroupUsers

    gettable_fields = [
        "links",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "unix_group",
    ]
    """links,name,svm.links,svm.name,svm.uuid,unix_group,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "records",
        "skip_name_validation",
    ]
    """name,records,skip_name_validation,"""

class UnixGroupUsers(Resource):
    """Allows interaction with UnixGroupUsers objects on the host"""

    _schema = UnixGroupUsersSchema
    _path = "/api/name-services/unix-groups/{svm[uuid]}/{unix_group[name]}/users"
    _keys = ["svm.uuid", "unix_group.name", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves users for the specified UNIX group and SVM.
### Related ONTAP commands
* `vserver services name-service unix-group show`

### Learn more
* [`DOC /name-services/unix-groups/{svm.uuid}/{unix_group.name}/users`](#docs-name-services-name-services_unix-groups_{svm.uuid}_{unix_group.name}_users)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all UnixGroupUsers resources that match the provided query"""
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
        """Returns a list of RawResources that represent UnixGroupUsers resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["UnixGroupUsers"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["UnixGroupUsers"], NetAppResponse]:
        r"""Adds users to the specified UNIX group and SVM.
### Important notes
- Multiple users can be added in a single call using the "records" parameter.
- "records" parameter must not be specified when "name" parameter is specified.
- Specified users are appended to the existing list of users.
- Duplicate users are ignored.
### Related ONTAP commands
* `vserver services name-service unix-group adduser`
* `vserver services name-service unix-group addusers`

### Learn more
* [`DOC /name-services/unix-groups/{svm.uuid}/{unix_group.name}/users`](#docs-name-services-name-services_unix-groups_{svm.uuid}_{unix_group.name}_users)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["UnixGroupUsers"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a user from the specified UNIX group.
### Related ONTAP commands
* `vserver services name-service unix-group deluser`

### Learn more
* [`DOC /name-services/unix-groups/{svm.uuid}/{unix_group.name}/users`](#docs-name-services-name-services_unix-groups_{svm.uuid}_{unix_group.name}_users)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves users for the specified UNIX group and SVM.
### Related ONTAP commands
* `vserver services name-service unix-group show`

### Learn more
* [`DOC /name-services/unix-groups/{svm.uuid}/{unix_group.name}/users`](#docs-name-services-name-services_unix-groups_{svm.uuid}_{unix_group.name}_users)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves users for the specified UNIX group and SVM.
### Related ONTAP commands
* `vserver services name-service unix-group show`

### Learn more
* [`DOC /name-services/unix-groups/{svm.uuid}/{unix_group.name}/users`](#docs-name-services-name-services_unix-groups_{svm.uuid}_{unix_group.name}_users)"""
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
        r"""Adds users to the specified UNIX group and SVM.
### Important notes
- Multiple users can be added in a single call using the "records" parameter.
- "records" parameter must not be specified when "name" parameter is specified.
- Specified users are appended to the existing list of users.
- Duplicate users are ignored.
### Related ONTAP commands
* `vserver services name-service unix-group adduser`
* `vserver services name-service unix-group addusers`

### Learn more
* [`DOC /name-services/unix-groups/{svm.uuid}/{unix_group.name}/users`](#docs-name-services-name-services_unix-groups_{svm.uuid}_{unix_group.name}_users)"""
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
        r"""Deletes a user from the specified UNIX group.
### Related ONTAP commands
* `vserver services name-service unix-group deluser`

### Learn more
* [`DOC /name-services/unix-groups/{svm.uuid}/{unix_group.name}/users`](#docs-name-services-name-services_unix-groups_{svm.uuid}_{unix_group.name}_users)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


