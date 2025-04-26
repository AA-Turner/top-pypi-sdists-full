r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
These APIs provide information about a specific multi-admin verification rule.
Rules define the ONTAP commands (operations) that should be protected by multi-admin approval.
While the feature is turned on, any ONTAP operation that is defined with a rule will be enforced with multi-admin approval to execute the command (operation).
<br />
---
## Examples
### Retrieving a multi-admin-verify rule
Displays information about a specific multi admin verification rule.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyRule

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyRule(
        operation="volume+delete",
        **{"owner.uuid": "52b75787-7011-11ec-a23d-005056a78fd5"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
MultiAdminVerifyRule(
    {
        "create_time": "2022-01-07T22:14:03-05:00",
        "operation": "volume delete",
        "system_defined": False,
        "query": "-vserver vs0",
        "owner": {
            "name": "cluster1",
            "_links": {
                "self": {"href": "/api/svm/svms/52b75787-7011-11ec-a23d-005056a78fd5"}
            },
            "uuid": "52b75787-7011-11ec-a23d-005056a78fd5",
        },
        "required_approvers": 1,
        "auto_request_create": True,
    }
)

```
</div>
</div>

---
### Updating a multi-admin-verify rule
Modifies the attributes of the rule.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyRule

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyRule(
        operation="volume+delete",
        **{"owner.uuid": "52b75787-7011-11ec-a23d-005056a78fd5"}
    )
    resource.required_approvers = 1
    resource.patch()

```

---
### Deleting a multi-admin-verify rule
Deletes the specified approval group.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import MultiAdminVerifyRule

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = MultiAdminVerifyRule(
        operation="volume+delete",
        **{"owner.uuid": "52b75787-7011-11ec-a23d-005056a78fd5"}
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


__all__ = ["MultiAdminVerifyRule", "MultiAdminVerifyRuleSchema"]
__pdoc__ = {
    "MultiAdminVerifyRuleSchema.resource": False,
    "MultiAdminVerifyRuleSchema.opts": False,
}


class MultiAdminVerifyRuleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MultiAdminVerifyRule object"""

    approval_expiry = marshmallow_fields.Str(
        data_key="approval_expiry",
        allow_none=True,
    )
    r""" Time for requests to be approved, in ISO-8601 duration format. If not set, the global setting is used."""

    approval_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.multi_admin_verify_approval_group.MultiAdminVerifyApprovalGroupSchema", unknown=EXCLUDE, allow_none=True), data_key="approval_groups", allow_none=True)
    r""" List of approval groups that are allowed to approve requests for rules that don't have approval groups."""

    auto_request_create = marshmallow_fields.Boolean(
        data_key="auto_request_create",
        allow_none=True,
    )
    r""" When true, ONTAP automatically creates a request for any failed operation where there is no matching pending request."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The create_time field of the multi_admin_verify_rule."""

    execution_expiry = marshmallow_fields.Str(
        data_key="execution_expiry",
        allow_none=True,
    )
    r""" Time for requests to be executed once approved, in ISO-8601 duration format. If not set, the global setting is used."""

    operation = marshmallow_fields.Str(
        data_key="operation",
        allow_none=True,
    )
    r""" Command that requires one or more approvals."""

    owner = marshmallow_fields.Nested("netapp_ontap.models.multi_admin_verify_rule_owner.MultiAdminVerifyRuleOwnerSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner of the rule. The only valid owner is currently the cluster."""

    query = marshmallow_fields.Str(
        data_key="query",
        allow_none=True,
    )
    r""" When specified, this property limits the entries that require approvals to those that match the specified query."""

    required_approvers = Size(
        data_key="required_approvers",
        allow_none=True,
    )
    r""" The number of required approvers, excluding the user that made the request."""

    system_defined = marshmallow_fields.Boolean(
        data_key="system_defined",
        allow_none=True,
    )
    r""" Specifies whether the rule is system-defined or user-defined."""

    @property
    def resource(self):
        return MultiAdminVerifyRule

    gettable_fields = [
        "approval_expiry",
        "approval_groups.name",
        "auto_request_create",
        "create_time",
        "execution_expiry",
        "operation",
        "owner",
        "query",
        "required_approvers",
        "system_defined",
    ]
    """approval_expiry,approval_groups.name,auto_request_create,create_time,execution_expiry,operation,owner,query,required_approvers,system_defined,"""

    patchable_fields = [
        "approval_expiry",
        "approval_groups.name",
        "auto_request_create",
        "execution_expiry",
        "owner",
        "query",
        "required_approvers",
    ]
    """approval_expiry,approval_groups.name,auto_request_create,execution_expiry,owner,query,required_approvers,"""

    postable_fields = [
        "approval_expiry",
        "approval_groups.name",
        "auto_request_create",
        "execution_expiry",
        "operation",
        "owner",
        "query",
        "required_approvers",
    ]
    """approval_expiry,approval_groups.name,auto_request_create,execution_expiry,operation,owner,query,required_approvers,"""

class MultiAdminVerifyRule(Resource):
    """Allows interaction with MultiAdminVerifyRule objects on the host"""

    _schema = MultiAdminVerifyRuleSchema
    _path = "/api/security/multi-admin-verify/rules"
    _keys = ["owner.uuid", "operation"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves multi-admin-verify rules.

### Learn more
* [`DOC /security/multi-admin-verify/rules`](#docs-security-security_multi-admin-verify_rules)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all MultiAdminVerifyRule resources that match the provided query"""
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
        """Returns a list of RawResources that represent MultiAdminVerifyRule resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["MultiAdminVerifyRule"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a multi-admin-verify rule.

### Learn more
* [`DOC /security/multi-admin-verify/rules/{owner.uuid}/{operation}`](#docs-security-security_multi-admin-verify_rules_{owner.uuid}_{operation})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["MultiAdminVerifyRule"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["MultiAdminVerifyRule"], NetAppResponse]:
        r"""Creates a multi-admin-verify rule.

### Learn more
* [`DOC /security/multi-admin-verify/rules`](#docs-security-security_multi-admin-verify_rules)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["MultiAdminVerifyRule"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a multi-admin-verify rule.

### Learn more
* [`DOC /security/multi-admin-verify/rules/{owner.uuid}/{operation}`](#docs-security-security_multi-admin-verify_rules_{owner.uuid}_{operation})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves multi-admin-verify rules.

### Learn more
* [`DOC /security/multi-admin-verify/rules`](#docs-security-security_multi-admin-verify_rules)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a multi-admin-verify rule.

### Learn more
* [`DOC /security/multi-admin-verify/rules/{owner.uuid}/{operation}`](#docs-security-security_multi-admin-verify_rules_{owner.uuid}_{operation})"""
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
        r"""Creates a multi-admin-verify rule.

### Learn more
* [`DOC /security/multi-admin-verify/rules`](#docs-security-security_multi-admin-verify_rules)"""
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
        r"""Updates a multi-admin-verify rule.

### Learn more
* [`DOC /security/multi-admin-verify/rules/{owner.uuid}/{operation}`](#docs-security-security_multi-admin-verify_rules_{owner.uuid}_{operation})"""
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
        r"""Deletes a multi-admin-verify rule.

### Learn more
* [`DOC /security/multi-admin-verify/rules/{owner.uuid}/{operation}`](#docs-security-security_multi-admin-verify_rules_{owner.uuid}_{operation})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


