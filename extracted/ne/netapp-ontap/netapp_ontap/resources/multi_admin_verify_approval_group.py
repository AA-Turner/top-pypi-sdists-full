r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
These APIs provide information about a specific multi-admin verification approval-group.
A group of users can be defined in a cluster server context.
Approval groups can be associated with a rule or global setting from which the associated request can retrieve approvals.
<br />
---
## Examples
### Retrieving a multi-admin-verify approval group
Displays information about a specific approval group and the users that are registered within that group.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyApprovalGroup

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyApprovalGroup(
        name="group1", **{"owner.uuid": "52b75787-7011-11ec-a23d-005056a78fd5"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
MultiAdminVerifyApprovalGroup(
    {
        "owner": {
            "name": "cluster1",
            "_links": {
                "self": {"href": "/api/svm/svms/52b75787-7011-11ec-a23d-005056a78fd5"}
            },
            "uuid": "52b75787-7011-11ec-a23d-005056a78fd5",
        },
        "name": "group1",
        "email": ["group1.approvers@email.com"],
        "approvers": ["admin"],
    }
)

```
</div>
</div>

---
### Updating a multi-admin-verify approval group
Modifies attributes of an approval group.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyApprovalGroup

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyApprovalGroup(
        name="group1", **{"owner.uuid": "52b75787-7011-11ec-a23d-005056a78fd5"}
    )
    resource.approvers = ["admin1"]
    resource.email = ["group1.approvers.new@email.com"]
    resource.patch()

```

---
### Deleting a multi-admin-verify approval group
Deletes the specified approval group.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyApprovalGroup

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyApprovalGroup(
        name="group1", **{"owner.uuid": "52b75787-7011-11ec-a23d-005056a78fd5"}
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


__all__ = ["MultiAdminVerifyApprovalGroup", "MultiAdminVerifyApprovalGroupSchema"]
__pdoc__ = {
    "MultiAdminVerifyApprovalGroupSchema.resource": False,
    "MultiAdminVerifyApprovalGroupSchema.opts": False,
}


class MultiAdminVerifyApprovalGroupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MultiAdminVerifyApprovalGroup object"""

    approvers = marshmallow_fields.List(marshmallow_fields.Str, data_key="approvers", allow_none=True)
    r""" List of users that can approve a request."""

    email = marshmallow_fields.List(marshmallow_fields.Str, data_key="email", allow_none=True)
    r""" Email addresses that are notified when a request is created, approved, vetoed, or executed."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the approval group."""

    owner = marshmallow_fields.Nested("netapp_ontap.models.multi_admin_verify_approval_group_owner.MultiAdminVerifyApprovalGroupOwnerSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner of the approval group. The only valid owner is currently the cluster."""

    @property
    def resource(self):
        return MultiAdminVerifyApprovalGroup

    gettable_fields = [
        "approvers",
        "email",
        "name",
        "owner",
    ]
    """approvers,email,name,owner,"""

    patchable_fields = [
        "approvers",
        "email",
        "owner",
    ]
    """approvers,email,owner,"""

    postable_fields = [
        "approvers",
        "email",
        "name",
        "owner",
    ]
    """approvers,email,name,owner,"""

class MultiAdminVerifyApprovalGroup(Resource):
    """Allows interaction with MultiAdminVerifyApprovalGroup objects on the host"""

    _schema = MultiAdminVerifyApprovalGroupSchema
    _path = "/api/security/multi-admin-verify/approval-groups"
    _keys = ["owner.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves multi-admin-verify approval groups.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups`](#docs-security-security_multi-admin-verify_approval-groups)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all MultiAdminVerifyApprovalGroup resources that match the provided query"""
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
        """Returns a list of RawResources that represent MultiAdminVerifyApprovalGroup resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["MultiAdminVerifyApprovalGroup"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a multi-admin-verify approval group.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups/{owner.uuid}/{name}`](#docs-security-security_multi-admin-verify_approval-groups_{owner.uuid}_{name})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["MultiAdminVerifyApprovalGroup"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["MultiAdminVerifyApprovalGroup"], NetAppResponse]:
        r"""Creates a multi-admin-verify approval group.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups`](#docs-security-security_multi-admin-verify_approval-groups)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["MultiAdminVerifyApprovalGroup"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a multi-admin-verify approval group.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups/{owner.uuid}/{name}`](#docs-security-security_multi-admin-verify_approval-groups_{owner.uuid}_{name})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves multi-admin-verify approval groups.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups`](#docs-security-security_multi-admin-verify_approval-groups)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a multi-admin-verify approval group.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups/{owner.uuid}/{name}`](#docs-security-security_multi-admin-verify_approval-groups_{owner.uuid}_{name})"""
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
        r"""Creates a multi-admin-verify approval group.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups`](#docs-security-security_multi-admin-verify_approval-groups)"""
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
        r"""Updates a multi-admin-verify approval group.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups/{owner.uuid}/{name}`](#docs-security-security_multi-admin-verify_approval-groups_{owner.uuid}_{name})"""
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
        r"""Deletes a multi-admin-verify approval group.

### Learn more
* [`DOC /security/multi-admin-verify/approval-groups/{owner.uuid}/{name}`](#docs-security-security_multi-admin-verify_approval-groups_{owner.uuid}_{name})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


