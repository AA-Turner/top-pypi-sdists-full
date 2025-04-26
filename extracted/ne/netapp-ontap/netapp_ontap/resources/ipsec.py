r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The following operations are supported:

* GET to retrieve the IPsec status: GET security/ipsec
* Patch to update IPsec status: PATCH security/ipsec"""

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


__all__ = ["Ipsec", "IpsecSchema"]
__pdoc__ = {
    "IpsecSchema.resource": False,
    "IpsecSchema.opts": False,
}


class IpsecSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Ipsec object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ipsec."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether or not IPsec is enabled."""

    offload_enabled = marshmallow_fields.Boolean(
        data_key="offload_enabled",
        allow_none=True,
    )
    r""" Indicates whether or not IPsec hardware offload is enabled."""

    replay_window = Size(
        data_key="replay_window",
        allow_none=True,
    )
    r""" Replay window size in packets, where 0 indicates that the relay window is disabled."""

    @property
    def resource(self):
        return Ipsec

    gettable_fields = [
        "links",
        "enabled",
        "offload_enabled",
        "replay_window",
    ]
    """links,enabled,offload_enabled,replay_window,"""

    patchable_fields = [
        "enabled",
        "offload_enabled",
        "replay_window",
    ]
    """enabled,offload_enabled,replay_window,"""

    postable_fields = [
        "enabled",
        "offload_enabled",
        "replay_window",
    ]
    """enabled,offload_enabled,replay_window,"""

class Ipsec(Resource):
    r""" Manages IPsec configuration via REST APIs. """

    _schema = IpsecSchema
    _path = "/api/security/ipsec"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves IPsec configuration via REST APIs.
### Related ONTAP commands
* 'security ipsec config show'

### Learn more
* [`DOC /security/ipsec`](#docs-security-security_ipsec)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates IPsec configuration via REST APIs.
### Optional properties
* 'enabled' - Enable IPsec.
* 'replay_window' - Replay window size in packets.
* 'offload_enabled' - Enable IPsec hardware offload.
### Related ONTAP commands
* 'security ipsec config modify'

### Learn more
* [`DOC /security/ipsec`](#docs-security-security_ipsec)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



