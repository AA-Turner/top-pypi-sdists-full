r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Use this API to invoke and retrieve AutoSupport messages from the nodes in the cluster.<p/>
This API supports POST and GET calls. Use a POST call to invoke AutoSupport and a GET call to retrieve AutoSupport messages.
---
## Examples
### Invoking an AutoSupport on all nodes in the cluster
The following example invokes an AutoSupport on every node in the cluster.
Note that AutoSupport is invoked on all nodes in the cluster if the `node` parameter is omitted. Also, note that the `subject` line is the same when invoking on all nodes.<p/>
By default, the response is an empty object. If `return_records=true` is passed in the request, the response includes information about the node and the index of the invoked AutoSupport message.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutosupportMessage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutosupportMessage()
    resource.message = "test_msg"
    resource.type = "all"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AutosupportMessage(
    {
        "node": {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
                }
            },
            "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        },
        "index": 4,
    }
)

```
</div>
</div>

---
### Invoking an AutoSupport on a single node
The following examples invoke an AutoSupport on a single node in the cluster.
Note that AutoSupport is invoked on all nodes in the cluster if the `node` parameter is omitted. You can specify the node-name with either `node` or `node.name` parameter. You can also specify UUID of the node with the `node.uuid` parameter.<p/>
By default, the response is an empty object. If `return_records=true` is passed in the request, the response includes information about the node and the index of the invoked AutoSupport message.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutosupportMessage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutosupportMessage()
    resource.message = "test_msg"
    resource.type = "test"
    resource.node = {"name": "node1"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
AutosupportMessage(
    {
        "node": {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
                }
            },
            "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        },
        "index": 8,
    }
)

```
</div>
</div>

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutosupportMessage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutosupportMessage()
    resource.message = "test_msg"
    resource.type = "test"
    resource.node.name = "node2"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
AutosupportMessage(
    {
        "node": {
            "name": "node2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
                }
            },
            "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
        },
        "index": 4,
    }
)

```
</div>
</div>

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutosupportMessage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AutosupportMessage()
    resource.message = "test_msg"
    resource.type = "test"
    resource.node.uuid = "092e0298-f250-11e8-9a05-005056bb6666"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
AutosupportMessage(
    {
        "node": {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
                }
            },
            "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
        },
        "index": 5,
    }
)

```
</div>
</div>

---
### Retrieving AutoSupport messages from all nodes in the cluster
The following example retrieves AutoSupport messages from every node in the cluster.
Note that if the <i>fields=*</i> parameter is not specified, only node, index, and destination fields are returned.
Filters can be added on the fields to limit the results.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutosupportMessage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(AutosupportMessage.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    AutosupportMessage(
        {
            "destination": "smtp",
            "subject": "USER_TRIGGERED (TEST:test_msg)",
            "generated_on": "2019-03-28T10:18:04-04:00",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
                    }
                },
                "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
            },
            "state": "ignore",
            "index": 1,
        }
    ),
    AutosupportMessage(
        {
            "destination": "http",
            "subject": "USER_TRIGGERED (TEST:test_msg)",
            "generated_on": "2019-03-28T10:18:04-04:00",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
                    }
                },
                "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
            },
            "state": "sent_successful",
            "index": 1,
        }
    ),
    AutosupportMessage(
        {
            "destination": "noteto",
            "subject": "USER_TRIGGERED (TEST:test_msg)",
            "generated_on": "2019-03-28T10:18:04-04:00",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
                    }
                },
                "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
            },
            "state": "ignore",
            "index": 1,
        }
    ),
    AutosupportMessage(
        {
            "destination": "smtp",
            "subject": "USER_TRIGGERED (TEST:test_msg)",
            "generated_on": "2019-03-28T10:18:06-04:00",
            "node": {
                "name": "node2",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
                    }
                },
                "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
            },
            "state": "ignore",
            "index": 1,
        }
    ),
    AutosupportMessage(
        {
            "destination": "http",
            "subject": "USER_TRIGGERED (TEST:test_msg)",
            "generated_on": "2019-03-28T10:18:06-04:00",
            "node": {
                "name": "node2",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
                    }
                },
                "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
            },
            "state": "sent_successful",
            "index": 1,
        }
    ),
    AutosupportMessage(
        {
            "destination": "noteto",
            "subject": "USER_TRIGGERED (TEST:test_msg)",
            "generated_on": "2019-03-28T10:18:06-04:00",
            "node": {
                "name": "node2",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/e47d2630-f250-11e8-b186-005056bb5cab"
                    }
                },
                "uuid": "e47d2630-f250-11e8-b186-005056bb5cab",
            },
            "state": "ignore",
            "index": 1,
        }
    ),
]

```
</div>
</div>

---
### Retrieving AutoSupport messages from a specific node and has 'sent_successful' state
The following example retrieves AutoSupport messages from a specific node in the cluster.
Note that if the `fields=*` parameter is not specified, only node, index, and destination fields are returned.
This example uses a filter on the `node.name` and `state` fields. You can add filters to any fields in the response.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AutosupportMessage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            AutosupportMessage.get_collection(
                state="sent_successful",
                fields="*",
                return_timeout=15,
                **{"node.name": "node1"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
[
    AutosupportMessage(
        {
            "destination": "http",
            "subject": "USER_TRIGGERED (TEST:test_msg)",
            "generated_on": "2019-03-28T10:18:04-04:00",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/092e0298-f250-11e8-9a05-005056bb6666"
                    }
                },
                "uuid": "092e0298-f250-11e8-9a05-005056bb6666",
            },
            "state": "sent_successful",
            "index": 1,
        }
    )
]

```
</div>
</div>

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


__all__ = ["AutosupportMessage", "AutosupportMessageSchema"]
__pdoc__ = {
    "AutosupportMessageSchema.resource": False,
    "AutosupportMessageSchema.opts": False,
}


class AutosupportMessageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AutosupportMessage object"""

    destination = marshmallow_fields.Str(
        data_key="destination",
        validate=enum_validation(['smtp', 'http', 'noteto', 'retransmit']),
        allow_none=True,
    )
    r""" Destination for the AutoSupport

Valid choices:

* smtp
* http
* noteto
* retransmit"""

    error = marshmallow_fields.Nested("netapp_ontap.models.autosupport_message_error.AutosupportMessageErrorSchema", data_key="error", unknown=EXCLUDE, allow_none=True)
    r""" Last error during delivery attempt. Empty if "status=sent-successful"."""

    generated_on = ImpreciseDateTime(
        data_key="generated_on",
        allow_none=True,
    )
    r""" Date and Time of AutoSupport generation in ISO-8601 format

Example: 2019-03-25T21:30:04.000+0000"""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Sequence number of the AutoSupport

Example: 9"""

    message = marshmallow_fields.Str(
        data_key="message",
        allow_none=True,
    )
    r""" Message included in the AutoSupport subject

Example: invoked_test_autosupport_rest"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the autosupport_message."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['initializing', 'collection_failed', 'collection_in_progress', 'queued', 'transmitting', 'sent_successful', 'ignore', 're_queued', 'transmission_failed', 'ondemand_ignore', 'cancelled']),
        allow_none=True,
    )
    r""" State of AutoSupport delivery

Valid choices:

* initializing
* collection_failed
* collection_in_progress
* queued
* transmitting
* sent_successful
* ignore
* re_queued
* transmission_failed
* ondemand_ignore
* cancelled"""

    subject = marshmallow_fields.Str(
        data_key="subject",
        allow_none=True,
    )
    r""" Subject line for the AutoSupport

Example: WEEKLY_LOG"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['test', 'performance', 'all']),
        allow_none=True,
    )
    r""" Type of AutoSupport collection to issue

Valid choices:

* test
* performance
* all"""

    uri = marshmallow_fields.Str(
        data_key="uri",
        allow_none=True,
    )
    r""" Alternate destination for the AutoSupport

Example: https://1.2.3.4/delivery_uri"""

    @property
    def resource(self):
        return AutosupportMessage

    gettable_fields = [
        "destination",
        "error",
        "generated_on",
        "index",
        "node.links",
        "node.name",
        "node.uuid",
        "state",
        "subject",
    ]
    """destination,error,generated_on,index,node.links,node.name,node.uuid,state,subject,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "message",
        "node.name",
        "node.uuid",
        "type",
        "uri",
    ]
    """message,node.name,node.uuid,type,uri,"""

class AutosupportMessage(Resource):
    """Allows interaction with AutosupportMessage objects on the host"""

    _schema = AutosupportMessageSchema
    _path = "/api/support/autosupport/messages"
    _keys = ["node.uuid", "index", "destination"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves AutoSupport message history from all nodes in the cluster.<p/>
There can be a short delay on invoked AutoSupport messages showing in history, dependent on processing of other AutoSupports in the queue.
### Related ONTAP commands
* `system node autosupport history show`
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)
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
        """Returns a count of all AutosupportMessage resources that match the provided query"""
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
        """Returns a list of RawResources that represent AutosupportMessage resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["AutosupportMessage"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["AutosupportMessage"], NetAppResponse]:
        r"""Creates and sends an AutoSupport message with the provided input parameters.<p/>
Important note:
* By default, the response is an empty object. If `return_records=true` is passed in the request, the response includes information about the node and the index of the invoked AutoSupport message.
### Recommended optional properties
* `message` - Message included in the AutoSupport subject. Use this to identify the generated AutoSupport message.
### Default property values
If not specified in POST, the following are the default property values:
* `type` - _all_
* `node.name` or `node.uuid` - Not specifying these properties invokes AutoSupport on all nodes in the cluster.
### Related ONTAP commands
* `system node autosupport invoke`
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves AutoSupport message history from all nodes in the cluster.<p/>
There can be a short delay on invoked AutoSupport messages showing in history, dependent on processing of other AutoSupports in the queue.
### Related ONTAP commands
* `system node autosupport history show`
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information about a single Autosupport message.
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)"""
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
        r"""Creates and sends an AutoSupport message with the provided input parameters.<p/>
Important note:
* By default, the response is an empty object. If `return_records=true` is passed in the request, the response includes information about the node and the index of the invoked AutoSupport message.
### Recommended optional properties
* `message` - Message included in the AutoSupport subject. Use this to identify the generated AutoSupport message.
### Default property values
If not specified in POST, the following are the default property values:
* `type` - _all_
* `node.name` or `node.uuid` - Not specifying these properties invokes AutoSupport on all nodes in the cluster.
### Related ONTAP commands
* `system node autosupport invoke`
### Learn more
* [`DOC /support/autosupport/messages`](#docs-support-support_autosupport_messages)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)




