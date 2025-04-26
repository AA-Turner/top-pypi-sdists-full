r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API configures the Duo profile for an SVM.
Specify the owner UUID. The owner UUID corresponds to the UUID of the SVM containing the Duo profile and can be obtained from the response body of the GET request performed on the API “/api/svm/svms".
## Examples
### Retrieving the specific configured Duo profile of the cluster or SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duo(**{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Duo(
    {
        "status": "Ok",
        "fail_mode": "safe",
        "max_prompts": 1,
        "comment": "Duo profile for Cserver",
        "push_info": True,
        "owner": {"name": "cluster-1", "uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"},
        "api_host": "api-******.duosecurity.com",
        "integration_key": "AAAA1A11A1AAA1AAA111",
        "fingerprint": "xxxxxxxxxc8f58b1d52317e1212e9f067a958c387e5e2axxxxxxxxxxxxxxxxxx",
        "is_enabled": True,
        "auto_push": True,
    }
)

```
</div>
</div>

### Modifying the Duo profile
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duo(**{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"})
    resource.comment = "Testing"
    resource.auto_push = False
    resource.patch()

```

### Deleting the Duo profile
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Duo

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Duo(**{"owner.uuid": "f810005a-d908-11ed-a6e6-0050568e8ef2"})
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


__all__ = ["Duo", "DuoSchema"]
__pdoc__ = {
    "DuoSchema.resource": False,
    "DuoSchema.opts": False,
}


class DuoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Duo object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the duo."""

    api_host = marshmallow_fields.Str(
        data_key="api_host",
        allow_none=True,
    )
    r""" The URL at which the Duo API is hosted.

Example: api-****.duo.com"""

    auto_push = marshmallow_fields.Boolean(
        data_key="auto_push",
        allow_none=True,
    )
    r""" Automatically sends a push notification for authentication when using Duo.

Example: true"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Comment for the Duo profile."""

    fail_mode = marshmallow_fields.Str(
        data_key="fail_mode",
        validate=enum_validation(['safe', 'secure']),
        allow_none=True,
    )
    r""" Determines the behavior of the system when it cannot communicate with the Duo service.

Valid choices:

* safe
* secure"""

    fingerprint = marshmallow_fields.Str(
        data_key="fingerprint",
        allow_none=True,
    )
    r""" The SHA fingerprint corresponding to the Duo secret key."""

    http_proxy = marshmallow_fields.Str(
        data_key="http_proxy",
        allow_none=True,
    )
    r""" Specifies the HTTP proxy server to be used when connecting to the Duo service.

Example: IPaddress:port"""

    integration_key = marshmallow_fields.Str(
        data_key="integration_key",
        allow_none=True,
    )
    r""" The Integration Key associated with the Duo profile."""

    is_enabled = marshmallow_fields.Boolean(
        data_key="is_enabled",
        allow_none=True,
    )
    r""" Indicates whether the Duo authentication feature is active or inactive.

Example: true"""

    max_prompts = Size(
        data_key="max_prompts",
        validate=integer_validation(minimum=1, maximum=3),
        allow_none=True,
    )
    r""" The maximum number of authentication attempts allowed for a user before the process is terminated.

Example: 1"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the duo."""

    push_info = marshmallow_fields.Boolean(
        data_key="push_info",
        allow_none=True,
    )
    r""" Additional information sent along with the push notification for Duo authentication.

Example: true"""

    secret_key = marshmallow_fields.Str(
        data_key="secret_key",
        allow_none=True,
    )
    r""" The Secret Key associated with the Duo profile."""

    status = marshmallow_fields.Str(
        data_key="status",
        allow_none=True,
    )
    r""" Information on the reachability status of Duo.

Example: OK"""

    @property
    def resource(self):
        return Duo

    gettable_fields = [
        "links",
        "api_host",
        "auto_push",
        "comment",
        "fail_mode",
        "fingerprint",
        "http_proxy",
        "integration_key",
        "is_enabled",
        "max_prompts",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "push_info",
        "status",
    ]
    """links,api_host,auto_push,comment,fail_mode,fingerprint,http_proxy,integration_key,is_enabled,max_prompts,owner.links,owner.name,owner.uuid,push_info,status,"""

    patchable_fields = [
        "api_host",
        "auto_push",
        "comment",
        "fail_mode",
        "http_proxy",
        "integration_key",
        "is_enabled",
        "max_prompts",
        "owner.name",
        "owner.uuid",
        "push_info",
        "secret_key",
    ]
    """api_host,auto_push,comment,fail_mode,http_proxy,integration_key,is_enabled,max_prompts,owner.name,owner.uuid,push_info,secret_key,"""

    postable_fields = [
        "api_host",
        "auto_push",
        "comment",
        "fail_mode",
        "http_proxy",
        "integration_key",
        "is_enabled",
        "max_prompts",
        "owner.name",
        "owner.uuid",
        "push_info",
        "secret_key",
    ]
    """api_host,auto_push,comment,fail_mode,http_proxy,integration_key,is_enabled,max_prompts,owner.name,owner.uuid,push_info,secret_key,"""

class Duo(Resource):
    r""" Duo profile for the SVM or cluster-management server (Cserver). """

    _schema = DuoSchema
    _path = "/api/security/authentication/duo/profiles"
    _keys = ["owner.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the configured Duo profiles.
### Related ONTAP commands
* `security login duo show`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
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
        """Returns a count of all Duo resources that match the provided query"""
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
        """Returns a list of RawResources that represent Duo resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Duo"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a configured Duo profile for a cluster or an SVM.
### Related ONTAP commands
* `security login duo modify`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
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
        records: Iterable["Duo"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Duo"], NetAppResponse]:
        r"""Creates a Duo profile.
### Required properties
* `api_host` - Duo API host
* `integration_key` - Integration key
* `secret_key` - Secret key
### Related ONTAP commands
* `security login duo create`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
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
        records: Iterable["Duo"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the Duo profile of the SVM or cluster.
### Related ONTAP commands
* `security login duo delete`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the configured Duo profiles.
### Related ONTAP commands
* `security login duo show`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Duo profile configured for the cluster or an SVM.
### Related ONTAP commands
* `security login duo show`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
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
        r"""Creates a Duo profile.
### Required properties
* `api_host` - Duo API host
* `integration_key` - Integration key
* `secret_key` - Secret key
### Related ONTAP commands
* `security login duo create`
### Learn more
* [`DOC /security/authentication/duo/profiles`](#docs-security-security_authentication_duo_profiles)
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
        r"""Updates a configured Duo profile for a cluster or an SVM.
### Related ONTAP commands
* `security login duo modify`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
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
        r"""Deletes the Duo profile of the SVM or cluster.
### Related ONTAP commands
* `security login duo delete`
### Learn more
* [`DOC /security/authentication/duo/profiles/{owner.uuid}`](#docs-security-security_authentication_duo_profiles_{owner.uuid})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


