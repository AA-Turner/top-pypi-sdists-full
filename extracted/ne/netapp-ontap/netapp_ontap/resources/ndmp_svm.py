r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

You can use this API to manage NDMP configurations of SVMs.
### Examples
Updates the "enabled" field:
   <br/>
   ```
   PATCH "/api/protocols/ndmp/svms/9b372ce7-3a4b-11e9-a7f8-0050568e3d73" '{"enabled":"false"}'
   ```
   <br/>
Updates the "authentication_types" field:
   <br/>
   ```
   PATCH "/api/protocols/ndmp/svms/9b372ce7-3a4b-11e9-a7f8-0050568e3d73" '{"authentication_types":["challenge"]}'
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


__all__ = ["NdmpSvm", "NdmpSvmSchema"]
__pdoc__ = {
    "NdmpSvmSchema.resource": False,
    "NdmpSvmSchema.opts": False,
}


class NdmpSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NdmpSvm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ndmp_svm."""

    authentication_types = marshmallow_fields.List(marshmallow_fields.Str, data_key="authentication_types", allow_none=True)
    r""" NDMP authentication types.

Example: ["plaintext","challenge"]"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Is the NDMP service enabled on the SVM?

Example: true"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ndmp_svm."""

    @property
    def resource(self):
        return NdmpSvm

    gettable_fields = [
        "links",
        "authentication_types",
        "enabled",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,authentication_types,enabled,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "authentication_types",
        "enabled",
    ]
    """authentication_types,enabled,"""

    postable_fields = [
        "authentication_types",
        "enabled",
    ]
    """authentication_types,enabled,"""

class NdmpSvm(Resource):
    """Allows interaction with NdmpSvm objects on the host"""

    _schema = NdmpSvmSchema
    _path = "/api/protocols/ndmp/svms"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NDMP configurations for all SVMs.
### Related ONTAP commands
* `vserver services ndmp show`
### Learn more
* [`DOC /protocols/ndmp/svms`](#docs-ndmp-protocols_ndmp_svms)
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
        """Returns a count of all NdmpSvm resources that match the provided query"""
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
        """Returns a list of RawResources that represent NdmpSvm resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NdmpSvm"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the NDMP configuration for a specific SVM.
### Related ONTAP commands
* `vserver services ndmp modify`
### Learn more
* [`DOC /protocols/ndmp/svms`](#docs-ndmp-protocols_ndmp_svms)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NDMP configurations for all SVMs.
### Related ONTAP commands
* `vserver services ndmp show`
### Learn more
* [`DOC /protocols/ndmp/svms`](#docs-ndmp-protocols_ndmp_svms)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NDMP configuration for a specific SVM.
### Related ONTAP commands
* `vserver services ndmp show`
### Learn more
* [`DOC /protocols/ndmp/svms`](#docs-ndmp-protocols_ndmp_svms)
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
        r"""Updates the NDMP configuration for a specific SVM.
### Related ONTAP commands
* `vserver services ndmp modify`
### Learn more
* [`DOC /protocols/ndmp/svms`](#docs-ndmp-protocols_ndmp_svms)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



