r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to manage transfers on an existing SnapMirror relationship.</br>
You can initiate SnapMirror operations such as "initialize", "update", "restore-transfer", and "abort" using this API on asynchronous SnapMirror relationship. On a synchronous SnapMirror relationship, you can initiate SnapMirror "initialize" operation. The GET for this API reports the status of both active transfers and transfers that have terminated within the past 24 hours.<br>For the restore relationships, the POST on transfers API triggers "restore-transfer". Successful completion of "restore" also deletes the restore relationship. If the "restore" fails, DELETE on relationships must be called to delete the restore relationship.<br/>
A transfer on an asynchronous SnapMirror relationship with Application Consistency Group endpoints expands the destination Application Consistency Group endpoint if the source Application Consistency Group endpoint is already expanded.<br/>"""

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


__all__ = ["SnapmirrorTransfer", "SnapmirrorTransferSchema"]
__pdoc__ = {
    "SnapmirrorTransferSchema.resource": False,
    "SnapmirrorTransferSchema.opts": False,
}


class SnapmirrorTransferSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorTransfer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snapmirror_transfer."""

    bytes_transferred = Size(
        data_key="bytes_transferred",
        allow_none=True,
    )
    r""" Bytes transferred"""

    checkpoint_size = Size(
        data_key="checkpoint_size",
        allow_none=True,
    )
    r""" Amount of data transferred in bytes as recorded in the restart checkpoint."""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" End time of the transfer.

Example: 2020-12-03T02:36:19.000+0000"""

    error_info = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_transfer_error_info.SnapmirrorTransferErrorInfoSchema", data_key="error_info", unknown=EXCLUDE, allow_none=True)
    r""" Error information for the transfer."""

    files = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.snapmirror_transfer_files.SnapmirrorTransferFilesSchema", unknown=EXCLUDE, allow_none=True), data_key="files", allow_none=True)
    r""" This is supported for transfer of restore relationship only. This specifies the list of files or LUNs to be restored. Can contain up to eight files or LUNs."""

    last_updated_time = ImpreciseDateTime(
        data_key="last_updated_time",
        allow_none=True,
    )
    r""" Last updated time of the bytes transferred in an active transfer.

Example: 2023-09-15T23:58:39.000+0000"""

    network_compression_ratio = marshmallow_fields.Str(
        data_key="network_compression_ratio",
        allow_none=True,
    )
    r""" Specifies the compression ratio achieved for the data sent over the wire with network compression enabled. This property is only valid for active transfers.

Example: 61"""

    on_demand_attrs = marshmallow_fields.Str(
        data_key="on_demand_attrs",
        validate=enum_validation(['off', 'read_write_with_user_data_pull']),
        allow_none=True,
    )
    r""" Specifies whether or not an on-demand restore is being carried out. This is only supported for the transfer of restore relationships for entire volumes from the object store. A value for read_write_with_user_data_pull should be provided to start an on-demand restore. A file restore from the object store does not support this option.

Valid choices:

* off
* read_write_with_user_data_pull"""

    options = marshmallow_fields.List(marshmallow_fields.Dict, data_key="options", allow_none=True)
    r""" Options for snapmirror transfer."""

    relationship = marshmallow_fields.Nested("netapp_ontap.models.snapmirror_transfer_relationship.SnapmirrorTransferRelationshipSchema", data_key="relationship", unknown=EXCLUDE, allow_none=True)
    r""" The relationship field of the snapmirror_transfer."""

    snapshot = marshmallow_fields.Str(
        data_key="snapshot",
        allow_none=True,
    )
    r""" Name of snapshot being transferred."""

    source_snapshot = marshmallow_fields.Str(
        data_key="source_snapshot",
        allow_none=True,
    )
    r""" Specifies the snapshot on the source to be transferred to the destination."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['aborted', 'failed', 'hard_aborted', 'queued', 'success', 'transferring']),
        allow_none=True,
    )
    r""" Status of the transfer. Set PATCH state to "aborted" to abort the transfer. Set PATCH state to "hard_aborted" to abort the transfer and discard the restart checkpoint. To find "queued" transfers refer to relationships GET API.

Valid choices:

* aborted
* failed
* hard_aborted
* queued
* success
* transferring"""

    storage_efficiency_enabled = marshmallow_fields.Boolean(
        data_key="storage_efficiency_enabled",
        allow_none=True,
    )
    r""" This is supported for transfer of restore relationship only. Set this property to "false" to turn off storage efficiency for data transferred over the wire and written to the destination."""

    throttle = Size(
        data_key="throttle",
        allow_none=True,
    )
    r""" Throttle, in KBs per second. This "throttle" overrides the "throttle" set on the SnapMirror relationship or SnapMirror relationship's policy. If neither of these are set, defaults to 0, which is interpreted as unlimited."""

    total_duration = marshmallow_fields.Str(
        data_key="total_duration",
        allow_none=True,
    )
    r""" Elapsed transfer time.

Example: PT28M41S"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Unique identifier of the SnapMirror transfer.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return SnapmirrorTransfer

    gettable_fields = [
        "links",
        "bytes_transferred",
        "checkpoint_size",
        "end_time",
        "error_info",
        "last_updated_time",
        "network_compression_ratio",
        "on_demand_attrs",
        "relationship",
        "snapshot",
        "state",
        "throttle",
        "total_duration",
        "uuid",
    ]
    """links,bytes_transferred,checkpoint_size,end_time,error_info,last_updated_time,network_compression_ratio,on_demand_attrs,relationship,snapshot,state,throttle,total_duration,uuid,"""

    patchable_fields = [
        "on_demand_attrs",
        "state",
    ]
    """on_demand_attrs,state,"""

    postable_fields = [
        "files",
        "on_demand_attrs",
        "options",
        "source_snapshot",
        "storage_efficiency_enabled",
        "throttle",
    ]
    """files,on_demand_attrs,options,source_snapshot,storage_efficiency_enabled,throttle,"""

class SnapmirrorTransfer(Resource):
    r""" SnapMirror transfer information """

    _schema = SnapmirrorTransferSchema
    _path = "/api/snapmirror/relationships/{relationship[uuid]}/transfers"
    _keys = ["relationship.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the list of ongoing SnapMirror transfers for the specified relationship.
### Related ONTAP commands
* `snapmirror show`
### Example
<br/>
```
GET "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers"
```
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
<br/>
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
        """Returns a count of all SnapmirrorTransfer resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnapmirrorTransfer resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnapmirrorTransfer"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Aborts an ongoing SnapMirror transfer. This operation is applicable on asynchronous SnapMirror relationships.
### Related ONTAP commands
* `snapmirror abort`
### Example
<br/>
```
PATCH "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers/293baa53-e63d-11e8-bff1-005056a793dd" '{"state":"aborted"}'
```
<br/>
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnapmirrorTransfer"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnapmirrorTransfer"], NetAppResponse]:
        r"""Starts a SnapMirror transfer operation. This API initiates a restore operation if the SnapMirror relationship is of type "restore". Otherwise, it initiates a SnapMirror "initialize" operation or "update" operation based on the current SnapMirror state.
### Default property values
* `storage_efficiency_enabled` - _true_
### Related ONTAP commands
* `snapmirror update`
* `snapmirror initialize`
* `snapmirror restore`

### Examples
The following examples show how to perform SnapMirror "initialize", "update", and "restore" operations.
<br/>
   Perform SnapMirror initialize or update
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{}'
   ```
   <br/>
   Perform SnapMirror initialize, update or restore with throttle value set
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"throttle":"100"}'
   ```
   <br/>
   Perform SnapMirror restore transfer of a file
   <br/>
   ```
   POST "/api/snapmirror/relationships/c8c62a90-0fef-11e9-b09e-0050568e7067/transfers" '{"source_snapshot": "src", "files":[{"source_path": "/a1.txt.0", "destination_path": "/a1-renamed.txt.0"}]}'
   ```
   <br/>
   Performing a SnapMirror initialize or update using a particular snapshot.
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"source_snapshot":"snap1"}'
   ```
   <br/>
   
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the list of ongoing SnapMirror transfers for the specified relationship.
### Related ONTAP commands
* `snapmirror show`
### Example
<br/>
```
GET "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers"
```
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
<br/>
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the attributes of a specific ongoing SnapMirror transfer.
### Related ONTAP commands
* `snapmirror show`
### Example
<br/>
```
GET "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers/293baa53-e63d-11e8-bff1-005056a793dd"
```
<br/>
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
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
        r"""Starts a SnapMirror transfer operation. This API initiates a restore operation if the SnapMirror relationship is of type "restore". Otherwise, it initiates a SnapMirror "initialize" operation or "update" operation based on the current SnapMirror state.
### Default property values
* `storage_efficiency_enabled` - _true_
### Related ONTAP commands
* `snapmirror update`
* `snapmirror initialize`
* `snapmirror restore`

### Examples
The following examples show how to perform SnapMirror "initialize", "update", and "restore" operations.
<br/>
   Perform SnapMirror initialize or update
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{}'
   ```
   <br/>
   Perform SnapMirror initialize, update or restore with throttle value set
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"throttle":"100"}'
   ```
   <br/>
   Perform SnapMirror restore transfer of a file
   <br/>
   ```
   POST "/api/snapmirror/relationships/c8c62a90-0fef-11e9-b09e-0050568e7067/transfers" '{"source_snapshot": "src", "files":[{"source_path": "/a1.txt.0", "destination_path": "/a1-renamed.txt.0"}]}'
   ```
   <br/>
   Performing a SnapMirror initialize or update using a particular snapshot.
   <br/>
   ```
   POST "/api/snapmirror/relationships/e4e7e130-0279-11e9-b566-0050568e9909/transfers" '{"source_snapshot":"snap1"}'
   ```
   <br/>
   
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
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
        r"""Aborts an ongoing SnapMirror transfer. This operation is applicable on asynchronous SnapMirror relationships.
### Related ONTAP commands
* `snapmirror abort`
### Example
<br/>
```
PATCH "/api/snapmirror/relationships/293baa53-e63d-11e8-bff1-005056a793dd/transfers/293baa53-e63d-11e8-bff1-005056a793dd" '{"state":"aborted"}'
```
<br/>
### Learn more
* [`DOC /snapmirror/relationships/{relationship.uuid}/transfers`](#docs-snapmirror-snapmirror_relationships_{relationship.uuid}_transfers)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



