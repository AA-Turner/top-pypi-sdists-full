r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Quality of Service Options
A QoS option represents a configuration detail that is used by QoS.
<br />
---
## Examples
### Retrieving a QoS option from the cluster
The following example retrieves the QoS option in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosOption

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QosOption()
    resource.get(return_timeout=0)
    print(resource)

```

---
### 2) Update a QoS option
The following example shows how to modify the background task reserve policy to 40%.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import QosOption

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = QosOption()
    resource.background_task_reserve = 40
    resource.patch(hydrate=True, return_timeout=0)

```

----"""

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


__all__ = ["QosOption", "QosOptionSchema"]
__pdoc__ = {
    "QosOptionSchema.resource": False,
    "QosOptionSchema.opts": False,
}


class QosOptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QosOption object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the qos_option."""

    background_task_reserve = Size(
        data_key="background_task_reserve",
        allow_none=True,
    )
    r""" Percentage reserve for critical background tasks.

Example: 33"""

    @property
    def resource(self):
        return QosOption

    gettable_fields = [
        "links",
        "background_task_reserve",
    ]
    """links,background_task_reserve,"""

    patchable_fields = [
        "background_task_reserve",
    ]
    """background_task_reserve,"""

    postable_fields = [
        "background_task_reserve",
    ]
    """background_task_reserve,"""

class QosOption(Resource):
    """Allows interaction with QosOption objects on the host"""

    _schema = QosOptionSchema
    _path = "/api/storage/qos/qos-options"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves QoS options.
This option is available only at diagnostic privilege level and above.
### Related ONTAP commands
* `qos settings cluster-options show`

### Learn more
* [`DOC /storage/qos/qos-options`](#docs-storage-storage_qos_qos-options)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Update a specific QoS option.
This option is available only at diagnostic privilege level and above.
### Related ONTAP commands
* `qos settings cluster-options modify`

### Learn more
* [`DOC /storage/qos/qos-options`](#docs-storage-storage_qos_qos-options)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



