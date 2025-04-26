r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The following APIs can be used to add/remove/retrieve the IPsec CA certificates:

* Creation Post: POST security/ipsec/ca-certificates
* Collection Get: GET security/ipsec/ca-certificates
* Instance Get: GET security/ipsec/ca-certificates/{certificate.uuid}
* Instance Delete: DELETE security/ipsec/ca-certificates/{certificate.uuid}"""

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


__all__ = ["IpsecCaCertificate", "IpsecCaCertificateSchema"]
__pdoc__ = {
    "IpsecCaCertificateSchema.resource": False,
    "IpsecCaCertificateSchema.opts": False,
}


class IpsecCaCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpsecCaCertificate object"""

    certificate = marshmallow_fields.Nested("netapp_ontap.models.ipsec_ca_certificate_uuid.IpsecCaCertificateUuidSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" IPsec CA certificate UUID"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" The scope field of the ipsec_ca_certificate."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ipsec_ca_certificate."""

    @property
    def resource(self):
        return IpsecCaCertificate

    gettable_fields = [
        "certificate",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """certificate,scope,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "scope",
    ]
    """scope,"""

    postable_fields = [
        "certificate",
        "scope",
        "svm.name",
        "svm.uuid",
    ]
    """certificate,scope,svm.name,svm.uuid,"""

class IpsecCaCertificate(Resource):
    """Allows interaction with IpsecCaCertificate objects on the host"""

    _schema = IpsecCaCertificateSchema
    _path = "/api/security/ipsec/ca-certificates"
    _keys = ["certificate.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of IPsec CA certificates configured for cluster and all SVMs.
### Related ONTAP commands
* `security ipsec ca-certificate show`

### Learn more
* [`DOC /security/ipsec/ca-certificates`](#docs-security-security_ipsec_ca-certificates)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all IpsecCaCertificate resources that match the provided query"""
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
        """Returns a list of RawResources that represent IpsecCaCertificate resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["IpsecCaCertificate"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IpsecCaCertificate"], NetAppResponse]:
        r"""Add CA certificate to IPsec. The CA certificate should already be installed on the cluster prior to adding them to IPsec.
The CA certificate can be installed on the cluster using the /security/certificates endpoint.
The svm.uuid or svm.name should not be supplied for certificates that have a scope of cluster.
### Related ONTAP commands
* `security ipsec ca-certificate add`

### Learn more
* [`DOC /security/ipsec/ca-certificates`](#docs-security-security_ipsec_ca-certificates)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["IpsecCaCertificate"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the IPsec CA certificate with the specified UUID from IPsec.
### Related ONTAP commands
* `security ipsec ca-certificate remove`

### Learn more
* [`DOC /security/ipsec/ca-certificates`](#docs-security-security_ipsec_ca-certificates)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of IPsec CA certificates configured for cluster and all SVMs.
### Related ONTAP commands
* `security ipsec ca-certificate show`

### Learn more
* [`DOC /security/ipsec/ca-certificates`](#docs-security-security_ipsec_ca-certificates)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific CA certificate configured for IPsec.
### Related ONTAP commands
* `security ipsec ca-certificate show`

### Learn more
* [`DOC /security/ipsec/ca-certificates`](#docs-security-security_ipsec_ca-certificates)"""
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
        r"""Add CA certificate to IPsec. The CA certificate should already be installed on the cluster prior to adding them to IPsec.
The CA certificate can be installed on the cluster using the /security/certificates endpoint.
The svm.uuid or svm.name should not be supplied for certificates that have a scope of cluster.
### Related ONTAP commands
* `security ipsec ca-certificate add`

### Learn more
* [`DOC /security/ipsec/ca-certificates`](#docs-security-security_ipsec_ca-certificates)"""
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
        r"""Deletes the IPsec CA certificate with the specified UUID from IPsec.
### Related ONTAP commands
* `security ipsec ca-certificate remove`

### Learn more
* [`DOC /security/ipsec/ca-certificates`](#docs-security-security_ipsec_ca-certificates)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


