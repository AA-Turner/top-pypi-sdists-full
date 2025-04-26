r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

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


__all__ = ["ExportClient", "ExportClientSchema"]
__pdoc__ = {
    "ExportClientSchema.resource": False,
    "ExportClientSchema.opts": False,
}


class ExportClientSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ExportClient object"""

    match = marshmallow_fields.Str(
        data_key="match",
        allow_none=True,
    )
    r""" Client Match Hostname, IP Address, Netgroup, or Domain.
You can specify the match as a string value in any of the
          following formats:

* As a hostname; for instance, host1
* As an IPv4 address; for instance, 10.1.12.24
* As an IPv6 address; for instance, fd20:8b1e:b255:4071::100:1
* As an IPv4 address with a subnet mask expressed as a number of bits; for instance, 10.1.12.0/24
* As an IPv6 address with a subnet mask expressed as a number of bits; for instance, fd20:8b1e:b255:4071::/64
* As an IPv4 address with a network mask; for instance, 10.1.16.0/255.255.255.0
* As a netgroup, with the netgroup name preceded by the @ character; for instance, @eng
* As a domain name preceded by the . character; for instance, .example.com


Example: 0.0.0.0/0"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.export_client_policy.ExportClientPolicySchema", data_key="policy", unknown=EXCLUDE, allow_none=True)
    r""" The policy field of the export_client."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the export_client."""

    @property
    def resource(self):
        return ExportClient

    gettable_fields = [
        "index",
        "match",
        "policy",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """index,match,policy,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "match",
        "svm.name",
        "svm.uuid",
    ]
    """match,svm.name,svm.uuid,"""

    postable_fields = [
        "match",
        "policy",
        "svm.name",
        "svm.uuid",
    ]
    """match,policy,svm.name,svm.uuid,"""

class ExportClient(Resource):
    """Allows interaction with ExportClient objects on the host"""

    _schema = ExportClientSchema
    _path = "/api/protocols/nfs/export-policies/{policy[id]}/rules/{export_rule[index]}/clients"
    _keys = ["policy.id", "export_rule.index", "match"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves export policy rule clients.
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        """Returns a count of all ExportClient resources that match the provided query"""
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
        """Returns a list of RawResources that represent ExportClient resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["ExportClient"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ExportClient"], NetAppResponse]:
        r"""Creates an export policy rule client
### Required properties
* `policy.id` - Existing export policy that contains export policy rules for the client being added.
* `index`  - Existing export policy rule for which to create an export client.
* `match`  - Base name for the export policy client.
### Related ONTAP commands
* `vserver export-policy rule add-clientmatches`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        records: Iterable["ExportClient"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an export policy client
### Related ONTAP commands
* `vserver export-policy rule remove-clientmatches`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves export policy rule clients.
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)


    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates an export policy rule client
### Required properties
* `policy.id` - Existing export policy that contains export policy rules for the client being added.
* `index`  - Existing export policy rule for which to create an export client.
* `match`  - Base name for the export policy client.
### Related ONTAP commands
* `vserver export-policy rule add-clientmatches`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
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
        r"""Deletes an export policy client
### Related ONTAP commands
* `vserver export-policy rule remove-clientmatches`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


