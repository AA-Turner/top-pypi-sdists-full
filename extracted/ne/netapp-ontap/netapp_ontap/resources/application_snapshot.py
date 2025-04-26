r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Applications support snapshots across all member storage elements. These snapshots can be created and restored at any time or as scheduled. Most applications have hourly snapshots enabled by default, unless the RPO setting is overridden during the creation of the application. An application snapshot can be flagged as either _application consistent_, or _crash consistent_. From an ONTAP perspective, there is no difference between these two consistency types. These types are available for record keeping so that snapshots taken after the application is quiesced (application consistent) can be tracked separately from those snapshots taken without first quiescing the application (crash consistent). By default, all application snapshots are flagged to be _crash consistent_, and snapshots taken at a scheduled time are also considered _crash consistent_.<br/>
The functionality provided by these APIs is not integrated with the host application. Snapshots have limited value without host coordination, so the use of the SnapCenter Backup Management suite is recommended to ensure correct interaction between host applications and ONTAP."""

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


__all__ = ["ApplicationSnapshot", "ApplicationSnapshotSchema"]
__pdoc__ = {
    "ApplicationSnapshotSchema.resource": False,
    "ApplicationSnapshotSchema.opts": False,
}


class ApplicationSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationSnapshot object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the application_snapshot."""

    application = marshmallow_fields.Nested("netapp_ontap.models.application_snapshot_application.ApplicationSnapshotApplicationSchema", data_key="application", unknown=EXCLUDE, allow_none=True)
    r""" The application field of the application_snapshot."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=255),
        allow_none=True,
    )
    r""" Comment. Valid in POST."""

    components = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_snapshot_components.ApplicationSnapshotComponentsSchema", unknown=EXCLUDE, allow_none=True), data_key="components", allow_none=True)
    r""" The components field of the application_snapshot."""

    consistency_type = marshmallow_fields.Str(
        data_key="consistency_type",
        validate=enum_validation(['crash', 'application']),
        allow_none=True,
    )
    r""" Consistency type. This is for categorization purposes only. A snapshot should not be set to 'application consistent' unless the host application is quiesced for the snapshot. Valid in POST.

Valid choices:

* crash
* application"""

    create_time = marshmallow_fields.Str(
        data_key="create_time",
        allow_none=True,
    )
    r""" Creation time"""

    is_partial = marshmallow_fields.Boolean(
        data_key="is_partial",
        allow_none=True,
    )
    r""" A partial snapshot means that not all volumes in an application component were included in the snapshot."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The snapshot name. Valid in POST."""

    svm = marshmallow_fields.Nested("netapp_ontap.models.application_component_svm.ApplicationComponentSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the application_snapshot."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The snapshot UUID. Valid in URL."""

    @property
    def resource(self):
        return ApplicationSnapshot

    gettable_fields = [
        "links",
        "application",
        "comment",
        "components",
        "consistency_type",
        "create_time",
        "is_partial",
        "name",
        "svm",
        "uuid",
    ]
    """links,application,comment,components,consistency_type,create_time,is_partial,name,svm,uuid,"""

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

class ApplicationSnapshot(Resource):
    """Allows interaction with ApplicationSnapshot objects on the host"""

    _schema = ApplicationSnapshotSchema
    _path = "/api/application/applications/{application[uuid]}/snapshots"
    _keys = ["application.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves snapshots of an application.
### Query examples
The following query returns all snapshots from May 4, 2017 EST. For readability, the colon (`:`) is left in this example. For an actual call, they should be escaped as `%3A`.<br/><br/>
```
GET /application/applications/{application.uuid}/snapshots?create_time=2017-05-04T00:00:00-05:00..2017-05-04T23:59:59-05:00
```
<br/>The following query returns all snapshots that have been flagged as _application consistent_.<br/><br/>
```
GET /application/applications/{application.uuid}/snapshots?consistency_type=application
```
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
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
        """Returns a count of all ApplicationSnapshot resources that match the provided query"""
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
        """Returns a list of RawResources that represent ApplicationSnapshot resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["ApplicationSnapshot"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ApplicationSnapshot"], NetAppResponse]:
        r"""Creates a snapshot of the application.

### Required properties
* `name`
### Recommended optional properties
* `consistency_type` - Track whether this snapshot is _application_ or _crash_ consistent.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
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
        records: Iterable["ApplicationSnapshot"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Delete a snapshot of an application

### Query examples
Individual snapshots can be destroyed with no query parameters, or a range of snapshots can be destroyed at one time using a query.<br/>
The following query deletes all application snapshots created before May 4, 2017<br/><br/>
```
DELETE /application/applications/{application.uuid}/snapshots?create_time=<2017-05-04T00:00:00-05:00
```

### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves snapshots of an application.
### Query examples
The following query returns all snapshots from May 4, 2017 EST. For readability, the colon (`:`) is left in this example. For an actual call, they should be escaped as `%3A`.<br/><br/>
```
GET /application/applications/{application.uuid}/snapshots?create_time=2017-05-04T00:00:00-05:00..2017-05-04T23:59:59-05:00
```
<br/>The following query returns all snapshots that have been flagged as _application consistent_.<br/><br/>
```
GET /application/applications/{application.uuid}/snapshots?consistency_type=application
```
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
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
* [`GET /application/applications/{uuid}/snapshots`](#operations-application-application_snapshot_create)
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
        r"""Creates a snapshot of the application.

### Required properties
* `name`
### Recommended optional properties
* `consistency_type` - Track whether this snapshot is _application_ or _crash_ consistent.
### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)
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
        r"""Delete a snapshot of an application

### Query examples
Individual snapshots can be destroyed with no query parameters, or a range of snapshots can be destroyed at one time using a query.<br/>
The following query deletes all application snapshots created before May 4, 2017<br/><br/>
```
DELETE /application/applications/{application.uuid}/snapshots?create_time=<2017-05-04T00:00:00-05:00
```

### Learn more
* [`DOC /application/applications/{application.uuid}/snapshots`](#docs-application-application_applications_{application.uuid}_snapshots)"""
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
        r"""Restore an application snapshot<br/>

Restoring an application snapshot reverts all storage elements in the snapshot to the state in which the snapshot was in when the snapshot was taken. This restoration does not apply to access settings that might have changed since the snapshot was created.
### Learn more
* [`DOC /application`](#docs-application-overview)
* [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

