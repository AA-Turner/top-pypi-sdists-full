r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

##  Export Policies
### 1) Retrieve the export policy details
#### NOTE: This is used to read in the whole policy.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ExportPolicy.get_collection()))

```

---
### 2) Create an export policy for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportPolicy()
    resource.name = "P1"
    resource.rules = [
        {
            "clients": [{"match": "host1"}],
            "ro_rule": ["krb5"],
            "rw_rule": ["ntlm"],
            "anonymous_user": "anon1",
            "chown_mode": "restricted",
            "allow_suid": True,
        },
        {
            "clients": [{"match": "host2"}],
            "ro_rule": ["sys"],
            "rw_rule": ["ntlm"],
            "superuser": ["any"],
            "allow_device_creation": True,
            "ntfs_unix_security": "fail",
        },
    ]
    resource.post(hydrate=True)
    print(resource)

```

---
### 3) Update an export policy for an SVM
#### NOTE: This is used to either update the policy name or update all of the rules at once in an existing export policy.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportPolicy(id=8589934594)
    resource.name = "S1"
    resource.rules = [
        {"clients": [{"match": "host4"}], "ro_rule": ["krb5"], "rw_rule": ["ntlm"]}
    ]
    resource.patch()

```

---
### 4) Delete an export policy for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportPolicy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportPolicy(id=8589934594)
    resource.delete()

```

---
##  Export Rules
### 1) Retrieve the export policy rule details for an export policy
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportRule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ExportRule.get_collection(8589934595)))

```

---
### 2) Create an export policy rule for an export policy
#### NOTE: This is used to add a single new rule to an existing export policy.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportRule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportRule(8589934595)
    resource.clients = [{"match": "host2"}]
    resource.ro_rule = ["sys"]
    resource.rw_rule = ["ntlm"]
    resource.post(hydrate=True)
    print(resource)

```

---
### 3) Update an export policy rule for an export policy
#### NOTE: This is used to edit an existing single rule in an existing export policy.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportRule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportRule(8589934595, index=5)
    resource.clients = [{"match": "host4"}]
    resource.ro_rule = ["sys"]
    resource.rw_rule = ["krb5"]
    resource.patch(hydrate=True, new_index=10)

```

---
### 4) Delete an export policy rule for an export policy
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportRule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportRule(8589934595, index=15)
    resource.delete()

```

---
##  Export Clients
### 1) Retrieve the export client matches of an export policy rule
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportClient

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ExportClient.get_collection(8589934593, 2)))

```

---
### 2) Add an export client match to an export policy rule
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportClient

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportClient(8589934593, 1)
    resource.match = "host4"
    resource.post(hydrate=True)
    print(resource)

```

---
### 3) Delete an export client match from an export policy rule
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportClient

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ExportClient(8589934593, 1, match="host1,host2")
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


__all__ = ["ExportPolicy", "ExportPolicySchema"]
__pdoc__ = {
    "ExportPolicySchema.resource": False,
    "ExportPolicySchema.opts": False,
}


class ExportPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ExportPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the export_policy."""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" Export Policy ID"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Export Policy Name"""

    rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.export_rules.ExportRulesSchema", unknown=EXCLUDE, allow_none=True), data_key="rules", allow_none=True)
    r""" Rules of the Export Policy."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the export_policy."""

    @property
    def resource(self):
        return ExportPolicy

    gettable_fields = [
        "links",
        "id",
        "name",
        "rules",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,id,name,rules,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "name",
        "rules",
        "svm.name",
        "svm.uuid",
    ]
    """name,rules,svm.name,svm.uuid,"""

    postable_fields = [
        "name",
        "rules",
        "svm.name",
        "svm.uuid",
    ]
    """name,rules,svm.name,svm.uuid,"""

class ExportPolicy(Resource):
    """Allows interaction with ExportPolicy objects on the host"""

    _schema = ExportPolicySchema
    _path = "/api/protocols/nfs/export-policies"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves export policies.
### Related ONTAP commands
* `vserver export-policy show`
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        """Returns a count of all ExportPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent ExportPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["ExportPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of an export policy to change an export policy name or replace all export policy rules.
### Related ONTAP commands
* `vserver export-policy rename`
* `vserver export-policy rule delete`
* `vserver export-policy rule create`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["ExportPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ExportPolicy"], NetAppResponse]:
        r"""Creates an export policy. An SVM can have any number of export policies to define rules for which clients can access data exported by the SVM. A policy with no rules prohibits access.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create an export policy.
* `name`  - Name of the export policy.
### Recommended optional properties
* `rules`  - Rule(s) of an export policy. Used to create the export rule and populate the export policy with export rules in a single request.
* `rules[].index` - If you specify an index number that already matches a rule, the index number of the existing rule is incremented, as are the index numbers of all subsequent rules, either to the end of the list or to an open space in the list. If you do not specify an index number, the new rule is placed at the end of the policy's list.
### Related ONTAP commands
* `vserver export-policy create`
* `vserver export-policy rule create`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        records: Iterable["ExportPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an export policy.
### Related ONTAP commands
* `vserver export-policy delete`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves export policies.
### Related ONTAP commands
* `vserver export-policy show`
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an export policy.
### Related ONTAP commands
* `vserver export-policy show`
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        r"""Creates an export policy. An SVM can have any number of export policies to define rules for which clients can access data exported by the SVM. A policy with no rules prohibits access.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create an export policy.
* `name`  - Name of the export policy.
### Recommended optional properties
* `rules`  - Rule(s) of an export policy. Used to create the export rule and populate the export policy with export rules in a single request.
* `rules[].index` - If you specify an index number that already matches a rule, the index number of the existing rule is incremented, as are the index numbers of all subsequent rules, either to the end of the list or to an open space in the list. If you do not specify an index number, the new rule is placed at the end of the policy's list.
### Related ONTAP commands
* `vserver export-policy create`
* `vserver export-policy rule create`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        r"""Updates the properties of an export policy to change an export policy name or replace all export policy rules.
### Related ONTAP commands
* `vserver export-policy rename`
* `vserver export-policy rule delete`
* `vserver export-policy rule create`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        r"""Deletes an export policy.
### Related ONTAP commands
* `vserver export-policy delete`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


