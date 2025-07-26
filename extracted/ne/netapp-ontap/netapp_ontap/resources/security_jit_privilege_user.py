r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to create, retrieve, and delete relevant information related to user-specific JIT privilege session configurations.
Prerequisites:
    You must create a user that has a JIT supported login method configured on the SVM that you want to create the elevated session configurations.
## Examples
### Creating the JIT session configuration for a user
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityJitPrivilegeUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityJitPrivilegeUser()
    resource.owner = {"name": "Cserver"}
    resource.account = {"name": "joe"}
    resource.application = "ssh"
    resource.role = {"name": "admin"}
    resource.session_validity = "PT30M"
    resource.jit_validity = "PT2H10M20S"
    resource.post(hydrate=True)
    print(resource)

```

### Retrieving the configured JIT privilege sessions for users
Retrieves the JIT privilege user session configurations or a filtered list (for a specific SVM, user, etc).
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityJitPrivilegeUser

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityJitPrivilegeUser.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    SecurityJitPrivilegeUser(
        {
            "owner": {
                "uuid": "b009a9e7-4081-b576-7575-ada21efcaf16",
                "name": "Cserver",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/b009a9e7-4081-b576-7575-ada21efcaf16"
                    }
                },
            },
            "application": "ssh",
            "account": {"name": "testUser"},
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


__all__ = ["SecurityJitPrivilegeUser", "SecurityJitPrivilegeUserSchema"]
__pdoc__ = {
    "SecurityJitPrivilegeUserSchema.resource": False,
    "SecurityJitPrivilegeUserSchema.opts": False,
}


class SecurityJitPrivilegeUserSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityJitPrivilegeUser object"""

    account = marshmallow_fields.Nested("netapp_ontap.resources.account.AccountSchema", data_key="account", unknown=EXCLUDE, allow_none=True)
    r""" The name of the user."""

    application = marshmallow_fields.Str(
        data_key="application",
        validate=enum_validation(['ssh']),
        allow_none=True,
    )
    r""" The name of the application.


Valid choices:

* ssh"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" The description of the elevation rule.


Example: Comment text"""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" The end date and time of the JIT privilege session in UTC.


Example: 2024-11-08T11:15:31.000+0000"""

    jit_state = marshmallow_fields.Str(
        data_key="jit_state",
        validate=enum_validation(['preactive', 'idle', 'active']),
        allow_none=True,
    )
    r""" The current status of the rule: preactive, idle, or active.


Valid choices:

* preactive
* idle
* active"""

    jit_validity = marshmallow_fields.Str(
        data_key="jit_validity",
        allow_none=True,
    )
    r""" The JIT validity period on this SVM for this user.


Example: P90D"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the security_jit_privilege_user."""

    role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", data_key="role", unknown=EXCLUDE, allow_none=True)
    r""" The role field of the security_jit_privilege_user."""

    session_validity = marshmallow_fields.Str(
        data_key="session_validity",
        allow_none=True,
    )
    r""" The session validity period on this SVM for this user.


Example: PT1H"""

    start_time = ImpreciseDateTime(
        data_key="start_time",
        allow_none=True,
    )
    r""" The start date and time of the JIT privilege session in UTC.


Example: 2024-11-08T10:15:31.000+0000"""

    @property
    def resource(self):
        return SecurityJitPrivilegeUser

    gettable_fields = [
        "account.links",
        "account.name",
        "application",
        "comment",
        "end_time",
        "jit_state",
        "jit_validity",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "role.links",
        "role.name",
        "session_validity",
        "start_time",
    ]
    """account.links,account.name,application,comment,end_time,jit_state,jit_validity,owner.links,owner.name,owner.uuid,role.links,role.name,session_validity,start_time,"""

    patchable_fields = [
        "account.name",
    ]
    """account.name,"""

    postable_fields = [
        "account.name",
        "application",
        "comment",
        "jit_validity",
        "owner.name",
        "owner.uuid",
        "role.name",
        "session_validity",
        "start_time",
    ]
    """account.name,application,comment,jit_validity,owner.name,owner.uuid,role.name,session_validity,start_time,"""

class SecurityJitPrivilegeUser(Resource):
    """Allows interaction with SecurityJitPrivilegeUser objects on the host"""

    _schema = SecurityJitPrivilegeUserSchema
    _path = "/api/security/jit-privilege-users"
    _keys = ["owner.uuid", "account.name", "application"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the JIT privilege user configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege user show`

### Learn more
* [`DOC /security/jit-privilege-users`](#docs-security-security_jit-privilege-users)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityJitPrivilegeUser resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityJitPrivilegeUser resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["SecurityJitPrivilegeUser"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SecurityJitPrivilegeUser"], NetAppResponse]:
        r"""Creates the JIT privilege user configurations for an SVM.
### Required properties
* `owner.uuid` - Account owner UUID.
* `account.name` - User name.
* `application` - Application
### Related ONTAP commands
* `security jit-privilege user create`

### Learn more
* [`DOC /security/jit-privilege-users`](#docs-security-security_jit-privilege-users)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityJitPrivilegeUser"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the JIT privilege user configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege user delete`
### Required properties
* `owner.uuid`
* `application`
* `account.name`

### Learn more
* [`DOC /security/jit-privilege-users`](#docs-security-security_jit-privilege-users)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the JIT privilege user configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege user show`

### Learn more
* [`DOC /security/jit-privilege-users`](#docs-security-security_jit-privilege-users)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the JIT privilege user configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege user show`

### Learn more
* [`DOC /security/jit-privilege-users`](#docs-security-security_jit-privilege-users)"""
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
        r"""Creates the JIT privilege user configurations for an SVM.
### Required properties
* `owner.uuid` - Account owner UUID.
* `account.name` - User name.
* `application` - Application
### Related ONTAP commands
* `security jit-privilege user create`

### Learn more
* [`DOC /security/jit-privilege-users`](#docs-security-security_jit-privilege-users)"""
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
        r"""Deletes the JIT privilege user configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege user delete`
### Required properties
* `owner.uuid`
* `application`
* `account.name`

### Learn more
* [`DOC /security/jit-privilege-users`](#docs-security-security_jit-privilege-users)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


