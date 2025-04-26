r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

You can use this API to manage node configurations. The authentication types "plaintext" and "plaintext_sso" are used to show that the password uses clear text. Also, they contain no differences for NDMP node scope.
### Examples
Updates "enabled" and "authentication_types" fields:
   <br/>
   ```
   PATCH "/api/protocols/ndmp/nodes/13bb2092-458b-11e9-9c06-0050568ea64e" '{"enabled":"false","authentication_types":["plaintext"]}'
   ```
   <br/>
Updates the "user" field:
   <br/>
   ```
   PATCH "/api/protocols/ndmp/nodes/13bb2092-458b-11e9-9c06-0050568ea64e" '{"user":"user22"}'
   ```
   <br/>"""

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


__all__ = ["NdmpNode", "NdmpNodeSchema"]
__pdoc__ = {
    "NdmpNodeSchema.resource": False,
    "NdmpNodeSchema.opts": False,
}


class NdmpNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NdmpNode object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ndmp_node."""

    authentication_types = marshmallow_fields.List(marshmallow_fields.Str, data_key="authentication_types", allow_none=True)
    r""" NDMP authentication types.

Example: ["plaintext","challenge"]"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Is the NDMP service enabled?

Example: true"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the ndmp_node."""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" NDMP password. This can only be set and cannot be read back."""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" NDMP user ID

Example: ndmp_user"""

    @property
    def resource(self):
        return NdmpNode

    gettable_fields = [
        "links",
        "authentication_types",
        "enabled",
        "node.links",
        "node.name",
        "node.uuid",
        "user",
    ]
    """links,authentication_types,enabled,node.links,node.name,node.uuid,user,"""

    patchable_fields = [
        "authentication_types",
        "enabled",
        "password",
        "user",
    ]
    """authentication_types,enabled,password,user,"""

    postable_fields = [
        "authentication_types",
        "enabled",
        "password",
        "user",
    ]
    """authentication_types,enabled,password,user,"""

class NdmpNode(Resource):
    """Allows interaction with NdmpNode objects on the host"""

    _schema = NdmpNodeSchema
    _path = "/api/protocols/ndmp/nodes"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NDMP node configurations for all of the nodes.
### Related ONTAP commands
* `system services ndmp show`
### Learn more
* [`DOC /protocols/ndmp/nodes`](#docs-ndmp-protocols_ndmp_nodes)
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
        """Returns a count of all NdmpNode resources that match the provided query"""
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
        """Returns a list of RawResources that represent NdmpNode resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NdmpNode"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the NDMP node configuration for a specific node.
### Related ONTAP commands
* `system services ndmp modify`
### Learn more
* [`DOC /protocols/ndmp/nodes`](#docs-ndmp-protocols_ndmp_nodes)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NDMP node configurations for all of the nodes.
### Related ONTAP commands
* `system services ndmp show`
### Learn more
* [`DOC /protocols/ndmp/nodes`](#docs-ndmp-protocols_ndmp_nodes)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NDMP node configuration for a specific node.
### Related ONTAP commands
* `system services ndmp show`
### Learn more
* [`DOC /protocols/ndmp/nodes`](#docs-ndmp-protocols_ndmp_nodes)
"""
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
        r"""Updates the NDMP node configuration for a specific node.
### Related ONTAP commands
* `system services ndmp modify`
### Learn more
* [`DOC /protocols/ndmp/nodes`](#docs-ndmp-protocols_ndmp_nodes)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



