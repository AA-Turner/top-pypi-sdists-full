r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API configures the public keys for end-user (non-cluster admin) accounts.
Specify the owner UUID, the user account name, and the index in the URI path. The owner UUID corresponds to the UUID of the SVM containing the user account associated with the public key and can be obtained from the response body of the GET request performed on the API “/api/svm/svms".<br/> The index value corresponds to the public key that needs to be modified or deleted (it is possible to create more than one public key for the same user account).
## Examples
### Retrieving the specific configured public key for user accounts
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Publickey

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Publickey(
        index=0,
        **{
            "account.name": "pubuser4",
            "owner.uuid": "513a78c7-8c13-11e9-8f78-005056bbf6ac",
        }
    )
    resource.get()
    print(resource)

```

### Updating the public key, certificate, and comment for user accounts
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Publickey

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Publickey(
        index=0,
        **{
            "account.name": "pubuser1",
            "owner.uuid": "d49de271-8c11-11e9-8f78-005056bbf6ac",
        }
    )
    resource.comment = "Cserver-modification"
    resource.certificate = "<CERTIFICATE-CONTENT>"
    resource.public_key = "<SSH-PUBLIC-KEY>"
    resource.patch()

```

### Deleting the public key for user accounts
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Publickey

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Publickey(
        index=0,
        **{
            "account.name": "pubuser1",
            "owner.uuid": "d49de271-8c11-11e9-8f78-005056bbf6ac",
        }
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
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["Publickey", "PublickeySchema"]
__pdoc__ = {
    "PublickeySchema.resource": False,
    "PublickeySchema.opts": False,
}

class PublickeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Publickey object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the publickey."""

    account = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.account", "AccountSchema"),
                data_key="account",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The account field of the publickey."""

    certificate = marshmallow_fields.Str(
        data_key="certificate",
        allow_none=True,
    )
    r""" Optional certificate for the public key."""

    certificate_details = marshmallow_fields.Str(
        data_key="certificate_details",
        allow_none=True,
    )
    r""" The details present in the certificate (READONLY)."""

    certificate_expired = marshmallow_fields.Str(
        data_key="certificate_expired",
        allow_none=True,
    )
    r""" The expiration details of the certificate (READONLY)."""

    certificate_revoked = marshmallow_fields.Str(
        data_key="certificate_revoked",
        allow_none=True,
    )
    r""" The revocation details of the certificate (READONLY)."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        allow_none=True,
    )
    r""" Optional comment for the public key."""

    index = Size(
        data_key="index",
        validate=integer_validation(minimum=0, maximum=99),
        allow_none=True,
    )
    r""" Index number for the public key (where there are multiple keys for the same account)."""

    obfuscated_fingerprint = marshmallow_fields.Str(
        data_key="obfuscated_fingerprint",
        allow_none=True,
    )
    r""" The obfuscated fingerprint for the public key (READONLY)."""

    owner = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                data_key="owner",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The owner field of the publickey."""

    public_key = marshmallow_fields.Str(
        data_key="public_key",
        allow_none=True,
    )
    r""" The public key"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    sha_fingerprint = marshmallow_fields.Str(
        data_key="sha_fingerprint",
        allow_none=True,
    )
    r""" The SHA fingerprint for the public key (READONLY)."""

    @property
    def resource(self):
        return Publickey

    gettable_fields = [
        "links",
        "account.links",
        "account.name",
        "certificate",
        "certificate_details",
        "certificate_expired",
        "certificate_revoked",
        "comment",
        "index",
        "obfuscated_fingerprint",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "public_key",
        "scope",
        "sha_fingerprint",
    ]
    """links,account.links,account.name,certificate,certificate_details,certificate_expired,certificate_revoked,comment,index,obfuscated_fingerprint,owner.links,owner.name,owner.uuid,public_key,scope,sha_fingerprint,"""

    patchable_fields = [
        "account.name",
        "certificate",
        "comment",
        "public_key",
    ]
    """account.name,certificate,comment,public_key,"""

    postable_fields = [
        "account.name",
        "certificate",
        "comment",
        "index",
        "owner.name",
        "owner.uuid",
        "public_key",
    ]
    """account.name,certificate,comment,index,owner.name,owner.uuid,public_key,"""

class Publickey(Resource):
    r""" The public key for the user account (to access SSH). """

    _schema = PublickeySchema
    _path = "/api/security/authentication/publickeys"
    _keys = ["owner.uuid", "account.name", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the public keys configured for user accounts.
### Related ONTAP commands
* `security login publickey show`
### Learn more
* [`DOC /security/authentication/publickeys`](#docs-security-security_authentication_publickeys)
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
        """Returns a count of all Publickey resources that match the provided query"""
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
        """Returns a list of RawResources that represent Publickey resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Publickey"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the public key and/or certificate for a user account.
### Related ONTAP commands
* `security login publickey modify`
### Learn more
* [`DOC /security/authentication/publickeys/{owner.uuid}/{account.name}/{index}`](#docs-security-security_authentication_publickeys_{owner.uuid}_{account.name}_{index})
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
        records: Iterable["Publickey"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Publickey"], NetAppResponse]:
        r"""Creates a public key along with an optional certificate for a user account.
### Required properties
* `owner.uuid` - UUID of the account owner.
* `name` - User account name.
* `index` - Index number for the public key (where there are multiple keys for the same account).
* `public_key` - The publickey details for the creation of the user account.
### Optional properties
* `comment` - Comment text for the public key.
* `certificate` - The certificate in PEM format.
### Related ONTAP commands
* `security login publickey create`
### Learn more
* [`DOC /security/authentication/publickeys`](#docs-security-security_authentication_publickeys)
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
        records: Iterable["Publickey"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the public key for a user account.
### Related ONTAP commands
* `security login publickey delete`
### Learn more
* [`DOC /security/authentication/publickeys/{owner.uuid}/{account.name}/{index}`](#docs-security-security_authentication_publickeys_{owner.uuid}_{account.name}_{index})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the public keys configured for user accounts.
### Related ONTAP commands
* `security login publickey show`
### Learn more
* [`DOC /security/authentication/publickeys`](#docs-security-security_authentication_publickeys)
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the public keys configured for a user account.
### Related ONTAP commands
* `security login publickey show`
### Learn more
* [`DOC /security/authentication/publickeys/{owner.uuid}/{account.name}/{index}`](#docs-security-security_authentication_publickeys_{owner.uuid}_{account.name}_{index})
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
        r"""Creates a public key along with an optional certificate for a user account.
### Required properties
* `owner.uuid` - UUID of the account owner.
* `name` - User account name.
* `index` - Index number for the public key (where there are multiple keys for the same account).
* `public_key` - The publickey details for the creation of the user account.
### Optional properties
* `comment` - Comment text for the public key.
* `certificate` - The certificate in PEM format.
### Related ONTAP commands
* `security login publickey create`
### Learn more
* [`DOC /security/authentication/publickeys`](#docs-security-security_authentication_publickeys)
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
        r"""Updates the public key and/or certificate for a user account.
### Related ONTAP commands
* `security login publickey modify`
### Learn more
* [`DOC /security/authentication/publickeys/{owner.uuid}/{account.name}/{index}`](#docs-security-security_authentication_publickeys_{owner.uuid}_{account.name}_{index})
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
        r"""Deletes the public key for a user account.
### Related ONTAP commands
* `security login publickey delete`
### Learn more
* [`DOC /security/authentication/publickeys/{owner.uuid}/{account.name}/{index}`](#docs-security-security_authentication_publickeys_{owner.uuid}_{account.name}_{index})
* [`DOC /security/accounts`](#docs-security-security_accounts)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


