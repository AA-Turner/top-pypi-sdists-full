r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to restore a directory from a volume snapshot without having to use data copy. The directory in the snapshot contains sub-directories and files.<br/>
When a directory from a volume snapshot is restored, all the directory entries (dentries) in the source should remain as they are (except for the junction path inodes). The dentries in the restored directory contain new inodes which are in the AFS (Active File System).<br/>
The newly created inodes in the AFS have the same attributes as those in the source snapshot.<br/>
## Directory restore API
The following API is used to perform the following operations:

* POST      /api/storage/directory-restore"""

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


__all__ = ["DirectoryRestore", "DirectoryRestoreSchema"]
__pdoc__ = {
    "DirectoryRestoreSchema.resource": False,
    "DirectoryRestoreSchema.opts": False,
}


class DirectoryRestoreSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DirectoryRestore object"""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Source from where the directory is restored.

Example: src_file1 or dir1/src_file2 or ./.snapshot/snap1/src_file3"""

    restore_path = marshmallow_fields.Str(
        data_key="restore_path",
        allow_none=True,
    )
    r""" Destination directory where the new directory tree is created.

Example: dest_file1 or dir1/dest_file2"""

    snapshot = marshmallow_fields.Str(
        data_key="snapshot",
        allow_none=True,
    )
    r""" Name of the volume snapshot from which the directory is restored."""

    volume = marshmallow_fields.Str(
        data_key="volume",
        allow_none=True,
    )
    r""" Name of the volume from which the snapshot is used for directory restore."""

    vserver = marshmallow_fields.Str(
        data_key="vserver",
        allow_none=True,
    )
    r""" Name of the SVM."""

    @property
    def resource(self):
        return DirectoryRestore

    gettable_fields = [
        "path",
        "restore_path",
        "snapshot",
        "volume",
        "vserver",
    ]
    """path,restore_path,snapshot,volume,vserver,"""

    patchable_fields = [
        "path",
        "restore_path",
        "snapshot",
        "volume",
        "vserver",
    ]
    """path,restore_path,snapshot,volume,vserver,"""

    postable_fields = [
        "path",
        "restore_path",
        "snapshot",
        "volume",
        "vserver",
    ]
    """path,restore_path,snapshot,volume,vserver,"""

class DirectoryRestore(Resource):
    r""" Restores a directory from a volume snapshot. """

    _schema = DirectoryRestoreSchema
    _path = "/api/storage/directory-restore"



    @classmethod
    def post_collection(
        cls,
        records: Iterable["DirectoryRestore"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["DirectoryRestore"], NetAppResponse]:
        r"""Restores the source directory from the volume snapshot on the destination directory.
### Required Properties
* `vserver`
* `volume.name`
* `snapshot.name`
* `source_path`
* `restore_path`
### Related ONTAP commands
* `volume snapshot directory-restore start`
```
# The API:
/api/storage/directory-restore
# The call:
curl -X POST "https://<mgmt_ip>/api/storage/directory-restore" -H "accept: application/hal+json" -d '{"svm":"vs1", "volume": "vol1", "snapshot": "sp1", "path": "/aaaa", "restore_path": "/bbbb"}'
# The response:
{
  "job": {
    "uuid": "23b5ff3a-4743-11ee-a08d-005056bb9d00",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/23b5ff3a-4743-11ee-a08d-005056bb9d00"
      }
    }
  }
}
```

### Learn more
* [`DOC /storage/directory-restore`](#docs-storage-storage_directory-restore)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)




    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Restores the source directory from the volume snapshot on the destination directory.
### Required Properties
* `vserver`
* `volume.name`
* `snapshot.name`
* `source_path`
* `restore_path`
### Related ONTAP commands
* `volume snapshot directory-restore start`
```
# The API:
/api/storage/directory-restore
# The call:
curl -X POST "https://<mgmt_ip>/api/storage/directory-restore" -H "accept: application/hal+json" -d '{"svm":"vs1", "volume": "vol1", "snapshot": "sp1", "path": "/aaaa", "restore_path": "/bbbb"}'
# The response:
{
  "job": {
    "uuid": "23b5ff3a-4743-11ee-a08d-005056bb9d00",
    "_links": {
      "self": {
        "href": "/api/cluster/jobs/23b5ff3a-4743-11ee-a08d-005056bb9d00"
      }
    }
  }
}
```

### Learn more
* [`DOC /storage/directory-restore`](#docs-storage-storage_directory-restore)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




