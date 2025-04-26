r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

### Overview
This API is used to manage and map groups to ONTAP roles. The POST request creates a group to role mapping. Various responses are shown in the examples below.
<br />
## Examples
### Creating a group to role mapping entry
The following output shows how to create a group to role mapping entry.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GroupRoleMappings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = GroupRoleMappings()
    resource.group_id = 1
    resource.ontap_role = {"name": "admin"}
    resource.comment = "Group1 admin role"
    resource.post(hydrate=True)
    print(resource)

```

### Retrieving all group to role mapping entries
The following output shows all group to role mapping entries.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import GroupRoleMappings

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(GroupRoleMappings.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[GroupRoleMappings({"ontap_role": {"name": "admin"}, "group_id": 1})]

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
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["GroupRoleMappings", "GroupRoleMappingsSchema"]
__pdoc__ = {
    "GroupRoleMappingsSchema.resource": False,
    "GroupRoleMappingsSchema.opts": False,
}


class GroupRoleMappingsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupRoleMappings object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the group_role_mappings."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Any comment regarding this group entry."""

    group_id = Size(
        data_key="group_id",
        allow_none=True,
    )
    r""" Group ID.

Example: 1"""

    ontap_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", data_key="ontap_role", unknown=EXCLUDE, allow_none=True)
    r""" The ontap_role field of the group_role_mappings."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    @property
    def resource(self):
        return GroupRoleMappings

    gettable_fields = [
        "links",
        "comment",
        "group_id",
        "ontap_role.links",
        "ontap_role.name",
        "scope",
    ]
    """links,comment,group_id,ontap_role.links,ontap_role.name,scope,"""

    patchable_fields = [
        "comment",
    ]
    """comment,"""

    postable_fields = [
        "comment",
        "group_id",
        "ontap_role.name",
    ]
    """comment,group_id,ontap_role.name,"""

class GroupRoleMappings(Resource):
    """Allows interaction with GroupRoleMappings objects on the host"""

    _schema = GroupRoleMappingsSchema
    _path = "/api/security/group/role-mappings"
    _keys = ["group_id", "ontap_role.name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all the group to role mapping entries.
### Related ONTAP commands
* `security login group role-mapping show`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all GroupRoleMappings resources that match the provided query"""
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
        """Returns a list of RawResources that represent GroupRoleMappings resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["GroupRoleMappings"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a configured group role-mapping.
### Related ONTAP commands
* `security login group role-mapping modify`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["GroupRoleMappings"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["GroupRoleMappings"], NetAppResponse]:
        r"""Creates a group to role mapping entry.
### Required properties
* `group_id`
* `ontap_role`
### Optional properties
* `comment`
### Related ONTAP commands
* `security login group role-mapping create`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["GroupRoleMappings"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a group to role mapping entry.
### Related ONTAP commands
* `security login group role-mapping delete`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all the group to role mapping entries.
### Related ONTAP commands
* `security login group role-mapping show`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a group to role mapping entry.
### Related ONTAP commands
* `security login group role-mapping show`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
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
        r"""Creates a group to role mapping entry.
### Required properties
* `group_id`
* `ontap_role`
### Optional properties
* `comment`
### Related ONTAP commands
* `security login group role-mapping create`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
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
        r"""Updates a configured group role-mapping.
### Related ONTAP commands
* `security login group role-mapping modify`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
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
        r"""Deletes a group to role mapping entry.
### Related ONTAP commands
* `security login group role-mapping delete`

### Learn more
* [`DOC /security/group/role-mappings`](#docs-security-security_group_role-mappings)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


