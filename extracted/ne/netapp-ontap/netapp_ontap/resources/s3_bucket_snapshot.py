r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 bucket snapshot is an image of the bucket as it exists at the time when the snapshot is created. <br/>
S3 bucket snapshots can be created using scheduled snapshot policies set on the bucket, or user requested snapshot creations. <br/>
S3 bucket snapshot APIs allow you to create, delete, and retrieve snapshots. <br/>
## Snapshot APIs
The following APIs are used to perform operations related to snapshots.

* POST      /api/protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots
* GET       /api/protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots
* GET       /api/protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots/{uuid}
* DELETE    /api/protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots/{uuid}
## Examples
### Creating an S3 bucket snapshot
The POST operation is used to create an S3 bucket snapshot with the specified name.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSnapshot("{svm.uuid}", "{s3_bucket.uuid}")
    resource.name = "ss1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
S3BucketSnapshot({"name": "ss1"})

```
</div>
</div>

### Retrieving S3 bucket snapshots
The GET operation is used to retrieve all S3 bucket snapshots for a specific bucket.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(S3BucketSnapshot.get_collection("{svm.uuid}", "{s3_bucket.uuid}")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    S3BucketSnapshot({"name": "ss1", "uuid": "20837456-3c8b-405a-aa3a-5300c048f87d"}),
    S3BucketSnapshot({"name": "ss2", "uuid": "c67cd056-d386-477a-8378-fcc06987bedf"}),
]

```
</div>
</div>

### Retrieving S3 bucket snapshots and all snapshot attributes
The GET operation is used to retrieve all S3 bucket snapshots for a specific bucket along with all the snapshot attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            S3BucketSnapshot.get_collection(
                "{svm.uuid}", "{s3_bucket.uuid}", fields="**"
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    S3BucketSnapshot(
        {
            "create_time": "2024-08-22T14:23:54-04:00",
            "name": "ss1",
            "uuid": "20837456-3c8b-405a-aa3a-5300c048f87d",
            "svm": {"uuid": "148b9bbd-58d8-11ef-b7ca-005056ae1130"},
        }
    ),
    S3BucketSnapshot(
        {
            "create_time": "2024-08-22T14:30:42-04:00",
            "name": "ss2",
            "uuid": "c67cd056-d386-477a-8378-fcc06987bedf",
            "svm": {"uuid": "148b9bbd-58d8-11ef-b7ca-005056ae1130"},
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of a specific S3 bucket snapshot
The GET operation is used to retrieve the attributes of a specific S3 bucket snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSnapshot("{svm.uuid}", "{s3_bucket.uuid}", uuid="{uuid}")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
S3BucketSnapshot(
    {
        "create_time": "2024-08-22T14:30:42-04:00",
        "name": "ss2",
        "uuid": "c67cd056-d386-477a-8378-fcc06987bedf",
        "svm": {"uuid": "148b9bbd-58d8-11ef-b7ca-005056ae1130"},
    }
)

```
</div>
</div>

### Deleting an S3 bucket snapshot
The DELETE operation is used to delete an S3 bucket snapshot.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSnapshot

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSnapshot("{svm.uuid}", "{s3_bucket.uuid}", uuid="{uuid}")
    resource.delete()

```
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


__all__ = ["S3BucketSnapshot", "S3BucketSnapshotSchema"]
__pdoc__ = {
    "S3BucketSnapshotSchema.resource": False,
    "S3BucketSnapshotSchema.opts": False,
}


class S3BucketSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSnapshot object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the s3_bucket_snapshot."""

    bucket_uuid = marshmallow_fields.Str(
        data_key="bucket_uuid",
        allow_none=True,
    )
    r""" The unique identifier of the bucket.

Example: 2aec8270-58e3-11ef-861e-005056ae1130"""

    create_time = ImpreciseDateTime(
        data_key="create_time",
        allow_none=True,
    )
    r""" Creation time of the snapshot. It is the storage unit access time when the snapshot was created.

Example: 2024-08-22T00:18:04.000+0000"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the snapshot. Snapshot names must start with a lowercase letter, a number, or a hyphen, must end with a lowercase letter or a number, and cannot exceed 30 characters.

Example: snap1"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_bucket_snapshot."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID of the snapshot in the bucket that uniquely identifies the snapshot in that bucket.

Example: 522b29a1-3b26-11e9-bd58-0050568ea321"""

    @property
    def resource(self):
        return S3BucketSnapshot

    gettable_fields = [
        "links",
        "bucket_uuid",
        "create_time",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,bucket_uuid,create_time,name,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
    ]
    """name,"""

class S3BucketSnapshot(Resource):
    r""" Information about an S3 bucket snapshot. """

    _schema = S3BucketSnapshotSchema
    _path = "/api/protocols/s3/services/{svm[uuid]}/buckets/{s3_bucket[uuid]}/snapshots"
    _keys = ["svm.uuid", "s3_bucket.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of S3 bucket snapshots.
### Related ONTAP commands
* `vserver object-store-server bucket snapshot show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets_{s3_bucket.uuid}_snapshots)
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
        """Returns a count of all S3BucketSnapshot resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3BucketSnapshot resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3BucketSnapshot"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3BucketSnapshot"], NetAppResponse]:
        r"""Creates an S3 bucket snapshot.
### Required properties
* `name` - Name of the S3 bucket snapshot to be created.
### Related ONTAP commands
* `vserver object-store-server bucket snapshot create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets_{s3_bucket.uuid}_snapshots)
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
        records: Iterable["S3BucketSnapshot"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes S3 bucket snapshot.
### Related ONTAP commands
* `vserver object-store-server bucket snapshot delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets_{s3_bucket.uuid}_snapshots)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of S3 bucket snapshots.
### Related ONTAP commands
* `vserver object-store-server bucket snapshot show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets_{s3_bucket.uuid}_snapshots)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of a specific S3 bucket snapshot.
### Related ONTAP commands
* `vserver object-store-server bucket snapshot show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets_{s3_bucket.uuid}_snapshots)
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
        r"""Creates an S3 bucket snapshot.
### Required properties
* `name` - Name of the S3 bucket snapshot to be created.
### Related ONTAP commands
* `vserver object-store-server bucket snapshot create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets_{s3_bucket.uuid}_snapshots)
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
        r"""Deletes S3 bucket snapshot.
### Related ONTAP commands
* `vserver object-store-server bucket snapshot delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets/{s3_bucket.uuid}/snapshots`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets_{s3_bucket.uuid}_snapshots)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


