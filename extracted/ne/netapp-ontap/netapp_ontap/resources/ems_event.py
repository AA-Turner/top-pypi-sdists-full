r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Queries a live collection of observed events on the system.
Note: The `filter.name` parameter is used to pass a filter to be applied to the event collection returned. To retrieve the list of available filters, refer to [/support/ems/filters](#/docs/support/ems_filter_collection_get)
## Example
### Querying for the latest event received by EMS
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsEvent

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(EmsEvent.get_collection(fields="message.name", max_records=1)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    EmsEvent(
        {
            "message": {"name": "raid.aggr.log.CP.count"},
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f087b8e3-99ac-11e8-b5a5-005056bb4ec7"
                    }
                },
                "uuid": "f087b8e3-99ac-11e8-b5a5-005056bb4ec7",
            },
            "_links": {"self": {"href": "/api/support/ems/events/node1/661"}},
            "index": 661,
        }
    )
]

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


__all__ = ["EmsEvent", "EmsEventSchema"]
__pdoc__ = {
    "EmsEventSchema.resource": False,
    "EmsEventSchema.opts": False,
}


class EmsEventSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsEvent object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.ems_event_links.EmsEventLinksSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_event."""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Index of the event. Returned by default.

Example: 1"""

    log_message = marshmallow_fields.Str(
        data_key="log_message",
        allow_none=True,
    )
    r""" A formatted text string populated with parameter details. Returned by default."""

    message = marshmallow_fields.Nested("netapp_ontap.models.ems_event_message1.EmsEventMessage1Schema", data_key="message", unknown=EXCLUDE, allow_none=True)
    r""" The message field of the ems_event."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the ems_event."""

    parameters = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_event_parameter.EmsEventParameterSchema", unknown=EXCLUDE, allow_none=True), data_key="parameters", allow_none=True)
    r""" A list of parameters provided with the EMS event."""

    source = marshmallow_fields.Str(
        data_key="source",
        allow_none=True,
    )
    r""" Source"""

    time = ImpreciseDateTime(
        data_key="time",
        allow_none=True,
    )
    r""" Timestamp of the event. Returned by default."""

    @property
    def resource(self):
        return EmsEvent

    gettable_fields = [
        "links",
        "index",
        "log_message",
        "message",
        "node.links",
        "node.name",
        "node.uuid",
        "parameters",
        "source",
        "time",
    ]
    """links,index,log_message,message,node.links,node.name,node.uuid,parameters,source,time,"""

    patchable_fields = [
        "log_message",
    ]
    """log_message,"""

    postable_fields = [
    ]
    """"""

class EmsEvent(Resource):
    """Allows interaction with EmsEvent objects on the host"""

    _schema = EmsEventSchema
    _path = "/api/support/ems/events"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of observed events.
### Related ONTAP commands
* `event log show`

### Learn more
* [`DOC /support/ems/events`](#docs-support-support_ems_events)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all EmsEvent resources that match the provided query"""
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
        """Returns a list of RawResources that represent EmsEvent resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of observed events.
### Related ONTAP commands
* `event log show`

### Learn more
* [`DOC /support/ems/events`](#docs-support-support_ems_events)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






