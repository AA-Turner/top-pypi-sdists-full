r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API endpoint retrieves WebAuthn global settings for the cluster or SVM.
Specify the owner UUID and the unique identifier for the cluster or SVM to retrieve the WebAuthn global settings for the cluster or SVM.
## Examples
### Retrieving the WebAuthn global settings for the cluster or SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WebauthnGlobal

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = WebauthnGlobal(**{"owner.uuid": "d49de271-8c11-11e9-8f78-005056bbf6ac"})
    resource.get()
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


__all__ = ["WebauthnGlobal", "WebauthnGlobalSchema"]
__pdoc__ = {
    "WebauthnGlobalSchema.resource": False,
    "WebauthnGlobalSchema.opts": False,
}


class WebauthnGlobalSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebauthnGlobal object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the webauthn_global."""

    attestation = marshmallow_fields.Str(
        data_key="attestation",
        validate=enum_validation(['none', 'indirect', 'direct', 'enterprise']),
        allow_none=True,
    )
    r""" Attestation conveyance type.

Valid choices:

* none
* indirect
* direct
* enterprise"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" WebAuthn settings owner. Used to identify a cluster or an SVM."""

    require_rk = marshmallow_fields.Boolean(
        data_key="require_rk",
        allow_none=True,
    )
    r""" Specifies whether the resident key is required.

Example: false"""

    resident_key = marshmallow_fields.Str(
        data_key="resident_key",
        validate=enum_validation(['required', 'preferred', 'discouraged']),
        allow_none=True,
    )
    r""" Resident key.

Valid choices:

* required
* preferred
* discouraged"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    timeout = Size(
        data_key="timeout",
        allow_none=True,
    )
    r""" The timeout interval for the WebAuthn request, in milliseconds.

Example: 600000"""

    user_verification = marshmallow_fields.Str(
        data_key="user_verification",
        validate=enum_validation(['required', 'preferred', 'discouraged']),
        allow_none=True,
    )
    r""" User verification.

Valid choices:

* required
* preferred
* discouraged"""

    @property
    def resource(self):
        return WebauthnGlobal

    gettable_fields = [
        "links",
        "attestation",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "require_rk",
        "resident_key",
        "scope",
        "timeout",
        "user_verification",
    ]
    """links,attestation,owner.links,owner.name,owner.uuid,require_rk,resident_key,scope,timeout,user_verification,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class WebauthnGlobal(Resource):
    r""" WebAuthn global settings. """

    _schema = WebauthnGlobalSchema
    _path = "/api/security/webauthn/global-settings"
    _keys = ["owner.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieve WebAuthn global settings for a cluster and all SVMs.
### Related ONTAP commands
* `security webauthn show`

### Learn more
* [`DOC /security/webauthn/global-settings`](#docs-security-security_webauthn_global-settings)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all WebauthnGlobal resources that match the provided query"""
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
        """Returns a list of RawResources that represent WebauthnGlobal resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieve WebAuthn global settings for a cluster and all SVMs.
### Related ONTAP commands
* `security webauthn show`

### Learn more
* [`DOC /security/webauthn/global-settings`](#docs-security-security_webauthn_global-settings)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a WebAuthn global setting entry.
### Related ONTAP commands
* `security webauthn show`

### Learn more
* [`DOC /security/webauthn/global-settings/{owner.uuid}`](#docs-security-security_webauthn_global-settings_{owner.uuid})"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





