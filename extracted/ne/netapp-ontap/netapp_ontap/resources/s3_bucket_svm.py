r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 bucket is a container of objects. Each bucket defines an object namespace. S3 server requests specify objects using a bucket-name and object-name pair. An object consists of data, along with optional metadata and access controls, accessible via a name. An object resides within a bucket. There can be more than one bucket in an S3 server. Buckets which are created for the server are associated with an S3 user that is created on the S3 server.
An access policy is an object that when associated with a resource, defines their permissions. Buckets and objects are defined as resources. By default, only the "root" user can access these resources. Access policies are used to manage access to these resources by enabling ONTAP admin to provide "grants" to allow other users to perform operations on the buckets.
## Examples
### Retrieving all fields for all S3 buckets of an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            S3BucketSvm.get_collection(
                "12f3ba4c-7ae0-11e9-8c06-0050568ea123", fields="**"
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
    S3BucketSvm(
        {
            "audit_event_selector": {"access": "all", "permission": "all"},
            "svm": {"uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123", "name": "vs1"},
            "uuid": "527812ab-7c6d-11e9-97e8-0050568ea123",
            "comment": "S3 bucket.",
            "volume": {
                "uuid": "51276f5f-7c6d-11e9-97e8-0050568ea123",
                "name": "fg_oss_1558514455",
            },
            "qos_policy": {
                "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
                "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
            },
            "name": "bucket-2",
            "encryption": {"enabled": False},
            "logical_used_size": 157286400,
            "size": 209715200,
        }
    ),
    S3BucketSvm(
        {
            "svm": {"uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123", "name": "vs1"},
            "uuid": "a8234aec-7e06-11e9-97e8-0050568ea123",
            "comment": "bucket1",
            "cors": {
                "rules": [
                    {
                        "id": "string",
                        "allowed_origins": ["http://www.example.com"],
                        "allowed_headers": ["x-amz-request-id"],
                        "max_age_seconds": 1024,
                        "allowed_methods": ["PUT", "DELETE"],
                        "expose_headers": ["http://www.example.com"],
                    }
                ]
            },
            "volume": {
                "uuid": "a36a1ea7-7e06-11e9-97e8-0050568ea123",
                "name": "fg_oss_1558690256",
            },
            "qos_policy": {
                "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
                "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
            },
            "name": "bucket-1",
            "encryption": {"enabled": False},
            "policy": {
                "statements": [
                    {
                        "effect": "allow",
                        "sid": "fullAccessForAliceToBucket",
                        "actions": ["*"],
                        "resources": ["*"],
                        "principals": ["Alice"],
                    },
                    {
                        "effect": "allow",
                        "sid": "AccessToListAndGetObjectForAnnAndJack",
                        "actions": ["ListBucket", "GetObject"],
                        "resources": ["bucket-1", "bucket-1/*"],
                        "conditions": [
                            {"operator": "ip_address", "source_ips": ["1.1.1.1/10"]},
                            {
                                "usernames": ["user1", "user2"],
                                "operator": "string_equals",
                                "delimiters": ["del1", "del2"],
                                "prefixes": ["pref1", "pref2"],
                            },
                            {"operator": "numeric_equals", "max_keys": [100]},
                        ],
                        "principals": ["ann", "jack"],
                    },
                    {
                        "effect": "deny",
                        "sid": "DenyAccessToGetPutDeleteObjectForMike",
                        "actions": ["*Object"],
                        "resources": [
                            "bucket-1/policy-docs/*",
                            "bucket-1/confidential-*",
                        ],
                        "principals": ["mike", "group/group1", "nasgroup/group2"],
                    },
                    {
                        "effect": "allow",
                        "sid": "AccessToGetObjectForAnonymousUsers",
                        "actions": ["GetObject"],
                        "resources": ["bucket-1/readme"],
                        "principals": ["*"],
                    },
                    {
                        "effect": "allow",
                        "sid": "AccessToGetObjectForAllUsersOfSVM",
                        "actions": ["GetObject"],
                        "resources": ["bucket-1/policies/examples/*"],
                        "principals": [],
                    },
                ]
            },
            "logical_used_size": 0,
            "size": 1677721600,
        }
    ),
]

```
</div>
</div>

### Retrieving the specified bucket associated with an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "12f3ba4c-7ae0-11e9-8c06-0050568ea123",
        uuid="527812ab-7c6d-11e9-97e8-0050568ea123",
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
S3BucketSvm(
    {
        "svm": {"uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123", "name": "vs1"},
        "uuid": "527812ab-7c6d-11e9-97e8-0050568ea123",
        "comment": "S3 bucket.",
        "volume": {
            "uuid": "51276f5f-7c6d-11e9-97e8-0050568ea123",
            "name": "fg_oss_1558514455",
        },
        "qos_policy": {
            "uuid": "39ac471f-ff35-11e9-b0f9-005056a7ab52",
            "name": "vs0_auto_gen_policy_39a9522f_ff35_11e9_b0f9_005056a7ab52",
        },
        "name": "bucket-2",
        "encryption": {"enabled": False},
        "logical_used_size": 157286400,
        "size": 209715200,
    }
)

```
</div>
</div>

### Creating an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("12f3ba4c-7ae0-11e9-8c06-0050568ea123")
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea123"}
    ]
    resource.comment = "S3 bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-3"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
S3BucketSvm({"comment": "S3 bucket.", "name": "bucket-3"})

```
</div>
</div>

### Creating an S3 bucket along with QoS policies and event selector for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("3e538980-f0af-11e9-ba68-0050568e9798")
    resource.comment = "S3 bucket."
    resource.name = "bucket-3"
    resource.qos_policy = {
        "min_throughput_iops": 0,
        "min_throughput_mbps": 0,
        "max_throughput_iops": 1000000,
        "max_throughput_mbps": 900000,
        "uuid": "02d07a93-6177-11ea-b241-000c293feac8",
        "name": "vs0_auto_gen_policy_02cfa02a_6177_11ea_b241_000c293feac8",
    }
    resource.audit_event_selector = {"access": "all", "permission": "all"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
S3BucketSvm({"comment": "S3 bucket.", "name": "bucket-3"})

```
</div>
</div>

### Creating an S3 bucket along with policies for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("3e538980-f0af-11e9-ba68-0050568e9798")
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
                    },
                    {"max_keys": [1000], "operator": "numeric_equals"},
                    {
                        "delimiters": ["/"],
                        "operator": "string_equals",
                        "prefixes": ["pref"],
                        "usernames": ["user1"],
                    },
                ],
                "effect": "allow",
                "resources": ["bucket-3/policies/examples/*"],
                "sid": "AccessToGetObjectForAllUsersofSVM",
            },
            {
                "actions": ["*Object"],
                "effect": "deny",
                "principals": ["mike", "group/grp1"],
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
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
S3BucketSvm({"comment": "S3 bucket.", "name": "bucket-3"})

```
</div>
</div>

### Creating an S3 bucket along with lifecycle management rules
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("3e538980-f0af-11e9-ba68-0050568e9798")
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
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
S3BucketSvm({"comment": "S3 bucket.", "name": "bucket-4"})

```
</div>
</div>

### Creating an S3 bucket with object locking enabled for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("12f3ba4c-7ae0-11e9-8c06-0050568ea143")
    resource.aggregates = [
        {"name": "aggr5", "uuid": "12f3ba4c-7ae0-11e9-8c06-0050568ea143"}
    ]
    resource.comment = "S3 Compliance mode bucket."
    resource.constituents_per_aggregate = 4
    resource.name = "bucket-5"
    resource.retention = {"mode": "compliance", "default_period": "P1Y"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
S3BucketSvm({"comment": "S3 Compliance mode bucket.", "name": "bucket-5"})

```
</div>
</div>

### Creating an S3 bucket with CORS rules for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm("2da46d66-2327-11ef-ab73-005056a7a2dd")
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
    resource.name = "bucket1"
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
S3BucketSvm(
    {
        "uuid": "baf69601-23e5-11ef-ab73-005056a7a2dd",
        "type": "s3",
        "cors": {
            "rules": [
                {
                    "id": "id1",
                    "allowed_origins": ["http://www.example.com"],
                    "allowed_headers": ["x-amz-request-id"],
                    "max_age_seconds": 1024,
                    "allowed_methods": ["PUT", "DELETE"],
                    "expose_headers": ["http://www.example.com"],
                }
            ]
        },
        "name": "bucket1",
    }
)

```
</div>
</div>

### Creating an S3 bucket with a snapshot-policy
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm("12f3ba4c-7ae0-11e9-8c06-0050568ea143")
    resource.comment = "S3 snapshot policy bucket."
    resource.snapshot_policy = {
        "name": "default-1weekly",
        "uuid": "f9c5f090-4ac8-11ef-ba24-005056a7ceb6",
    }
    resource.name = "bucket-6"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
S3BucketSvm(
    {
        "comment": "S3 snapshot policy bucket.",
        "snapshot_policy": {
            "uuid": "f9c5f090-4ac8-11ef-ba24-005056a7ceb6",
            "name": "default-1weekly",
        },
        "name": "bucket-6",
    }
)

```
</div>
</div>

### Updating an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "12f3ba4c-7ae0-11e9-8c06-0050568ea123",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
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

### Updating an S3 bucket policy and event selector for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.policy = {
        "statements": [
            {
                "actions": ["*"],
                "conditions": [
                    {
                        "operator": "ip_address",
                        "source_ips": ["1.1.1.1/23", "1.2.2.2/20"],
                    },
                    {"max_keys": [1000], "operator": "numeric_equals"},
                    {
                        "delimiters": ["/"],
                        "operator": "string_equals",
                        "prefixes": ["pref"],
                        "usernames": ["user1"],
                    },
                ],
                "effect": "allow",
                "resources": ["*"],
                "sid": "fullAccessForAllPrincipalsToBucket",
            }
        ]
    }
    resource.audit_event_selector = {"access": "read", "permission": "deny"}
    resource.patch()

```

### Updating the default-retention period on an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.retention = {"default_period": "P10Y"}
    resource.patch()

```

### Updating the CORS rules of an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "2da46d66-2327-11ef-ab73-005056a7a2dd",
        uuid="dce4e40-2330-11ef-ab73-005056a7a2dd",
    )
    resource.cors = {
        "rules": [
            {
                "allowed_headers": ["x-amz-new-header"],
                "allowed_methods": ["PUT"],
                "allowed_origins": ["http://www.example.in"],
                "expose_headers": ["http://www.example"],
                "id": "id3",
                "max_age_seconds": 10,
            }
        ]
    }
    resource.patch(hydrate=True, return_timeout=0)

```

### Updating the snapshot-policy for an S3 bucket for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.snapshot_policy = {
        "name": "default-1weekly",
        "uuid": "f9c5f090-4ac8-11ef-ba24-005056a7ceb6",
    }
    resource.patch()

```

### Deleting an S3 bucket policy for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.policy = {"statements": []}
    resource.patch()

```

### Deleting CORS rules for an S3 bucket in an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3BucketSvm(
        "3e538980-f0af-11e9-ba68-0050568e9798",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea122",
    )
    resource.cors = {"rules": []}
    resource.patch()

```

### Deleting an S3 bucket for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3BucketSvm

with HostConnection("<mgmt-ip>", username="admin", password="<password>", verify=False):
    resource = S3BucketSvm(
        "12f3ba4c-7ae0-11e9-8c06-0050568ea123",
        uuid="754389d0-7e13-11e9-bfdc-0050568ea123",
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


__all__ = ["S3BucketSvm", "S3BucketSvmSchema"]
__pdoc__ = {
    "S3BucketSvmSchema.resource": False,
    "S3BucketSvmSchema.opts": False,
}


class S3BucketSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3BucketSvm object"""

    aggregates = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_aggregates.S3BucketAggregatesSchema", unknown=EXCLUDE, allow_none=True), data_key="aggregates", allow_none=True)
    r""" A list of aggregates for FlexGroup volume constituents where the bucket is hosted. If this option is not specified, the bucket is auto-provisioned as a FlexGroup volume. The "uuid" field cannot be used with the field "storage_service_level"."""

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
    r""" Specifies the number of constituents or FlexVol volumes per aggregate. A FlexGroup volume consisting of all such constituents across all specified aggregates is created. This option is used along with the aggregates option and cannot be used independently. This field cannot be set using the PATCH method.

Example: 4"""

    cors = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_svm_cors.S3BucketSvmCorsSchema", data_key="cors", unknown=EXCLUDE, allow_none=True)
    r""" Cross-origin resource sharing (CORS) specifies an object associated with a bucket. The CORS configuration enables the bucket to service the cross-origin requests. A request might typically come from an origin with a domain that is different to that of the bucket. By configuring a CORS rule, you can define a combination of allowed origins, HTTP headers and methods that a bucket can use to filter out the cross-origin requests that it can service successfully."""

    encryption = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_svm_encryption.S3BucketSvmEncryptionSchema", data_key="encryption", unknown=EXCLUDE, allow_none=True)
    r""" The encryption field of the s3_bucket_svm."""

    is_consistent_etag = marshmallow_fields.Boolean(
        data_key="is_consistent_etag",
        allow_none=True,
    )
    r""" Specifies whether the NAS bucket returns a consistent ETag across different S3 requests."""

    is_nas_path_mutable = marshmallow_fields.Boolean(
        data_key="is_nas_path_mutable",
        allow_none=True,
    )
    r""" Specifies whether the NAS bucket mapping or association with a NAS volume can change according to the changes in the NAS volume junction-path due to volume operations like mount and unmount and therefore the NAS bucket will have access to any path in a NAS volume that matches the specified nas-path. Or is immutable and therefore the NAS bucket will always have access to the same nas-path that was specified during bucket creation even if the volume junction-path has undergone changes after the bucket creation."""

    lifecycle_management = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_svm_lifecycle_management.S3BucketSvmLifecycleManagementSchema", data_key="lifecycle_management", unknown=EXCLUDE, allow_none=True)
    r""" Lifecycle management is implemented as an object associated with a bucket. It defines rules to be applied against objects within a bucket. These rules are applied in the background and can delete objects."""

    logical_used_size = Size(
        data_key="logical_used_size",
        allow_none=True,
    )
    r""" Specifies the bucket logical used size up to this point. This field cannot be set using the PATCH method."""

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

    protection_status = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_svm_protection_status.S3BucketSvmProtectionStatusSchema", data_key="protection_status", unknown=EXCLUDE, allow_none=True)
    r""" Specifies attributes of bucket protection."""

    qos_policy = marshmallow_fields.Nested("netapp_ontap.resources.qos_policy.QosPolicySchema", data_key="qos_policy", unknown=EXCLUDE, allow_none=True)
    r""" The qos_policy field of the s3_bucket_svm."""

    retention = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_retention.S3BucketRetentionSchema", data_key="retention", unknown=EXCLUDE, allow_none=True)
    r""" Information about the retention-mode and default-retention-period configured on the bucket."""

    role = marshmallow_fields.Str(
        data_key="role",
        validate=enum_validation(['standalone', 'active', 'passive']),
        allow_none=True,
    )
    r""" Specifies the role of the bucket. This field cannot be set in a POST method.

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

Example: 819200000"""

    snapshot_policy = marshmallow_fields.Nested("netapp_ontap.models.s3_bucket_snapshot_policy.S3BucketSnapshotPolicySchema", data_key="snapshot_policy", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the bucket snapshot policy."""

    storage_service_level = marshmallow_fields.Str(
        data_key="storage_service_level",
        validate=enum_validation(['value', 'performance', 'extreme']),
        allow_none=True,
    )
    r""" Specifies the storage service level of the FlexGroup volume on which the bucket should be created. Valid values are "value", "performance" or "extreme". This field cannot be used with the field "aggregates.uuid" or with the "constituents_per_aggregate" in a POST method. This field cannot be set using the PATCH method.

Valid choices:

* value
* performance
* extreme"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_bucket_svm."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['s3', 'nas']),
        allow_none=True,
    )
    r""" Specifies the bucket type. Valid values are "s3"and "nas". This field cannot be set using the PATCH method.

Valid choices:

* s3
* nas"""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" Specifies the unique identifier of the bucket. This field cannot be specified in a POST or PATCH method."""

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
    r""" The volume field of the s3_bucket_svm."""

    @property
    def resource(self):
        return S3BucketSvm

    gettable_fields = [
        "audit_event_selector",
        "comment",
        "cors",
        "encryption",
        "is_consistent_etag",
        "is_nas_path_mutable",
        "lifecycle_management",
        "logical_used_size",
        "name",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.links",
        "qos_policy.max_throughput",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput",
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
    """audit_event_selector,comment,cors,encryption,is_consistent_etag,is_nas_path_mutable,lifecycle_management,logical_used_size,name,nas_path,policy,protection_status,qos_policy.links,qos_policy.max_throughput,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,role,size,snapshot_policy,svm.links,svm.name,svm.uuid,type,uuid,versioning_state,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "audit_event_selector",
        "comment",
        "cors",
        "is_consistent_etag",
        "lifecycle_management",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.max_throughput",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput",
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
    """audit_event_selector,comment,cors,is_consistent_etag,lifecycle_management,nas_path,policy,protection_status,qos_policy.max_throughput,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,size,snapshot_policy,type,versioning_state,"""

    postable_fields = [
        "aggregates.name",
        "aggregates.uuid",
        "audit_event_selector",
        "comment",
        "constituents_per_aggregate",
        "cors",
        "is_consistent_etag",
        "is_nas_path_mutable",
        "lifecycle_management",
        "name",
        "nas_path",
        "policy",
        "protection_status",
        "qos_policy.max_throughput",
        "qos_policy.max_throughput_iops",
        "qos_policy.max_throughput_mbps",
        "qos_policy.min_throughput",
        "qos_policy.min_throughput_iops",
        "qos_policy.min_throughput_mbps",
        "qos_policy.name",
        "qos_policy.uuid",
        "retention",
        "size",
        "snapshot_policy",
        "storage_service_level",
        "type",
        "versioning_state",
    ]
    """aggregates.name,aggregates.uuid,audit_event_selector,comment,constituents_per_aggregate,cors,is_consistent_etag,is_nas_path_mutable,lifecycle_management,name,nas_path,policy,protection_status,qos_policy.max_throughput,qos_policy.max_throughput_iops,qos_policy.max_throughput_mbps,qos_policy.min_throughput,qos_policy.min_throughput_iops,qos_policy.min_throughput_mbps,qos_policy.name,qos_policy.uuid,retention,size,snapshot_policy,storage_service_level,type,versioning_state,"""

class S3BucketSvm(Resource):
    r""" A bucket is a container of objects. Each bucket defines an object namespace. S3 requests specify objects using a bucket-name and object-name pair. An object resides within a bucket. """

    _schema = S3BucketSvmSchema
    _path = "/api/protocols/s3/services/{svm[uuid]}/buckets"
    _keys = ["svm.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the S3 bucket's configuration of an SVM. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
        """Returns a count of all S3BucketSvm resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3BucketSvm resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["S3BucketSvm"] = None,
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
  * `policy` - An access policy for resources (buckets and objects) that defines their permissions. New policies are created after existing policies are deleted. To retain any of the existing policy statements, you need to specify those statements again. Policy conditions can also be modified using this API.
  * `qos_policy` - A QoS policy for buckets.
  * `audit_event_selector` - Audit policy for buckets.  None can be specified for both access and permission to remove audit event selector.
  * `versioning_state` - Versioning state for buckets.
  * `nas_path` - NAS path to which the NAS bucket corresponds to.
  * `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
  * `cors` - Specifying CORS rules enables the bucket to service the cross-origin requests. New CORS rules are created after existing rules are deleted. To retain any of the existing rules, you need to specify those CORS rules again. To remove all the existing CORS rules, specify an empty CORS rules list.
  * `snapshot_policy` - Snapshot policy for the bucket.
  * `is_consistent_etag` - Return a consistent ETag for NAS buckets.
### Related ONTAP commands
* `vserver object-store-server bucket modify`
* `vserver object-store-server bucket policy statement modify`
* `vserver object-store-server bucket policy-statement-condition modify`
* `vserver object-store-server bucket cors-rule create`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3BucketSvm"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3BucketSvm"], NetAppResponse]:
        r"""Creates the S3 bucket configuration of an SVM.
<personalities supports=unified,asar2>
### Important notes
- Each SVM can have one or more bucket configurations.
- Aggregate lists should be specified explicitly. If not specified, then the bucket is auto-provisioned as a FlexGroup.
- Constituents per aggregate specifies the number of components (or FlexVols) per aggregate. Is specified only when an aggregate list is explicitly defined.
- An access policy can be created when a bucket is created.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
- Cross-origin resource sharing (CORS) configuration can be specified when a bucket is created.
</personalities>
<personalities supports=aiml>
### Important notes
- Each SVM can have one or more bucket configurations.
- An access policy can be created when a bucket is created.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
- Cross-origin resource sharing (CORS) configuration can be specified when a bucket is created.
</personalities>
### Required properties
* `svm.uuid` - Existing SVM in which to create the bucket configuration.
* `name` - Bucket name that is to be created.
<personalities supports=unified,asar2>
### Recommended optional properties
* `aggregates` - List of aggregates for the FlexGroup on which the bucket is hosted on.
* `constituents_per_aggregate` - Number of constituents per aggregate.
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying policy enables users to perform operations on buckets; specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - The NAS path to which the NAS bucket corresponds to.
* `use_mirrored_aggregates` - Specifies whether mirrored aggregates are selected when provisioning a FlexGroup volume.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
* `cors` - Specifying CORS rules enables the bucket to service the cross-origin requests.
* `snapshot_policy` - Snapshot policy for the bucket.
* `is_consistent_etag` - Return a consistent ETag for NAS buckets.
* `is_nas_path_mutable` - Specifies whether the NAS bucket mapping with a NAS volume can change according to the changes in the NAS volume junction-path due to volume operations like mount and unmount.
### Default property values
* `size` - 800MB
* `comment` - ""
* `aggregates` - No default value.
* `constituents_per_aggregate` - _4_ , if an aggregates list is specified. Otherwise, no default value.
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `qos-policy` - No default value.
* `versioning_state` - disabled.
* `use_mirrored_aggregates` - _true_ for a MetroCluster configuration and _false_ for a non-MetroCluster configuration.
* `type` - S3.
* `retention.mode` - no_lock
* `is_consistent_etag` - false
</personalities>
<personalities supports=aiml>
### Recommended optional properties
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying policy enables users to perform operations on buckets; specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - The NAS path to which the NAS bucket corresponds to.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
* `cors` - Specifying CORS rules enables the bucket to service the cross-origin requests.
* `snapshot_policy` - Snapshot policy for the bucket.
* `is_consistent_etag` - Return a consistent ETag for NAS buckets.
* `is_nas_path_mutable` - Specifies whether the NAS bucket mapping with a NAS volume can change according to the changes in the NAS volume junction-path due to volume operations like mount and unmount.
### Default property values
* `size` - 800MB
* `comment` - ""
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `qos-policy` - No default value.
* `versioning_state` - disabled.
* `type` - S3.
* `retention.mode` - no_lock
* `is_consistent_etag` - false
</personalities>
### Related ONTAP commands
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket policy-statement-condition create`
* `vserver object-store-server bucket lifecycle-management-rule create`
* `vserver object-store-server bucket cors-rule create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
        records: Iterable["S3BucketSvm"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 bucket configuration of an SVM. An access policy is also deleted on an S3 bucket "delete" command. All CORS rules are also deleted on bucket deletion.
### Related ONTAP commands
* `vserver object-store-server bucket delete`
* `vserver object-store-server bucket policy statement delete`
* `vserver object-store-server bucket policy-statement-condition delete`
* `vserver object-store-server bucket lifecycle-management-rule delete`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the S3 bucket's configuration of an SVM. Note that in order to retrieve S3 bucket policy conditions, the 'fields' option should be set to '**'.
### Related ONTAP commands
* `vserver object-store-server bucket show`
* `vserver object-store-server bucket policy statement show`
* `vserver object-store-server bucket policy-statement-condition show`
* `vserver object-store-server bucket lifecycle-management-rule show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
<personalities supports=unified,asar2>
### Important notes
- Each SVM can have one or more bucket configurations.
- Aggregate lists should be specified explicitly. If not specified, then the bucket is auto-provisioned as a FlexGroup.
- Constituents per aggregate specifies the number of components (or FlexVols) per aggregate. Is specified only when an aggregate list is explicitly defined.
- An access policy can be created when a bucket is created.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
- Cross-origin resource sharing (CORS) configuration can be specified when a bucket is created.
</personalities>
<personalities supports=aiml>
### Important notes
- Each SVM can have one or more bucket configurations.
- An access policy can be created when a bucket is created.
- "qos_policy" can be specified if a bucket needs to be attached to a QoS group policy during creation time.
- "audit_event_selector" can be specified if a bucket needs to be specify access and permission type for auditing.
- Cross-origin resource sharing (CORS) configuration can be specified when a bucket is created.
</personalities>
### Required properties
* `svm.uuid` - Existing SVM in which to create the bucket configuration.
* `name` - Bucket name that is to be created.
<personalities supports=unified,asar2>
### Recommended optional properties
* `aggregates` - List of aggregates for the FlexGroup on which the bucket is hosted on.
* `constituents_per_aggregate` - Number of constituents per aggregate.
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying policy enables users to perform operations on buckets; specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - The NAS path to which the NAS bucket corresponds to.
* `use_mirrored_aggregates` - Specifies whether mirrored aggregates are selected when provisioning a FlexGroup volume.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
* `cors` - Specifying CORS rules enables the bucket to service the cross-origin requests.
* `snapshot_policy` - Snapshot policy for the bucket.
* `is_consistent_etag` - Return a consistent ETag for NAS buckets.
* `is_nas_path_mutable` - Specifies whether the NAS bucket mapping with a NAS volume can change according to the changes in the NAS volume junction-path due to volume operations like mount and unmount.
### Default property values
* `size` - 800MB
* `comment` - ""
* `aggregates` - No default value.
* `constituents_per_aggregate` - _4_ , if an aggregates list is specified. Otherwise, no default value.
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `qos-policy` - No default value.
* `versioning_state` - disabled.
* `use_mirrored_aggregates` - _true_ for a MetroCluster configuration and _false_ for a non-MetroCluster configuration.
* `type` - S3.
* `retention.mode` - no_lock
* `is_consistent_etag` - false
</personalities>
<personalities supports=aiml>
### Recommended optional properties
* `size` - Specifying the bucket size is recommended.
* `policy` - Specifying policy enables users to perform operations on buckets; specifying the resource permissions is recommended.
* `qos_policy` - A QoS policy for buckets.
* `audit_event_selector` - Audit policy for buckets.
* `versioning_state` - Versioning state for buckets.
* `type` - Type of bucket.
* `nas_path` - The NAS path to which the NAS bucket corresponds to.
* `lifecycle_management` - Object store server lifecycle management policy.
* `retention.mode` - Object lock mode supported on the bucket.
* `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
* `cors` - Specifying CORS rules enables the bucket to service the cross-origin requests.
* `snapshot_policy` - Snapshot policy for the bucket.
* `is_consistent_etag` - Return a consistent ETag for NAS buckets.
* `is_nas_path_mutable` - Specifies whether the NAS bucket mapping with a NAS volume can change according to the changes in the NAS volume junction-path due to volume operations like mount and unmount.
### Default property values
* `size` - 800MB
* `comment` - ""
* `policy.statements.actions` - GetObject, PutObject, DeleteObject, ListBucket, ListBucketMultipartUploads, ListMultipartUploadParts, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `policy.statements.principals` - all S3 users and groups in the SVM or the NAS groups.
* `policy.statements.resources` - all objects in the bucket.
* `policy.statements.conditions` - list of bucket policy conditions.
* `qos-policy` - No default value.
* `versioning_state` - disabled.
* `type` - S3.
* `retention.mode` - no_lock
* `is_consistent_etag` - false
</personalities>
### Related ONTAP commands
* `vserver object-store-server bucket create`
* `vserver object-store-server bucket policy statement create`
* `vserver object-store-server bucket policy-statement-condition create`
* `vserver object-store-server bucket lifecycle-management-rule create`
* `vserver object-store-server bucket cors-rule create`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
  * `policy` - An access policy for resources (buckets and objects) that defines their permissions. New policies are created after existing policies are deleted. To retain any of the existing policy statements, you need to specify those statements again. Policy conditions can also be modified using this API.
  * `qos_policy` - A QoS policy for buckets.
  * `audit_event_selector` - Audit policy for buckets.  None can be specified for both access and permission to remove audit event selector.
  * `versioning_state` - Versioning state for buckets.
  * `nas_path` - NAS path to which the NAS bucket corresponds to.
  * `retention.default_period` - Specifies the duration of default-retention applicable for objects on the object store bucket.
  * `cors` - Specifying CORS rules enables the bucket to service the cross-origin requests. New CORS rules are created after existing rules are deleted. To retain any of the existing rules, you need to specify those CORS rules again. To remove all the existing CORS rules, specify an empty CORS rules list.
  * `snapshot_policy` - Snapshot policy for the bucket.
  * `is_consistent_etag` - Return a consistent ETag for NAS buckets.
### Related ONTAP commands
* `vserver object-store-server bucket modify`
* `vserver object-store-server bucket policy statement modify`
* `vserver object-store-server bucket policy-statement-condition modify`
* `vserver object-store-server bucket cors-rule create`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
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
        r"""Deletes the S3 bucket configuration of an SVM. An access policy is also deleted on an S3 bucket "delete" command. All CORS rules are also deleted on bucket deletion.
### Related ONTAP commands
* `vserver object-store-server bucket delete`
* `vserver object-store-server bucket policy statement delete`
* `vserver object-store-server bucket policy-statement-condition delete`
* `vserver object-store-server bucket lifecycle-management-rule delete`
* `vserver object-store-server bucket cors-rule delete`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/buckets`](#docs-object-store-protocols_s3_services_{svm.uuid}_buckets)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


