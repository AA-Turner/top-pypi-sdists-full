r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API endpoint retrieves a specific WebAuthn supported algorithms entry.
Specify the owner UUID, the unique identifier for the cluster or SVM, and the algorithm name to retrieve the specific WebAuthn supported algorithms entry.
## Examples
### Retrieving the specific WebAuthn supported algorithms entry
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SupportedAlgorithms

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SupportedAlgorithms(
        **{
            "algorithm.name": "ES-256",
            "owner.uuid": "d49de271-8c11-11e9-8f78-005056bbf6ac",
        }
    )
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


__all__ = ["SupportedAlgorithms", "SupportedAlgorithmsSchema"]
__pdoc__ = {
    "SupportedAlgorithmsSchema.resource": False,
    "SupportedAlgorithmsSchema.opts": False,
}


class SupportedAlgorithmsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SupportedAlgorithms object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the supported_algorithms."""

    algorithm = marshmallow_fields.Nested("netapp_ontap.models.supported_algorithms_algorithm.SupportedAlgorithmsAlgorithmSchema", data_key="algorithm", unknown=EXCLUDE, allow_none=True)
    r""" The algorithm field of the supported_algorithms."""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" Used to identify a cluster or an SVM."""

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
        return SupportedAlgorithms

    gettable_fields = [
        "links",
        "algorithm",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "scope",
    ]
    """links,algorithm,owner.links,owner.name,owner.uuid,scope,"""

    patchable_fields = [
        "algorithm",
    ]
    """algorithm,"""

    postable_fields = [
        "algorithm",
    ]
    """algorithm,"""

class SupportedAlgorithms(Resource):
    r""" WebAuthn supported algorithms. """

    _schema = SupportedAlgorithmsSchema
    _path = "/api/security/webauthn/supported-algorithms"
    _keys = ["owner.uuid", "algorithm.name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieve all WebAuthn supported algorithms entries.
### Related ONTAP commands
* `security webauthn supported-algorithms show`

### Learn more
* [`DOC /security/webauthn/supported-algorithms`](#docs-security-security_webauthn_supported-algorithms)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SupportedAlgorithms resources that match the provided query"""
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
        """Returns a list of RawResources that represent SupportedAlgorithms resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieve all WebAuthn supported algorithms entries.
### Related ONTAP commands
* `security webauthn supported-algorithms show`

### Learn more
* [`DOC /security/webauthn/supported-algorithms`](#docs-security-security_webauthn_supported-algorithms)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a WebAuthn supported algorithms entry.
### Related ONTAP commands
* `security webauthn supported-algorithms show`

### Learn more
* [`DOC /security/webauthn/supported-algorithms/{owner.uuid}/{algorithm.name}`](#docs-security-security_webauthn_supported-algorithms_{owner.uuid}_{algorithm.name})"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





