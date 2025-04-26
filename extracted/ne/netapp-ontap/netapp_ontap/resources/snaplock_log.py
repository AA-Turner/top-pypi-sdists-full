r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

The SnapLock log volume can be a SnapLock Compliance volume or SnapLock Enterprise volume. The SnapLock log infrastructure creates directories and files in this volume to store the SnapLock log records. The directory named "snaplock_log" is created under the root. There are three subdirectories created under the "snaplock_log" directory. They are "privileged_delete_logs", "system_logs" and "legal_hold_logs". The log files are created and populated under these subdirectories when respective SnapLock operations are initiated. The maximum log size specifies the maximum size of a log file that stores SnapLock log records. When the file reaches this size, the log infrastructure archives it and creates a new log file. An active log file has the suffix "-present" in the name. When a file is archived, it is renamed such that the suffix is replaced with the date of archival. The default retention period is the length of time the log file is retained, if the SnapLock log records that are stored in the file do not carry any retention period.
### Examples
1. Verifies that the audit log is configured for the specified SVM:
   <br/>
   ```
   GET "/api/storage/snaplock/audit-logs/?svm.name=VS0"
   ```
   <br/>
2. Verifies that the specified volume is an audit log volume:
   <br/>
   ```
   GET "/api/storage/snaplock/audit-logs/?log_volume.volume.name=VS0_ALOG"
   ```
   <br/>
### Examples
1. Creates a SnapLock log configuration by providing SVM name:
   <br/>
   ```
   POST "/api/storage/snaplock/audit-logs" '{"svm": {"name":"VS3"}, "log_volume": { "volume": { "name":"VS3_ALOG"}, "max_log_size":"20971520", "retention_period":"P30Y" }}'
   ```
   <br/>
2. Creates a SnapLock log configuration by providing SVM UUID:
   <br/>
   ```
   POST "/api/storage/snaplock/audit-logs" '{"svm": {"uuid":"bc744cc7-296d-11e9-a26f-0050568e5b05"}, "log_volume": { "volume": { "name":"VS3_ALOG"}, "max_log_size":"20971520", "retention_period":"P30Y" }}'
   ```
   <br/>
3. Creates a SnapLock log configuration without specifying a retention period:
   <br/>
   ```
   POST "/api/storage/snaplock/audit-logs" '{"svm": {"name":"VS3"}, "log_volume": {"volume": {"name":"VS3_ALOG"}}}'
   ```
   <br/>
### Examples
1. Updates the audit log volume:
   <br/>
   ```
   PATCH "/api/storage/snaplock/audit-logs/bc744cc7-296d-11e9-a26f-0050568e5b05" '{"log_volume":{"volume":{"name":"VS4_ALOG_NEW"}}}'
   ```
   <br/>
2. Updates the maximum size of the log file and the retention period:
   <br/>
   ```
   PATCH "/api/storage/snaplock/audit-logs/420cac7a-296a-11e9-a26f-0050568e5b05" '{"log_volume":{"max_log_size":"20971520", "retention_period":"P1Y"}}'
   ```
   <br/>
3. Archives all of the audit log files:
   <br/>
   ```
   PATCH "/api/storage/snaplock/audit-logs/c7e4fa7d-2968-11e9-a26f-0050568e5b05" '{"log_archive":{"archive":"true"}}'
   ```
   <br/>
4. Archives the specified audit log file:
   <br/>
   ```
   PATCH "/api/storage/snaplock/audit-logs/c7e4fa7d-2968-11e9-a26f-0050568e5b05" '{"log_archive":{"archive":"true","base_name":"privileged_delete"}}'
   ```"""

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


__all__ = ["SnaplockLog", "SnaplockLogSchema"]
__pdoc__ = {
    "SnaplockLogSchema.resource": False,
    "SnaplockLogSchema.opts": False,
}


class SnaplockLogSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLog object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snaplock_log."""

    log_archive = marshmallow_fields.Nested("netapp_ontap.models.snaplock_log_archive.SnaplockLogArchiveSchema", data_key="log_archive", unknown=EXCLUDE, allow_none=True)
    r""" The log_archive field of the snaplock_log."""

    log_files = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.snaplock_log_file.SnaplockLogFileSchema", unknown=EXCLUDE, allow_none=True), data_key="log_files", allow_none=True)
    r""" The log_files field of the snaplock_log."""

    log_volume = marshmallow_fields.Nested("netapp_ontap.models.snaplock_log_volume.SnaplockLogVolumeSchema", data_key="log_volume", unknown=EXCLUDE, allow_none=True)
    r""" The log_volume field of the snaplock_log."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the snaplock_log."""

    @property
    def resource(self):
        return SnaplockLog

    gettable_fields = [
        "links",
        "log_archive",
        "log_files",
        "log_volume",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,log_archive,log_files,log_volume,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "log_archive",
        "log_volume",
    ]
    """log_archive,log_volume,"""

    postable_fields = [
        "log_volume",
        "svm.name",
        "svm.uuid",
    ]
    """log_volume,svm.name,svm.uuid,"""

class SnaplockLog(Resource):
    """Allows interaction with SnaplockLog objects on the host"""

    _schema = SnaplockLogSchema
    _path = "/api/storage/snaplock/audit-logs"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of SVMs configured with audit log volumes.
### Related ONTAP commands
* `snaplock log show`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
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
        """Returns a count of all SnaplockLog resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnaplockLog resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnaplockLog"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates one of the following:
  - the audit log volume,
  - the attributes of the audit log volume present, or
  - archive the current audit log files
### Related ONTAP commands
* `snaplock log modify`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnaplockLog"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnaplockLog"], NetAppResponse]:
        r"""Creates a SnapLock log configuration for an SVM. A SnapLock log configuration consists of a volume to store the log, the maximum size of the log file, and the default period of time for which the log file should be retained. The volume must be a Read-Write SnapLock volume of type Enterprise or Compliance. The input parameter retention_period expects the duration in ISO 8601 format.
### Required properties
* `svm.uuid` or `svm.name` - Name or UUID of the SVM.
* `log_volume.volume.name` or `log_volume.volume.uuid` - Name or UUID of audit log volume.
### Recommended optional properties
* `log_volume.max_log_size` - Max log file size.
* `log_volume.volume.retention_period` - Retention period of log file.
### Default property values
If not specified in POST, the following default property values are assigned:
* `log_volume.retention_period` - _P6M_
* `log_volume.max_log_size` - _10MB_
### Related ONTAP commands
* `snaplock log create`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
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
        records: Iterable["SnaplockLog"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Disassociates a SnapLock volume as the audit log volume for an SVM. This API closes all the active log files in the log volume and marks the volume as disabled for SnapLock logging.
### Related ONTAP commands
* `snaplock log delete`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of SVMs configured with audit log volumes.
### Related ONTAP commands
* `snaplock log show`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves SnapLock logs for the specified SVM.
### Related ONTAP commands
* `snaplock log show`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
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
        r"""Creates a SnapLock log configuration for an SVM. A SnapLock log configuration consists of a volume to store the log, the maximum size of the log file, and the default period of time for which the log file should be retained. The volume must be a Read-Write SnapLock volume of type Enterprise or Compliance. The input parameter retention_period expects the duration in ISO 8601 format.
### Required properties
* `svm.uuid` or `svm.name` - Name or UUID of the SVM.
* `log_volume.volume.name` or `log_volume.volume.uuid` - Name or UUID of audit log volume.
### Recommended optional properties
* `log_volume.max_log_size` - Max log file size.
* `log_volume.volume.retention_period` - Retention period of log file.
### Default property values
If not specified in POST, the following default property values are assigned:
* `log_volume.retention_period` - _P6M_
* `log_volume.max_log_size` - _10MB_
### Related ONTAP commands
* `snaplock log create`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
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
        r"""Updates one of the following:
  - the audit log volume,
  - the attributes of the audit log volume present, or
  - archive the current audit log files
### Related ONTAP commands
* `snaplock log modify`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
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
        r"""Disassociates a SnapLock volume as the audit log volume for an SVM. This API closes all the active log files in the log volume and marks the volume as disabled for SnapLock logging.
### Related ONTAP commands
* `snaplock log delete`
### Learn more
* [`DOC /storage/snaplock/audit-logs`](#docs-snaplock-storage_snaplock_audit-logs)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


