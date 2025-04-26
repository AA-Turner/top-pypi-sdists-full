r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The CIFS server can use local groups for authorization when determining share, file and directory access rights.
You can use this API to display local group information and to control local group configurations.
## Retrieving local group information
The local group GET endpoint retrieves all of the local groups configurations for data SVMs.
## Examples
### Retrieving all of the fields for all of the local group configurations
The local group GET endpoint retrieves all of the local groups configurations for data SVMs.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LocalCifsGroup.get_collection(fields="**")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    LocalCifsGroup(
        {
            "members": [
                {"name": "CIFS_SERVER\\Administrator"},
                {"name": "AD_DOMAIN\\Domain Admins"},
            ],
            "sid": "S-1-5-32-544",
            "description": "Built-in Administrators group",
            "name": "BUILTIN\\Administrators",
            "svm": {"name": "vs1", "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16"},
        }
    ),
    LocalCifsGroup(
        {
            "members": [{"name": "AD_DOMAIN\\Domain Users"}],
            "sid": "S-1-5-32-545",
            "description": "All users",
            "name": "BUILTIN\\Users",
            "svm": {"name": "vs1", "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16"},
        }
    ),
    LocalCifsGroup(
        {
            "members": [{"name": "SACHILDAP02\\Domain Guests"}],
            "sid": "S-1-5-32-546",
            "description": "Built-in Guests Group",
            "name": "BUILTIN\\Guests",
            "svm": {"name": "vs1", "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16"},
        }
    ),
    LocalCifsGroup(
        {
            "sid": "S-1-5-32-547",
            "description": "Restricted administrative privileges",
            "name": "BUILTIN\\Power Users",
            "svm": {"name": "vs1", "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16"},
        }
    ),
    LocalCifsGroup(
        {
            "sid": "S-1-5-32-551",
            "description": "Backup Operators group",
            "name": "BUILTIN\\Backup Operators",
            "svm": {"name": "vs1", "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16"},
        }
    ),
    LocalCifsGroup(
        {
            "sid": "S-1-5-21-256008430-3394229847-3930036330-1001",
            "description": "local group2",
            "name": "CIFS_SERVER\\group2",
            "svm": {"name": "vs1", "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16"},
        }
    ),
    LocalCifsGroup(
        {
            "members": [
                {"name": "VS2.CIFS\\Administrator"},
                {"name": "VS2.CIFS\\user3"},
                {"name": "SACHILDAP02\\Domain Admins"},
            ],
            "sid": "S-1-5-32-544",
            "description": "Built-in Administrators group",
            "name": "BUILTIN\\Administrators",
            "svm": {"name": "vs2", "uuid": "5060077c-5be6-11eb-90b7-0050568e5169"},
        }
    ),
    LocalCifsGroup(
        {
            "members": [{"name": "SACHILDAP02\\Domain Users"}],
            "sid": "S-1-5-32-545",
            "description": "All users",
            "name": "BUILTIN\\Users",
            "svm": {"name": "vs2", "uuid": "5060077c-5be6-11eb-90b7-0050568e5169"},
        }
    ),
    LocalCifsGroup(
        {
            "members": [{"name": "SACHILDAP02\\Domain Guests"}],
            "sid": "S-1-5-32-546",
            "description": "Built-in Guests Group",
            "name": "BUILTIN\\Guests",
            "svm": {"name": "vs2", "uuid": "5060077c-5be6-11eb-90b7-0050568e5169"},
        }
    ),
    LocalCifsGroup(
        {
            "sid": "S-1-5-32-547",
            "description": "Restricted administrative privileges",
            "name": "BUILTIN\\Power Users",
            "svm": {"name": "vs2", "uuid": "5060077c-5be6-11eb-90b7-0050568e5169"},
        }
    ),
    LocalCifsGroup(
        {
            "sid": "S-1-5-32-551",
            "description": "Backup Operators group",
            "name": "BUILTIN\\Backup Operators",
            "svm": {"name": "vs2", "uuid": "5060077c-5be6-11eb-90b7-0050568e5169"},
        }
    ),
    LocalCifsGroup(
        {
            "sid": "S-1-5-21-1625922807-3304708894-3529444428-1001",
            "description": "local group1",
            "name": "CIFS_SERVER\\group1",
            "svm": {"name": "vs2", "uuid": "5060077c-5be6-11eb-90b7-0050568e5169"},
        }
    ),
]

```
</div>
</div>

### Retrieving a local group configuration of a specific SVM and group
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalCifsGroup(
        sid="S-1-5-21-256008430-3394229847-3930036330-1001",
        **{"svm.uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
LocalCifsGroup(
    {
        "sid": "S-1-5-21-256008430-3394229847-3930036330-1001",
        "description": "local group",
        "name": "CIFS_SERVER\\group1",
        "svm": {"name": "vs1", "uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"},
    }
)

```
</div>
</div>

## Creating a local group configuration
The local group POST endpoint creates a local group configuration for the specified SVM.
## Example
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalCifsGroup()
    resource.svm = {"uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    resource.name = "group1"
    resource.post(hydrate=True)
    print(resource)

```

## Updating a local group configuration
The local group PATCH endpoint updates the name and description of the specified local group and the specified SVM.
## Example
### Update the local group name from 'group1' to 'group2'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalCifsGroup(
        sid="S-1-5-21-256008430-3394229847-3930036330-1257",
        **{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
    )
    resource.name = "group2"
    resource.description = "local group"
    resource.patch()

```

## Deleting a local group configuration
The local group DELETE endpoint deletes the specified local group of the specified SVM.
## Example
### Delete the local group 'group1'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalCifsGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalCifsGroup(
        sid="S-1-5-21-256008430-3394229847-3930036330-1001",
        **{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"}
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


__all__ = ["LocalCifsGroup", "LocalCifsGroupSchema"]
__pdoc__ = {
    "LocalCifsGroupSchema.resource": False,
    "LocalCifsGroupSchema.opts": False,
}


class LocalCifsGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalCifsGroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the local_cifs_group."""

    description = marshmallow_fields.Str(
        data_key="description",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Description for the local group.


Example: This is a local group"""

    members = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.local_cifs_group_members_no_records.LocalCifsGroupMembersNoRecordsSchema", unknown=EXCLUDE, allow_none=True), data_key="members", allow_none=True)
    r""" The members field of the local_cifs_group."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" Local group name. The maximum supported length of a group name is 256 characters.


Example: SMB_SERVER01\group"""

    sid = marshmallow_fields.Str(
        data_key="sid",
        allow_none=True,
    )
    r""" The security ID of the local group which uniquely identifies the group. The group SID is automatically generated in POST and it is retrieved using the GET method.


Example: S-1-5-21-256008430-3394229847-3930036330-1001"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the local_cifs_group."""

    @property
    def resource(self):
        return LocalCifsGroup

    gettable_fields = [
        "links",
        "description",
        "members",
        "name",
        "sid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,description,members,name,sid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "description",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """description,name,svm.name,svm.uuid,"""

    postable_fields = [
        "description",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """description,name,svm.name,svm.uuid,"""

class LocalCifsGroup(Resource):
    """Allows interaction with LocalCifsGroup objects on the host"""

    _schema = LocalCifsGroupSchema
    _path = "/api/protocols/cifs/local-groups"
    _keys = ["svm.uuid", "sid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the local groups for all of the SVMs.
### Advanced properties
* `members`
### Related ONTAP commands
* `vserver cifs users-and-groups local-group show`
* `vserver cifs users-and-groups local-group show-members`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
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
        """Returns a count of all LocalCifsGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent LocalCifsGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["LocalCifsGroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the local group information of the specified group in the specified SVM. This API can also be used to rename a local group.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group modify`
* `vserver cifs users-and-groups local-group rename`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["LocalCifsGroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["LocalCifsGroup"], NetAppResponse]:
        r"""Creates the local group configuration for the specified SVM.
### Important notes
* The group name can contain up to 256 characters.
* The group name cannot be terminated by a period.
* The group name does not support any of the following characters: \" / ? [ ] , : | < > + = ; ? * @ or ASCII characters in the range 1-31.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the local group.
* `name` - Name of the local group.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group create`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
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
        records: Iterable["LocalCifsGroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a local group configuration for the specified SVM.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group delete`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the local groups for all of the SVMs.
### Advanced properties
* `members`
### Related ONTAP commands
* `vserver cifs users-and-groups local-group show`
* `vserver cifs users-and-groups local-group show-members`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves local group information for the specified group and SVM.
### Advanced properties
* `members`
### Related ONTAP commands
* `vserver cifs users-and-groups local-group show`
* `vserver cifs users-and-groups local-group show-members`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
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
        r"""Creates the local group configuration for the specified SVM.
### Important notes
* The group name can contain up to 256 characters.
* The group name cannot be terminated by a period.
* The group name does not support any of the following characters: \" / ? [ ] , : | < > + = ; ? * @ or ASCII characters in the range 1-31.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the local group.
* `name` - Name of the local group.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group create`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
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
        r"""Updates the local group information of the specified group in the specified SVM. This API can also be used to rename a local group.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group modify`
* `vserver cifs users-and-groups local-group rename`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
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
        r"""Deletes a local group configuration for the specified SVM.
### Related ONTAP commands
* `vserver cifs users-and-groups local-group delete`
### Learn more
* [`DOC /protocols/cifs/local-groups`](#docs-NAS-protocols_cifs_local-groups)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


