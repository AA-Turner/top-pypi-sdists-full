r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

You can use this API to manage NDMP mode: SVM-scope or node-scope.
### Examples
Updates NDMP mode to SVM:
   <br/>
   ```
   PATCH "/api/protocols/ndmp" '{"mode":"svm"}'
   ```
   <br/>
Updates NDMP mode to node:
   <br/>
   ```
   PATCH "/api/protocols/ndmp" '{"mode":"node"}'
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


__all__ = ["ClusterNdmpProperties", "ClusterNdmpPropertiesSchema"]
__pdoc__ = {
    "ClusterNdmpPropertiesSchema.resource": False,
    "ClusterNdmpPropertiesSchema.opts": False,
}


class ClusterNdmpPropertiesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNdmpProperties object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cluster_ndmp_properties."""

    mode = marshmallow_fields.Str(
        data_key="mode",
        validate=enum_validation(['svm', 'node']),
        allow_none=True,
    )
    r""" Indicates whether NDMP is in node-scoped or SVM-scoped mode.

Valid choices:

* svm
* node"""

    @property
    def resource(self):
        return ClusterNdmpProperties

    gettable_fields = [
        "links",
        "mode",
    ]
    """links,mode,"""

    patchable_fields = [
        "mode",
    ]
    """mode,"""

    postable_fields = [
        "mode",
    ]
    """mode,"""

class ClusterNdmpProperties(Resource):
    """Allows interaction with ClusterNdmpProperties objects on the host"""

    _schema = ClusterNdmpPropertiesSchema
    _path = "/api/protocols/ndmp"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the current NDMP mode.
### Related ONTAP commands
* `system services ndmp node-scope-mode status`
### Learn more
* [`DOC /protocols/ndmp`](#docs-ndmp-protocols_ndmp)
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
        r"""Updates the NDMP mode.
### Related ONTAP commands
* `system services ndmp node-scope-mode`
### Learn more
* [`DOC /protocols/ndmp`](#docs-ndmp-protocols_ndmp)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



