r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API configures the Duo group for an SVM.
Specify the owner UUID. The owner UUID corresponds to the UUID of the SVM containing the Duo groups and can be obtained from the response body of the GET request performed on the API “/api/svm/svms".
## Examples
### Retrieving the specific configured Duo group(s) of the cluster or SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duogroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duogroup(
        name="test", **{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Duogroup(
    {
        "excluded_users": ["tsmith", "msmith"],
        "name": "test",
        "comment": "test group create",
        "owner": {"name": "cluster-1", "uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"},
    }
)

```
</div>
</div>

### Modifying a Duo group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duogroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duogroup(
        name="test", **{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"}
    )
    resource.comment = "Testing"
    resource.patch()

```

### Deleting a  Duo group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duogroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duogroup(
        name="test", **{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"}
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


__all__ = ["Duogroup", "DuogroupSchema"]
__pdoc__ = {
    "DuogroupSchema.resource": False,
    "DuogroupSchema.opts": False,
}


class DuogroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Duogroup object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the duogroup."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Comment for the Duo group."""

    excluded_users = marshmallow_fields.List(marshmallow_fields.Str, data_key="excluded_users", allow_none=True)
    r""" List of excluded users.

Example: ["user1","user2"]"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the group to be included in Duo authentication.

Example: AD_Group"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the duogroup."""

    @property
    def resource(self):
        return Duogroup

    gettable_fields = [
        "links",
        "comment",
        "excluded_users",
        "name",
        "owner.links",
        "owner.name",
        "owner.uuid",
    ]
    """links,comment,excluded_users,name,owner.links,owner.name,owner.uuid,"""

    patchable_fields = [
        "comment",
        "excluded_users",
    ]
    """comment,excluded_users,"""

    postable_fields = [
        "comment",
        "excluded_users",
        "name",
        "owner.name",
        "owner.uuid",
    ]
    """comment,excluded_users,name,owner.name,owner.uuid,"""

class Duogroup(Resource):
    r""" Group profile to include in Duo authentication. """

    _schema = DuogroupSchema
    _path = "/api/security/authentication/duo/groups"
    _keys = ["owner.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the configured groups.
### Related ONTAP commands
* `security login duo group show`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        """Returns a count of all Duogroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent Duogroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Duogroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a configured Duo group for a cluster or SVM.
### Related ONTAP commands
* `security login duo group modify`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Duogroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Duogroup"], NetAppResponse]:
        r"""Creates a Duo group.
### Required properties
* `name` - Group name
### Related ONTAP commands
* `security login duo group create`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        records: Iterable["Duogroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a Duo group of the SVM or cluster.
### Related ONTAP commands
* `security login duo group delete`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the configured groups.
### Related ONTAP commands
* `security login duo group show`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Duo group configured for an SVM or cluster.
### Related ONTAP commands
* `security login duo group show`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        r"""Creates a Duo group.
### Required properties
* `name` - Group name
### Related ONTAP commands
* `security login duo group create`
### Learn more
* [`DOC /security/authentication/duo/groups`](#docs-security-security_authentication_duo_groups)
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        r"""Updates a configured Duo group for a cluster or SVM.
### Related ONTAP commands
* `security login duo group modify`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
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
        r"""Deletes a Duo group of the SVM or cluster.
### Related ONTAP commands
* `security login duo group delete`
### Learn more
* [`DOC /security/authentication/duo/groups/{owner.uuid}/{name}`](#docs-security-security_authentication_duo_groups_{owner.uuid}_{name})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


