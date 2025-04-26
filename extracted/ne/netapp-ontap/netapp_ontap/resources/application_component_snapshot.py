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


__all__ = ["ApplicationComponentSnapshot", "ApplicationComponentSnapshotSchema"]
__pdoc__ = {
    "ApplicationComponentSnapshotSchema.resource": False,
    "ApplicationComponentSnapshotSchema.opts": False,
}


class ApplicationComponentSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationComponentSnapshot object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the application_component_snapshot."""

    application = marshmallow_fields.Nested("netapp_ontap.models.application_component_snapshot_application.ApplicationComponentSnapshotApplicationSchema", data_key="application", unknown=EXCLUDE, allow_none=True)
    r""" The application field of the application_component_snapshot."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=255),
        allow_none=True,
    )
    r""" Comment. Valid in POST"""

    component = marshmallow_fields.Nested("netapp_ontap.models.application_component_snapshot_component.ApplicationComponentSnapshotComponentSchema", data_key="component", unknown=EXCLUDE, allow_none=True)
    r""" The component field of the application_component_snapshot."""

    consistency_type = marshmallow_fields.Str(
        data_key="consistency_type",
        validate=enum_validation(['crash', 'application']),
        allow_none=True,
    )
    r""" Consistency Type. This is for categorization only. A snapshot should not be set to application consistent unless the host application is quiesced for the snapshot. Valid in POST

Valid choices:

* crash
* application"""

    create_time = marshmallow_fields.Str(
        data_key="create_time",
        allow_none=True,
    )
    r""" Creation Time"""

    is_partial = marshmallow_fields.Boolean(
        data_key="is_partial",
        allow_none=True,
    )
    r""" A partial snapshot means that not all volumes in an application component were included in the snapshot."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Snapshot name. Valid in POST"""

    svm = marshmallow_fields.Nested("netapp_ontap.models.application_component_snapshot_svm.ApplicationComponentSnapshotSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the application_component_snapshot."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Snapshot UUID. Valid in URL"""

    @property
    def resource(self):
        return ApplicationComponentSnapshot

    gettable_fields = [
        "links",
        "application",
        "comment",
        "component",
        "consistency_type",
        "create_time",
        "is_partial",
        "name",
        "svm",
        "uuid",
    ]
    """links,application,comment,component,consistency_type,create_time,is_partial,name,svm,uuid,"""

    patchable_fields = [
        "comment",
        "consistency_type",
        "name",
    ]
    """comment,consistency_type,name,"""

    postable_fields = [
        "comment",
        "consistency_type",
        "name",
    ]
    """comment,consistency_type,name,"""

class ApplicationComponentSnapshot(Resource):
    """Allows interaction with ApplicationComponentSnapshot objects on the host"""

    _schema = ApplicationComponentSnapshotSchema
    _path = "/api/application/applications/{application[uuid]}/components/{component[uuid]}/snapshots"
    _keys = ["application.uuid", "component.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves snapshots of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_collection_get)
* [`DOC /application`](#docs-application-overview)
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
        """Returns a count of all ApplicationComponentSnapshot resources that match the provided query"""
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
        """Returns a list of RawResources that represent ApplicationComponentSnapshot resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["ApplicationComponentSnapshot"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ApplicationComponentSnapshot"], NetAppResponse]:
        r"""Creates a snapshot of an application component.<br/>

This endpoint is only supported for Maxdata template applications.<br/>
### Required properties
* `name`
### Recommended optional properties
* `consistency_type` - Track whether this snapshot is _application_ or _crash_ consistent.
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_create)
* [`DOC /application`](#docs-application-overview)
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
        records: Iterable["ApplicationComponentSnapshot"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Delete a snapshot of an application component.<br/>

This endpoint is only supported for Maxdata template applications.<br/>
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`DELETE /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_delete)
* [`DOC /application`](#docs-application-overview)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves snapshots of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_collection_get)
* [`DOC /application`](#docs-application-overview)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieve a snapshot of an application component.<br/>
This endpoint is only supported for Maxdata template applications.<br/>
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_get)
* [`DOC /application`](#docs-application-overview)
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
        r"""Creates a snapshot of an application component.<br/>

This endpoint is only supported for Maxdata template applications.<br/>
### Required properties
* `name`
### Recommended optional properties
* `consistency_type` - Track whether this snapshot is _application_ or _crash_ consistent.
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_create)
* [`DOC /application`](#docs-application-overview)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Delete a snapshot of an application component.<br/>

This endpoint is only supported for Maxdata template applications.<br/>
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`DELETE /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_delete)
* [`DOC /application`](#docs-application-overview)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    def restore(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Restore a snapshot of an application component.<br/>

This endpoint is only supported for Maxdata template applications.<br/>
Component snapshots are essentially more granular application snapshots. There is no difference beyond the scope of the operation.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
* [`POST /application/applications/{application.uuid}/snapshots/{uuid}/restore`](#operations-application-application_snapshot_restore)
* [`DOC /application`](#docs-application-overview)
* [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

