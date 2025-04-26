r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 server is an object store server that is compatible with the Amazon S3 protocol. In the initial version, only a subset of the protocol features necessary to support Fabric Pool capacity tier usecases are implemented. S3 server allows you to store objects in ONTAP using Amazon S3 protocol. This feature can be used as a target object store server for ONTAP FabricPools.
## Performance monitoring
Performance of the SVM can be monitored by the `metric.*` and `statistics.*` properties. These show the performance of the SVM in terms of IOPS, latency and throughput. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
## Examples
### Retrieving all of the S3 configurations
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(S3Service.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    S3Service(
        {
            "name": "vs1",
            "enabled": False,
            "svm": {"name": "vs2", "uuid": "cf90b8f2-8071-11e9-8190-0050568eae21"},
            "max_lock_retention_period": "none",
            "min_lock_retention_period": "none",
            "comment": "S3 server",
        }
    ),
    S3Service(
        {
            "name": "Server-1",
            "enabled": True,
            "svm": {"name": "vs1", "uuid": "d7f1219c-7f8e-11e9-9124-0050568eae21"},
            "max_lock_retention_period": "none",
            "users": [
                {"name": "user-1", "comment": "S3 user", "access_key": "(token)"},
                {"name": "user-2", "comment": "", "access_key": "(token)"},
            ],
            "min_lock_retention_period": "none",
            "comment": "S3 server",
            "buckets": [
                {
                    "name": "bucket-1",
                    "uuid": "e08665af-8114-11e9-8190-0050568eae21",
                    "logical_used_size": 157286400,
                    "comment": "s3 bucket",
                    "size": 209715200,
                    "volume": {
                        "name": "fg_oss_1559026220",
                        "uuid": "de146bff-8114-11e9-8190-0050568eae21",
                    },
                    "encryption": {"enabled": False},
                },
                {
                    "name": "bucket-2",
                    "uuid": "fb1912ef-8114-11e9-8190-0050568eae21",
                    "logical_used_size": 78643200,
                    "comment": "s3 bucket",
                    "size": 1048576000,
                    "volume": {
                        "name": "fg_oss_1559026269",
                        "uuid": "f9b1cdd0-8114-11e9-8190-0050568eae21",
                    },
                    "encryption": {"enabled": False},
                },
            ],
        }
    ),
]

```
</div>
</div>

### Retrieving all S3 configurations for a particular SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Service(**{"svm.uuid": "24c2567a-f269-11e8-8852-0050568e5298"})
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
S3Service(
    {
        "name": "Server-1",
        "enabled": True,
        "svm": {"name": "vs1", "uuid": "d7f1219c-7f8e-11e9-9124-0050568eae21"},
        "max_lock_retention_period": "none",
        "users": [
            {"name": "user-1", "comment": "s3 user", "access_key": "(token)"},
            {"name": "user-2", "comment": "", "access_key": "(token)"},
        ],
        "min_lock_retention_period": "none",
        "comment": "S3 server",
        "buckets": [
            {
                "name": "bucket-1",
                "uuid": "e08665af-8114-11e9-8190-0050568eae21",
                "policy": {
                    "statements": [
                        {
                            "sid": "DenyAccessToGetPutDeleteObjectForMike",
                            "effect": "deny",
                            "actions": ["*Object"],
                            "principals": ["mike"],
                            "resources": [
                                "bucket-1/policy-docs/*",
                                "bucket-1/confidential-*",
                            ],
                        },
                        {
                            "sid": "AccessToGetObjectForAnonymousUser",
                            "effect": "allow",
                            "actions": ["GetObject"],
                            "principals": ["*"],
                            "resources": ["bucket-1/readme"],
                        },
                    ]
                },
                "logical_used_size": 157286400,
                "comment": "s3 bucket",
                "size": 209715200,
                "volume": {
                    "name": "fg_oss_1559026220",
                    "uuid": "de146bff-8114-11e9-8190-0050568eae21",
                },
                "encryption": {"enabled": False},
                "cors": {
                    "rules": [
                        {
                            "max_age_seconds": 1024,
                            "expose_headers": ["http://www.example.com"],
                            "allowed_origins": ["http://www.example.com"],
                            "id": "string",
                            "allowed_headers": ["x-amz-request-id"],
                            "allowed_methods": ["PUT", "DELETE"],
                        }
                    ]
                },
            },
            {
                "name": "bucket-2",
                "uuid": "fb1912ef-8114-11e9-8190-0050568eae21",
                "logical_used_size": 1075838976,
                "comment": "s3 bucket",
                "size": 1677721600,
                "volume": {
                    "name": "fg_oss_1559026269",
                    "uuid": "f9b1cdd0-8114-11e9-8190-0050568eae21",
                },
                "encryption": {"enabled": False},
            },
        ],
    }
)

```
</div>
</div>

### Creating an S3 server, users, and buckets configurations with required fields specified
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Service()
    resource.buckets = [{"name": "bucket-1"}, {"name": "bucket-2"}]
    resource.enabled = True
    resource.name = "Server-1"
    resource.svm = {"uuid": "d49ef663-7f8e-11e9-9b2c-0050568e4594"}
    resource.users = [{"name": "user-1"}, {"name": "user-2"}]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
S3Service(
    {
        "_links": {"self": {"href": "/api/protocols/s3/services/"}},
        "users": [
            {
                "name": "user-1",
                "secret_key": "<secret_key_here>",
                "access_key": "(token)",
            },
            {
                "name": "user-2",
                "secret_key": "<secret_key_here>",
                "access_key": "(token)",
            },
        ],
    }
)

```
</div>
</div>

### Creating an S3 server, users, and buckets configurations
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Service()
    resource.buckets = [
        {
            "aggregates": [
                {"name": "aggr1", "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412"}
            ],
            "constituents_per_aggregate": 4,
            "name": "bucket-1",
            "size": "209715200",
            "policy": {
                "statements": [
                    {
                        "actions": ["*"],
                        "conditions": [
                            {
                                "operator": "ip_address",
                                "source_ips": ["1.1.1.1/23", "1.2.2.2/20"],
                            }
                        ],
                        "effect": "allow",
                        "resources": ["bucket-1", "bucket-1*"],
                        "sid": "fullAccessForAllPrincipalsToBucket",
                    }
                ]
            },
        },
        {
            "aggregates": [
                {"name": "aggr1", "uuid": "1cd8a442-86d1-11e0-ae1c-123478563412"},
                {"name": "aggr2", "uuid": "982fc4d0-d1a2-4da4-9c47-5b433f24757d"},
            ],
            "constituents_per_aggregate": 4,
            "name": "bucket-2",
        },
    ]
    resource.enabled = True
    resource.name = "Server-1"
    resource.max_lock_retention_period = "P1Y"
    resource.svm = {"name": "vs1", "uuid": "d49ef663-7f8e-11e9-9b2c-0050568e4594"}
    resource.users = [{"name": "user-1"}, {"name": "user-2"}]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
S3Service(
    {
        "_links": {"self": {"href": "/api/protocols/s3/services/"}},
        "users": [
            {
                "name": "user-1",
                "secret_key": "<secret_key_here>",
                "access_key": "(token)",
            },
            {
                "name": "user-2",
                "secret_key": "<secret_key_here>",
                "access_key": "(token)",
            },
        ],
    }
)

```
</div>
</div>

### Creating an S3 server configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Service()
    resource.comment = "S3 server"
    resource.enabled = True
    resource.name = "Server-1"
    resource.svm = {"name": "vs1", "uuid": "db2ec036-8375-11e9-99e1-0050568e3ed9"}
    resource.post(hydrate=True)
    print(resource)

```

### Disable s3 server for the specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Service(**{"svm.uuid": "03ce5c36-f269-11e8-8852-0050568e5298"})
    resource.enabled = False
    resource.patch()

```

### Deleting the S3 server for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Service(**{"svm.uuid": "a425f10b-ad3b-11e9-b559-0050568e8222"})
    resource.delete(delete_all=False)

```

### Deleting all of the S3 server configuration for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Service

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Service(**{"svm.uuid": "03ce5c36-f269-11e8-8852-0050568e5298"})
    resource.delete(delete_all=True)

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


__all__ = ["S3Service", "S3ServiceSchema"]
__pdoc__ = {
    "S3ServiceSchema.resource": False,
    "S3ServiceSchema.opts": False,
}


class S3ServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3Service object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the s3_service."""

    buckets = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.s3_bucket.S3BucketSchema", unknown=EXCLUDE, allow_none=True), data_key="buckets", allow_none=True)
    r""" This field cannot be specified in a PATCH method."""

    certificate = marshmallow_fields.Nested("netapp_ontap.resources.security_certificate.SecurityCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" The certificate field of the s3_service."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Can contain any additional information about the server being created or modified.

Example: S3 server"""

    default_unix_user = marshmallow_fields.Str(
        data_key="default_unix_user",
        allow_none=True,
    )
    r""" Specifies the default UNIX user for NAS Access."""

    default_win_user = marshmallow_fields.Str(
        data_key="default_win_user",
        allow_none=True,
    )
    r""" Specifies the default Windows user for NAS Access."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies whether the S3 server being created or modified should be up or down."""

    is_http_enabled = marshmallow_fields.Boolean(
        data_key="is_http_enabled",
        allow_none=True,
    )
    r""" Specifies whether HTTP is enabled on the S3 server being created or modified. By default, HTTP is disabled on the S3 server."""

    is_https_enabled = marshmallow_fields.Boolean(
        data_key="is_https_enabled",
        allow_none=True,
    )
    r""" Specifies whether HTTPS is enabled on the S3 server being created or modified. By default, HTTPS is enabled on the S3 server."""

    max_key_time_to_live = marshmallow_fields.Str(
        data_key="max_key_time_to_live",
        allow_none=True,
    )
    r""" Indicates the maximum time period that an S3 user can specify for the 'key_time_to_live' property.

* Valid format is: 'PnDTnHnMnS|PnW'. For example, P2DT6H3M10S specifies a time period of 2 days, 6 hours, 3 minutes, and 10 seconds.
* If no value is specified for this property or the value specified is '0' seconds, then a user can specify any valid value.


Example: PT6H3M"""

    max_lock_retention_period = marshmallow_fields.Str(
        data_key="max_lock_retention_period",
        allow_none=True,
    )
    r""" Specifies the maximum value that can be set as the retention period for an object in a bucket with locking enabled. The value for this property can be in years or days, not both. The value represents a duration and must be specified in the ISO-8601 duration format.  A period specified for years and days is represented in the ISO-8601 format as "P<num>Y" and "P<num>D" respectively, for example "P10Y" represents a duration of 10 years.

Example: P10Y"""

    metric = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_svm.PerformanceMetricSvmSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" The metric field of the s3_service."""

    min_lock_retention_period = marshmallow_fields.Str(
        data_key="min_lock_retention_period",
        allow_none=True,
    )
    r""" Specifies the minimum value that can be set as the retention period for an object in a bucket with locking enabled. The value for this property can be in years or days, not both. The value represents a duration and must be specified in the ISO-8601 duration format.  A period specified for years and days is represented in the ISO-8601 format as "P<num>Y" and "P<num>D" respectively, for example "P10Y" represents a duration of 10 years.

Example: P10Y"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=3, maximum=253),
        allow_none=True,
    )
    r""" Specifies the name of the S3 server. A server name can contain 3 to 253 characters using only the following combination of characters':' 0-9, A-Z, a-z, ".", and "-".

Example: Server-1"""

    port = Size(
        data_key="port",
        validate=integer_validation(minimum=1, maximum=65535),
        allow_none=True,
    )
    r""" Specifies the HTTP listener port for the S3 server. By default, HTTP is enabled on port 80. Valid values range from 1 to 65535.

Example: 80"""

    secure_port = Size(
        data_key="secure_port",
        validate=integer_validation(minimum=1, maximum=65535),
        allow_none=True,
    )
    r""" Specifies the HTTPS listener port for the S3 server. By default, HTTPS is enabled on port 443. Valid values range from 1 to 65535.

Example: 443"""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_svm.PerformanceMetricRawSvmSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the s3_service."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_service."""

    users = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.s3_user.S3UserSchema", unknown=EXCLUDE, allow_none=True), data_key="users", allow_none=True)
    r""" This field cannot be specified in a PATCH method."""

    @property
    def resource(self):
        return S3Service

    gettable_fields = [
        "links",
        "buckets",
        "certificate.links",
        "certificate.name",
        "certificate.uuid",
        "comment",
        "default_unix_user",
        "default_win_user",
        "enabled",
        "is_http_enabled",
        "is_https_enabled",
        "max_key_time_to_live",
        "max_lock_retention_period",
        "metric.links",
        "metric.duration",
        "metric.iops",
        "metric.latency",
        "metric.status",
        "metric.throughput",
        "metric.timestamp",
        "min_lock_retention_period",
        "name",
        "port",
        "secure_port",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "users",
    ]
    """links,buckets,certificate.links,certificate.name,certificate.uuid,comment,default_unix_user,default_win_user,enabled,is_http_enabled,is_https_enabled,max_key_time_to_live,max_lock_retention_period,metric.links,metric.duration,metric.iops,metric.latency,metric.status,metric.throughput,metric.timestamp,min_lock_retention_period,name,port,secure_port,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,svm.links,svm.name,svm.uuid,users,"""

    patchable_fields = [
        "certificate.name",
        "certificate.uuid",
        "comment",
        "default_unix_user",
        "default_win_user",
        "enabled",
        "is_http_enabled",
        "is_https_enabled",
        "max_key_time_to_live",
        "max_lock_retention_period",
        "min_lock_retention_period",
        "name",
        "port",
        "secure_port",
    ]
    """certificate.name,certificate.uuid,comment,default_unix_user,default_win_user,enabled,is_http_enabled,is_https_enabled,max_key_time_to_live,max_lock_retention_period,min_lock_retention_period,name,port,secure_port,"""

    postable_fields = [
        "buckets",
        "certificate.name",
        "certificate.uuid",
        "comment",
        "default_unix_user",
        "default_win_user",
        "enabled",
        "is_http_enabled",
        "is_https_enabled",
        "max_key_time_to_live",
        "max_lock_retention_period",
        "min_lock_retention_period",
        "name",
        "port",
        "secure_port",
        "svm.name",
        "svm.uuid",
        "users",
    ]
    """buckets,certificate.name,certificate.uuid,comment,default_unix_user,default_win_user,enabled,is_http_enabled,is_https_enabled,max_key_time_to_live,max_lock_retention_period,min_lock_retention_period,name,port,secure_port,svm.name,svm.uuid,users,"""

class S3Service(Resource):
    r""" Specifies the S3 server configuration. """

    _schema = S3ServiceSchema
    _path = "/api/protocols/s3/services"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the S3 server configuration for all SVMs. Note that in order to retrieve S3 bucket policy conditions, 'fields' option should be set to '**'.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver object-store-server show`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
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
        """Returns a count of all S3Service resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3Service resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["S3Service"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 Server configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server modify`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3Service"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3Service"], NetAppResponse]:
        r"""Creates an S3 server, users, and buckets configurations.
### Important notes
- Each SVM can have one S3 server configuration.
- One or more buckets and users can also be created using this end-point.
- If creating a user configuration fails, buckets are not created either and already created users are not saved.
- If creating a bucket configuration fails, all buckets already created are saved with no new buckets created.
### Required properties
* `svm.uuid` - Existing SVM in which to create an S3 server configuration.
### Recommended optional properties
* `enabled` - Specifies the state of the server created.
* `comment` - Any information related to the server created.
### Default property values
* `comment` - ""
* `enabled` - _true_
### Related ONTAP commands
* `vserver object-store-server create`
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket policy-statement-condition create`
* `vserver object-store-server bucket cors-rule create`
* `vserver object-store-server user create`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
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
        records: Iterable["S3Service"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 server configuration of an SVM. If the 'delete_all' parameter is set to false, only the S3 server is deleted. Otherwise S3 users and buckets present on the SVM are also deleted. Note that only empty buckets can be deleted. This endpoint returns the S3 server delete job-uuid in response. To monitor the job status follow /api/cluster/jobs/<job-uuid>.
### Related ONTAP commands
* `vserver object-store-server delete`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the S3 server configuration for all SVMs. Note that in order to retrieve S3 bucket policy conditions, 'fields' option should be set to '**'.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver object-store-server show`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the S3 Server configuration of an SVM. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server show`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
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
        r"""Creates an S3 server, users, and buckets configurations.
### Important notes
- Each SVM can have one S3 server configuration.
- One or more buckets and users can also be created using this end-point.
- If creating a user configuration fails, buckets are not created either and already created users are not saved.
- If creating a bucket configuration fails, all buckets already created are saved with no new buckets created.
### Required properties
* `svm.uuid` - Existing SVM in which to create an S3 server configuration.
### Recommended optional properties
* `enabled` - Specifies the state of the server created.
* `comment` - Any information related to the server created.
### Default property values
* `comment` - ""
* `enabled` - _true_
### Related ONTAP commands
* `vserver object-store-server create`
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket policy-statement-condition create`
* `vserver object-store-server bucket cors-rule create`
* `vserver object-store-server user create`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
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
        r"""Updates the S3 Server configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server modify`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
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
        r"""Deletes the S3 server configuration of an SVM. If the 'delete_all' parameter is set to false, only the S3 server is deleted. Otherwise S3 users and buckets present on the SVM are also deleted. Note that only empty buckets can be deleted. This endpoint returns the S3 server delete job-uuid in response. To monitor the job status follow /api/cluster/jobs/<job-uuid>.
### Related ONTAP commands
* `vserver object-store-server delete`
### Learn more
* [`DOC /protocols/s3/services`](#docs-object-store-protocols_s3_services)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


