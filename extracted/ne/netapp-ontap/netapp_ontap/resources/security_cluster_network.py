r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use the security cluster-network API endpoints to modify the cluster network security configuration.
The following operations are supported:

* GET to retrieve the cluster network security status: GET security/cluster-network
* PATCH to update the cluster network security configuration: PATCH security/cluster-network"""

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


__all__ = ["SecurityClusterNetwork", "SecurityClusterNetworkSchema"]
__pdoc__ = {
    "SecurityClusterNetworkSchema.resource": False,
    "SecurityClusterNetworkSchema.opts": False,
}

class SecurityClusterNetworkSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetwork object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the security_cluster_network."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether cluster network security is enabled."""

    mode = marshmallow_fields.Str(
        data_key="mode",
        validate=enum_validation(['tls']),
        allow_none=True,
    )
    r""" The cluster network security mode.

Valid choices:

* tls"""

    status = marshmallow_fields.Str(
        data_key="status",
        allow_none=True,
    )
    r""" The status of the cluster network security configuration.

Example: ENABLING | DISABLING | READY"""

    @property
    def resource(self):
        return SecurityClusterNetwork

    gettable_fields = [
        "links",
        "enabled",
        "mode",
        "status",
    ]
    """links,enabled,mode,status,"""

    patchable_fields = [
        "enabled",
        "mode",
    ]
    """enabled,mode,"""

    postable_fields = [
        "enabled",
        "mode",
    ]
    """enabled,mode,"""

class SecurityClusterNetwork(Resource):
    r""" Manages the cluster network security configuration. """

    _schema = SecurityClusterNetworkSchema
    _path = "/api/security/cluster-network"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster network security configuration.
### Related ONTAP commands
* 'security cluster-network show'

### Learn more
* [`DOC /security/cluster-network`](#docs-security-security_cluster-network)"""
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
        r"""Updates the cluster network security configuration.
### Optional properties
* 'enabled' - Indicates whether cluster network security is enabled.
* 'mode' - The cluster network security mode.
### Related ONTAP commands
* 'security cluster-network modify'

### Learn more
* [`DOC /security/cluster-network`](#docs-security-security_cluster-network)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



