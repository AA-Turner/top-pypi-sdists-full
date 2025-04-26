r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can configure NTP to use shared private keys between ONTAP and trusted external NTP time servers.</br>
You acquire the keys from the external NTP time servers and individual entries created for each
unique key. You can use the /cluster/ntp/servers API to associate a key with an external NTP time server
used by ONTAP and enable authentication.
### Fields used for adding an NTP shared key
The required fields are:

* `id`
* `digest_type`
* `secret_key`
## Example
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NtpKey

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NtpKey()
    resource.id = 10
    resource.digest_type = "sha1"
    resource.value = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    resource.post(hydrate=True)
    print(resource)

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


__all__ = ["NtpKey", "NtpKeySchema"]
__pdoc__ = {
    "NtpKeySchema.resource": False,
    "NtpKeySchema.opts": False,
}


class NtpKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NtpKey object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ntp_key."""

    digest_type = marshmallow_fields.Str(
        data_key="digest_type",
        validate=enum_validation(['sha1']),
        allow_none=True,
    )
    r""" The type of cryptographic hash used to create and verify the NTP's message authentication code appended to each NTP packet header.


Valid choices:

* sha1"""

    id = Size(
        data_key="id",
        validate=integer_validation(minimum=1, maximum=65535),
        allow_none=True,
    )
    r""" NTP symmetric authentication key identifier or index number (ID). This ID is included
in the NTP cryptographic hash encoded header.


Example: 10"""

    value = marshmallow_fields.Str(
        data_key="value",
        allow_none=True,
    )
    r""" A hexadecimal digit string that represents the cryptographic key that is shared with the remote NTP server.
The current expected length is 40 characters.
</br>
Use the cryptographic key and key ID to create a unique hash value used to authenticate the rest of the NTP data.


Example: da39a3ee5e6b4b0d3255bfef95601890afd80709"""

    @property
    def resource(self):
        return NtpKey

    gettable_fields = [
        "links",
        "digest_type",
        "id",
        "value",
    ]
    """links,digest_type,id,value,"""

    patchable_fields = [
        "digest_type",
        "value",
    ]
    """digest_type,value,"""

    postable_fields = [
        "digest_type",
        "id",
        "value",
    ]
    """digest_type,id,value,"""

class NtpKey(Resource):
    """Allows interaction with NtpKey objects on the host"""

    _schema = NtpKeySchema
    _path = "/api/cluster/ntp/keys"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of NTP symmetric authentication keys known by ONTAP that
are uniquely indexed by an identifier.
### Related ONTAP commands
* `cluster time-service ntp key show`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
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
        """Returns a count of all NtpKey resources that match the provided query"""
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
        """Returns a list of RawResources that represent NtpKey resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NtpKey"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the details of a specific NTP symmetric authentication key by numeric
identifier or index (ID).
### Required properties
* `digest_type` - Shared private key cryptographic hash type.
* `value` - Value of shared private key.
### Related ONTAP commands
* `cluster time-service ntp key modify`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["NtpKey"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NtpKey"], NetAppResponse]:
        r"""Creates an NTP symmetric authentication key entry including the type of key
using an unused identifier or index number (ID).
### Required properties
* `id` - Shared symmetric key number (ID).
* `digest_type` - Shared private key cryptographic hash type.
* `value` - Value of shared private key.
### Related ONTAP commands
* `cluster time-service ntp key create`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
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
        records: Iterable["NtpKey"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an NTP key.
### Related ONTAP commands
* `cluster time-service ntp key delete`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of NTP symmetric authentication keys known by ONTAP that
are uniquely indexed by an identifier.
### Related ONTAP commands
* `cluster time-service ntp key show`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a specific NTP symmetric authentication key by numeric identifier or index (ID).
### Related ONTAP commands
* `cluster time-service ntp key show`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
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
        r"""Creates an NTP symmetric authentication key entry including the type of key
using an unused identifier or index number (ID).
### Required properties
* `id` - Shared symmetric key number (ID).
* `digest_type` - Shared private key cryptographic hash type.
* `value` - Value of shared private key.
### Related ONTAP commands
* `cluster time-service ntp key create`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
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
        r"""Updates the details of a specific NTP symmetric authentication key by numeric
identifier or index (ID).
### Required properties
* `digest_type` - Shared private key cryptographic hash type.
* `value` - Value of shared private key.
### Related ONTAP commands
* `cluster time-service ntp key modify`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
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
        r"""Deletes an NTP key.
### Related ONTAP commands
* `cluster time-service ntp key delete`
### Learn more
* [`DOC /cluster/ntp/keys`](#docs-cluster-cluster_ntp_keys)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


