r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Quality of Service Configuration
A QoS policy defines measurable service level objectives (SLOs) that apply to the storage objects with which the policy is associated. There are two types of policies that can be configured: fixed, which defines a fixed SLO, or adaptive which defines a variable SLO for a storage object. Adaptive policies vary the SLO depending on the space usage of the storage object. A policy can be either a fixed policy or an adaptive one, not both.
<br />
Service level objectives include minimum and maximum limits on throughput in terms of IOPS. Only maximum limits can be set in terms of both IOPS and/or throughput (MB/s). A QoS policy can be used to enforce SLOs for multiple storage objects by specifying "capacity_shared" to true. For example, if a QoS policy with "capacity_shared" is set to true and it has maximum_throughput_iops set to 1000, and this policy is assigned to four volumes, then the combined throughput of all four volumes is limited to 1000 IOPS. If "capacity_shared" is set to false then, each storage object will have it's SLOs enforced individually. For example, in the previous case if the same policy was applied to four volumes but with "capacity_shared" set to false, then each of the volumes would be limited to 1000 IOPS individually. Once "capacity_shared" is set, it cannot be modified.
<br />
Adaptive parameters can specify the variable SLOs in terms of IOPS/TB. The actual IOPS enforced on the storage object can be calculated using the allocated space on the storage object. The policies are enforced individually amongst storage objects.
## Examples
### 1) Create a fixed QoS policy
The following example shows how to create a fixed QoS policy to limit throughput for a storage object between 5000 IOPS and 10000 IOPS which has capacity_shared set to false. This QoS policy can be used as a template to apply on multiple storage objects to provide individual SLOs to each object.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosPolicy

with HostConnection(
    "172.21.69.245", username="admin", password="password", verify=False
):
    resource = QosPolicy()
    resource.fixed = {
        "capacity_shared": False,
        "max_throughput_iops": 10000,
        "min_throughput_iops": 5000,
    }
    resource.name = "qos_policy_5000_to_10000_iops"
    resource.svm = {"name": "vs0"}
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```

---
### 2) Create an adaptive QoS policy
The following example shows how to create an adaptive QoS policy which provides 5000 IOPS per GB of allocated space for a storage object with a peak of 6000 IOPS. Minimum IOPS regardless of allocated space are 1000 IOPS.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosPolicy

with HostConnection(
    "172.21.69.245", username="admin", password="password", verify=False
):
    resource = QosPolicy()
    resource.adaptive = {
        "absolute_min_iops": 1000,
        "expected_iops": 5000,
        "expected_iops_allocation": "used_space",
        "peak_iops": 6000,
        "peak_iops_allocation": "allocated_space",
    }
    resource.name = "adaptive_pg_5k_to_6k"
    resource.svm = {"name": "vs0"}
    resource.post(hydrate=True, return_timeout=0)
    print(resource)

```

----
### 3) Update an existing QoS policy
The following example shows how to update SLOs of an existing QoS policy and also rename it.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosPolicy

with HostConnection(
    "172.21.69.245", username="admin", password="password", verify=False
):
    resource = QosPolicy(uuid="d38bafc0-5a51-11e9-bd5b-005056ac6f1f")
    resource.fixed = {"max_throughput_iops": 15000, "min_throughput_iops": 10000}
    resource.name = "qos_policy_10k_to_15k_iops"
    resource.patch(hydrate=True, return_timeout=0)

```

---
### 4) Delete an existing QoS policy
When a QoS policy is deleted any associations of the policy with a storage objects are also removed.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosPolicy

with HostConnection(
    "172.21.69.245", username="admin", password="password", verify=False
):
    resource = QosPolicy(uuid="d38bafc0-5a51-11e9-bd5b-005056ac6f1f")
    resource.delete(return_timeout=0)

```

---"""

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


__all__ = ["QosPolicy", "QosPolicySchema"]
__pdoc__ = {
    "QosPolicySchema.resource": False,
    "QosPolicySchema.opts": False,
}


class QosPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QosPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the qos_policy."""

    adaptive = marshmallow_fields.Nested("netapp_ontap.models.qos_policy_adaptive.QosPolicyAdaptiveSchema", data_key="adaptive", unknown=EXCLUDE, allow_none=True)
    r""" Adaptive QoS policy-groups define measurable service level objectives (SLOs) that adjust based on the storage object used space and the storage object allocated space."""

    fixed = marshmallow_fields.Nested("netapp_ontap.models.qos_policy_fixed.QosPolicyFixedSchema", data_key="fixed", unknown=EXCLUDE, allow_none=True)
    r""" QoS policy-groups define a fixed service level objective (SLO) for a storage object."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the QoS policy.

Example: extreme"""

    object_count = Size(
        data_key="object_count",
        allow_none=True,
    )
    r""" Number of objects attached to this policy."""

    pgid = Size(
        data_key="pgid",
        allow_none=True,
    )
    r""" Policy group ID of the QoS policy."""

    policy_class = marshmallow_fields.Str(
        data_key="policy_class",
        validate=enum_validation(['undefined', 'preset', 'user_defined', 'system_defined', 'autovolume', 'load_control']),
        allow_none=True,
    )
    r""" Class of the QoS policy.

Valid choices:

* undefined
* preset
* user_defined
* system_defined
* autovolume
* load_control"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the qos_policy."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the qos_policy.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return QosPolicy

    gettable_fields = [
        "links",
        "adaptive",
        "fixed",
        "name",
        "object_count",
        "pgid",
        "policy_class",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,adaptive,fixed,name,object_count,pgid,policy_class,scope,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "adaptive",
        "fixed",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """adaptive,fixed,name,svm.name,svm.uuid,"""

    postable_fields = [
        "adaptive",
        "fixed",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """adaptive,fixed,name,svm.name,svm.uuid,"""

class QosPolicy(Resource):
    """Allows interaction with QosPolicy objects on the host"""

    _schema = QosPolicySchema
    _path = "/api/storage/qos/policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of QoS policies.
### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all QosPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent QosPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["QosPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Update a specific QoS policy.
### Related ONTAP commands
* `qos policy-group modify`
* `qos adaptive-policy-group modify`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["QosPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["QosPolicy"], NetAppResponse]:
        r"""Creates a QoS policy.
### Required properties
* `svm.uuid` or `svm.name` - The existing SVM owning the QoS policy.
* `name` - The name of the QoS policy.
* `fixed.*` or `adaptive.*` - Either of the fixed or adaptive parameters.
### Default property values
* If `fixed.*` parameters are specified, then capacity.shared is set to false by default.
### Related ONTAP commands
* `qos policy-group create`
* `qos adaptive-policy-group create`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["QosPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a QoS policy. All QoS workloads associated with the policy are removed.
### Related ONTAP commands
* `qos policy-group delete`
* `qos adaptive-policy-group delete`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of QoS policies.
### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific QoS policy.
### Related ONTAP commands
* `qos policy-group show`
* `qos adaptive-policy-group show`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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
        r"""Creates a QoS policy.
### Required properties
* `svm.uuid` or `svm.name` - The existing SVM owning the QoS policy.
* `name` - The name of the QoS policy.
* `fixed.*` or `adaptive.*` - Either of the fixed or adaptive parameters.
### Default property values
* If `fixed.*` parameters are specified, then capacity.shared is set to false by default.
### Related ONTAP commands
* `qos policy-group create`
* `qos adaptive-policy-group create`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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
        r"""Update a specific QoS policy.
### Related ONTAP commands
* `qos policy-group modify`
* `qos adaptive-policy-group modify`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
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
        r"""Deletes a QoS policy. All QoS workloads associated with the policy are removed.
### Related ONTAP commands
* `qos policy-group delete`
* `qos adaptive-policy-group delete`

### Learn more
* [`DOC /storage/qos/policies`](#docs-storage-storage_qos_policies)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


