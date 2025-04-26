r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Use this API to display all Event Based Retention (EBR) operations and to apply an EBR policy on a specified volume or path within the volume. Only a user with security login role vsadmin-snaplock can perform the operation.
### Examples
1. Displays all of the EBR operations:
   <br/>
   ```
   GET "/api/storage/snaplock/event-retention/operations"
   ```
   <br/>
2. Displays all completed EBR operations:
   <br/>
   ```
   GET "/api/storage/snaplock/event-retention/operations?state=completed"
   ```
   <br/>
3. Displays all completed EBR operations with filter set as volume.uuid:
   <br/>
   ```
   GET "/api/storage/snaplock/event-retention/operations?volume.uuid=b96f976e-404b-11e9-bff2-0050568e4dbe"
   ```
   <br/>
4. Displays all of the EBR operations with filter set as volume.name:
   <br/>
   ```
   GET "/api/storage/snaplock/event-retention/operations?volume.name=SLCVOL"
   ```
   <br/>
### Examples
1. Applies an EBR policy on a specific path:
   <br/>
   ```
   POST "/api/storage/snaplock/event-retention/operations" '{"volume.name":"SLCVOL", "policy.name":"p1day", "path":"/dir1/file.txt"}'
   ```
   <br/>
2. Applies an EBR policy on the complete volume:
   <br/>
   ```
   POST "/api/storage/snaplock/event-retention/operations" '{"volume.name":"SLCVOL", "policy.name":"p1day", "path":"/"}'
   ```
   <br/>
### Example
<br/>
```
DELETE "/api/storage/snaplock/event-retention/operations/16842999"
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


__all__ = ["EbrOperation", "EbrOperationSchema"]
__pdoc__ = {
    "EbrOperationSchema.resource": False,
    "EbrOperationSchema.opts": False,
}


class EbrOperationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EbrOperation object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ebr_operation."""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" Operation ID

Example: 16842759"""

    num_files_failed = Size(
        data_key="num_files_failed",
        allow_none=True,
    )
    r""" Specifies the number of files on which the application of EBR policy failed.

Example: 0"""

    num_files_processed = Size(
        data_key="num_files_processed",
        allow_none=True,
    )
    r""" Specifies the number of files on which EBR policy was applied successfully.

Example: 50"""

    num_files_skipped = Size(
        data_key="num_files_skipped",
        allow_none=True,
    )
    r""" Specifies the number of files on which the application of EBR policy was skipped.

Example: 2"""

    num_inodes_ignored = Size(
        data_key="num_inodes_ignored",
        allow_none=True,
    )
    r""" Specifies the number of inodes on which the application of EBR policy was not attempted because they were not regular files.

Example: 2"""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" The path for the EBR operation. Specifies the path relative to the output volume root, of the form "/path". The path can be path to a file or a directory.

Example: /dir1/file"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.snaplock_retention_policy_operation.SnaplockRetentionPolicyOperationSchema", data_key="policy", unknown=EXCLUDE, allow_none=True)
    r""" The policy field of the ebr_operation."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['unknown', 'in_progress', 'failed', 'aborting', 'completed']),
        allow_none=True,
    )
    r""" Specifies the operation status of an EBR operation.

Valid choices:

* unknown
* in_progress
* failed
* aborting
* completed"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ebr_operation."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the ebr_operation."""

    @property
    def resource(self):
        return EbrOperation

    gettable_fields = [
        "links",
        "id",
        "num_files_failed",
        "num_files_processed",
        "num_files_skipped",
        "num_inodes_ignored",
        "path",
        "policy",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,id,num_files_failed,num_files_processed,num_files_skipped,num_inodes_ignored,path,policy,state,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "path",
        "policy",
        "volume.name",
        "volume.uuid",
    ]
    """path,policy,volume.name,volume.uuid,"""

class EbrOperation(Resource):
    """Allows interaction with EbrOperation objects on the host"""

    _schema = EbrOperationSchema
    _path = "/api/storage/snaplock/event-retention/operations"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of all EBR operations.
### Related ONTAP commands
* `snaplock event-retention show`
### Learn more
* [`DOC /storage/snaplock/event-retention/operations`](#docs-snaplock-storage_snaplock_event-retention_operations)
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
        """Returns a count of all EbrOperation resources that match the provided query"""
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
        """Returns a list of RawResources that represent EbrOperation resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["EbrOperation"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["EbrOperation"], NetAppResponse]:
        r"""Start an EBR operation. This operation applies an EBR policy to a specific volume or to a path within the volume.
### Required properties
* `path` - Path of the file.
* `policy.name` - Name of the EBR policy.
  Either volume.name or volume.uuid must be specified when applying EBR policy to the volume or a path within the volume.
* `volume.name` - Volume name.
* `volume.uuid` - Volume uuid.
### Related ONTAP commands
* `snaplock event-retention apply`
### Learn more
* [`DOC /storage/snaplock/event-retention/operations`](#docs-snaplock-storage_snaplock_event-retention_operations)
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
        records: Iterable["EbrOperation"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Aborts an ongoing EBR operation.
### Related ONTAP commands
* `snaplock event-retention abort`
### Learn more
* [`DOC /storage/snaplock/event-retention/operations`](#docs-snaplock-storage_snaplock_event-retention_operations)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of all EBR operations.
### Related ONTAP commands
* `snaplock event-retention show`
### Learn more
* [`DOC /storage/snaplock/event-retention/operations`](#docs-snaplock-storage_snaplock_event-retention_operations)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a list of attributes for an EBR operation.
### Related ONTAP commands
* `snaplock event-retention show`
### Learn more
* [`DOC /storage/snaplock/event-retention/operations`](#docs-snaplock-storage_snaplock_event-retention_operations)
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
        r"""Start an EBR operation. This operation applies an EBR policy to a specific volume or to a path within the volume.
### Required properties
* `path` - Path of the file.
* `policy.name` - Name of the EBR policy.
  Either volume.name or volume.uuid must be specified when applying EBR policy to the volume or a path within the volume.
* `volume.name` - Volume name.
* `volume.uuid` - Volume uuid.
### Related ONTAP commands
* `snaplock event-retention apply`
### Learn more
* [`DOC /storage/snaplock/event-retention/operations`](#docs-snaplock-storage_snaplock_event-retention_operations)
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
        r"""Aborts an ongoing EBR operation.
### Related ONTAP commands
* `snaplock event-retention abort`
### Learn more
* [`DOC /storage/snaplock/event-retention/operations`](#docs-snaplock-storage_snaplock_event-retention_operations)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


