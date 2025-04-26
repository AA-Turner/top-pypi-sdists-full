r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 group consists of one or many users. Policies are attached to the S3 group to have access control over S3 resources at group level.
## Examples
### Retrieving all fields for all S3 groups of an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Group

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            S3Group.get_collection(
                "12f3ba4c-7ae0-11e9-8c06-0050568ea123", fields="*", return_timeout=15
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
    S3Group(
        {
            "users": [{"name": "User1"}, {"name": "User2"}, {"name": "User3"}],
            "policies": [{"name": "Policy1"}, {"name": "Policy2"}, {"name": "Policy3"}],
            "name": "Admin-Group",
            "comment": "Admin group",
            "id": 5,
            "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
        }
    ),
    S3Group(
        {
            "users": [{"name": "User1"}, {"name": "User2"}, {"name": "User6"}],
            "policies": [{"name": "Policy1"}, {"name": "Policy2"}, {"name": "Policy3"}],
            "name": "Admin-Group1",
            "comment": "Admin group",
            "id": 6,
            "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
        }
    ),
]

```
</div>
</div>

### Retrieving the specified group in the SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Group

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Group("12f3ba4c-7ae0-11e9-8c06-0050568ea123", id=5)
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
S3Group(
    {
        "users": [{"name": "User1"}, {"name": "User2"}, {"name": "User3"}],
        "policies": [{"name": "Policy1"}, {"name": "Policy2"}, {"name": "Policy3"}],
        "name": "Admin-Group",
        "comment": "Admin group",
        "id": 5,
        "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
    }
)

```
</div>
</div>

### Creating an S3 group for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Group

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Group("12f3ba4c-7ae0-11e9-8c06-0050568ea123")
    resource.comment = "Admin group"
    resource.name = "Admin-Group"
    resource.policies = [{"name": "Policy1"}, {"name": "Policy2"}, {"name": "Policy3"}]
    resource.users = [{"name": "User1"}, {"name": "User2"}, {"name": "User3"}]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
S3Group(
    {
        "users": [{"name": "User1"}, {"name": "User2"}, {"name": "User3"}],
        "policies": [{"name": "Policy1"}, {"name": "Policy2"}, {"name": "Policy3"}],
        "name": "Admin-Group",
        "comment": "Admin group",
        "id": 5,
        "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
    }
)

```
</div>
</div>

### Updating an S3 group for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Group

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Group("12f3ba4c-7ae0-11e9-8c06-0050568ea123", id=5)
    resource.comment = "Admin group"
    resource.name = "Admin-Group"
    resource.policies = [{"name": "Policy1"}]
    resource.users = [{"name": "user-1"}]
    resource.patch()

```

### Deleting an S3 group for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Group

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Group("12f3ba4c-7ae0-11e9-8c06-0050568ea123", id=5)
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


__all__ = ["S3Group", "S3GroupSchema"]
__pdoc__ = {
    "S3GroupSchema.resource": False,
    "S3GroupSchema.opts": False,
}


class S3GroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3Group object"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Can contain any additional information about the group being created or modified.

Example: Admin group"""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" Specifies a unique Group ID used to identify a particular group. This parameter should not be specified in the POST or PATCH method. A Group ID is automatically generated and it is retrieved using the GET method. Group ID is SVM-scoped.

Example: 5"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=128),
        allow_none=True,
    )
    r""" Specifies the name of the group. A group name length can range from 1 to 128 characters and can only contain the following combination of characters 0-9, A-Z, a-z, "_", "+", "=", ",", ".","@", and "-".

Example: Admin-Group"""

    policies = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.s3_policy.S3PolicySchema", unknown=EXCLUDE, allow_none=True), data_key="policies", allow_none=True)
    r""" Specifies a list of policies that are attached to the group. The wildcard character "*" is a valid value for specifying all policies."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_group."""

    users = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.s3_user.S3UserSchema", unknown=EXCLUDE, allow_none=True), data_key="users", allow_none=True)
    r""" Specifies the list of users who belong to the group."""

    @property
    def resource(self):
        return S3Group

    gettable_fields = [
        "comment",
        "id",
        "name",
        "policies.links",
        "policies.name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "users.links",
        "users.name",
    ]
    """comment,id,name,policies.links,policies.name,svm.links,svm.name,svm.uuid,users.links,users.name,"""

    patchable_fields = [
        "comment",
        "name",
        "policies.name",
        "users.name",
    ]
    """comment,name,policies.name,users.name,"""

    postable_fields = [
        "comment",
        "name",
        "policies.name",
        "users.name",
    ]
    """comment,name,policies.name,users.name,"""

class S3Group(Resource):
    r""" This is a container for S3 user groups. """

    _schema = S3GroupSchema
    _path = "/api/protocols/s3/services/{svm[uuid]}/groups"
    _keys = ["svm.uuid", "id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the S3 group's SVM configuration.
### Related ONTAP commands
* `vserver object-store-server group show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
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
        """Returns a count of all S3Group resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3Group resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["S3Group"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 group configuration of an SVM.
### Important notes
- The following fields can be modified for a group:
* `name` - Group name that needs to be modified.
* `users` - List of users present in the group.
* `policies` - List of policies to be attached to this group.
### Recommended optional properties
* `comment` - Short description about the S3 Group.
### Related ONTAP commands
* `vserver object-store-server group modify`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3Group"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3Group"], NetAppResponse]:
        r"""Creates the S3 group configuration.
### Important notes
- Each SVM can have one or more s3 group configurations.
### Required properties
* `svm.uuid` - Existing SVM in which to create the user configuration.
* `name` - Group name that is to be created.
* `users` - List of users to be added into the group.
* `policies` - List of policies are to be attached to this group.
### Recommended optional properties
* `comment` - Short description about the S3 Group.
### Related ONTAP commands
* `vserver object-store-server group create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
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
        records: Iterable["S3Group"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 group configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server group delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the S3 group's SVM configuration.
### Related ONTAP commands
* `vserver object-store-server group show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the S3 group configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server group show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
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
        r"""Creates the S3 group configuration.
### Important notes
- Each SVM can have one or more s3 group configurations.
### Required properties
* `svm.uuid` - Existing SVM in which to create the user configuration.
* `name` - Group name that is to be created.
* `users` - List of users to be added into the group.
* `policies` - List of policies are to be attached to this group.
### Recommended optional properties
* `comment` - Short description about the S3 Group.
### Related ONTAP commands
* `vserver object-store-server group create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 group configuration of an SVM.
### Important notes
- The following fields can be modified for a group:
* `name` - Group name that needs to be modified.
* `users` - List of users present in the group.
* `policies` - List of policies to be attached to this group.
### Recommended optional properties
* `comment` - Short description about the S3 Group.
### Related ONTAP commands
* `vserver object-store-server group modify`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 group configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server group delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/groups`](#docs-object-store-protocols_s3_services_{svm.uuid}_groups)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


