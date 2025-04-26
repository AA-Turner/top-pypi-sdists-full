r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

### Overview
This API is used to manage group configurations in ONTAP. The POST request creates a group configuration. Various responses are shown in the examples below.
<br />
## Examples
### Creating a group configuration
The following output shows how to create a group configuration.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityGroup()
    resource.name = "AzureGroup1"
    resource.owner = {
        "name": "C1_sti213-vsim-sr023a_1718680001",
        "uuid": "116127b1-2d21-11ef-a5e1-005056ae1bc2",
    }
    resource.type = "entra"
    resource.uuid = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    resource.comment = "Azure Group"
    resource.post(hydrate=True)
    print(resource)

```

### Retrieving all group configurations
The following output shows all group configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityGroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityGroup.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    SecurityGroup(
        {
            "name": "AzureGroup1",
            "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "id": 1,
            "owner": {
                "name": "C1_sti213-vsim-sr023a_1718680001",
                "uuid": "116127b1-2d21-11ef-a5e1-005056ae1bc2",
            },
            "type": "entra",
        }
    )
]

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


__all__ = ["SecurityGroup", "SecurityGroupSchema"]
__pdoc__ = {
    "SecurityGroupSchema.resource": False,
    "SecurityGroupSchema.opts": False,
}


class SecurityGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityGroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_group."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Any comment regarding this group entry.

Example: Azure Group"""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Date and time indicating when this group entry was created."""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" Group ID which is unique per group across the system. It is a read-only field and it automatically assigns the next available unique number."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Group name.

Example: AzureGroup1"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the security_group."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['entra']),
        allow_none=True,
    )
    r""" Group type.

Valid choices:

* entra"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Group UUID from external Active Directory."""

    @property
    def resource(self):
        return SecurityGroup

    gettable_fields = [
        "links",
        "comment",
        "create_time",
        "id",
        "name",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "scope",
        "type",
        "uuid",
    ]
    """links,comment,create_time,id,name,owner.links,owner.name,owner.uuid,scope,type,uuid,"""

    patchable_fields = [
        "comment",
        "uuid",
    ]
    """comment,uuid,"""

    postable_fields = [
        "comment",
        "name",
        "owner.name",
        "owner.uuid",
        "type",
        "uuid",
    ]
    """comment,name,owner.name,owner.uuid,type,uuid,"""

class SecurityGroup(Resource):
    """Allows interaction with SecurityGroup objects on the host"""

    _schema = SecurityGroupSchema
    _path = "/api/security/groups"
    _keys = ["owner.uuid", "name", "type"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all group entries.
### Related ONTAP commands
* `security login group show`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SecurityGroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates configured group information.
### Related ONTAP commands
* `security login group modify`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SecurityGroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SecurityGroup"], NetAppResponse]:
        r"""Creates a group entry.
### Required properties
* `name`
### Optional properties
* `owner`
* `type`
* `uuid`
* `comment`
### Related ONTAP commands
* `security login group create`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityGroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a group entry.
### Related ONTAP commands
* `security login group delete`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all group entries.
### Related ONTAP commands
* `security login group show`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a group entry.
### Related ONTAP commands
* `security login group show`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
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
        r"""Creates a group entry.
### Required properties
* `name`
### Optional properties
* `owner`
* `type`
* `uuid`
* `comment`
### Related ONTAP commands
* `security login group create`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
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
        r"""Updates configured group information.
### Related ONTAP commands
* `security login group modify`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
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
        r"""Deletes a group entry.
### Related ONTAP commands
* `security login group delete`

### Learn more
* [`DOC /security/groups`](#docs-security-security_groups)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


