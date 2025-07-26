r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to retrieve and configure relevant information related to the Global JIT (Just In Time) privilege configuration in the cluster.
## Examples
### Retrieving the configured JIT privilege settings for the cluster
Retrieves the JIT privileges for the cluster or a filtered list (for a specific SVM).
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityJitPrivilege

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SecurityJitPrivilege.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SecurityJitPrivilege(
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
            "_links": {
                "self": {
                    "href": "/api/security/jit-privileges/b009a9e7-4081-b576-7575-ada21efcaf16/ssh"
                }
            },
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


__all__ = ["SecurityJitPrivilege", "SecurityJitPrivilegeSchema"]
__pdoc__ = {
    "SecurityJitPrivilegeSchema.resource": False,
    "SecurityJitPrivilegeSchema.opts": False,
}


class SecurityJitPrivilegeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityJitPrivilege object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_jit_privilege."""

    application = marshmallow_fields.Str(
        data_key="application",
        validate=enum_validation(['ssh']),
        allow_none=True,
    )
    r""" The name of the application.


Valid choices:

* ssh"""

    default_session_validity_period = marshmallow_fields.Str(
        data_key="default_session_validity_period",
        allow_none=True,
    )
    r""" The default session validity period on this SVM.


Example: PT1H"""

    max_jit_validity_period = marshmallow_fields.Str(
        data_key="max_jit_validity_period",
        allow_none=True,
    )
    r""" The maximum JIT validity period allowed on this SVM.


Example: P90D"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the security_jit_privilege."""

    @property
    def resource(self):
        return SecurityJitPrivilege

    gettable_fields = [
        "links",
        "application",
        "default_session_validity_period",
        "max_jit_validity_period",
        "owner.links",
        "owner.name",
        "owner.uuid",
    ]
    """links,application,default_session_validity_period,max_jit_validity_period,owner.links,owner.name,owner.uuid,"""

    patchable_fields = [
        "default_session_validity_period",
        "max_jit_validity_period",
    ]
    """default_session_validity_period,max_jit_validity_period,"""

    postable_fields = [
        "application",
        "owner.name",
        "owner.uuid",
    ]
    """application,owner.name,owner.uuid,"""

class SecurityJitPrivilege(Resource):
    """Allows interaction with SecurityJitPrivilege objects on the host"""

    _schema = SecurityJitPrivilegeSchema
    _path = "/api/security/jit-privileges"
    _keys = ["owner.uuid", "application"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves global JIT privilege configurations on an SVM.
### Related ONTAP commands
* `security jit-privilege show`

### Learn more
* [`DOC /security/jit-privileges`](#docs-security-security_jit-privileges)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityJitPrivilege resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityJitPrivilege resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SecurityJitPrivilege"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies the JIT privilege configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege modify`

### Learn more
* [`DOC /security/jit-privileges`](#docs-security-security_jit-privileges)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves global JIT privilege configurations on an SVM.
### Related ONTAP commands
* `security jit-privilege show`

### Learn more
* [`DOC /security/jit-privileges`](#docs-security-security_jit-privileges)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the JIT privilege configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege show`

### Learn more
* [`DOC /security/jit-privileges`](#docs-security-security_jit-privileges)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies the JIT privilege configurations for an SVM.
### Related ONTAP commands
* `security jit-privilege modify`

### Learn more
* [`DOC /security/jit-privileges`](#docs-security-security_jit-privileges)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



