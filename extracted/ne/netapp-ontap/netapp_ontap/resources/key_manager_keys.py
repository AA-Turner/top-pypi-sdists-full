r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Retrieves the key manager keys on the give node. The following operations are supported:

* Get
## Examples
### Retrieving key manager key-id information for a node
The following example shows how to retrieve key-ids present on a node for a key manager.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerKeys

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyManagerKeys(
        "f4f98a48-8a5c-c548-cd03-c6335f5803a8",
        "00000000-0000-0000-0000-000000000000",
        key_id="000000000000000002000000000005009ad4da8fea2cafe2bed803078b780ebe0000000000000c01",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
KeyManagerKeys(
    {
        "encryption_algorithm": "XTS-AES-256",
        "key_user": "datavs",
        "key_type": "vek",
        "svm": {"name": "cluster-1"},
        "node": {"uuid": "00000000-0000-0000-0000-000000000000"},
        "key_manager": "onboard",
        "key_store": "onboard",
        "_links": {
            "self": {
                "href": "/api/security/key-managers/f4f98a48-8a5c-c548-cd03-c6335f5803a8/keys/00000000-0000-0000-0000-000000000000/key-ids/000000000000000002000000000005009ad4da8fea2cafe2bed803078b780ebe0000000000000c01"
            }
        },
        "restored": False,
        "key_store_type": "okm",
        "key_tag": "vsim1",
        "key_id": "000000000000000002000000000005009ad4da8fea2cafe2bed803078b780ebe0000000000000c01",
        "security_key_manager": {"uuid": "f4f98a48-8a5c-c548-cd03-c6335f5803a8"},
    }
)

```
</div>
</div>

---
### Retrieving key manager key-id information of a specific key-type for a node
The following example shows how to retrieve key-ids of a specific key-type present on a node for a key manager.
```
# The API:
GET /api/security/key-manager/{security_key_manager.uuid}/keys/{node.uuid}/key-ids
# The call:
curl -X GET "https://<mgmt-ip>/api/security/key-managers/7c179931-044b-11ed-b7cd-005056bbc535/keys/44dac31e-0449-11ed-b7cd-005056bbc535/key-ids?key_type=nse_ak&return_records=true&return_timeout=15" -H "accept: application/json"
# The response:
  {
    "records": [
      {
        "key_server": "10.225.89.34:5696",
        "key_id": "000000000000000002000000000001003d5c5f8c497e8e36aa80566e08749a3d0000000000000000",
        "key_type": "nse_ak"
      },
      {
        "key_server": "10.225.89.34:5696",
        "key_id": "00000000000000000200000000000100c2dce9a3a15aeb8480db8d49c17d056c0000000000000000",
        "key_type": "nse_ak"
      }
    ],
    "num_records": 2
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


__all__ = ["KeyManagerKeys", "KeyManagerKeysSchema"]
__pdoc__ = {
    "KeyManagerKeysSchema.resource": False,
    "KeyManagerKeysSchema.opts": False,
}


class KeyManagerKeysSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyManagerKeys object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the key_manager_keys."""

    crn = marshmallow_fields.Str(
        data_key="crn",
        allow_none=True,
    )
    r""" Cloud resource name.

Example: CRN=v1:bluemix:public:containers-kubernetes"""

    encryption_algorithm = marshmallow_fields.Str(
        data_key="encryption_algorithm",
        allow_none=True,
    )
    r""" Encryption algorithm for the key

Example: XTS-AES-256"""

    key_id = marshmallow_fields.Str(
        data_key="key_id",
        allow_none=True,
    )
    r""" Key identifier.

Example: 000000000000000002000000000001008963c9213194c59555c1bec8db3603c800000000"""

    key_manager = marshmallow_fields.Str(
        data_key="key_manager",
        allow_none=True,
    )
    r""" Key manager key server managing the key. Indicates the external key server when external key manager is configured.

Example: keyserver1.local:5696"""

    key_server = marshmallow_fields.Str(
        data_key="key_server",
        allow_none=True,
    )
    r""" External key server for key management.

Example: keyserver1.com:5698"""

    key_store = marshmallow_fields.Str(
        data_key="key_store",
        validate=enum_validation(['onboard', 'external']),
        allow_none=True,
    )
    r""" Security key manager configured for the given key manager UUID. Key manager keystore value can be onboard or external.

Valid choices:

* onboard
* external"""

    key_store_type = marshmallow_fields.Str(
        data_key="key_store_type",
        validate=enum_validation(['okm', 'kmip', 'akv', 'unset', 'gcp', 'aws', 'ikp']),
        allow_none=True,
    )
    r""" Security key manager keystore type. Keystore type can be onboard, external, or supported cloud key manager.

Valid choices:

* okm
* kmip
* akv
* unset
* gcp
* aws
* ikp"""

    key_tag = marshmallow_fields.Str(
        data_key="key_tag",
        allow_none=True,
    )
    r""" Additional information associated with the key.

Example: key#"""

    key_type = marshmallow_fields.Str(
        data_key="key_type",
        validate=enum_validation(['nse_ak', 'aek', 'vek', 'nek', 'svm_kek', 'mroot_ak']),
        allow_none=True,
    )
    r""" Encryption Key type.

Valid choices:

* nse_ak
* aek
* vek
* nek
* svm_kek
* mroot_ak"""

    key_user = marshmallow_fields.Str(
        data_key="key_user",
        allow_none=True,
    )
    r""" SVM associated with the key.

Example: vs1"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the key_manager_keys."""

    policy = marshmallow_fields.Str(
        data_key="policy",
        allow_none=True,
    )
    r""" Key store policy.

Example: IBM_Key_Lore"""

    restored = marshmallow_fields.Boolean(
        data_key="restored",
        allow_none=True,
    )
    r""" Indicates whether the key is present locally on the node.

Example: true"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the key_manager_keys."""

    security_key_manager = marshmallow_fields.Nested("netapp_ontap.resources.security_key_manager.SecurityKeyManagerSchema", data_key="security_key_manager", unknown=EXCLUDE, allow_none=True)
    r""" The security_key_manager field of the key_manager_keys."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the key_manager_keys."""

    @property
    def resource(self):
        return KeyManagerKeys

    gettable_fields = [
        "links",
        "crn",
        "encryption_algorithm",
        "key_id",
        "key_manager",
        "key_server",
        "key_store",
        "key_store_type",
        "key_tag",
        "key_type",
        "key_user",
        "node.links",
        "node.name",
        "node.uuid",
        "policy",
        "restored",
        "scope",
        "security_key_manager.links",
        "security_key_manager.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,crn,encryption_algorithm,key_id,key_manager,key_server,key_store,key_store_type,key_tag,key_type,key_user,node.links,node.name,node.uuid,policy,restored,scope,security_key_manager.links,security_key_manager.uuid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class KeyManagerKeys(Resource):
    r""" Displays the keys stored in a key manager. """

    _schema = KeyManagerKeysSchema
    _path = "/api/security/key-managers/{security_key_manager[uuid]}/keys/{node[uuid]}/key-ids"
    _keys = ["security_key_manager.uuid", "node.uuid", "key_id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves key manager configurations.
### Required properties
* `security_key_manager.uuid` - Key manager UUID.
* `node.uuid` - Node UUID.
### Related ONTAP commands
* `security key-manager key query`
* `security key-manager key query -node <node>`
* `security key-manager key query -node <node> -key-manager <key_manager>`

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/keys/{node.uuid}/key-ids`](#docs-security-security_key-managers_{security_key_manager.uuid}_keys_{node.uuid}_key-ids)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all KeyManagerKeys resources that match the provided query"""
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
        """Returns a list of RawResources that represent KeyManagerKeys resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves key manager configurations.
### Required properties
* `security_key_manager.uuid` - Key manager UUID.
* `node.uuid` - Node UUID.
### Related ONTAP commands
* `security key-manager key query`
* `security key-manager key query -node <node>`
* `security key-manager key query -node <node> -key-manager <key_manager>`

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/keys/{node.uuid}/key-ids`](#docs-security-security_key-managers_{security_key_manager.uuid}_keys_{node.uuid}_key-ids)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the key management keys information for the specified key_id.
### Related ONTAP commands
* `security key-manager key query -key-id <key_id>`
* `security key-manager key query -key-id <key_id> -node <node>`
* `security key-manager key query -key-id <key_id> -node <node> -key-manager <key_manager>`

### Learn more
* [`DOC /security/key-managers/{security_key_manager.uuid}/keys/{node.uuid}/key-ids`](#docs-security-security_key-managers_{security_key_manager.uuid}_keys_{node.uuid}_key-ids)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





