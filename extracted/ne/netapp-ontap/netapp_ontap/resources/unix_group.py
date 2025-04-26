r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to display local UNIX group information and to control UNIX group configurations.
## Retrieving UNIX group information
The UNIX group GET endpoint retrieves all of the local UNIX groups configurations for data SVMs.
## Examples
### Retrieving all of the fields for all of the UNIX group configurations
The UNIX group GET endpoint retrieves all of the local UNIX groups configurations for data SVMs.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(UnixGroup.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    UnixGroup(
        {
            "users": [{"name": "user1"}, {"name": "user2"}, {"name": "user3"}],
            "name": "group1",
            "_links": {
                "self": {
                    "href": "/api/name-services/unix-groups/b009a9e7-4081-b576-7575-ada21efcaf16/group1"
                }
            },
            "id": 11,
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b009a9e7-4081-b576-7575-ada21efcaf16"
                    }
                },
                "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16",
            },
        }
    ),
    UnixGroup(
        {
            "users": [{"name": "user1"}, {"name": "user2"}],
            "name": "group2",
            "_links": {
                "self": {
                    "href": "/api/name-services/unix-groups/b009a9e7-4081-b576-7575-ada21efcaf16/group2"
                }
            },
            "id": 12,
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b009a9e7-4081-b576-7575-ada21efcaf16"
                    }
                },
                "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16",
            },
        }
    ),
    UnixGroup(
        {
            "users": [{"name": "user2"}, {"name": "user3"}],
            "name": "group1",
            "_links": {
                "self": {
                    "href": "/api/name-services/unix-groups/b009a9e7-4081-b576-7575-ada21efcad17/group1"
                }
            },
            "id": 11,
            "svm": {
                "name": "vs2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b009a9e7-4081-b576-7575-ada21efcad17"
                    }
                },
                "uuid": "b009a9e7-4081-b576-7575-ada21efcad17",
            },
        }
    ),
]

```
</div>
</div>

### Retrieving all of the UNIX group configurations whose group name is 'group1'.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(UnixGroup.get_collection(name="group1")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    UnixGroup(
        {
            "name": "group1",
            "_links": {
                "self": {
                    "href": "/api/name-services/unix-groups/b009a9e7-4081-b576-7575-ada21efcaf16/group1"
                }
            },
            "id": 11,
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b009a9e7-4081-b576-7575-ada21efcaf16"
                    }
                },
                "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16",
            },
        }
    )
]

```
</div>
</div>

## Creating a UNIX group configuration
The UNIX group POST endpoint creates a UNIX group configuration for the specified SVM.
## Example
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixGroup()
    resource.svm = {"uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    resource.name = "group1"
    resource.id = 111
    resource.post(hydrate=True)
    print(resource)

```

## Updating a UNIX group configuration
The UNIX group PATCH endpoint updates the UNIX group ID of the specified UNIX group and the specified SVM.
## Example
### Modify the group ID of group1 to 112
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixGroup(
        name="group1", **{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    )
    resource.id = 112
    resource.patch()

```

## Deleting a UNIX group configuration
The UNIX group DELETE endpoint deletes the specified UNIX group of the specified SVM.
## Example
### Delete the group 'group1'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixGroup(
        name="group1", **{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    )
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


__all__ = ["UnixGroup", "UnixGroupSchema"]
__pdoc__ = {
    "UnixGroupSchema.resource": False,
    "UnixGroupSchema.opts": False,
}


class UnixGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the UnixGroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the unix_group."""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" UNIX group ID of the specified user."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" UNIX group name to be added to the local database.


Example: group1"""

    skip_name_validation = marshmallow_fields.Boolean(
        data_key="skip_name_validation",
        allow_none=True,
    )
    r""" Indicates whether or not the validation for the specified UNIX group name is disabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the unix_group."""

    users = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.unix_group_users_no_records.UnixGroupUsersNoRecordsSchema", unknown=EXCLUDE, allow_none=True), data_key="users", allow_none=True)
    r""" The users field of the unix_group."""

    @property
    def resource(self):
        return UnixGroup

    gettable_fields = [
        "links",
        "id",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "users",
    ]
    """links,id,name,svm.links,svm.name,svm.uuid,users,"""

    patchable_fields = [
        "id",
    ]
    """id,"""

    postable_fields = [
        "id",
        "name",
        "skip_name_validation",
        "svm.name",
        "svm.uuid",
    ]
    """id,name,skip_name_validation,svm.name,svm.uuid,"""

class UnixGroup(Resource):
    """Allows interaction with UnixGroup objects on the host"""

    _schema = UnixGroupSchema
    _path = "/api/name-services/unix-groups"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the UNIX groups for all of the SVMs. UNIX users who are the members of the group are also displayed.
### Related ONTAP commands
* `vserver services name-service unix-group show`
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
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
        """Returns a count of all UnixGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent UnixGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["UnixGroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the UNIX group information of the specified group in the specified SVM.
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["UnixGroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["UnixGroup"], NetAppResponse]:
        r"""Creates the local UNIX group configuration for the specified SVM.<br/>
Group name and group ID are mandatory parameters.
### Important notes
* The default limit for local UNIX groups and group members is 32768.
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
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
        records: Iterable["UnixGroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a UNIX group configuration for the specified SVM.
### Related ONTAP commands
* `vserver services name-service unix-group delete`
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the UNIX groups for all of the SVMs. UNIX users who are the members of the group are also displayed.
### Related ONTAP commands
* `vserver services name-service unix-group show`
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves UNIX group information for the specified group and SVM. UNIX users who are part of this group
are also retrieved.
### Related ONTAP commands
* `vserver services name-service unix-group show`
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
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
        r"""Creates the local UNIX group configuration for the specified SVM.<br/>
Group name and group ID are mandatory parameters.
### Important notes
* The default limit for local UNIX groups and group members is 32768.
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
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
        r"""Updates the UNIX group information of the specified group in the specified SVM.
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
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
        r"""Deletes a UNIX group configuration for the specified SVM.
### Related ONTAP commands
* `vserver services name-service unix-group delete`
### Learn more
* [`DOC /name-services/unix-groups`](#docs-name-services-name-services_unix-groups)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


