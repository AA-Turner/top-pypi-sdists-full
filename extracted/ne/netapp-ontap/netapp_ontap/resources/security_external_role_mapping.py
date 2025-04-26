r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

### Overview
This API is used to map external identity provider roles to ONTAP roles. The POST request creates an external role to ONTAP role mapping. Various responses are shown in the examples below.
### Examples
### Creating an external role to ONTAP role mapping entry
The following output shows how to create an external role to ONTAP role mapping entry.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityExternalRoleMapping

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityExternalRoleMapping()
    resource.external_role = "Administrator"
    resource.ontap_role = {"name": "admin"}
    resource.provider = "adfs"
    resource.comment = "Admin role"
    resource.post(hydrate=True)
    print(resource)

```

### Retrieving all external role to ONTAP role mapping entries
The following output shows all external role to ONTAP role mapping entries.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityExternalRoleMapping

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityExternalRoleMapping.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[SecurityExternalRoleMapping({"provider": "adfs", "external_role": "Administrator"})]

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


__all__ = ["SecurityExternalRoleMapping", "SecurityExternalRoleMappingSchema"]
__pdoc__ = {
    "SecurityExternalRoleMappingSchema.resource": False,
    "SecurityExternalRoleMappingSchema.opts": False,
}


class SecurityExternalRoleMappingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityExternalRoleMapping object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_external_role_mapping."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Any comment regarding this external-role-mapping entry."""

    external_role = marshmallow_fields.Str(
        data_key="external_role",
        allow_none=True,
    )
    r""" External Identity provider role."""

    ontap_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", data_key="ontap_role", unknown=EXCLUDE, allow_none=True)
    r""" The ontap_role field of the security_external_role_mapping."""

    provider = marshmallow_fields.Str(
        data_key="provider",
        validate=enum_validation(['adfs', 'auth0', 'entra', 'keycloak', 'basic']),
        allow_none=True,
    )
    r""" Type of the external identity provider.

Valid choices:

* adfs
* auth0
* entra
* keycloak
* basic"""

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
        allow_none=True,
    )
    r""" Date and time indicating when this external-role-mapping entry was created."""

    @property
    def resource(self):
        return SecurityExternalRoleMapping

    gettable_fields = [
        "links",
        "comment",
        "external_role",
        "ontap_role.links",
        "ontap_role.name",
        "provider",
        "timestamp",
    ]
    """links,comment,external_role,ontap_role.links,ontap_role.name,provider,timestamp,"""

    patchable_fields = [
        "comment",
        "ontap_role.name",
    ]
    """comment,ontap_role.name,"""

    postable_fields = [
        "comment",
        "external_role",
        "ontap_role.name",
        "provider",
    ]
    """comment,external_role,ontap_role.name,provider,"""

class SecurityExternalRoleMapping(Resource):
    """Allows interaction with SecurityExternalRoleMapping objects on the host"""

    _schema = SecurityExternalRoleMappingSchema
    _path = "/api/security/external-role-mappings"
    _keys = ["external_role", "provider"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all external-role-mapping entries.
### Related ONTAP commands
* `security login external-role-mapping show`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityExternalRoleMapping resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityExternalRoleMapping resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SecurityExternalRoleMapping"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an external-role-mapping entry.
### Related ONTAP commands
* `security login external-role-mapping modify`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SecurityExternalRoleMapping"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SecurityExternalRoleMapping"], NetAppResponse]:
        r"""Creates an external-role-mapping entry.
### Required properties
* `external_role`
* `provider`
* `ontap_role`
### Optional properties
* `comment`
### Related ONTAP commands
* `security login external-role-mapping create`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityExternalRoleMapping"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an external-role-mapping entry.
### Related ONTAP commands
* `security login external-role-mapping delete`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all external-role-mapping entries.
### Related ONTAP commands
* `security login external-role-mapping show`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an external-role-mapping entry.
### Related ONTAP commands
* `security login external-role-mapping show`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
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
        r"""Creates an external-role-mapping entry.
### Required properties
* `external_role`
* `provider`
* `ontap_role`
### Optional properties
* `comment`
### Related ONTAP commands
* `security login external-role-mapping create`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
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
        r"""Updates an external-role-mapping entry.
### Related ONTAP commands
* `security login external-role-mapping modify`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
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
        r"""Deletes an external-role-mapping entry.
### Related ONTAP commands
* `security login external-role-mapping delete`

### Learn more
* [`DOC /security/external-role-mappings`](#docs-security-security_external-role-mappings)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


