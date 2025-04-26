r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

This API manages the ComplianceClock of the system. ComplianceClock determines the expiry time of the SnapLock objects in the system. The user can initialize the ComplianceClock. The ComplianceClock can be re-initialized if all nodes in the cluster are healthy, all volumes are in online state, no volumes are present in the volume recovery queue and there are no SnapLock volumes or volumes with \"snapshot-locking-enabled\" set to true or S3 buckets with object locking enabled."""

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


__all__ = ["SnaplockComplianceClock", "SnaplockComplianceClockSchema"]
__pdoc__ = {
    "SnaplockComplianceClockSchema.resource": False,
    "SnaplockComplianceClockSchema.opts": False,
}


class SnaplockComplianceClockSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockComplianceClock object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snaplock_compliance_clock."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the snaplock_compliance_clock."""

    time = ImpreciseDateTime(
        data_key="time",
        allow_none=True,
    )
    r""" Compliance clock time

Example: 2018-06-04T19:00:00.000+0000"""

    @property
    def resource(self):
        return SnaplockComplianceClock

    gettable_fields = [
        "links",
        "node.links",
        "node.name",
        "node.uuid",
        "time",
    ]
    """links,node.links,node.name,node.uuid,time,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""

class SnaplockComplianceClock(Resource):
    """Allows interaction with SnaplockComplianceClock objects on the host"""

    _schema = SnaplockComplianceClockSchema
    _path = "/api/storage/snaplock/compliance-clocks"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the SnapLock ComplianceClock for all of the nodes in the cluster.
### Related ONTAP commands
* `snaplock compliance-clock show`
### Learn more
* [`DOC /storage/snaplock/compliance-clocks`](#docs-snaplock-storage_snaplock_compliance-clocks)
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
        """Returns a count of all SnaplockComplianceClock resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnaplockComplianceClock resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnaplockComplianceClock"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnaplockComplianceClock"], NetAppResponse]:
        r"""Initializes the SnapLock ComplianceClock.
### Required properties
* `node.name` or `node.uuid` - Name or UUID of the node.
### Related ONTAP commands
* `snaplock compliance-clock initialize`
### Learn more
* [`DOC /storage/snaplock/compliance-clocks`](#docs-snaplock-storage_snaplock_compliance-clocks)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the SnapLock ComplianceClock for all of the nodes in the cluster.
### Related ONTAP commands
* `snaplock compliance-clock show`
### Learn more
* [`DOC /storage/snaplock/compliance-clocks`](#docs-snaplock-storage_snaplock_compliance-clocks)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the SnapLock ComplianceClock for a specific node.
### Related ONTAP commands
* `snaplock compliance-clock show`
### Learn more
* [`DOC /storage/snaplock/compliance-clocks`](#docs-snaplock-storage_snaplock_compliance-clocks)
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
        r"""Initializes the SnapLock ComplianceClock.
### Required properties
* `node.name` or `node.uuid` - Name or UUID of the node.
### Related ONTAP commands
* `snaplock compliance-clock initialize`
### Learn more
* [`DOC /storage/snaplock/compliance-clocks`](#docs-snaplock-storage_snaplock_compliance-clocks)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




