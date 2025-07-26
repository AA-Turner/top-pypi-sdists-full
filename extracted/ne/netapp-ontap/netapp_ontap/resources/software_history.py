r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to retrieve the history details for software installation requests.
<br/>
## Examples
### Retrieving software installation history information
The following example shows how to:<br/>
   - Retrieve the software package installation history information.<br/>
   - Display specific node level software installation history information.<br/>
   - Provide all the attributes by default in response when the self referential link is not present.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SoftwareHistory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SoftwareHistory.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SoftwareHistory(
    {
        "start_time": "2018-09-03T16:18:46+05:30",
        "to_version": "9.5.0",
        "state": "successful",
        "node": {
            "uuid": "58cd3a2b-af63-11e8-8b0d-0050568e7279",
            "name": "sti70-vsim-ucs165n",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/58cd3a2b-af63-11e8-8b0d-0050568e7279"
                }
            },
        },
        "from_version": "9.4.0",
        "end_time": "2018-05-21T10:14:51+05:30",
    }
)

```
</div>
</div>

---
### Learn more

* [`DOC /cluster/software/history`](#docs-cluster-cluster_software_history)"""

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


__all__ = ["SoftwareHistory", "SoftwareHistorySchema"]
__pdoc__ = {
    "SoftwareHistorySchema.resource": False,
    "SoftwareHistorySchema.opts": False,
}


class SoftwareHistorySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareHistory object"""

    end_time = ImpreciseDateTime(
        data_key="end_time",
        allow_none=True,
    )
    r""" Completion time of this installation request.

Example: 2019-02-02T20:00:00.000+0000"""

    from_version = marshmallow_fields.Str(
        data_key="from_version",
        allow_none=True,
    )
    r""" Previous version of node

Example: ONTAP_X1"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the software_history."""

    start_time = ImpreciseDateTime(
        data_key="start_time",
        allow_none=True,
    )
    r""" Start time of this installation request.

Example: 2019-02-02T19:00:00.000+0000"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['successful', 'canceled', 'skip_upgrade']),
        allow_none=True,
    )
    r""" Status of this installation request.

Valid choices:

* successful
* canceled
* skip_upgrade"""

    to_version = marshmallow_fields.Str(
        data_key="to_version",
        allow_none=True,
    )
    r""" Updated version of node

Example: ONTAP_X2"""

    @property
    def resource(self):
        return SoftwareHistory

    gettable_fields = [
        "end_time",
        "from_version",
        "node.links",
        "node.name",
        "node.uuid",
        "start_time",
        "state",
        "to_version",
    ]
    """end_time,from_version,node.links,node.name,node.uuid,start_time,state,to_version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class SoftwareHistory(Resource):
    """Allows interaction with SoftwareHistory objects on the host"""

    _schema = SoftwareHistorySchema
    _path = "/api/cluster/software/history"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the history details for software installation requests.
### Related ONTAP commands
* `cluster image show-update-history`
### Learn more
* [`DOC /cluster/software/history`](#docs-cluster-cluster_software_history)
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
        """Returns a count of all SoftwareHistory resources that match the provided query"""
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
        """Returns a list of RawResources that represent SoftwareHistory resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the history details for software installation requests.
### Related ONTAP commands
* `cluster image show-update-history`
### Learn more
* [`DOC /cluster/software/history`](#docs-cluster-cluster_software_history)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






