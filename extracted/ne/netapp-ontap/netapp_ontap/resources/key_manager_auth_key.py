r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Used to create and list authentication keys (NSE-AK).
## Example
### Creates an authentication key. Note: an external key  manager must be configured on the admin SVM, as the authentication key will be associated with the admin SVM.
The following example shows how to create an authentication key.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerAuthKey

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyManagerAuthKey("5fb1701a-d922-11e8-bfe8-005056bb017d")
    resource.post(hydrate=True, return_timeout=15)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
KeyManagerAuthKey(
    {
        "key_tag": "vsim1",
        "key_id": "00000000000000000200000000000100531d8cdc38437c2627b6b1726dd2675c0000000000000000",
    }
)

```
</div>
</div>

---
### Retrieving a list of all of the authentication keys associated with the admin SVM.
The following example shows how to retrieve a list of all of the authentication keys associated with the admin SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerAuthKey

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            KeyManagerAuthKey.get_collection(
                "5fb1701a-d922-11e8-bfe8-005056bb017d", fields="*"
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    KeyManagerAuthKey(
        {
            "key_tag": "vsim1",
            "key_id": "00000000000000000200000000000100052ab79fc51a430dbb16f1c0d2054cfe0000000000000000",
            "security_key_manager": {"uuid": "d36a654d-14b4-11ed-b82e-005056bb8f59"},
        }
    ),
    KeyManagerAuthKey(
        {
            "key_tag": "vsim1",
            "key_id": "000000000000000002000000000001003f32ce2dc55d2764c07da74e722c179b0000000000000000",
            "security_key_manager": {"uuid": "d36a654d-14b4-11ed-b82e-005056bb8f59"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific authentication key associated with the admin SVM.
The following example shows how to a specific authentication key associated with the admin SVM and return the key-tag.
```
# The API:
GET /api/security/key-managers/{security_key_manager.uuid}/auth-keys/{key-id}
# The call:
curl -X GET 'https://<mgmt-ip>/api/security/key-managers/5fb1701a-d922-11e8-bfe8-005056bb017d/auth-keys/0000000000000000020000000000010041a2dda969b0d179db8f1c78d629d0f10000000000000000?fields=key_tag' -H 'accept: application/hal+json'
# The response:
{
  "security_key_manager": {
    "uuid": "d36a654d-14b4-11ed-b82e-005056bb8f59"
  },
  "key_id": "0000000000000000020000000000010041a2dda969b0d179db8f1c78d629d0f10000000000000000",
  "key_tag": "vsim1"
}"""

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


__all__ = ["KeyManagerAuthKey", "KeyManagerAuthKeySchema"]
__pdoc__ = {
    "KeyManagerAuthKeySchema.resource": False,
    "KeyManagerAuthKeySchema.opts": False,
}


class KeyManagerAuthKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyManagerAuthKey object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the key_manager_auth_key."""

    key_id = marshmallow_fields.Str(
        data_key="key_id",
        allow_none=True,
    )
    r""" Key identifier.

Example: 000000000000000002000000000001003aa8ce6a4fea3e466620134bea9510a10000000000000000"""

    key_tag = marshmallow_fields.Str(
        data_key="key_tag",
        allow_none=True,
    )
    r""" Optional parameter to define key-tag for the authentication key, length 0-32 characters.

Example: Authentication-Key-01"""

    passphrase = marshmallow_fields.Str(
        data_key="passphrase",
        allow_none=True,
    )
    r""" Authentication passphrase, length 20-32 characters. May contain the '=' character.

Example: AuthenticationKey_01"""

    security_key_manager = marshmallow_fields.Nested("netapp_ontap.resources.security_key_manager.SecurityKeyManagerSchema", data_key="security_key_manager", unknown=EXCLUDE, allow_none=True)
    r""" The security_key_manager field of the key_manager_auth_key."""

    @property
    def resource(self):
        return KeyManagerAuthKey

    gettable_fields = [
        "links",
        "key_id",
        "key_tag",
        "security_key_manager.links",
        "security_key_manager.uuid",
    ]
    """links,key_id,key_tag,security_key_manager.links,security_key_manager.uuid,"""

    patchable_fields = [
        "key_tag",
        "security_key_manager.uuid",
    ]
    """key_tag,security_key_manager.uuid,"""

    postable_fields = [
        "key_tag",
        "passphrase",
        "security_key_manager.uuid",
    ]
    """key_tag,passphrase,security_key_manager.uuid,"""

class KeyManagerAuthKey(Resource):
    """Allows interaction with KeyManagerAuthKey objects on the host"""

    _schema = KeyManagerAuthKeySchema
    _path = "/api/security/key-managers/{security_key_manager[uuid]}/auth-keys"
    _keys = ["security_key_manager.uuid", "key_id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of all authentication keys associated with the admin SVM.
### Related ONTAP commands
* `security key-manager key query`
### Required properties
* `security_key_manager.uuid` - UUID of the external key manager.

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/auth-keys`](#docs-security-security_key-managers_{security_key_manager.uuid}_auth-keys)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all KeyManagerAuthKey resources that match the provided query"""
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
        """Returns a list of RawResources that represent KeyManagerAuthKey resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["KeyManagerAuthKey"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["KeyManagerAuthKey"], NetAppResponse]:
        r"""Creates an authentication key.
### Related ONTAP commands
* `security key-manager key create`
### Required properties
* `security_key_manager.uuid` - UUID of the external key manager.

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/auth-keys`](#docs-security-security_key-managers_{security_key_manager.uuid}_auth-keys)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["KeyManagerAuthKey"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an authentication key.
### Related ONTAP commands
* `security key-manager key delete`
### Required properties
* `security_key_manager.uuid` - UUID of the external key manager.
* `key_id` - Key ID of the authentication key to be deleted.

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/auth-keys`](#docs-security-security_key-managers_{security_key_manager.uuid}_auth-keys)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of all authentication keys associated with the admin SVM.
### Related ONTAP commands
* `security key-manager key query`
### Required properties
* `security_key_manager.uuid` - UUID of the external key manager.

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/auth-keys`](#docs-security-security_key-managers_{security_key_manager.uuid}_auth-keys)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the authentication key identified by the 'key_id' and associated with the admin SVM.
### Related ONTAP commands
* `security key-manager key query`
### Required properties
* `security_key_manager.uuid` - UUID of the external key manager.
* `key_id` - Key ID of the authentication key to be retrieved.

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/auth-keys`](#docs-security-security_key-managers_{security_key_manager.uuid}_auth-keys)"""
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
        r"""Creates an authentication key.
### Related ONTAP commands
* `security key-manager key create`
### Required properties
* `security_key_manager.uuid` - UUID of the external key manager.

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/auth-keys`](#docs-security-security_key-managers_{security_key_manager.uuid}_auth-keys)"""
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
        r"""Deletes an authentication key.
### Related ONTAP commands
* `security key-manager key delete`
### Required properties
* `security_key_manager.uuid` - UUID of the external key manager.
* `key_id` - Key ID of the authentication key to be deleted.

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/auth-keys`](#docs-security-security_key-managers_{security_key_manager.uuid}_auth-keys)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


