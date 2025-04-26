r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Manages the legal-hold operations for the specified litigation ID.
### Examples
1. Adds a Legal-Hold.
   <br/>
   ```
   POST "/api/storage/snaplock/litigations/f8a67b60-4461-11e9-b327-0050568ebef5:l1/operations" '{"type" : "begin", "path" : "/a.txt"}'
   ```
   <br/>
2. Removes a Legal-Hold.
   <br/>
   ```
   POST "/api/storage/snaplock/litigations/f8a67b60-4461-11e9-b327-0050568ebef5:l1/operations" '{"type" : "end", "path" : "/a.txt"}'
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


__all__ = ["SnaplockLegalHoldOperation", "SnaplockLegalHoldOperationSchema"]
__pdoc__ = {
    "SnaplockLegalHoldOperationSchema.resource": False,
    "SnaplockLegalHoldOperationSchema.opts": False,
}


class SnaplockLegalHoldOperationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLegalHoldOperation object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snaplock_legal_hold_operation."""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" Operation ID.

Example: 16842759"""

    num_files_failed = marshmallow_fields.Str(
        data_key="num_files_failed",
        allow_none=True,
    )
    r""" Specifies the number of files on which legal-hold operation failed.

Example: 0"""

    num_files_processed = marshmallow_fields.Str(
        data_key="num_files_processed",
        allow_none=True,
    )
    r""" Specifies the number of files on which legal-hold operation was successful.

Example: 30"""

    num_files_skipped = marshmallow_fields.Str(
        data_key="num_files_skipped",
        allow_none=True,
    )
    r""" Specifies the number of files on which legal-hold begin operation was skipped. The legal-hold begin operation is skipped on a file if it is already under hold for a given litigation.

Example: 10"""

    num_inodes_ignored = marshmallow_fields.Str(
        data_key="num_inodes_ignored",
        allow_none=True,
    )
    r""" Specifies the number of inodes on which the legal-hold operation was not attempted because they were not regular files.

Example: 10"""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Specifies the path on which legal-hold operation is applied.

Example: /dir1"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['in_progress', 'failed', 'aborting', 'completed']),
        allow_none=True,
    )
    r""" Specifies the status of legal-hold operation.

Valid choices:

* in_progress
* failed
* aborting
* completed"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['begin', 'end']),
        allow_none=True,
    )
    r""" Specifies the type of legal-hold operation.

Valid choices:

* begin
* end"""

    @property
    def resource(self):
        return SnaplockLegalHoldOperation

    gettable_fields = [
        "links",
        "id",
        "num_files_failed",
        "num_files_processed",
        "num_files_skipped",
        "num_inodes_ignored",
        "path",
        "state",
        "type",
    ]
    """links,id,num_files_failed,num_files_processed,num_files_skipped,num_inodes_ignored,path,state,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "path",
        "type",
    ]
    """path,type,"""

class SnaplockLegalHoldOperation(Resource):
    """Allows interaction with SnaplockLegalHoldOperation objects on the host"""

    _schema = SnaplockLegalHoldOperationSchema
    _path = "/api/storage/snaplock/litigations/{litigation[id]}/operations"
    _keys = ["litigation.id", "id"]



    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnaplockLegalHoldOperation"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnaplockLegalHoldOperation"], NetAppResponse]:
        r"""Creates or removes litigations for the specified path.
### Required properties
* `type` - Legal-Hold operation type.
* `path` - Litigation path.
### Related ONTAP commands
* `snaplock legal-hold begin`
* `snaplock legal-hold end`
### Learn more
* [`DOC /storage/snaplock/litigations/{litigation.id}/operations`](#docs-snaplock-storage_snaplock_litigations_{litigation.id}_operations)
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
        records: Iterable["SnaplockLegalHoldOperation"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Aborts the ongoing legal-hold operation. An abort does not rollback any changes already made. You must re-run begin or end for cleanup.
### Related ONTAP commands
* `snaplock legal-hold abort`
### Example
<br/>
```
DELETE "/api/storage/snaplock/litigations/f8a67b60-4461-11e9-b327-0050568ebef5:l1/operations/16908292"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/litigations/{litigation.id}/operations`](#docs-snaplock-storage_snaplock_litigations_{litigation.id}_operations)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)


    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the status of legal-hold for the specified operation ID.
### Related ONTAP commands
* `snaplock legal-hold show`
### Learn more
* [`DOC /storage/snaplock/litigations/{litigation.id}/operations`](#docs-snaplock-storage_snaplock_litigations_{litigation.id}_operations)
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
        r"""Creates or removes litigations for the specified path.
### Required properties
* `type` - Legal-Hold operation type.
* `path` - Litigation path.
### Related ONTAP commands
* `snaplock legal-hold begin`
* `snaplock legal-hold end`
### Learn more
* [`DOC /storage/snaplock/litigations/{litigation.id}/operations`](#docs-snaplock-storage_snaplock_litigations_{litigation.id}_operations)
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
        r"""Aborts the ongoing legal-hold operation. An abort does not rollback any changes already made. You must re-run begin or end for cleanup.
### Related ONTAP commands
* `snaplock legal-hold abort`
### Example
<br/>
```
DELETE "/api/storage/snaplock/litigations/f8a67b60-4461-11e9-b327-0050568ebef5:l1/operations/16908292"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/litigations/{litigation.id}/operations`](#docs-snaplock-storage_snaplock_litigations_{litigation.id}_operations)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


