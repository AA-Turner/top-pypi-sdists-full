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


__all__ = ["ShadowcopySet", "ShadowcopySetSchema"]
__pdoc__ = {
    "ShadowcopySetSchema.resource": False,
    "ShadowcopySetSchema.opts": False,
}


class ShadowcopySetSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShadowcopySet object"""

    keep_snapshots = marshmallow_fields.Boolean(
        data_key="keep_snapshots",
        allow_none=True,
    )
    r""" Request the storage system to keep the snapshot copies taken as a part of the shadow copy set creation.

Example: true"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the shadowcopy_set."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The universally-unique identifier of the storage's shadow copy set.

Example: f8328660-00e6-11e6-80d9-005056bd65a9"""

    @property
    def resource(self):
        return ShadowcopySet

    gettable_fields = [
        "keep_snapshots",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """keep_snapshots,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "keep_snapshots",
    ]
    """keep_snapshots,"""

    postable_fields = [
        "keep_snapshots",
    ]
    """keep_snapshots,"""

class ShadowcopySet(Resource):
    """Allows interaction with ShadowcopySet objects on the host"""

    _schema = ShadowcopySetSchema
    _path = "/api/protocols/cifs/shadowcopy-sets"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Shadowcopy Sets.
### Related ONTAP commands
* `vserver cifs shadowcopy show-sets`
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
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
        """Returns a count of all ShadowcopySet resources that match the provided query"""
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
        """Returns a list of RawResources that represent ShadowcopySet resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["ShadowcopySet"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a Shadowcopy set
### Learn more
* [`DOC /protocols/cifs/shadowcopy`](#docs-NAS-protocols_cifs_shadowcopy)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Shadowcopy Sets.
### Related ONTAP commands
* `vserver cifs shadowcopy show-sets`
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a Shadowcopy set
### Related ONTAP commands
* `vserver cifs shadowcopy show-sets`
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
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
        r"""Updates a Shadowcopy set
### Learn more
* [`DOC /protocols/cifs/shadowcopy`](#docs-NAS-protocols_cifs_shadowcopy)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



