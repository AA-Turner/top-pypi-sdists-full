r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Use this API to view key information about files and volumes, including the file type (regular, WORM, or WORM appendable), the volume expiration date, and so on."""

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


__all__ = ["SnaplockFileFingerprint", "SnaplockFileFingerprintSchema"]
__pdoc__ = {
    "SnaplockFileFingerprintSchema.resource": False,
    "SnaplockFileFingerprintSchema.opts": False,
}


class SnaplockFileFingerprintSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockFileFingerprint object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snaplock_file_fingerprint."""

    algorithm = marshmallow_fields.Str(
        data_key="algorithm",
        validate=enum_validation(['md5', 'sha256']),
        allow_none=True,
    )
    r""" The digest algorithm which is used for the fingerprint computation

Valid choices:

* md5
* sha256"""

    data_fingerprint = marshmallow_fields.Str(
        data_key="data_fingerprint",
        allow_none=True,
    )
    r""" The digest value of data of the file. The fingerprint is base64 encoded. This field is not included if the scope is metadata-only.

Example: MOFJVevxNSJm3C/4Bn5oEEYH51CrudOzZYK4r5Cfy1g="""

    file_size = Size(
        data_key="file_size",
        allow_none=True,
    )
    r""" The size of the file in bytes.

Example: 1048576"""

    file_type = marshmallow_fields.Str(
        data_key="file_type",
        validate=enum_validation(['worm', 'worm_appendable', 'worm_active_log', 'worm_log', 'regular']),
        allow_none=True,
    )
    r""" The type of the file.

Valid choices:

* worm
* worm_appendable
* worm_active_log
* worm_log
* regular"""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" A unique identifier for the fingerprint operation

Example: 17039367"""

    metadata_fingerprint = marshmallow_fields.Str(
        data_key="metadata_fingerprint",
        allow_none=True,
    )
    r""" The digest value of metadata of the file. The metadata fingerprint is calculated for file size, file ctime, file mtime, file crtime, file retention time, file uid, file gid, and file type. The fingerprint is base64 encoded. This field is not included if the scope is data-only.

Example: 8iMjqJXiNcqgXT5XuRhLiEwIrJEihDmwS0hrexnjgmc="""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Specifies the path on which file fingerprint operation is running or has completed. Specifies the path relative to the output volume root, of the form "/path". The path can be path to a file or a directory.

Example: /homedir/dir1"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['data_and_metadata', 'data_only', 'metadata_only']),
        allow_none=True,
    )
    r""" The scope of the file which is used for the fingerprint computation

Valid choices:

* data_and_metadata
* data_only
* metadata_only"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['in_progress', 'failed', 'aborting', 'completed']),
        allow_none=True,
    )
    r""" Specifies the status of fingerprint operation.

Valid choices:

* in_progress
* failed
* aborting
* completed"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the snaplock_file_fingerprint."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the snaplock_file_fingerprint."""

    @property
    def resource(self):
        return SnaplockFileFingerprint

    gettable_fields = [
        "links",
        "algorithm",
        "data_fingerprint",
        "file_size",
        "file_type",
        "id",
        "metadata_fingerprint",
        "path",
        "scope",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,algorithm,data_fingerprint,file_size,file_type,id,metadata_fingerprint,path,scope,state,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "algorithm",
        "path",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """algorithm,path,svm.name,svm.uuid,volume.name,volume.uuid,"""

class SnaplockFileFingerprint(Resource):
    """Allows interaction with SnaplockFileFingerprint objects on the host"""

    _schema = SnaplockFileFingerprintSchema
    _path = "/api/storage/snaplock/file-fingerprints"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of all the fingerprint operations of the specified SVM and volume.
### Related ONTAP commands
* `volume file fingerprint show`
### Example
<br/>
```
GET "/api/storage/snaplock/file-fingerprints/?svm.uuid=23940494-3f3a-11e9-8675-0050568e8f89&volume.uuid=36cdb58c-3f3a-11e9-8675-0050568e8f89"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/file-fingerprints`](#docs-snaplock-storage_snaplock_file-fingerprints)
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
        """Returns a count of all SnaplockFileFingerprint resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnaplockFileFingerprint resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnaplockFileFingerprint"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnaplockFileFingerprint"], NetAppResponse]:
        r"""Creates a fingerprint computation session on the file and returns a session-id. This session-id is a unique identifier that you can use to retrieve the progress of an ongoing fingerprint operation. When the operation is complete, you can use the session-id to retrieve the complete fingerprint output for the file .
### Required properties
* `svm.uuid` or `svm.name` - Name or UUID of the SVM.
* `volume.name` or `volume.uuid` - Name or UUID of the volume.
* `path` - Path of the file.
### Default property values
If not specified in POST, the follow default property values are assigned:
* `algorithm` - _sha256_
### Related ONTAP commands
* `volume file fingerprint start`
### Example
<br/>
```
POST "/api/storage/snaplock/file-fingerprints" '{"svm":{"uuid":"23940494-3f3a-11e9-8675-0050568e8f89"},"volume": {"uuid":"26cdb58c-3f3a-11e9-8675-0050568e8f89"},"path":"/vol/a1.txt","algorithm":"md5"}'
```
<br/>
### Learn more
* [`DOC /storage/snaplock/file-fingerprints`](#docs-snaplock-storage_snaplock_file-fingerprints)
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
        records: Iterable["SnaplockFileFingerprint"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Aborts an in-progress fingerprint operation. This API takes session-id as input and aborts the fingerprint operation that is associated with the specified session-id.
### Related ONTAP commands
* `volume file fingerprint abort`
### Learn more
* [`DOC /storage/snaplock/file-fingerprints`](#docs-snaplock-storage_snaplock_file-fingerprints)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of all the fingerprint operations of the specified SVM and volume.
### Related ONTAP commands
* `volume file fingerprint show`
### Example
<br/>
```
GET "/api/storage/snaplock/file-fingerprints/?svm.uuid=23940494-3f3a-11e9-8675-0050568e8f89&volume.uuid=36cdb58c-3f3a-11e9-8675-0050568e8f89"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/file-fingerprints`](#docs-snaplock-storage_snaplock_file-fingerprints)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the file fingerprint information for a specific session ID.
### Related ONTAP commands
* `volume file fingerprint dump`
### Learn more
* [`DOC /storage/snaplock/file-fingerprints`](#docs-snaplock-storage_snaplock_file-fingerprints)
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
        r"""Creates a fingerprint computation session on the file and returns a session-id. This session-id is a unique identifier that you can use to retrieve the progress of an ongoing fingerprint operation. When the operation is complete, you can use the session-id to retrieve the complete fingerprint output for the file .
### Required properties
* `svm.uuid` or `svm.name` - Name or UUID of the SVM.
* `volume.name` or `volume.uuid` - Name or UUID of the volume.
* `path` - Path of the file.
### Default property values
If not specified in POST, the follow default property values are assigned:
* `algorithm` - _sha256_
### Related ONTAP commands
* `volume file fingerprint start`
### Example
<br/>
```
POST "/api/storage/snaplock/file-fingerprints" '{"svm":{"uuid":"23940494-3f3a-11e9-8675-0050568e8f89"},"volume": {"uuid":"26cdb58c-3f3a-11e9-8675-0050568e8f89"},"path":"/vol/a1.txt","algorithm":"md5"}'
```
<br/>
### Learn more
* [`DOC /storage/snaplock/file-fingerprints`](#docs-snaplock-storage_snaplock_file-fingerprints)
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
        r"""Aborts an in-progress fingerprint operation. This API takes session-id as input and aborts the fingerprint operation that is associated with the specified session-id.
### Related ONTAP commands
* `volume file fingerprint abort`
### Learn more
* [`DOC /storage/snaplock/file-fingerprints`](#docs-snaplock-storage_snaplock_file-fingerprints)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


