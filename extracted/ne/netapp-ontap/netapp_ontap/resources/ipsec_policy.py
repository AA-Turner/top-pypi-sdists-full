r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The following operations are supported:

* Collection Get: GET security/ipsec/policies
* Creation Post: POST security/ipsec/policies
* Instance Get: GET security/ipsec/policies/uuid
* Instance Patch: PATCH security/ipsec/policies/uuid
* Instance Delete: DELETE security/ipsec/policies/uuid"""

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


__all__ = ["IpsecPolicy", "IpsecPolicySchema"]
__pdoc__ = {
    "IpsecPolicySchema.resource": False,
    "IpsecPolicySchema.opts": False,
}


class IpsecPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpsecPolicy object"""

    action = marshmallow_fields.Str(
        data_key="action",
        validate=enum_validation(['bypass', 'discard', 'esp_transport', 'esp_udp']),
        allow_none=True,
    )
    r""" Action for the IPsec policy.

Valid choices:

* bypass
* discard
* esp_transport
* esp_udp"""

    authentication_method = marshmallow_fields.Str(
        data_key="authentication_method",
        validate=enum_validation(['none', 'psk', 'pki']),
        allow_none=True,
    )
    r""" Authentication method for the IPsec policy.

Valid choices:

* none
* psk
* pki"""

    certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" The certificate field of the ipsec_policy."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether or not the policy is enabled."""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the ipsec_policy."""

    local_endpoint = marshmallow_fields.Nested("netapp_ontap.models.ipsec_endpoint.IpsecEndpointSchema", data_key="local_endpoint", unknown=EXCLUDE, allow_none=True)
    r""" Endpoint specification for the IPsec policy"""

    local_identity = marshmallow_fields.Str(
        data_key="local_identity",
        allow_none=True,
    )
    r""" Local Identity"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=64),
        allow_none=True,
    )
    r""" IPsec policy name."""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        allow_none=True,
    )
    r""" Lower layer protocol to be covered by the IPsec policy.

Example: 17"""

    remote_endpoint = marshmallow_fields.Nested("netapp_ontap.models.ipsec_endpoint.IpsecEndpointSchema", data_key="remote_endpoint", unknown=EXCLUDE, allow_none=True)
    r""" Endpoint specification for the IPsec policy"""

    remote_identity = marshmallow_fields.Str(
        data_key="remote_identity",
        allow_none=True,
    )
    r""" Remote Identity"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the ipsec_policy."""

    secret_key = marshmallow_fields.Str(
        data_key="secret_key",
        validate=len_validation(minimum=18, maximum=128),
        allow_none=True,
    )
    r""" Pre-shared key for IKE negotiation."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ipsec_policy."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the IPsec policy.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return IpsecPolicy

    gettable_fields = [
        "action",
        "authentication_method",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "enabled",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "local_endpoint",
        "local_identity",
        "name",
        "protocol",
        "remote_endpoint",
        "remote_identity",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """action,authentication_method,certificate.links,certificate.name,certificate.uuid,enabled,ipspace.links,ipspace.name,ipspace.uuid,local_endpoint,local_identity,name,protocol,remote_endpoint,remote_identity,scope,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "certificate.name",
        "certificate.uuid",
        "enabled",
        "local_endpoint",
        "local_identity",
        "protocol",
        "remote_endpoint",
        "remote_identity",
        "scope",
    ]
    """certificate.name,certificate.uuid,enabled,local_endpoint,local_identity,protocol,remote_endpoint,remote_identity,scope,"""

    postable_fields = [
        "action",
        "authentication_method",
        "certificate.name",
        "certificate.uuid",
        "enabled",
        "ipspace.name",
        "ipspace.uuid",
        "local_endpoint",
        "local_identity",
        "name",
        "protocol",
        "remote_endpoint",
        "remote_identity",
        "scope",
        "secret_key",
        "svm.name",
        "svm.uuid",
    ]
    """action,authentication_method,certificate.name,certificate.uuid,enabled,ipspace.name,ipspace.uuid,local_endpoint,local_identity,name,protocol,remote_endpoint,remote_identity,scope,secret_key,svm.name,svm.uuid,"""

class IpsecPolicy(Resource):
    r""" IPsec policy object. """

    _schema = IpsecPolicySchema
    _path = "/api/security/ipsec/policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of IPsec policies.
### Related ONTAP commands
* `security ipsec policy show`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all IpsecPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent IpsecPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["IpsecPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a specific IPsec policy.
### Related ONTAP commands
* `security ipsec policy modify`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["IpsecPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IpsecPolicy"], NetAppResponse]:
        r"""Creates an IPsec policy.
### Related ONTAP commands
* `security ipsec policy create`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["IpsecPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a specific IPsec policy.
### Related ONTAP commands
* `security ipsec policy delete`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of IPsec policies.
### Related ONTAP commands
* `security ipsec policy show`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific IPsec policy.
### Related ONTAP commands
* `security ipsec policy show`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
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
        r"""Creates an IPsec policy.
### Related ONTAP commands
* `security ipsec policy create`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
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
        r"""Updates a specific IPsec policy.
### Related ONTAP commands
* `security ipsec policy modify`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
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
        r"""Deletes a specific IPsec policy.
### Related ONTAP commands
* `security ipsec policy delete`

### Learn more
* [`DOC /security/ipsec/policies`](#docs-security-security_ipsec_policies)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


