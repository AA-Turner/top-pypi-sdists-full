r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 bucket is a container of objects. Each bucket defines an object namespace. S3 server requests specify objects using a bucket-name and object-name pair. An object consists of data, along with optional metadata and access controls, that is accessible using a name. An object resides within a bucket. There can be more than one bucket in an S3 server. Buckets that are created for the server are associated with an S3 user that is created on the S3 server.
## Examples
### Retrieving all fields for all S3 buckets of a cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(S3Bucket.get_collection(fields="**")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    S3Bucket(
        {
            "name": "bucket-2",
            "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
            "uuid": "527812ab-7c6d-11e9-97e8-0050568ea123",
            "logical_used_size": 157286400,
            "qos_policy": {
                "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
                "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
            },
            "comment": "S3 bucket.",
            "size": 209715200,
            "volume": {
                "name": "fg_oss_1558514455",
                "uuid": "51276f5f-7c6d-11e9-97e8-0050568ea123",
            },
            "encryption": {"enabled": False},
        }
    ),
    S3Bucket(
        {
            "name": "bucket-1",
            "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
            "uuid": "a8234aec-7e06-11e9-97e8-0050568ea123",
            "logical_used_size": 0,
            "qos_policy": {
                "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
                "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
            },
            "comment": "bucket2",
            "size": 1677721600,
            "volume": {
                "name": "fg_oss_1558690256",
                "uuid": "a36a1ea7-7e06-11e9-97e8-0050568ea123",
            },
            "encryption": {"enabled": False},
        }
    ),
    S3Bucket(
        {
            "name": "bucket-3",
            "svm": {"name": "vs2", "uuid": "ee30eb2d-7ae1-11e9-8abe-0050568ea123"},
            "uuid": "19283b75-7ae2-11e9-8abe-0050568ea123",
            "policy": {
                "statements": [
                    {
                        "sid": "fullAccessForAliceToBucket",
                        "effect": "allow",
                        "conditions": [
                            {"operator": "ip_address", "source_ips": ["1.1.1.1/10"]}
                        ],
                        "actions": ["*"],
                        "principals": ["Alice"],
                        "resources": ["bucket-3", "bucket-3/*"],
                    }
                ]
            },
            "logical_used_size": 1075838976,
            "qos_policy": {
                "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
                "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
            },
            "comment": "bucket3",
            "size": 1677721600,
            "volume": {
                "name": "fg_oss_1558690257",
                "uuid": "a46a1ea7-7e06-11e9-97e8-0050568ea123",
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
        }
    ),
]

```
</div>
</div>

### Retrieving all S3 buckets of a cluster ordered by size
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(S3Bucket.get_collection(order_by="size")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    S3Bucket(
        {
            "name": "bb1",
            "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
            "uuid": "754389d0-7e13-11e9-bfdc-0050568ea123",
            "size": 838860800,
        }
    ),
    S3Bucket(
        {
            "name": "bb2",
            "svm": {"name": "vs2", "uuid": "ee30eb2d-7ae1-11e9-8abe-0050568ea123"},
            "uuid": "19283b75-7ae2-11e9-8abe-0050568ea123",
            "size": 838860800,
        }
    ),
    S3Bucket(
        {
            "name": "bucket-1",
            "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
            "uuid": "a8234aec-7e06-11e9-97e8-0050568ea123",
            "size": 1677721600,
        }
    ),
]

```
</div>
</div>

### Retrieving all S3 buckets of a cluster with name  "bb2"
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(S3Bucket.get_collection(name="bb2")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    S3Bucket(
        {
            "name": "bb2",
            "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
            "uuid": "087d940e-7e15-11e9-bfdc-0050568ea123",
        }
    ),
    S3Bucket(
        {
            "name": "bb2",
            "svm": {"name": "vs2", "uuid": "ee30eb2d-7ae1-11e9-8abe-0050568ea123"},
            "uuid": "19283b75-7ae2-11e9-8abe-0050568ea123",
        }
    ),
]

```
</div>
</div>

### Retrieving the specified bucket associated with an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Bucket(
        uuid="527812ab-7c6d-11e9-97e8-0050568ea123",
        **{"svm.uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
S3Bucket(
    {
        "name": "bucket-2",
        "svm": {"name": "vs1", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"},
        "uuid": "527812ab-7c6d-11e9-97e8-0050568ea123",
        "logical_used_size": 157286400,
        "qos_policy": {
            "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
            "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
        },
        "comment": "S3 bucket.",
        "size": 209715200,
        "volume": {
            "name": "fg_oss_1558514455",
            "uuid": "51276f5f-7c6d-11e9-97e8-0050568ea123",
        },
        "encryption": {"enabled": False},
    }
)

```
</div>
</div>

### Creating an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3Bucket()
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-3"
    resource.svm = {"name": "vs1"}
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
S3Bucket({"name": "bucket-3", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket along with QoS policy for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3Bucket()
    resource.comment = "S3 bucket."
    resource.name = "bucket-3"
    resource.svm = {"name": "vs1"}
    resource.qos_policy = {
        "min_throughput_iops": 0,
        "min_throughput_mbps": 0,
        "max_throughput_iops": 1000000,
        "max_throughput_mbps": 900000,
        "uuid": "02d07a93-6177-11ea-b241-000c293feac8",
        "name": "vs0_auto_gen_policy_02cfa02a_6177_11ea_b241_000c293feac8",
    }
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
S3Bucket({"name": "bucket-3", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket along with policies and conditions for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3Bucket()
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-3"
    resource.policy = {
        "statements": [
            {
                "actions": ["GetObject"],
                "conditions": [
                    {
                        "operator": "ip_address",
                        "source_ips": ["1.1.1.1/23", "1.2.2.2/20"],
                    }
                ],
                "effect": "allow",
                "resources": ["bucket-3/policies/examples/*"],
                "sid": "AccessToGetObjectForAllUsersofSVM",
            },
            {
                "actions": ["*Object"],
                "effect": "deny",
                "principals": ["mike"],
                "resources": ["bucket-3/policy-docs/*", "bucket-3/confidential-*"],
                "sid": "DenyAccessToObjectForMike",
            },
            {
                "actions": ["GetObject"],
                "effect": "allow",
                "principals": ["*"],
                "resources": ["bucket-3/readme"],
                "sid": "AnonymousAccessToGetObjectForUsers",
            },
        ]
    }
    resource.svm = {"uuid": "259b4e46-2d33-11ea-9145-005056bbbec1"}
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
S3Bucket({"name": "bucket-3", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket and CORS rules for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Bucket()
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-3"
    resource.cors = {
        "rules": [
            {
                "allowed_headers": ["x-amz-request-id"],
                "allowed_methods": ["PUT", "DELETE"],
                "allowed_origins": ["http://www.example.com"],
                "expose_headers": ["http://www.example.com"],
                "id": "id1",
                "max_age_seconds": 1024,
            }
        ]
    }
    resource.svm = {"uuid": "259b4e46-2d33-11ea-9145-005056bbbec1"}
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
S3Bucket({"name": "bucket-3", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket along with a bucket lifecycle management rule for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3Bucket()
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-4"
    resource.lifecycle_management = {
        "rules": [
            {
                "name": "rule1",
                "expiration": {"object_age_days": "1000"},
                "abort_incomplete_multipart_upload": {"after_initiation_days": 200},
                "object_filter": {"prefix": "obj1*/", "size_greater_than": "1000"},
            },
            {
                "name": "rule2",
                "object_filter": {"size_greater_than": "50"},
                "expiration": {"object_age_days": "5000"},
            },
        ]
    }
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
S3Bucket({"name": "bucket-4", "comment": "S3 bucket."})

```
</div>
</div>

### Creating an S3 bucket with a snapshot-policy
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3Bucket()
    resource.comment = "S3 snapshot policy bucket."
    resource.snapshot_policy = {
        "name": "default-1weekly",
        "uuid": "f9c5f090-4ac8-11ef-ba24-005056a7ceb6",
    }
    resource.name = "bucket-7"
    resource.svm.uuid = "8c38f10b-4871-11ef-aab5-005056a7ceb6"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
S3Bucket(
    {
        "name": "bucket-7",
        "svm": {"uuid": "8c38f10b-4871-11ef-aab5-005056a7ceb6"},
        "comment": "S3 snapshot policy bucket.",
        "snapshot_policy": {
            "name": "default-1weekly",
            "uuid": "f9c5f090-4ac8-11ef-ba24-005056a7ceb6",
        },
    }
)

```
</div>
</div>

### Updating an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Bucket(
        uuid="376a2efd-2d4d-11ea-9c30-005056bb883a",
        **{"svm.uuid": "259b4e46-2d33-11ea-9145-005056bbbec1"}
    )
    resource.comment = "Bucket modified."
    resource.size = 111111111111
    resource.qos_policy = {
        "min_throughput_iops": 0,
        "min_throughput_mbps": 0,
        "max_throughput_iops": 1000000,
        "max_throughput_mbps": 900000,
        "uuid": "02d07a93-6177-11ea-b241-000c293feac8",
        "name": "vs0_auto_gen_policy_02cfa02a_6177_11ea_b241_000c293feac8",
    }
    resource.patch()

```

### Updating an S3 bucket policy for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Bucket(
        uuid="376a2efd-2d4d-11ea-9c30-005056bb883a",
        **{"svm.uuid": "259b4e46-2d33-11ea-9145-005056bbbec1"}
    )
    resource.policy = {
        "statements": [
            {
                "actions": ["*"],
                "conditions": [
                    {"operator": "ip_address", "source_ips": ["1.1.1.5/23"]}
                ],
                "effect": "allow",
                "resources": ["*"],
                "sid": "fullAccessForAllPrincipalsToBucket",
            }
        ]
    }
    resource.patch()

```

### Updating an S3 bucket CORS configuration for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Bucket(
        uuid="376a2efd-2d4d-11ea-9c30-005056bb883a",
        **{"svm.uuid": "259b4e46-2d33-11ea-9145-005056bbbec1"}
    )
    resource.cors = {
        "rules": [
            {
                "allowed_headers": ["x-amz-request-id"],
                "allowed_methods": ["PUT", "DELETE"],
                "allowed_origins": ["http://www.example.com"],
                "expose_headers": ["http://www.example.com"],
                "id": "id1",
                "max_age_seconds": 1024,
            }
        ]
    }
    resource.patch()

```

### Updating the snapshot-policy for an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Bucket(
        uuid="eec0d90e-4934-11ef-947d-005056a7ceb6",
        **{"svm.uuid": "8c38f10b-4871-11ef-aab5-005056a7ceb6"}
    )
    resource.snapshot_policy = {
        "name": "default-1weekly",
        "uuid": "f9c5f090-4ac8-11ef-ba24-005056a7ceb6",
    }
    resource.patch()

```

### Deleting an S3 bucket for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Bucket

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3Bucket(
        uuid="98528221-2d52-11ea-892e-005056bbbec1",
        **{"svm.uuid": "259b4e46-2d33-11ea-9145-005056bbbec1"}
    )
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


__all__ = ["S3Bucket", "S3BucketSchema"]
__pdoc__ = {
    "S3BucketSchema.resource": False,
    "S3BucketSchema.opts": False,
}


class S3BucketSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3Bucket object"""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.flexcache_aggregates.FlexcacheAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" A list of aggregates for FlexGroup volume constituents where the bucket is hosted. If this option is not specified, the bucket is auto-provisioned as a FlexGroup volume."""

    allowed = marshmallow_fields.Boolean(
        data_key="allowed",
        allow_none=True,
    )
    r""" If this is set to true, an SVM administrator can manage the S3 service. If it is false, only the cluster administrator can manage the service. This field cannot be specified in a POST method."""

    audit_event_selector = marshmallow_fields.Nested("netapp_ontap.models.s3_audit_event_selector.S3AuditEventSelectorSchema", data_key="audit_event_selector", unknown=EXCLUDE, allow_none=True)
    r""" S3 audit event selector per SVM per bucket.  Use to set access and permission type for S3 event audit."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Can contain any additional information about the bucket being created or modified.

Example: S3 bucket."""

    constituents_per_aggregate = Size(
        data_key="constituents_per_aggregate",
        validate=integer_validation(minimum=1, maximum=1000),
        allow_none=True,
    )
    r""" Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently.

Example: 4"""

    cors = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_cors.S3BucketCorsSchema", data_key="cors", unknown=EXCLUDE, allow_none=True)
    r""" Cross-origin resource sharing (CORS) specifies an object associated with a bucket. The CORS configuration enables the bucket to service the cross-origin requests. A request might typically come from an origin with a domain that is different to that of the bucket. By configuring a CORS rule, you can define a combination of allowed origins, HTTP headers and methods that a bucket can use to filter out the cross-origin requests that it can service successfully."""

    encryption = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_encryption.S3BucketEncryptionSchema", data_key="encryption", unknown=EXCLUDE, allow_none=True)
    r""" The encryption field of the s3_bucket."""

    lifecycle_management = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_lifecycle_management.S3BucketLifecycleManagementSchema", data_key="lifecycle_management", unknown=EXCLUDE, allow_none=True)
    r""" Lifecycle management is implemented as an object associated with a bucket. It defines rules to be applied against objects within a bucket. These rules are applied in the background and can delete objects."""

    logical_used_size = Size(
        data_key="logical_used_size",
        allow_none=True,
    )
    r""" Specifies the bucket logical used size up to this point. This field cannot be specified using a POST or PATCH method."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=3, maximum=63),
        allow_none=True,
    )
    r""" Specifies the name of the bucket. Bucket name is a string that can only contain the following combination of ASCII-range alphanumeric characters 0-9, a-z, ".", and "-".

Example: bucket1"""

    nas_path = marshmallow_fields.Str(
        data_key="nas_path",
        allow_none=True,
    )
    r""" Specifies the NAS path to which the nas bucket corresponds to.

Example: /"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_policy.S3BucketPolicySchema", data_key="policy", unknown=EXCLUDE, allow_none=True)
    r""" A policy is an object associated with a bucket. It defines resource (bucket, folder, or object) permissions. These policies get evaluated when an S3 user makes a request by executing a specific command. The user must be part of the principal (user or group) specified in the policy. Permissions in the policies determine whether the request is allowed or denied."""

    protection_status = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_protection_status.S3BucketProtectionStatusSchema", data_key="protection_status", unknown=EXCLUDE, allow_none=True)
    r""" Specifies attributes of bucket protection."""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.resources.qos_policy.QosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The qos_policy field of the s3_bucket."""

    retention = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_retention.S3BucketRetentionSchema", data_key="retention", unknown=EXCLUDE, allow_none=True)
    r""" Information about the retention-mode and default-retention-period configured on the bucket."""

    role = marshmallow_fields.Str(
        data_key="role",
        validate=enum_validation(['standalone', 'active', 'passive']),
        allow_none=True,
    )
    r""" Specifies the role of the bucket. This field cannot be specified using a POST method.

Valid choices:

* standalone
* active
* passive"""

    size = Size(
        data_key="size",
        validate=integer_validation(minimum=199229440, maximum=62672162783232000),
        allow_none=True,
    )
    r""" Specifies the bucket size in bytes; ranges from 190MB to 62PB.

Example: 1677721600"""

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_snapshot_policy.S3BucketSnapshotPolicySchema", data_key="snapshot_policy", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the bucket snapshot policy."""

    storage_service_level = marshmallow_fields.Str(
        data_key="storage_service_level",
        validate=enum_validation(['value', 'performance', 'extreme']),
        allow_none=True,
    )
    r""" Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are "value", "performance" or "extreme".

Valid choices:

* value
* performance
* extreme"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_bucket."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['s3', 'nas']),
        allow_none=True,
    )
    r""" Specifies the bucket type. Valid values are "s3"and "nas".

Valid choices:

* s3
* nas"""

    use_mirrored_aggregates = marshmallow_fields.Boolean(
        data_key="use_mirrored_aggregates",
        allow_none=True,
    )
    r""" Specifies whether mirrored aggregates are selected when provisioning a FlexGroup. Only mirrored aggregates are used if this parameter is set to "true" and only unmirrored aggregates are used if this parameter is set to "false". The default value is "true" for a MetroCluster configuration and is "false" for a non-MetroCluster configuration."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Specifies the unique identifier of the bucket.

Example: 414b29a1-3b26-11e9-bd58-0050568ea055"""

    versioning_state = marshmallow_fields.Str(
        data_key="versioning_state",
        validate=enum_validation(['disabled', 'enabled', 'suspended']),
        allow_none=True,
    )
    r""" Specifies the versioning state of the bucket. Valid values are "disabled", "enabled" or "suspended". Note that the versioning state cannot be modified to 'disabled' from any other state.

Valid choices:

* disabled
* enabled
* suspended"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the s3_bucket."""

    @property
    def resource(self):
        return S3Bucket

    gettable_fields = [
        "allowed",
        "audit_event_selector",
        "comment",
        "cors",
        "encryption",
        "lifecycle_management",
        "logical_used_size",
        "name",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.links",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "retention",
        "role",
        "size",
        "snapshot_policy",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "uuid",
        "versioning_state",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """allowed,audit_event_selector,comment,cors,encryption,lifecycle_management,logical_used_size,name,nas_path,policy,protection_status,qos_policy.links,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,role,size,snapshot_policy,svm.links,svm.name,svm.uuid,type,uuid,versioning_state,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "allowed",
        "audit_event_selector",
        "comment",
        "cors",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "retention",
        "size",
        "snapshot_policy",
        "type",
        "versioning_state",
    ]
    """allowed,audit_event_selector,comment,cors,nas_path,policy,protection_status,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,size,snapshot_policy,type,versioning_state,"""

    postable_fields = [
        "aggregates.name",
        "aggregates.uuid",
        "allowed",
        "audit_event_selector",
        "comment",
        "constituents_per_aggregate",
        "cors",
        "lifecycle_management",
        "name",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "retention",
        "size",
        "snapshot_policy",
        "storage_service_level",
        "svm.name",
        "svm.uuid",
        "type",
        "use_mirrored_aggregates",
        "versioning_state",
    ]
    """aggregates.name,aggregates.uuid,allowed,audit_event_selector,comment,constituents_per_aggregate,cors,lifecycle_management,name,nas_path,policy,protection_status,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,size,snapshot_policy,storage_service_level,svm.name,svm.uuid,type,use_mirrored_aggregates,versioning_state,"""

class S3Bucket(Resource):
    r""" A bucket is a container of objects. Each bucket defines an object namespace. S3 requests specify objects using a bucket-name and object-name pair. An object resides within a bucket. """

    _schema = S3BucketSchema
    _path = "/api/protocols/s3/buckets"
    _keys = ["svm.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all S3 buckets for all SVMs. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
* `vserver object-store-server bucket cors-rule show`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
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
        """Returns a count of all S3Bucket resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3Bucket resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["S3Bucket"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 bucket configuration of an SVM.
### Important notes
- The following fields can be modified for a bucket:
  * `comment` - Any information related to the bucket.
  * `size` - Bucket size.
  * `policy` - An access policy for resources (buckets and objects) that defines their permissions. New policies are created after existing policies are deleted. To retain any of the existing policy statements, you need to specify those statements again. Also, policy conditions can be specified as part of a bucket policy.
  * `qos_policy` - A QoS policy for buckets.
  * `audit_event_selector` - Audit policy for buckets. None can be specified for both access and permission to remove an audit event selector.
  * `versioning-state` - Versioning state of the buckets.
  * `nas_path` - NAS path to which the bucket corresponds to.
  * `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
  * `cors' - Specifying CORS rules enables the bucket to service the cross-origin requests. Note that the new CORS configuration specified will replace the existing one. If you need to retain any of the existing CORS rules, specify those rules again as part of the new CORS rules. To remove all the existing rules, specify an empty CORS configuration as input.
  * `snapshot_policy` - Snapshot policy for the bucket.
### Related ONTAP commands
* `vserver object-store-server bucket modify`
* `vserver object-store-server bucket policy statement modify`
* `vserver object-store-server bucket policy-statement-condition modify`
* `vserver object-store-server bucket cors-rule create`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3Bucket"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3Bucket"], NetAppResponse]:
        r"""Creates the S3 bucket configuration of an SVM.
### Important notes
- Each SVM can have one or more bucket configurations.
- Aggregate lists should be specified explicitly. If not specified, then the bucket is auto-provisioned as a FlexGroup volume.
- Constituents per aggregate specifies the number of components (or FlexVol volumes) per aggregate. Is specified only when an aggregate list is explicitly defined.
- An access policy can be created along with a bucket create. If creating an access policy fails, bucket configurations are saved and the access policy can be created using the PATCH endpoint.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
- A CORS configuration can be specified along with bucket creation.
### Required properties
* `svm.uuid or svm.name` - Existing SVM in which to create the bucket configuration.
* `name` - Bucket name that is to be created.
### Recommended optional properties
* `aggregates` - List of aggregates for the FlexGroup volume on which the bucket is hosted on.
* `constituents_per_aggregate` - Number of constituents per aggregate.
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying a policy enables users to perform operations on buckets; specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - NAS path to which the bucket corresponds to.
* `use_mirrored_aggregates` - Specifies whether mirrored aggregates are selected when provisioning a FlexGroup volume.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
* `cors' - Specifying CORS rules enables the bucket to service the cross-origin requests.
* `snapshot_policy` - Snapshot policy for the bucket.
### Default property values
* `size` - 800MB
* `comment` - ""
* `aggregates` - No default value.
* `constituents_per_aggregate` - _4_ , if an aggregates list is specified. Otherwise, no default value.
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `versioning_state` - disabled.
* `use_mirrored_aggregates` - _true_ for a MetroCluster configuration and _false_ for a non-MetroCluster configuration.
* `type` - S3
* `retention.mode` - no_lock
### Related ONTAP commands
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket lifecycle-management-rule create`
* `vserver object-store-server bucket cors-rule create`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
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
        records: Iterable["S3Bucket"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 bucket configuration of an SVM. An access policy is also deleted on an S3 bucket "delete" command.
### Related ONTAP commands
* `vserver object-store-server bucket delete`
* `vserver object-store-server bucket policy statement delete`
* `vserver object-store-server bucket policy-statement-condition delete`
* `vserver object-store-server bucket lifecycle-management-rule delete`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all S3 buckets for all SVMs. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
* `vserver object-store-server bucket cors-rule show`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the S3 bucket configuration of an SVM. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
* `vserver object-store-server bucket cors-rule show`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
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
        r"""Creates the S3 bucket configuration of an SVM.
### Important notes
- Each SVM can have one or more bucket configurations.
- Aggregate lists should be specified explicitly. If not specified, then the bucket is auto-provisioned as a FlexGroup volume.
- Constituents per aggregate specifies the number of components (or FlexVol volumes) per aggregate. Is specified only when an aggregate list is explicitly defined.
- An access policy can be created along with a bucket create. If creating an access policy fails, bucket configurations are saved and the access policy can be created using the PATCH endpoint.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
- A CORS configuration can be specified along with bucket creation.
### Required properties
* `svm.uuid or svm.name` - Existing SVM in which to create the bucket configuration.
* `name` - Bucket name that is to be created.
### Recommended optional properties
* `aggregates` - List of aggregates for the FlexGroup volume on which the bucket is hosted on.
* `constituents_per_aggregate` - Number of constituents per aggregate.
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying a policy enables users to perform operations on buckets; specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - NAS path to which the bucket corresponds to.
* `use_mirrored_aggregates` - Specifies whether mirrored aggregates are selected when provisioning a FlexGroup volume.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
* `cors' - Specifying CORS rules enables the bucket to service the cross-origin requests.
* `snapshot_policy` - Snapshot policy for the bucket.
### Default property values
* `size` - 800MB
* `comment` - ""
* `aggregates` - No default value.
* `constituents_per_aggregate` - _4_ , if an aggregates list is specified. Otherwise, no default value.
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `versioning_state` - disabled.
* `use_mirrored_aggregates` - _true_ for a MetroCluster configuration and _false_ for a non-MetroCluster configuration.
* `type` - S3
* `retention.mode` - no_lock
### Related ONTAP commands
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket lifecycle-management-rule create`
* `vserver object-store-server bucket cors-rule create`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
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
        r"""Updates the S3 bucket configuration of an SVM.
### Important notes
- The following fields can be modified for a bucket:
  * `comment` - Any information related to the bucket.
  * `size` - Bucket size.
  * `policy` - An access policy for resources (buckets and objects) that defines their permissions. New policies are created after existing policies are deleted. To retain any of the existing policy statements, you need to specify those statements again. Also, policy conditions can be specified as part of a bucket policy.
  * `qos_policy` - A QoS policy for buckets.
  * `audit_event_selector` - Audit policy for buckets. None can be specified for both access and permission to remove an audit event selector.
  * `versioning-state` - Versioning state of the buckets.
  * `nas_path` - NAS path to which the bucket corresponds to.
  * `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
  * `cors' - Specifying CORS rules enables the bucket to service the cross-origin requests. Note that the new CORS configuration specified will replace the existing one. If you need to retain any of the existing CORS rules, specify those rules again as part of the new CORS rules. To remove all the existing rules, specify an empty CORS configuration as input.
  * `snapshot_policy` - Snapshot policy for the bucket.
### Related ONTAP commands
* `vserver object-store-server bucket modify`
* `vserver object-store-server bucket policy statement modify`
* `vserver object-store-server bucket policy-statement-condition modify`
* `vserver object-store-server bucket cors-rule create`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
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
        r"""Deletes the S3 bucket configuration of an SVM. An access policy is also deleted on an S3 bucket "delete" command.
### Related ONTAP commands
* `vserver object-store-server bucket delete`
* `vserver object-store-server bucket policy statement delete`
* `vserver object-store-server bucket policy-statement-condition delete`
* `vserver object-store-server bucket lifecycle-management-rule delete`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/buckets`](#docs-object-store-protocols_s3_buckets)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


