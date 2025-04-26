r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to retrieve or delete a role. The role can be SVM-scoped or cluster-scoped.<p/>
Specify the owner UUID and the role name in the URI path. The owner UUID corresponds to the UUID of the SVM for which the role has been created and can be obtained from the response body of a GET call performed on one of the following APIs:
<i>/api/security/roles</i> for all roles
<i>/api/security/roles/?scope=svm</i> for SVM-scoped roles
<i>/api/security/roles/?owner.name=<svm-name></i> for roles in a specific SVM
This API response contains the complete URI for each role that can be used for retrieving or deleting a role.<p/>
Note: The pre-defined roles can be retrieved but cannot be deleted.
## Examples
### Retrieving the role configuration for a REST role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Role

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Role(
        name="secure_role", **{"owner.uuid": "aaef7c38-4bd3-11e9-b238-0050568e2e25"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Role(
    {
        "builtin": False,
        "name": "secure_role",
        "owner": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/aaef7c38-4bd3-11e9-b238-0050568e2e25"}
            },
            "uuid": "aaef7c38-4bd3-11e9-b238-0050568e2e25",
        },
        "_links": {
            "self": {
                "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/secure_role"
            }
        },
        "privileges": [
            {
                "_links": {
                    "self": {
                        "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/secure_role/privileges/%2Fapi%2Fsecurity"
                    }
                },
                "access": "all",
                "path": "/api/security",
            },
            {
                "_links": {
                    "self": {
                        "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/secure_role/privileges/%2Fapi%2Fstorage%2Fvolumes%2F651f7fdf-7752-11eb-8d4e-0050568ed6bd%2Fsnapshots"
                    }
                },
                "access": "readonly",
                "path": "/api/storage/volumes/651f7fdf-7752-11eb-8d4e-0050568ed6bd/snapshots",
            },
            {
                "_links": {
                    "self": {
                        "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/secure_role/privileges/%2Fapi%2Fstorage%2Fvolumes%2F6dfeb406-9a16-11ec-819e-005056bb1a7c%2Ftop-metrics%2Fclients"
                    }
                },
                "access": "readonly",
                "path": "/api/storage/volumes/6dfeb406-9a16-11ec-819e-005056bb1a7c/top-metrics/clients",
            },
        ],
        "scope": "svm",
    }
)

```
</div>
</div>

### Retrieving the role configuration for a custom legacy role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Role

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Role(
        name="finVolNoDel", **{"owner.uuid": "aaef7c38-4bd3-11e9-b238-0050568e2e25"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Role(
    {
        "builtin": False,
        "name": "finVolNoDel",
        "owner": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/aaef7c38-4bd3-11e9-b238-0050568e2e25"}
            },
            "uuid": "aaef7c38-4bd3-11e9-b238-0050568e2e25",
        },
        "_links": {
            "self": {
                "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/finVolNoDel"
            }
        },
        "privileges": [
            {
                "_links": {
                    "self": {
                        "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/finVolNoDel/privileges/DEFAULT"
                    }
                },
                "access": "none",
                "path": "DEFAULT",
            },
            {
                "_links": {
                    "self": {
                        "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/finVolNoDel/privileges/volume"
                    }
                },
                "access": "all",
                "path": "volume",
            },
            {
                "query": "-volume vol_fin*",
                "_links": {
                    "self": {
                        "href": "/api/security/roles/aaef7c38-4bd3-11e9-b238-0050568e2e25/finVolNoDel/privileges/volume%20delete"
                    }
                },
                "access": "none",
                "path": "volume delete",
            },
        ],
        "scope": "svm",
    }
)

```
</div>
</div>

### Deleting a custom role
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Role

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Role(
        name="svm_role1", **{"owner.uuid": "aaef7c38-4bd3-11e9-b238-0050568e2e25"}
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


__all__ = ["Role", "RoleSchema"]
__pdoc__ = {
    "RoleSchema.resource": False,
    "RoleSchema.opts": False,
}


class RoleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Role object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the role."""

    builtin = marshmallow_fields.Boolean(
        data_key="builtin",
        allow_none=True,
    )
    r""" Indicates if this is a built-in (pre-defined) role which cannot be modified or deleted."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Role name

Example: admin"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the role."""

    privileges = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.role_privilege.RolePrivilegeSchema", unknown=EXCLUDE, allow_none=True), data_key="privileges", allow_none=True)
    r""" The list of privileges that this role has been granted."""

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
        return Role

    gettable_fields = [
        "links",
        "builtin",
        "name",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "privileges",
        "scope",
    ]
    """links,builtin,name,owner.links,owner.name,owner.uuid,privileges,scope,"""

    patchable_fields = [
        "privileges",
    ]
    """privileges,"""

    postable_fields = [
        "name",
        "owner.name",
        "owner.uuid",
        "privileges",
    ]
    """name,owner.name,owner.uuid,privileges,"""

class Role(Resource):
    r""" A named set of privileges that defines the rights an account has when it is assigned the role. """

    _schema = RoleSchema
    _path = "/api/security/roles"
    _keys = ["owner.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of roles configured in the cluster.
### Related ONTAP commands
* `security login rest-role show`
* `security login role show`
### Learn more
* [`DOC /security/roles`](#docs-security-security_roles)
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
        """Returns a count of all Role resources that match the provided query"""
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
        """Returns a list of RawResources that represent Role resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["Role"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Role"], NetAppResponse]:
        r"""Creates a new cluster-scoped role or an SVM-scoped role. For an SVM-scoped role, specify either the SVM name as the owner.name or SVM UUID as the owner.uuid in the request body along with other parameters for the role. The owner.uuid or owner.name are not required to be specified for a cluster-scoped role.
### Required parameters
* `name` - Name of the role to be created.
* `privileges` - Array of privilege tuples. Each tuple consists of a REST API or command/command directory path and its desired access level. If the tuple refers to a command/command directory path, it could optionally contain a query.
### Optional parameters
* `owner.name` or `owner.uuid`  - Name or UUID of the SVM for an SVM-scoped role.
### Related ONTAP commands
* `security login rest-role create`
* `security login role create`
### Learn more
* [`DOC /security/roles`](#docs-security-security_roles)
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
        records: Iterable["Role"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the specified role.
### Required parameters
* `name` - Name of the role to be deleted.
* `owner.uuid` - UUID of the SVM housing the role.
### Related ONTAP commands
* `security login rest-role delete`
* `security login role delete`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}`](#docs-security-security_roles_{owner.uuid}_{name})
* [`DOC /security/roles`](#docs-security-security_roles)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of roles configured in the cluster.
### Related ONTAP commands
* `security login rest-role show`
* `security login role show`
### Learn more
* [`DOC /security/roles`](#docs-security-security_roles)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of the specified role.
### Related ONTAP commands
* `security login rest-role show`
* `security login role show`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}`](#docs-security-security_roles_{owner.uuid}_{name})
* [`DOC /security/roles`](#docs-security-security_roles)
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
        r"""Creates a new cluster-scoped role or an SVM-scoped role. For an SVM-scoped role, specify either the SVM name as the owner.name or SVM UUID as the owner.uuid in the request body along with other parameters for the role. The owner.uuid or owner.name are not required to be specified for a cluster-scoped role.
### Required parameters
* `name` - Name of the role to be created.
* `privileges` - Array of privilege tuples. Each tuple consists of a REST API or command/command directory path and its desired access level. If the tuple refers to a command/command directory path, it could optionally contain a query.
### Optional parameters
* `owner.name` or `owner.uuid`  - Name or UUID of the SVM for an SVM-scoped role.
### Related ONTAP commands
* `security login rest-role create`
* `security login role create`
### Learn more
* [`DOC /security/roles`](#docs-security-security_roles)
"""
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
        r"""Deletes the specified role.
### Required parameters
* `name` - Name of the role to be deleted.
* `owner.uuid` - UUID of the SVM housing the role.
### Related ONTAP commands
* `security login rest-role delete`
* `security login role delete`
### Learn more
* [`DOC /security/roles/{owner.uuid}/{name}`](#docs-security-security_roles_{owner.uuid}_{name})
* [`DOC /security/roles`](#docs-security-security_roles)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


