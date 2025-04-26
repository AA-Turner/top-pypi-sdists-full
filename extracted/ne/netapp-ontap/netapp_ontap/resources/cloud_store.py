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


__all__ = ["CloudStore", "CloudStoreSchema"]
__pdoc__ = {
    "CloudStoreSchema.resource": False,
    "CloudStoreSchema.opts": False,
}


class CloudStoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CloudStore object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cloud_store."""

    aggregate = marshmallow_fields.Nested("netapp_ontap.models.cloud_store_aggregate.CloudStoreAggregateSchema", data_key="aggregate", unknown=EXCLUDE, allow_none=True)
    r""" Aggregate"""

    availability = marshmallow_fields.Str(
        data_key="availability",
        validate=enum_validation(['available', 'unavailable']),
        allow_none=True,
    )
    r""" Availability of the object store.

Valid choices:

* available
* unavailable"""

    availability_at_partner = marshmallow_fields.Str(
        data_key="availability_at_partner",
        validate=enum_validation(['available', 'unavailable']),
        allow_none=True,
    )
    r""" Availability of the object store at the HA partner.

Valid choices:

* available
* unavailable"""

    mirror_degraded = marshmallow_fields.Boolean(
        data_key="mirror_degraded",
        allow_none=True,
    )
    r""" This field identifies if the mirror cloud store is in sync with the primary cloud store of a FabricPool."""

    primary = marshmallow_fields.Boolean(
        data_key="primary",
        allow_none=True,
    )
    r""" This field indicates whether the cloud store is the primary cloud store of a mirrored FabricPool."""

    resync_progress = Size(
        data_key="resync-progress",
        allow_none=True,
    )
    r""" Resync progress of the mirror object store in percentage."""

    target = marshmallow_fields.Nested("netapp_ontap.resources.cloud_target.CloudTargetSchema", data_key="target", unknown=EXCLUDE, allow_none=True)
    r""" The target field of the cloud_store."""

    unavailable_reason = marshmallow_fields.Nested("netapp_ontap.models.cloud_store_unavailable_reason.CloudStoreUnavailableReasonSchema", data_key="unavailable_reason", unknown=EXCLUDE, allow_none=True)
    r""" The unavailable_reason field of the cloud_store."""

    unreclaimed_space_threshold = Size(
        data_key="unreclaimed_space_threshold",
        allow_none=True,
    )
    r""" Usage threshold for reclaiming unused space in the cloud store. Valid values are 0 to 99. The default value depends on the provider type. This can be specified in PATCH but not POST.

Example: 20"""

    used = Size(
        data_key="used",
        allow_none=True,
    )
    r""" The amount of object space used. Calculated every 5 minutes and cached."""

    @property
    def resource(self):
        return CloudStore

    gettable_fields = [
        "links",
        "aggregate",
        "availability",
        "availability_at_partner",
        "mirror_degraded",
        "primary",
        "resync_progress",
        "target.links",
        "target.name",
        "target.uuid",
        "unavailable_reason",
        "unreclaimed_space_threshold",
        "used",
    ]
    """links,aggregate,availability,availability_at_partner,mirror_degraded,primary,resync_progress,target.links,target.name,target.uuid,unavailable_reason,unreclaimed_space_threshold,used,"""

    patchable_fields = [
        "primary",
        "unavailable_reason",
        "unreclaimed_space_threshold",
    ]
    """primary,unavailable_reason,unreclaimed_space_threshold,"""

    postable_fields = [
        "aggregate",
        "primary",
        "target.name",
        "target.uuid",
        "unavailable_reason",
        "unreclaimed_space_threshold",
    ]
    """aggregate,primary,target.name,target.uuid,unavailable_reason,unreclaimed_space_threshold,"""

class CloudStore(Resource):
    """Allows interaction with CloudStore objects on the host"""

    _schema = CloudStoreSchema
    _path = "/api/storage/aggregates/{aggregate[uuid]}/cloud-stores"
    _keys = ["aggregate.uuid", "target.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of cloud stores used by an aggregate.
### Related ONTAP commands
* `storage aggregate object-store show`
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
        """Returns a count of all CloudStore resources that match the provided query"""
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
        """Returns a list of RawResources that represent CloudStore resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["CloudStore"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the cloud store specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store modify`
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["CloudStore"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["CloudStore"], NetAppResponse]:
        r"""Attaches an object store to an aggregate, or adds a second object store as a mirror.
### Required properties
* `target.uuid` or `target.name` - UUID or name of the cloud target.
### Recommended optional properties
* `primary` - _true_ if the object store is primary or _false_ if it is a mirror.
* `allow_flexgroups` - Allow attaching object store to an aggregate containing FlexGroup constituents.
* `check_only` - Validate only and do not add the cloud store.
### Default property values
* `primary` - _true_
* `allow_flexgroups` - _false_
* `check_only` - _false_
### Related ONTAP commands
* `storage aggregate object-store attach`
* `storage aggregate object-store mirror`
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
        records: Iterable["CloudStore"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Removes the specified cloud target from the aggregate. Only removal of a mirror is allowed. The primary cannot be removed. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store unmirror`
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of cloud stores used by an aggregate.
### Related ONTAP commands
* `storage aggregate object-store show`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cloud store for the aggregate using the specified cloud target UUID.
### Related ONTAP commands
* `storage aggregate object-store show`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Attaches an object store to an aggregate, or adds a second object store as a mirror.
### Required properties
* `target.uuid` or `target.name` - UUID or name of the cloud target.
### Recommended optional properties
* `primary` - _true_ if the object store is primary or _false_ if it is a mirror.
* `allow_flexgroups` - Allow attaching object store to an aggregate containing FlexGroup constituents.
* `check_only` - Validate only and do not add the cloud store.
### Default property values
* `primary` - _true_
* `allow_flexgroups` - _false_
* `check_only` - _false_
### Related ONTAP commands
* `storage aggregate object-store attach`
* `storage aggregate object-store mirror`
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the cloud store specified by the UUID with the fields in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store modify`
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Removes the specified cloud target from the aggregate. Only removal of a mirror is allowed. The primary cannot be removed. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate object-store unmirror`
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


