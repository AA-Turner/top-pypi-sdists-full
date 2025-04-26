r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use these API's to create file clones, retrieve split status and manage split loads. These endpoints are used for cloning files within a volume, without taking much of extra space. Child and parent clones shares the unchanged blocks of data. REST support for sis clone creation for Flex Group volumes is blocked.<br/>
A file clone split operation detach child clone from its parent. Split operations use space. To ensure that file clone create operation is not affected by split, file clone tokens are use to reserve space. API endpoints can be used to update the validity and space reserved by token.<br/>
## File clone APIs
The following APIs are used to perform the following operations:

* POST      /api/storage/file/clone
*  GET      /api/storage/file/clone/split-status
* PATCH     /api/storage/file/clone/split-loads/{node.uuid}
*  GET      /api/storage/file/clone/split-loads/{node.uuid}
*  GET      /api/storage/file/clone/split-loads
*  GET      /api/storage/file/clone/tokens/
* DELETE    /api/storage/file/clone/tokens/{node.uuid}/{token.uuid}
* PATCH     /api/storage/file/clone/tokens/{node.uuid}/{token.uuid}"""

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


__all__ = ["FileClone", "FileCloneSchema"]
__pdoc__ = {
    "FileCloneSchema.resource": False,
    "FileCloneSchema.opts": False,
}


class FileCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FileClone object"""

    autodelete = marshmallow_fields.Boolean(
        data_key="autodelete",
        allow_none=True,
    )
    r""" Mark clone file for auto deletion."""

    destination_path = marshmallow_fields.Str(
        data_key="destination_path",
        allow_none=True,
    )
    r""" Relative path of the clone/destination file in the volume.

Example: dest_file1 or dir1/dest_file2"""

    is_backup = marshmallow_fields.Boolean(
        data_key="is_backup",
        allow_none=True,
    )
    r""" Mark clone file for backup.

Example: false"""

    overwrite_destination = marshmallow_fields.Boolean(
        data_key="overwrite_destination",
        allow_none=True,
    )
    r""" Destination file gets overwritten."""

    range = marshmallow_fields.List(marshmallow_fields.Str, data_key="range", allow_none=True)
    r""" List of block ranges for sub-file cloning in the format "source-file-block-number:destination-file-block-number:block-count"

Example: ["0:0:2"]"""

    source_path = marshmallow_fields.Str(
        data_key="source_path",
        allow_none=True,
    )
    r""" Relative path of the source file in the volume.

Example: src_file1 or dir1/src_file2 or ./.snapshot/snap1/src_file3"""

    token_uuid = marshmallow_fields.Str(
        data_key="token_uuid",
        allow_none=True,
    )
    r""" UUID of existing clone token with reserved split load."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the file_clone."""

    @property
    def resource(self):
        return FileClone

    gettable_fields = [
        "autodelete",
        "destination_path",
        "is_backup",
        "overwrite_destination",
        "range",
        "source_path",
        "token_uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """autodelete,destination_path,is_backup,overwrite_destination,range,source_path,token_uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "autodelete",
        "destination_path",
        "is_backup",
        "overwrite_destination",
        "range",
        "source_path",
        "token_uuid",
        "volume.name",
        "volume.uuid",
    ]
    """autodelete,destination_path,is_backup,overwrite_destination,range,source_path,token_uuid,volume.name,volume.uuid,"""

    postable_fields = [
        "autodelete",
        "destination_path",
        "is_backup",
        "overwrite_destination",
        "range",
        "source_path",
        "token_uuid",
        "volume.name",
        "volume.uuid",
    ]
    """autodelete,destination_path,is_backup,overwrite_destination,range,source_path,token_uuid,volume.name,volume.uuid,"""

class FileClone(Resource):
    r""" File clone """

    _schema = FileCloneSchema
    _path = "/api/storage/file/clone"



    @classmethod
    def post_collection(
        cls,
        records: Iterable["FileClone"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FileClone"], NetAppResponse]:
        r"""Creates a clone of the file.
### Required Properties
* `source_path`
* `destination_path`
* `volume.uuid` - Instance UUID of the volume in which to create clone.
### Optional Properties
* `range` -  Required only in the case of a sub file clone.
* `autodelete` - Marks a cloned file for auto deletion.
* `is_backup` - Cloned file is used as a backup.
* `volume.name` - Name of the volume in which to create the clone.
* `token_uuid` - UUID of existing clone token.
### Related Ontap commands
* `volume file clone create`
### Creating file clones
The POST operation is used to create file clones with the specified attributes in the body. Set the `volume.uuid` to identify the volume.
Set `source_path` and `destination_path` to identify the file path of the original and copied file. For a full file clone, the new file is created using `destination_path`.
For a sub file clone, set `range` in the format source-file-block-number:destination-file-block-number:block-count. The API returns an error for the following overlapping conditions: (a) if the source and destination files are the same and if any of the source ranges  overlap with any of the destination ranges. (b) if any of the source ranges overlap amongst themselves. (c) if any of the destination ranges overlap amongst themselves. If not provided, full file cloning is assumed.<br/>
If set to `autodelete`, the cloned file is deleted when the volumes are full.<br\>
```
# The API:
curl -X POST "https://<mgmt_ip>/api/storage/file/clone" -H "accept: application/hal+json" -d '{"volume": {"name": "vol1",  "uuid": "40e0fdc5-c28f-11eb-8270-005056bbeb0b"}, "source_path": "f1", "destination_path": "f2_c1"}'
# The response:
{
  "job": {
    "uuid": "0d025fd9-c4dc-11eb-adb5-005056bbeb0b",
    "_links": {
       "self": {
         "href": "/api/cluster/jobs/0d025fd9-c4dc-11eb-adb5-005056bbeb0b"
       }
    }
  }
}
```
### Learn More
* [`DOC /storage/file/clone`]

### Learn more
* [`DOC /storage/file/clone`](#docs-storage-storage_file_clone)"""
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
        r"""Creates a clone of the file.
### Required Properties
* `source_path`
* `destination_path`
* `volume.uuid` - Instance UUID of the volume in which to create clone.
### Optional Properties
* `range` -  Required only in the case of a sub file clone.
* `autodelete` - Marks a cloned file for auto deletion.
* `is_backup` - Cloned file is used as a backup.
* `volume.name` - Name of the volume in which to create the clone.
* `token_uuid` - UUID of existing clone token.
### Related Ontap commands
* `volume file clone create`
### Creating file clones
The POST operation is used to create file clones with the specified attributes in the body. Set the `volume.uuid` to identify the volume.
Set `source_path` and `destination_path` to identify the file path of the original and copied file. For a full file clone, the new file is created using `destination_path`.
For a sub file clone, set `range` in the format source-file-block-number:destination-file-block-number:block-count. The API returns an error for the following overlapping conditions: (a) if the source and destination files are the same and if any of the source ranges  overlap with any of the destination ranges. (b) if any of the source ranges overlap amongst themselves. (c) if any of the destination ranges overlap amongst themselves. If not provided, full file cloning is assumed.<br/>
If set to `autodelete`, the cloned file is deleted when the volumes are full.<br\>
```
# The API:
curl -X POST "https://<mgmt_ip>/api/storage/file/clone" -H "accept: application/hal+json" -d '{"volume": {"name": "vol1",  "uuid": "40e0fdc5-c28f-11eb-8270-005056bbeb0b"}, "source_path": "f1", "destination_path": "f2_c1"}'
# The response:
{
  "job": {
    "uuid": "0d025fd9-c4dc-11eb-adb5-005056bbeb0b",
    "_links": {
       "self": {
         "href": "/api/cluster/jobs/0d025fd9-c4dc-11eb-adb5-005056bbeb0b"
       }
    }
  }
}
```
### Learn More
* [`DOC /storage/file/clone`]

### Learn more
* [`DOC /storage/file/clone`](#docs-storage-storage_file_clone)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




