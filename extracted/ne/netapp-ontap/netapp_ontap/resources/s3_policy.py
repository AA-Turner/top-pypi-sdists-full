r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An S3 policy is an object that when associated with a resource, defines their permissions. Buckets and objects are defined as resources. Policies are used to manage access to these resources.
## Examples
### Retrieving all fields for all S3 policies of an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Policy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            S3Policy.get_collection(
                "12f3ba4c-7ae0-11e9-8c06-0050568ea123", fields="*", return_timeout=15
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
    S3Policy(
        {
            "name": "Policy1",
            "comment": "S3 policy.",
            "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
            "statements": [
                {
                    "sid": "FullAccessToBucket1",
                    "effect": "allow",
                    "actions": ["*"],
                    "index": 0,
                    "resources": ["bucket1", "bucket1/*"],
                },
                {
                    "sid": "DenyDeleteObjectAccessToAllResources",
                    "effect": "deny",
                    "actions": ["DeleteObject"],
                    "index": 1,
                    "resources": ["*"],
                },
            ],
        }
    ),
    S3Policy(
        {
            "name": "Policy2",
            "comment": "S3 policy 2.",
            "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
            "statements": [
                {
                    "sid": "AllowGetObjectAccessToAllResources",
                    "effect": "allow",
                    "actions": ["GetObject"],
                    "index": 3,
                    "resources": ["*"],
                },
                {
                    "sid": "DenyAccessToAllResources",
                    "effect": "deny",
                    "actions": ["*"],
                    "index": 3,
                    "resources": ["*"],
                },
            ],
        }
    ),
]

```
</div>
</div>

### Retrieving the specified policy in the SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Policy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Policy("12f3ba4c-7ae0-11e9-8c06-0050568ea123", name="Policy1")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
S3Policy(
    {
        "name": "Policy1",
        "comment": "S3 policy.",
        "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
        "statements": [
            {
                "sid": "DenyAccessToAllResources",
                "effect": "deny",
                "actions": [
                    "GetObject",
                    "PutObject",
                    "DeleteObject",
                    "ListBucket",
                    "ListMyBuckets",
                    "ListBucketMultipartUploads",
                    "ListMultipartUploadParts",
                    "GetObjectTagging",
                    "PutObjectTagging",
                    "DeleteObjectTagging",
                    "GetBucketVersioning",
                    "PutBucketVersioning",
                ],
                "index": 0,
                "resources": ["*"],
            }
        ],
    }
)

```
</div>
</div>

### Creating an S3 policy for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Policy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Policy("12f3ba4c-7ae0-11e9-8c06-0050568ea123")
    resource.comment = "S3 policy."
    resource.name = "Policy1"
    resource.statements = [
        {
            "actions": ["ListBucket", "ListMyBuckets", "CreateBucket", "DeleteBucket"],
            "effect": "allow",
            "resources": ["*"],
            "sid": "AllowListAccessToAllResources",
        }
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
S3Policy(
    {
        "name": "Policy1",
        "comment": "S3 policy.",
        "svm": {"name": "svm1", "uuid": "02c9e252-41be-11e9-81d5-00a0986138f7"},
        "statements": [
            {
                "sid": "AllowListAccessToAllResources",
                "effect": "allow",
                "actions": ["ListBucket", "ListMyBuckets"],
                "index": 5,
                "resources": ["*"],
            }
        ],
    }
)

```
</div>
</div>

### Updating an S3 policy for an SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Policy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Policy("12f3ba4c-7ae0-11e9-8c06-0050568ea123", name="Policy1")
    resource.comment = "S3 policy."
    resource.statements = [
        {
            "actions": [
                "GetObject",
                "PutObject",
                "DeleteObject",
                "ListBucket",
                "ListMyBuckets",
                "CreateBucket",
                "DeleteBucket",
            ],
            "effect": "allow",
            "resources": ["bucket1", "bucket1/*"],
            "sid": "FullAccessToAllResources",
        }
    ]
    resource.patch()

```

### Deleting an S3 policy for a specified SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import S3Policy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = S3Policy("12f3ba4c-7ae0-11e9-8c06-0050568ea123", name="Policy1")
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


__all__ = ["S3Policy", "S3PolicySchema"]
__pdoc__ = {
    "S3PolicySchema.resource": False,
    "S3PolicySchema.opts": False,
}


class S3PolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the S3Policy object"""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=256),
        allow_none=True,
    )
    r""" Can contain any additional information about the S3 policy.

Example: S3 policy."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=128),
        allow_none=True,
    )
    r""" Specifies the name of the policy. A policy name length can range from 1 to 128 characters and can only contain the following combination of characters 0-9, A-Z, a-z, "_", "+", "=", ",", ".","@", and "-". It cannot be specified in a PATCH method.

Example: Policy1"""

    read_only = marshmallow_fields.Boolean(
        data_key="read-only",
        allow_none=True,
    )
    r""" Specifies whether or not the s3 policy is read only. This parameter should not be specified in the POST method."""

    statements = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.s3_policy_statement.S3PolicyStatementSchema", unknown=EXCLUDE, allow_none=True), data_key="statements", allow_none=True)
    r""" Specifies the policy statements."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the s3_policy."""

    @property
    def resource(self):
        return S3Policy

    gettable_fields = [
        "comment",
        "name",
        "read_only",
        "statements",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """comment,name,read_only,statements,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "comment",
        "statements",
    ]
    """comment,statements,"""

    postable_fields = [
        "comment",
        "name",
        "statements",
    ]
    """comment,name,statements,"""

class S3Policy(Resource):
    r""" An S3 policy is an object. It defines resource (bucket, folder or object) permissions. These policies get evaluated when an object store user user makes a request. Permissions in the policies determine whether the request is allowed or denied. """

    _schema = S3PolicySchema
    _path = "/api/protocols/s3/services/{svm[uuid]}/policies"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the S3 policies SVM configuration.
### Related ONTAP commands
* `vserver object-store-server policy show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
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
        """Returns a count of all S3Policy resources that match the provided query"""
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
        """Returns a list of RawResources that represent S3Policy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["S3Policy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the S3 policy configuration of an SVM.
### Important notes
- The following fields can be modified for a policy:
  * `comment` - Any information related to the policy.
  * `statements` - Specifies the array of policy statements.
### Related ONTAP commands
* `vserver object-store-server policy modify`
* `vserver object-store-server policy modify-statement`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["S3Policy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["S3Policy"], NetAppResponse]:
        r"""Creates the S3 policy configuration.
### Important notes
- Each SVM can have one or more s3 policy configurations.
### Required properties
* `svm.uuid` - Existing SVM in which to create the s3 policy configuration.
* `name` - Policy name that is to be created.
### Recommended optional properties
* `comment` - Short description about the S3 policy.
* `statements.effect` - Indicates whether to allow or deny access.
* `statements.actions` - List of actions that can be allowed or denied access. Example: GetObject, PutObject, DeleteObject, ListBucket, ListMyBuckets, ListBucketMultipartUploads, ListMultipartUploadParts, CreateBucket, DeleteBucket, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `statements.resources` - Buckets or objects that can be allowed or denied access.
* `statements.sid` - Statement identifier providing additional information about the statement.
### Related ONTAP commands
* `vserver object-store-server policy create`
* `vserver object-store-server policy add-statement`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
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
        records: Iterable["S3Policy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the S3 policy configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server policy delete`
* `vserver object-store-server policy delete-statement`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the S3 policies SVM configuration.
### Related ONTAP commands
* `vserver object-store-server policy show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the S3 policy configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server policy show`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
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
        r"""Creates the S3 policy configuration.
### Important notes
- Each SVM can have one or more s3 policy configurations.
### Required properties
* `svm.uuid` - Existing SVM in which to create the s3 policy configuration.
* `name` - Policy name that is to be created.
### Recommended optional properties
* `comment` - Short description about the S3 policy.
* `statements.effect` - Indicates whether to allow or deny access.
* `statements.actions` - List of actions that can be allowed or denied access. Example: GetObject, PutObject, DeleteObject, ListBucket, ListMyBuckets, ListBucketMultipartUploads, ListMultipartUploadParts, CreateBucket, DeleteBucket, GetObjectTagging, PutObjectTagging, DeleteObjectTagging, GetBucketVersioning, PutBucketVersioning.
* `statements.resources` - Buckets or objects that can be allowed or denied access.
* `statements.sid` - Statement identifier providing additional information about the statement.
### Related ONTAP commands
* `vserver object-store-server policy create`
* `vserver object-store-server policy add-statement`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
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
        r"""Updates the S3 policy configuration of an SVM.
### Important notes
- The following fields can be modified for a policy:
  * `comment` - Any information related to the policy.
  * `statements` - Specifies the array of policy statements.
### Related ONTAP commands
* `vserver object-store-server policy modify`
* `vserver object-store-server policy modify-statement`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
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
        r"""Deletes the S3 policy configuration of an SVM.
### Related ONTAP commands
* `vserver object-store-server policy delete`
* `vserver object-store-server policy delete-statement`
### Learn more
* [`DOC /protocols/s3/services/{svm.uuid}/policies`](#docs-object-store-protocols_s3_services_{svm.uuid}_policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


