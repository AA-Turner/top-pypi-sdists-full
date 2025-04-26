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


__all__ = ["FcSwitch", "FcSwitchSchema"]
__pdoc__ = {
    "FcSwitchSchema.resource": False,
    "FcSwitchSchema.opts": False,
}


class FcSwitchSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcSwitch object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the fc_switch."""

    cache = marshmallow_fields.Nested("netapp_ontap.models.fabric_cache.FabricCacheSchema", data_key="cache", unknown=EXCLUDE, allow_none=True)
    r""" Properties of Fibre Chanel fabric cache."""

    domain_id = Size(
        data_key="domain_id",
        validate=integer_validation(minimum=1, maximum=239),
        allow_none=True,
    )
    r""" The domain identifier (ID) of the Fibre Channel (FC) switch. The domain ID is a unique identifier for the FC switch in the FC fabric.


Example: 1"""

    fabric = marshmallow_fields.Nested("netapp_ontap.resources.fabric.FabricSchema", data_key="fabric", unknown=EXCLUDE, allow_none=True)
    r""" The fabric field of the fc_switch."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The logical name of the Fibre Channel switch.


Example: switch1"""

    ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.fc_switch_port.FcSwitchPortSchema", unknown=EXCLUDE, allow_none=True), data_key="ports", allow_none=True)
    r""" An array of the Fibre Channel (FC) switch's ports and their attached FC devices."""

    release = marshmallow_fields.Str(
        data_key="release",
        allow_none=True,
    )
    r""" The firmware release of the Fibre Channel switch.


Example: 1.0."""

    vendor = marshmallow_fields.Str(
        data_key="vendor",
        allow_none=True,
    )
    r""" The vendor of the Fibre Channel switch.


Example: vendor1"""

    wwn = marshmallow_fields.Str(
        data_key="wwn",
        allow_none=True,
    )
    r""" The world-wide name (WWN) for the Fibre Channel switch.


Example: 10:00:e1:e2:e3:e4:e5:e6"""

    @property
    def resource(self):
        return FcSwitch

    gettable_fields = [
        "links",
        "cache",
        "domain_id",
        "fabric.links",
        "fabric.name",
        "name",
        "ports",
        "release",
        "vendor",
        "wwn",
    ]
    """links,cache,domain_id,fabric.links,fabric.name,name,ports,release,vendor,wwn,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class FcSwitch(Resource):
    r""" A Fibre Channel switch. """

    _schema = FcSwitchSchema
    _path = "/api/network/fc/fabrics/{fabric[name]}/switches"
    _keys = ["fabric.name", "wwn"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the Fibre Channel switches of a Fibre Channel fabric.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `ports`
### Related ONTAP commands
* `network fcp topology show`
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
        """Returns a count of all FcSwitch resources that match the provided query"""
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
        """Returns a list of RawResources that represent FcSwitch resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the Fibre Channel switches of a Fibre Channel fabric.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `ports`
### Related ONTAP commands
* `network fcp topology show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a Fibre Channel switch.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `ports`
### Related ONTAP commands
* `network fcp topology show`
### Learn more
* [`DOC /network/fc/fabrics`](#docs-networking-network_fc_fabrics)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





