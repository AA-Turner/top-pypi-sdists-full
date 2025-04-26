r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to retrieve all WebAuthn credentials entries.
## Examples
### Retrieving all Webauthn credentials entries
The following output shows all WebAuthn credentials entries.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WebauthnCredentials

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(WebauthnCredentials.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    WebauthnCredentials(
        {
            "relying_party": {"name": "ontap1.example.com", "id": "ontap1.example.com"},
            "username": "user_1",
            "_links": {
                "self": {
                    "href": "/api/security/webauthn/credentials/389758ee-40cd-11ef-bb21-005056aeae31/user_1/0/ontap1.example.com"
                }
            },
            "owner": {
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/389758ee-40cd-11ef-bb21-005056aeae31"
                    }
                },
                "uuid": "389758ee-40cd-11ef-bb21-005056aeae31",
            },
            "index": 0,
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


__all__ = ["WebauthnCredentials", "WebauthnCredentialsSchema"]
__pdoc__ = {
    "WebauthnCredentialsSchema.resource": False,
    "WebauthnCredentialsSchema.opts": False,
}


class WebauthnCredentialsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebauthnCredentials object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the webauthn_credentials."""

    creation_time = ImpreciseDateTime(
        data_key="creation_time",
        allow_none=True,
    )
    r""" Date and time indicating when this entry was created.

Example: 2024-08-06T02:38:55.000+0000"""

    credential = marshmallow_fields.Nested("netapp_ontap.models.webauthn_credentials_credential.WebauthnCredentialsCredentialSchema", data_key="credential", unknown=EXCLUDE, allow_none=True)
    r""" The credential field of the webauthn_credentials."""

    display_name = marshmallow_fields.Str(
        data_key="display_name",
        allow_none=True,
    )
    r""" Display name.

Example: admin"""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Index."""

    last_used_time = ImpreciseDateTime(
        data_key="last_used_time",
        allow_none=True,
    )
    r""" Date and time indicating when this entry was last used.

Example: 2024-08-06T02:48:55.000+0000"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" WebAuthn credential owner. Used to identify a cluster or an SVM."""

    public_key = marshmallow_fields.Nested("netapp_ontap.models.webauthn_credentials_public_key.WebauthnCredentialsPublicKeySchema", data_key="public_key", unknown=EXCLUDE, allow_none=True)
    r""" The public_key field of the webauthn_credentials."""

    relying_party = marshmallow_fields.Nested("netapp_ontap.models.webauthn_credentials_relying_party.WebauthnCredentialsRelyingPartySchema", data_key="relying_party", unknown=EXCLUDE, allow_none=True)
    r""" The relying_party field of the webauthn_credentials."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" Username.

Example: admin"""

    @property
    def resource(self):
        return WebauthnCredentials

    gettable_fields = [
        "links",
        "creation_time",
        "credential",
        "display_name",
        "index",
        "last_used_time",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "public_key",
        "relying_party",
        "scope",
        "username",
    ]
    """links,creation_time,credential,display_name,index,last_used_time,owner.links,owner.name,owner.uuid,public_key,relying_party,scope,username,"""

    patchable_fields = [
        "credential",
        "public_key",
        "relying_party",
    ]
    """credential,public_key,relying_party,"""

    postable_fields = [
        "credential",
        "public_key",
        "relying_party",
    ]
    """credential,public_key,relying_party,"""

class WebauthnCredentials(Resource):
    """Allows interaction with WebauthnCredentials objects on the host"""

    _schema = WebauthnCredentialsSchema
    _path = "/api/security/webauthn/credentials"
    _keys = ["owner.uuid", "username", "index", "relying_party.id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all WebAuthn credentials entries.
### Related ONTAP commands
* `security webauthn credentials show`

### Learn more
* [`DOC /security/webauthn/credentials`](#docs-security-security_webauthn_credentials)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all WebauthnCredentials resources that match the provided query"""
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
        """Returns a list of RawResources that represent WebauthnCredentials resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["WebauthnCredentials"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a WebAuthn credentials entry.
### Required properties
    * `owner.uuid`
    * `username`
    * `index`
    * `relying_party.id`
### Related ONTAP commands
* `security webauthn credentials delete`

### Learn more
* [`DOC /security/webauthn/credentials`](#docs-security-security_webauthn_credentials)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all WebAuthn credentials entries.
### Related ONTAP commands
* `security webauthn credentials show`

### Learn more
* [`DOC /security/webauthn/credentials`](#docs-security-security_webauthn_credentials)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a WebAuthn credentials entry.
### Related ONTAP commands
* `security webauthn credentials show`

### Learn more
* [`DOC /security/webauthn/credentials`](#docs-security-security_webauthn_credentials)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)



    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a WebAuthn credentials entry.
### Required properties
    * `owner.uuid`
    * `username`
    * `index`
    * `relying_party.id`
### Related ONTAP commands
* `security webauthn credentials delete`

### Learn more
* [`DOC /security/webauthn/credentials`](#docs-security-security_webauthn_credentials)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


