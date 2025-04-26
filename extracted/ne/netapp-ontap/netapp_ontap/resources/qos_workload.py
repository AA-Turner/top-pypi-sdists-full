r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Quality of Service Workloads
A QoS workload represents a storage object that is tracked by QoS.
<br />
---
## Examples
### Retrieving a list of QoS workloads from the cluster
The following example retrieves all the workloads in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosWorkload

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(QosWorkload.get_collection()))

```

---
### Retrieving a specific QoS workload from the cluster
The following example retrieves a requested workload from the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosWorkload

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QosWorkload(uuid="77b68b1c-a458-11eb-baaa-005056bb873e")
    resource.get()
    print(resource)

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


__all__ = ["QosWorkload", "QosWorkloadSchema"]
__pdoc__ = {
    "QosWorkloadSchema.resource": False,
    "QosWorkloadSchema.opts": False,
}


class QosWorkloadSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QosWorkload object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the qos_workload."""

    file = marshmallow_fields.Str(
        data_key="file",
        allow_none=True,
    )
    r""" Name of the file."""

    lun = marshmallow_fields.Str(
        data_key="lun",
        allow_none=True,
    )
    r""" Name of the LUN. The name of the LUN will be displayed as "(unknown)" if the name cannot be retrieved."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the QoS workload.

Example: volume1-wid123"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.qos_policy_group.QosPolicyGroupSchema", data_key="policy", unknown=EXCLUDE, allow_none=True)
    r""" The policy field of the qos_workload."""

    qtree = marshmallow_fields.Str(
        data_key="qtree",
        allow_none=True,
    )
    r""" Name of the Qtree."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the qos_workload."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The uuid field of the qos_workload.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    volume = marshmallow_fields.Str(
        data_key="volume",
        allow_none=True,
    )
    r""" Name of the volume. The name of the volume will be displayed as "(unknown)" if the name cannot be retrieved.

Example: volume1"""

    wid = Size(
        data_key="wid",
        allow_none=True,
    )
    r""" Workload ID of the QoS workload.

Example: 123"""

    workload_class = marshmallow_fields.Str(
        data_key="workload_class",
        validate=enum_validation(['undefined', 'preset', 'user_defined', 'system_defined', 'autovolume', 'load_control']),
        allow_none=True,
    )
    r""" Class of the QoS workload.

Valid choices:

* undefined
* preset
* user_defined
* system_defined
* autovolume
* load_control"""

    @property
    def resource(self):
        return QosWorkload

    gettable_fields = [
        "links",
        "file",
        "lun",
        "name",
        "policy.links",
        "policy.name",
        "policy.uuid",
        "qtree",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "volume",
        "wid",
        "workload_class",
    ]
    """links,file,lun,name,policy.links,policy.name,policy.uuid,qtree,svm.links,svm.name,svm.uuid,uuid,volume,wid,workload_class,"""

    patchable_fields = [
        "name",
        "policy.name",
        "policy.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """name,policy.name,policy.uuid,svm.name,svm.uuid,"""

    postable_fields = [
        "name",
        "policy.name",
        "policy.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """name,policy.name,policy.uuid,svm.name,svm.uuid,"""

class QosWorkload(Resource):
    """Allows interaction with QosWorkload objects on the host"""

    _schema = QosWorkloadSchema
    _path = "/api/storage/qos/workloads"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of QoS workloads.
### Learn more
* [`DOC /storage/qos/workloads`](#docs-storage-storage_qos_workloads)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all QosWorkload resources that match the provided query"""
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
        """Returns a list of RawResources that represent QosWorkload resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of QoS workloads.
### Learn more
* [`DOC /storage/qos/workloads`](#docs-storage-storage_qos_workloads)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific QoS workload.
### Related ONTAP command
* `qos workload show`

### Learn more
* [`DOC /storage/qos/workloads`](#docs-storage-storage_qos_workloads)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





