r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

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


__all__ = ["DataEngineEvent", "DataEngineEventSchema"]
__pdoc__ = {
    "DataEngineEventSchema.resource": False,
    "DataEngineEventSchema.opts": False,
}

class DataEngineEventSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineEvent object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the data_engine_event."""

    attributes = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_event_attributes", "DataEngineEventAttributesSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="attributes",
                allow_none=True
            )
    r""" The list of attributes associated with the event."""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" The time when the event was created.

Example: 2023-10-01T12:00:00.000+0000"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" The description of the event.

Example: Example Event"""

    job = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_event_job", "DataEngineEventJobSchema"),
                data_key="job",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The job associated with the event."""

    owner = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_event_owner", "DataEngineEventOwnerSchema"),
                data_key="owner",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The user or group whose action triggered the event."""

    resource = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.data_engine_event_resource", "DataEngineEventResourceSchema"),
                data_key="resource",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The resource associated with the event."""

    severity = marshmallow_fields.Str(
        data_key="severity",
        validate=enum_validation(['info', 'warning', 'error', 'critical']),
        allow_none=True,
    )
    r""" The severity level of the event.

Valid choices:

* info
* warning
* error
* critical"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the event.

Example: 123e4567-e89b-12d3-a456-426614173000"""

    visible_to = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.data_engine_event_visible_to", "DataEngineEventVisibleToSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="visible_to",
                allow_none=True
            )
    r""" The list of users, groups, or roles that can see the event."""

    @property
    def resource(self):
        return DataEngineEvent

    gettable_fields = [
        "links",
        "attributes",
        "create_time",
        "description",
        "job",
        "owner",
        "resource",
        "severity",
        "uuid",
        "visible_to",
    ]
    """links,attributes,create_time,description,job,owner,resource,severity,uuid,visible_to,"""

    patchable_fields = [
        "attributes",
    ]
    """attributes,"""

    postable_fields = [
        "attributes",
    ]
    """attributes,"""

class DataEngineEvent(Resource):
    r""" Data engine event information """

    _schema = DataEngineEventSchema
    _path = "/api/data-engine/events"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of data engine events.
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
        """Returns a count of all DataEngineEvent resources that match the provided query"""
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
        """Returns a list of RawResources that represent DataEngineEvent resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of data engine events.
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a specific data engine event.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





