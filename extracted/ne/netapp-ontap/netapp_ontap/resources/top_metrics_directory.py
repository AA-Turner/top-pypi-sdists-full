r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve a list of directories with the greatest value performance metric or capacity metric for a specified volume. Use the `top_metric` parameter to specify which type of metric to filter for. This API is used to provide insight into performance metrics, namely `iops` and `throughput`, or capacity metrics such as `non_recursive_bytes_used`. This API only supports returning one metric per request.
## Retrieve a list of the directories with the most I/O activity
For a report on the directories with the most I/O activity in the past several seconds returned in descending order, specify the performance metric type you want to filter for by passing the `iops` or `throughput` property into the top_metric parameter. If the metric type is not specified, by default the API returns a list of the directories with the greatest number of the average read operations per second. The current maximum number of directories returned by the API for a metric type is 25.
## Approximate accounting and error bars for the list of directories with the most I/O activity
When too many directories have recent activity, some directories might be dropped from the list. In this situation, the spread of values in the `error` field increases, indicating that there are larger error bars on the value for `iops` or `throughput`. As the list becomes increasingly more approximate due to dropped entries, some of the directories that would have otherwise been included might not be present in the final list returned by the API.
## Retrieve a list of the largest directories
For a report on the largest directories returned in descending order, specify the capacity metric by passing the `non_recursive_bytes_used` property into the top_metric parameter. If the metric type is not specified, by default the API returns a list of directories with the greatest number of average read operations per second. The current maximum number of directories returned by the API for a metric type is 25.
## Failure to return list of directories with most I/O activity
The API can sometimes fail to return the list of directories with the most I/O activity, due to the following reasons:

* The volume does not have the activity tracking feature enabled.
* The volume has not had any recent NFS/CIFS client traffic.
* The NFS/CIFS client operations are being served by the client-side filesystem cache.
* The NFS/CIFS client operations are being buffered by the client operating system.
* On rare occasions, the incoming traffic pattern is not suitable to obtain the list of directories with the most I/O activity.
## Failure to return list of largest directories
The API can sometimes fail to return the list of largest directories, due to the following reasons:

* The volume does not have file system analytics enabled.
* The volume's file system analytics database version doesn't support this report.
## Failure to return pathnames
The API can sometimes fail to obtain filesystem pathnames for certain directories, either due to internal transient errors or if those directories have been recently deleted.
In such cases, instead of the pathname, the API will return "{<volume_instance_uuid>.<fileid>}" for that directory.
## Examples
### Retrieving a list of the directories with the greatest average number of read operations per second
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsDirectory.get_collection("{volume.uuid}", top_metric="iops.read")
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    TopMetricsDirectory(
        {
            "volume": {"name": "vol1"},
            "iops": {"error": {"lower_bound": 1495, "upper_bound": 1505}, "read": 1495},
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir1%2Fdir2?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir1/dir2",
        }
    ),
    TopMetricsDirectory(
        {
            "volume": {"name": "vol1"},
            "iops": {"error": {"lower_bound": 1022, "upper_bound": 1032}, "read": 1022},
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir3%2Fdir4?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir3/dir4",
        }
    ),
    TopMetricsDirectory(
        {
            "volume": {
                "name": "vol1",
                "_links": {
                    "self": {
                        "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864"
                    }
                },
                "uuid": "73b293df-e9d7-46cc-a9ce-2df8e52ef864",
            },
            "iops": {"error": {"lower_bound": 345, "upper_bound": 355}, "read": 345},
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir12?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir12",
        }
    ),
]

```
</div>
</div>

### Retrieving a list of the directories with the most traffic with failure in obtaining the pathnames for the directories:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsDirectory.get_collection(
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
    TopMetricsDirectory(
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
    TopMetricsDirectory(
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
    TopMetricsDirectory(
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

### Retrieving a list of the largest directories
The following example shows how to retrieve a list of the largest directories based on the non-recursive bytes used by the contents of a directory.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsDirectory.get_collection(
                "{volume.uuid}", top_metric="non_recursive_bytes_used"
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
    TopMetricsDirectory(
        {
            "volume": {"name": "vol1"},
            "non_recursive_bytes_used": 345,
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir1%2Fdir2?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir1/dir2",
        }
    ),
    TopMetricsDirectory(
        {
            "volume": {"name": "vol1"},
            "non_recursive_bytes_used": 345,
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir3%2Fdir4?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir3/dir4",
        }
    ),
    TopMetricsDirectory(
        {
            "volume": {"name": "vol1"},
            "non_recursive_bytes_used": 345,
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir12?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir12",
        }
    ),
]

```
</div>
</div>

### Retrieving a list of the largest directories where incomplete data is reported
The following example retrieves a list of the largest directories when partial data is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsDirectory.get_collection(
                "{volume.uuid}", top_metric="non_recursive_bytes_used"
            )
        )
    )

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    TopMetricsDirectory(
        {
            "volume": {"name": "vol1"},
            "non_recursive_bytes_used": 1022,
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir1%2Fdir2?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir1/dir2",
        }
    ),
    TopMetricsDirectory(
        {
            "volume": {"name": "vol1"},
            "non_recursive_bytes_used": 261,
            "_links": {
                "metadata": {
                    "href": "/api/storage/volumes/73b293df-e9d7-46cc-a9ce-2df8e52ef864/files/dir12?return_metadata=true"
                }
            },
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/572361f3-e769-439d-9c04-2ba48a08ff43"
                    }
                },
                "uuid": "572361f3-e769-439d-9c04-2ba48a08ff43",
            },
            "path": "/dir12",
        }
    ),
]

```
</div>
</div>

### Retrieving a list of the largest directories when the file system analytics database version doesn't support this report
The following example shows the behavior of the API when the file system analytics database version doesn't support the large directory report.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsDirectory.get_collection(
                "{volume.uuid}", top_metric="non_recursive_bytes_used"
            )
        )
    )

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[]

```
</div>
</div>

## Example showing the behavior of the API when there is no read/write traffic:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import TopMetricsDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            TopMetricsDirectory.get_collection(
                "{volume.uuid}", top_metric="throughput.write"
            )
        )
    )

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
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


__all__ = ["TopMetricsDirectory", "TopMetricsDirectorySchema"]
__pdoc__ = {
    "TopMetricsDirectorySchema.resource": False,
    "TopMetricsDirectorySchema.opts": False,
}


class TopMetricsDirectorySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsDirectory object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.file_info_links.FileInfoLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the top_metrics_directory."""

    iops = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_directory_iops.TopMetricsDirectoryIopsSchema", data_key="iops", unknown=EXCLUDE, allow_none=True)
    r""" The iops field of the top_metrics_directory."""

    non_recursive_bytes_used = Size(
        data_key="non_recursive_bytes_used",
        allow_none=True,
    )
    r""" Non-recursive bytes used by the contents of a directory.

Example: 300"""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Path of the directory.

Example: /dir_abc/dir_123/dir_20"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the top_metrics_directory."""

    throughput = marshmallow_fields.Nested("netapp_ontap.models.top_metrics_directory_throughput.TopMetricsDirectoryThroughputSchema", data_key="throughput", unknown=EXCLUDE, allow_none=True)
    r""" The throughput field of the top_metrics_directory."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the top_metrics_directory."""

    @property
    def resource(self):
        return TopMetricsDirectory

    gettable_fields = [
        "links",
        "iops",
        "non_recursive_bytes_used",
        "path",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "throughput",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,iops,non_recursive_bytes_used,path,svm.links,svm.name,svm.uuid,throughput,volume.links,volume.name,volume.uuid,"""

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

class TopMetricsDirectory(Resource):
    r""" Information about a directory's IO metrics. """

    _schema = TopMetricsDirectorySchema
    _path = "/api/storage/volumes/{volume[uuid]}/top-metrics/directories"
    _keys = ["volume.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of directories with the greatest value performance metric or capacity metric.
### Platform Specifics
* **Unified ONTAP**: GET must be used to retrieve a list of directories with the greatest value performance metric or capacity metric.
* **ASA**: GET is not supported.

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/top-metrics/directories`](#docs-storage-storage_volumes_{volume.uuid}_top-metrics_directories)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all TopMetricsDirectory resources that match the provided query"""
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
        """Returns a list of RawResources that represent TopMetricsDirectory resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of directories with the greatest value performance metric or capacity metric.
### Platform Specifics
* **Unified ONTAP**: GET must be used to retrieve a list of directories with the greatest value performance metric or capacity metric.
* **ASA**: GET is not supported.

### Learn more
* [`DOC /storage/volumes/{volume.uuid}/top-metrics/directories`](#docs-storage-storage_volumes_{volume.uuid}_top-metrics_directories)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






