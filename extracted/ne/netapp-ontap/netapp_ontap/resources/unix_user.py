r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to display local UNIX user information and to control UNIX user configurations.
## Retrieving UNIX user information
You can use the UNIX user GET endpoint to retrieve all of the local UNIX user configurations for data SVMs.
## Examples
### Retrieving all of the fields for UNIX user configurations for all SVMs
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(UnixUser.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    UnixUser(
        {
            "full_name": "string",
            "primary_gid": 0,
            "name": "string",
            "id": 7,
            "svm": {"name": "vs1", "uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"},
        }
    ),
    UnixUser(
        {
            "full_name": "",
            "primary_gid": 65535,
            "name": "nobody",
            "id": 65535,
            "svm": {"name": "vs2", "uuid": "3f479a01-2971-11eb-88e1-0050568eefd4"},
        }
    ),
    UnixUser(
        {
            "full_name": "",
            "primary_gid": 65534,
            "name": "pcuser",
            "id": 65534,
            "svm": {"name": "vs2", "uuid": "3f479a01-2971-11eb-88e1-0050568eefd4"},
        }
    ),
    UnixUser(
        {
            "full_name": "",
            "primary_gid": 1,
            "name": "root",
            "id": 0,
            "svm": {"name": "vs2", "uuid": "3f479a01-2971-11eb-88e1-0050568eefd4"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving the UNIX user configuration of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            UnixUser.get_collection(
                fields="*", **{"svm.uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    UnixUser(
        {
            "full_name": "Full User Name for user1",
            "primary_gid": 1,
            "name": "user1",
            "id": 1,
            "svm": {"name": "vs1", "uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"},
        }
    )
]

```
</div>
</div>

---
### Retrieving a UNIX user configuration of a specific SVM and user
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixUser(
        name="user1", **{"svm.uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
UnixUser(
    {
        "full_name": "Full User Name for user1",
        "primary_gid": 1,
        "name": "user1",
        "id": 1,
        "svm": {"name": "vs1", "uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"},
    }
)

```
</div>
</div>

---
## Creating a UNIX user configuration
The UNIX user POST endpoint creates a UNIX user configuration for the specified SVM.
## Examples
### Creating a UNIX user configuration with all fields specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixUser()
    resource.full_name = "Full user name"
    resource.id = 7
    resource.name = "user2"
    resource.primary_gid = 10
    resource.skip_name_validation = False
    resource.svm = {"name": "vs1", "uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Creating a UNIX user configuration with only mandatory fields specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixUser()
    resource.id = 8
    resource.name = "user9"
    resource.primary_gid = 10
    resource.svm = {"name": "vs1", "uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"}
    resource.post(hydrate=True)
    print(resource)

```

---
## Updating a UNIX user configuration
The UNIX user PATCH endpoint updates the UNIX user configuration for the specified user and SVM. The following example shows a PATCH operation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixUser(
        name="user1", **{"svm.uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"}
    )
    resource.full_name = "Full name"
    resource.id = 7
    resource.primary_gid = 10
    resource.patch()

```

---
## Deleting a UNIX user configuration
The UNIX user DELETE endpoint deletes the specified UNIX user for the specified SVM. The following example shows a DELETE operation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import UnixUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = UnixUser(
        name="user1", **{"svm.uuid": "25b363a6-2971-11eb-88e1-0050568eefd4"}
    )
    resource.delete()

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


__all__ = ["UnixUser", "UnixUserSchema"]
__pdoc__ = {
    "UnixUserSchema.resource": False,
    "UnixUserSchema.opts": False,
}


class UnixUserSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the UnixUser object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the unix_user."""

    full_name = marshmallow_fields.Str(
        data_key="full_name",
        allow_none=True,
    )
    r""" User's full name.


Example: Full User Name for user1"""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" UNIX user ID of the specified user."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" UNIX user name to be added to the local database.


Example: user1"""

    primary_gid = Size(
        data_key="primary_gid",
        allow_none=True,
    )
    r""" Primary group ID to which the user belongs."""

    skip_name_validation = marshmallow_fields.Boolean(
        data_key="skip_name_validation",
        allow_none=True,
    )
    r""" Indicates whether or not the validation for the specified UNIX user name is disabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the unix_user."""

    @property
    def resource(self):
        return UnixUser

    gettable_fields = [
        "links",
        "full_name",
        "id",
        "name",
        "primary_gid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,full_name,id,name,primary_gid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "full_name",
        "id",
        "primary_gid",
    ]
    """full_name,id,primary_gid,"""

    postable_fields = [
        "full_name",
        "id",
        "name",
        "primary_gid",
        "skip_name_validation",
        "svm.name",
        "svm.uuid",
    ]
    """full_name,id,name,primary_gid,skip_name_validation,svm.name,svm.uuid,"""

class UnixUser(Resource):
    """Allows interaction with UnixUser objects on the host"""

    _schema = UnixUserSchema
    _path = "/api/name-services/unix-users"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all of the UNIX users for all of the SVMs.
### Important notes
* The current UNIX users count can be retrieved from the num_records field by calling the API with the parameter "return_records=false".
### Related ONTAP commands
* `vserver services name-service unix-user show`

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all UnixUser resources that match the provided query"""
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
        """Returns a list of RawResources that represent UnixUser resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["UnixUser"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates UNIX user information for the specified user and SVM.

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["UnixUser"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["UnixUser"], NetAppResponse]:
        r"""Creates the local UNIX user configuration for an SVM.<br/>
### Important notes
* The default limit for local UNIX users is 32768.

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["UnixUser"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a UNIX user configuration for the specified SVM.
### Related ONTAP commands
* `vserver services name-service unix-user delete`

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all of the UNIX users for all of the SVMs.
### Important notes
* The current UNIX users count can be retrieved from the num_records field by calling the API with the parameter "return_records=false".
### Related ONTAP commands
* `vserver services name-service unix-user show`

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves UNIX user information for the specified user and SVM.
### Related ONTAP commands
* `vserver services name-service unix-user show`

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
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
        r"""Creates the local UNIX user configuration for an SVM.<br/>
### Important notes
* The default limit for local UNIX users is 32768.

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
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
        r"""Updates UNIX user information for the specified user and SVM.

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
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
        r"""Deletes a UNIX user configuration for the specified SVM.
### Related ONTAP commands
* `vserver services name-service unix-user delete`

### Learn more
* [`DOC /name-services/unix-users`](#docs-name-services-name-services_unix-users)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


