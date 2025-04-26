r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview

* Collection Get: GET security/ipsec/security-associations
* Instance Get: GET security/ipsec/security-associations/uuid"""

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


__all__ = ["SecurityAssociation", "SecurityAssociationSchema"]
__pdoc__ = {
    "SecurityAssociationSchema.resource": False,
    "SecurityAssociationSchema.opts": False,
}


class SecurityAssociationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityAssociation object"""

    cipher_suite = marshmallow_fields.Str(
        data_key="cipher_suite",
        validate=enum_validation(['suite_aescbc', 'suiteb_gcm256', 'suiteb_gmac256']),
        allow_none=True,
    )
    r""" Cipher suite for the security association.

Valid choices:

* suite_aescbc
* suiteb_gcm256
* suiteb_gmac256"""

    ike = marshmallow_fields.Nested("netapp_ontap.models.security_association_ike.SecurityAssociationIkeSchema", data_key="ike", unknown=EXCLUDE, allow_none=True)
    r""" Objects containing parameters specific to IKE (Internet Key Exchange) security association."""

    ipsec = marshmallow_fields.Nested("netapp_ontap.models.security_association_ipsec.SecurityAssociationIpsecSchema", data_key="ipsec", unknown=EXCLUDE, allow_none=True)
    r""" Objects containing parameters specific to IPsec security association."""

    lifetime = Size(
        data_key="lifetime",
        allow_none=True,
    )
    r""" Lifetime for the security association in seconds."""

    local_address = marshmallow_fields.Str(
        data_key="local_address",
        allow_none=True,
    )
    r""" Local address of the security association."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the security_association."""

    policy_name = marshmallow_fields.Str(
        data_key="policy_name",
        allow_none=True,
    )
    r""" Policy name for the security association."""

    remote_address = marshmallow_fields.Str(
        data_key="remote_address",
        allow_none=True,
    )
    r""" Remote address of the security association."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the security_association."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the security_association."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['ipsec', 'ike']),
        allow_none=True,
    )
    r""" Type of security association, it can be IPsec or IKE (Internet Key Exchange).

Valid choices:

* ipsec
* ike"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the security association."""

    @property
    def resource(self):
        return SecurityAssociation

    gettable_fields = [
        "cipher_suite",
        "ike",
        "ipsec",
        "lifetime",
        "local_address",
        "node.links",
        "node.name",
        "node.uuid",
        "policy_name",
        "remote_address",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
    ]
    """cipher_suite,ike,ipsec,lifetime,local_address,node.links,node.name,node.uuid,policy_name,remote_address,scope,svm.links,svm.name,svm.uuid,type,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class SecurityAssociation(Resource):
    r""" Security association object for IPsec security association and IKE (Internet Key Exchange) security association. """

    _schema = SecurityAssociationSchema
    _path = "/api/security/ipsec/security-associations"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the IPsec and IKE (Internet Key Exchange) security associations.
### Related ONTAP commands
* `security ipsec show-ipsecsa`
* `security ipsec show-ikesa`

### Learn more
* [`DOC /security/ipsec/security-associations`](#docs-security-security_ipsec_security-associations)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityAssociation resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityAssociation resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the IPsec and IKE (Internet Key Exchange) security associations.
### Related ONTAP commands
* `security ipsec show-ipsecsa`
* `security ipsec show-ikesa`

### Learn more
* [`DOC /security/ipsec/security-associations`](#docs-security-security_ipsec_security-associations)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific IPsec or IKE (Internet Key Exchange) security association.
### Related ONTAP commands
* `security ipsec show-ipsecsa`
* `security ipsec show-ikesa`

### Learn more
* [`DOC /security/ipsec/security-associations`](#docs-security-security_ipsec_security-associations)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





