r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use the security ha-network API endpoint to modify the HA network security configuration for NVLog traffic.
The following operations are supported:

* GET to retrieve the HA network security status: GET security/ha-network
* PATCH to update the HA network security configuration: PATCH security/ha-network"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SecurityHaNetwork", "SecurityHaNetworkSchema"]
__pdoc__ = {
    "SecurityHaNetworkSchema.resource": False,
    "SecurityHaNetworkSchema.opts": False,
}

class SecurityHaNetworkSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityHaNetwork object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the security_ha_network."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates if HA network security is enabled."""

    node_name = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.node", "NodeSchema"),
                data_key="node.name",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The node_name field of the security_ha_network."""

    @property
    def resource(self):
        return SecurityHaNetwork

    gettable_fields = [
        "links",
        "enabled",
        "node_name.links",
        "node_name.name",
        "node_name.uuid",
    ]
    """links,enabled,node_name.links,node_name.name,node_name.uuid,"""

    patchable_fields = [
        "enabled",
        "node_name.name",
        "node_name.uuid",
    ]
    """enabled,node_name.name,node_name.uuid,"""

    postable_fields = [
        "enabled",
        "node_name.name",
        "node_name.uuid",
    ]
    """enabled,node_name.name,node_name.uuid,"""

class SecurityHaNetwork(Resource):
    r""" Manages the HA network security configuration. """

    _schema = SecurityHaNetworkSchema
    _path = "/api/security/ha-network"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the HA network security configuration.
### Related ONTAP commands
* 'security ha-network show'

### Learn more
* [`DOC /security/ha-network`](#docs-security-security_ha-network)"""
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
        r"""Updates the HA network security configuration.
### Optional properties
* 'enabled' - Indicates if HA network security for NVLog traffic is enabled.
### Related ONTAP commands
* 'security ha-network modify'

### Learn more
* [`DOC /security/ha-network`](#docs-security-security_ha-network)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



