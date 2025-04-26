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


__all__ = ["FcZone", "FcZoneSchema"]
__pdoc__ = {
    "FcZoneSchema.resource": False,
    "FcZoneSchema.opts": False,
}


class FcZoneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcZone object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the fc_zone."""

    cache = marshmallow_fields.Nested("netapp_ontap.models.fabric_cache.FabricCacheSchema", data_key="cache", unknown=EXCLUDE, allow_none=True)
    r""" Properties of Fibre Chanel fabric cache."""

    fabric = marshmallow_fields.Nested("netapp_ontap.resources.fabric.FabricSchema", data_key="fabric", unknown=EXCLUDE, allow_none=True)
    r""" The fabric field of the fc_zone."""

    members = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.fc_zone_member.FcZoneMemberSchema", unknown=EXCLUDE, allow_none=True), data_key="members", allow_none=True)
    r""" An array of Fibre Channel zone members."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the Fibre Channel zone.


Example: zone1"""

    @property
    def resource(self):
        return FcZone

    gettable_fields = [
        "links",
        "cache",
        "fabric.links",
        "fabric.name",
        "members",
        "name",
    ]
    """links,cache,fabric.links,fabric.name,members,name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class FcZone(Resource):
    r""" A Fibre Channel zone. """

    _schema = FcZoneSchema
    _path = "/api/network/fc/fabrics/{fabric[name]}/zones"
    _keys = ["fabric.name", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the zones of the active zoneset of a Fibre Channel fabric.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `members`
### Related ONTAP commands
* `network fcp zone show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
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
        """Returns a count of all FcZone resources that match the provided query"""
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
        """Returns a list of RawResources that represent FcZone resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the zones of the active zoneset of a Fibre Channel fabric.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `members`
### Related ONTAP commands
* `network fcp zone show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a zone of the active zoneset of a Fibre Channel fabric.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `members`
### Related ONTAP commands
* `network fcp zone show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





