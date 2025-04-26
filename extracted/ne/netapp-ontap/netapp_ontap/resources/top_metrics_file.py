r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve a list of files with the most I/O activity for a specified volume, within the past several seconds. Use the `top_metric` parameter to specify which type of I/O activity to filter for. This API is used to provide insight into I/O activity and supports ordering by I/O activity types, namely `iops` or `throughput` metrics. This API also supports only returning one I/O activity type per request.
## Approximate accounting and error bars
When too many files have recent activity, some files might be dropped from the list. In this situation, the spread of values in the `error` field increases, indicating that there are larger error bars on the value for `iops` or `throughput`. As the list becomes increasingly more approximate due to dropped entries, some of the files that would have otherwise been included might not be present in the final list returned by the API.
## Failure to return list of files with most I/O activity
The API can sometimes fail to return the list of files with the most I/O activity, due to the following reasons:

* The volume does not have the activity tracking feature enabled.
* The volume has not had any recent NFS/CIFS client traffic.
* The NFS/CIFS client operations are being served by the client-side filesystem cache.
* The NFS/CIFS client operations are being buffered by the client operating system.
* On rare occasions, the incoming traffic pattern is not suitable to obtain the list of files with the most I/O activity.
## Failure to return pathnames
The API can sometimes fail to obtain the filesystem pathnames for certain files, either due to internal transient errors or if those files have been recently deleted.
In such cases, instead of the pathname, the API will return "{<volume_instance_uuid>.<fileid>}" for that file.
## Retrieve a list of the files with the most I/O activity
For a report on the files with the most I/O activity returned in descending order, specify the I/O activity type you want to filter for by passing the `iops` or `throughput` property into the top_metric parameter. If the I/O activity type is not specified, by default the API returns a list of the files with the greatest number of the average read operations per second. The current maximum number of files returned by the API for an I/O activity type is 25.

* GET   /api/storage/volumes/{volume.uuid}/top-metrics/files
## Examples
### Retrieving a list of the files with the greatest average number of write bytes received per second:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsFile.get_collection(
                "{volume.uuid}", top_metric="throughput.write"
            )
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    TopMetricsFile(
        {
            "volume": {"name": "fv"},
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/4ec6d1ea-d5da-11eb-a25f-005056ac0f77/files/d5%2Ff5?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/0ba74c3e-d5ca-11eb-8fbb-005056ac0f77"
                    }
                },
                "uuid": "0ba74c3e-d5ca-11eb-8fbb-005056ac0f77",
            },
            "throughput": {
                "error": {"lower_bound": 24, "upper_bound": 29},
                "write": 24,
            },
            "path": "/d5/f5",
        }
    ),
    TopMetricsFile(
        {
            "volume": {"name": "fv"},
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/4ec6d1ea-d5da-11eb-a25f-005056ac0f77/files/d6%2Ff6?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/0ba74c3e-d5ca-11eb-8fbb-005056ac0f77"
                    }
                },
                "uuid": "0ba74c3e-d5ca-11eb-8fbb-005056ac0f77",
            },
            "throughput": {
                "error": {"lower_bound": 12, "upper_bound": 22},
                "write": 12,
            },
            "path": "/d6/f6",
        }
    ),
    TopMetricsFile(
        {
            "volume": {"name": "fv"},
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/4ec6d1ea-d5da-11eb-a25f-005056ac0f77/files/d3%2Ff3?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/0ba74c3e-d5ca-11eb-8fbb-005056ac0f77"
                    }
                },
                "uuid": "0ba74c3e-d5ca-11eb-8fbb-005056ac0f77",
            },
            "throughput": {"error": {"lower_bound": 8, "upper_bound": 10}, "write": 8},
            "path": "/d3/f3",
        }
    ),
]

```
</div>
</div>

### Retrieving a list of the files with the most traffic with failure in obtaining the pathnames for the files:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsFile.get_collection(
                "{volume.uuid}", top_metric="throughput.write"
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    TopMetricsFile(
        {
            "volume": {"name": "fv"},
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/0ba74c3e-d5ca-11eb-8fbb-005056ac0f77"
                    }
                },
                "uuid": "0ba74c3e-d5ca-11eb-8fbb-005056ac0f77",
            },
            "throughput": {
                "error": {"lower_bound": 24, "upper_bound": 29},
                "write": 24,
            },
            "path": "{4ec6d1ea-d5da-11eb-a25f-005056ac0f77:1232}",
        }
    ),
    TopMetricsFile(
        {
            "volume": {"name": "fv"},
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/0ba74c3e-d5ca-11eb-8fbb-005056ac0f77"
                    }
                },
                "uuid": "0ba74c3e-d5ca-11eb-8fbb-005056ac0f77",
            },
            "throughput": {
                "error": {"lower_bound": 12, "upper_bound": 22},
                "write": 12,
            },
            "path": "{4ec6d1ea-d5da-11eb-a25f-005056ac0f77:6754}",
        }
    ),
    TopMetricsFile(
        {
            "volume": {"name": "fv"},
            "svm": {
                "name": "vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/0ba74c3e-d5ca-11eb-8fbb-005056ac0f77"
                    }
                },
                "uuid": "0ba74c3e-d5ca-11eb-8fbb-005056ac0f77",
            },
            "throughput": {"error": {"lower_bound": 8, "upper_bound": 10}, "write": 8},
            "path": "{4ec6d1ea-d5da-11eb-a25f-005056ac0f77:8654}",
        }
    ),
]

```
</div>
</div>

## Example showing the behavior of the API when there is no read/write traffic:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsFile.get_collection(
                "{volume.uuid}", top_metric="throughput.write"
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[]

```
</div>
</div>
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


__all__ = ["TopMetricsFile", "TopMetricsFileSchema"]
__pdoc__ = {
    "TopMetricsFileSchema.resource": False,
    "TopMetricsFileSchema.opts": False,
}


class TopMetricsFileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsFile object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.file_info_links.FileInfoLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the top_metrics_file."""

    iops = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_file_iops.TopMetricsFileIopsSchema", data_key="iops", unknown=EXCLUDE, allow_none=True)
    r""" The iops field of the top_metrics_file."""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Path of the file.

Example: /dir_abc/dir_123/file_1"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the top_metrics_file."""

    throughput = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_file_throughput.TopMetricsFileThroughputSchema", data_key="throughput", unknown=EXCLUDE, allow_none=True)
    r""" The throughput field of the top_metrics_file."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the top_metrics_file."""

    @property
    def resource(self):
        return TopMetricsFile

    gettable_fields = [
        "links",
        "iops",
        "path",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "throughput",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,iops,path,svm.links,svm.name,svm.uuid,throughput,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "iops",
        "throughput",
    ]
    """iops,throughput,"""

    postable_fields = [
        "iops",
        "throughput",
    ]
    """iops,throughput,"""

class TopMetricsFile(Resource):
    r""" Information about a file's IO activity. """

    _schema = TopMetricsFileSchema
    _path = "/api/storage/volumes/{volume[uuid]}/top-metrics/files"
    _keys = ["volume.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of files with the most I/O activity.
### Platform Specifics
* **Unified ONTAP**: GET must be used to retrieve a list of files with the most I/O activity.
* **ASA**: GET is not supported.

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/top-metrics/files`](#docs-storage-storage_volumes_{volume.uuid}_top-metrics_files)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all TopMetricsFile resources that match the provided query"""
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
        """Returns a list of RawResources that represent TopMetricsFile resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of files with the most I/O activity.
### Platform Specifics
* **Unified ONTAP**: GET must be used to retrieve a list of files with the most I/O activity.
* **ASA**: GET is not supported.

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/top-metrics/files`](#docs-storage-storage_volumes_{volume.uuid}_top-metrics_files)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






