r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API changes the password for a local user account.<p/>
Only cluster administrators with the <i>"admin"</i> role can change the password for other cluster or SVM user accounts. If you are not a cluster administrator, you can only change your own password.
## Examples
### Changing the password of another cluster or SVM user account by a cluster administrator
Specify the user account name and the new password in the body of the POST request. The owner.uuid or owner.name are not required to be specified for a cluster-scoped user account.<p/>
For an SVM-scoped account, along with new password and user account name, specify either the SVM name as the owner.name or SVM uuid as the owner.uuid in the body of the POST request. These indicate the SVM for which the user account is created and can be obtained from the response body of a GET request performed on the <i>/api/svm/svms</i> API.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AccountPassword

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AccountPassword()
    resource.name = "cluster_user1"
    resource.password = "hello@1234"
    resource.post(hydrate=True)
    print(resource)

```

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AccountPassword

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AccountPassword()
    resource.owner.name = "svm1"
    resource.name = "svm_user1"
    resource.password = "hello@1234"
    resource.post(hydrate=True)
    print(resource)

```

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AccountPassword

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AccountPassword()
    resource.name = "cluster_user1"
    resource.password = "hello@1234"
    resource.password_hash_algorithm = "sha256"
    resource.post(hydrate=True)
    print(resource)

```

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AccountPassword

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AccountPassword()
    resource.owner.name = "svm1"
    resource.name = "svm_user1"
    resource.password = "hello@1234"
    resource.password_hash_algorithm = "sha256"
    resource.post(hydrate=True)
    print(resource)

```

### Changing the password of an SVM-scoped user
Note: The IP address in the URI must be same as one of the interfaces owned by the SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AccountPassword

with HostConnection("<svm-ip>", username="admin", password="password", verify=False):
    resource = AccountPassword()
    resource.name = "svm_user1"
    resource.password = "new1@1234"
    resource.post(hydrate=True)
    print(resource)

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


__all__ = ["AccountPassword", "AccountPasswordSchema"]
__pdoc__ = {
    "AccountPasswordSchema.resource": False,
    "AccountPasswordSchema.opts": False,
}


class AccountPasswordSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AccountPassword object"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The user account name whose password is being modified."""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the account_password."""

    password = marshmallow_fields.Str(
        data_key="password",
        validate=len_validation(minimum=8, maximum=128),
        allow_none=True,
    )
    r""" The password string"""

    password_hash_algorithm = marshmallow_fields.Str(
        data_key="password_hash_algorithm",
        validate=enum_validation(['sha512', 'sha256', 'md5']),
        allow_none=True,
    )
    r""" Optional property that specifies the password hash algorithm used to generate a hash of the user's password for password matching.

Valid choices:

* sha512
* sha256
* md5"""

    @property
    def resource(self):
        return AccountPassword

    gettable_fields = [
        "name",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "password_hash_algorithm",
    ]
    """name,owner.links,owner.name,owner.uuid,password_hash_algorithm,"""

    patchable_fields = [
        "name",
        "password",
        "password_hash_algorithm",
    ]
    """name,password,password_hash_algorithm,"""

    postable_fields = [
        "name",
        "owner.name",
        "owner.uuid",
        "password",
        "password_hash_algorithm",
    ]
    """name,owner.name,owner.uuid,password,password_hash_algorithm,"""

class AccountPassword(Resource):
    r""" The password object """

    _schema = AccountPasswordSchema
    _path = "/api/security/authentication/password"



    @classmethod
    def post_collection(
        cls,
        records: Iterable["AccountPassword"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["AccountPassword"], NetAppResponse]:
        r"""Updates the password for a user account.
### Required parameters
* `name` - User account name.
* `password` - New password for the user account.
### Optional parameters
* `owner.name` or `owner.uuid` - Name or UUID of the SVM for an SVM-scoped user account.
* `password_hash_algorithm` - Optional property that specifies the password hash algorithm used to generate a hash of the user's password for password matching. Default value is "sha512".
### Related ONTAP commands
* `security login password`
### Learn more
* [`DOC /security/authentication/password`](#docs-security-security_authentication_password)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)




    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the password for a user account.
### Required parameters
* `name` - User account name.
* `password` - New password for the user account.
### Optional parameters
* `owner.name` or `owner.uuid` - Name or UUID of the SVM for an SVM-scoped user account.
* `password_hash_algorithm` - Optional property that specifies the password hash algorithm used to generate a hash of the user's password for password matching. Default value is "sha512".
### Related ONTAP commands
* `security login password`
### Learn more
* [`DOC /security/authentication/password`](#docs-security-security_authentication_password)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




