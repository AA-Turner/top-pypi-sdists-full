r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Allows access to the EMS event catalog. The catalog contains a list of all events supported by the system and their corresponding descriptions, the reason for an event occurrence, and how to correct issues related to the event.
## Example
### Querying for the first event that has a message name beginning with 'C'
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsMessage

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(EmsMessage.get_collection(fields="name", max_records=1, name="C*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    EmsMessage(
        {
            "name": "CR.Data.File.Inaccessible",
            "_links": {
                "self": {"href": "/api/support/ems/messages/CR.Data.File.Inaccessible"}
            },
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


__all__ = ["EmsMessage", "EmsMessageSchema"]
__pdoc__ = {
    "EmsMessageSchema.resource": False,
    "EmsMessageSchema.opts": False,
}


class EmsMessageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsMessage object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_message."""

    corrective_action = marshmallow_fields.Str(
        data_key="corrective_action",
        allow_none=True,
    )
    r""" Corrective action"""

    deprecated = marshmallow_fields.Boolean(
        data_key="deprecated",
        allow_none=True,
    )
    r""" Is deprecated?

Example: true"""

    description = marshmallow_fields.Str(
        data_key="description",
        allow_none=True,
    )
    r""" Description of the event."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name of the event.

Example: callhome.spares.low"""

    severity = marshmallow_fields.Str(
        data_key="severity",
        validate=enum_validation(['emergency', 'alert', 'error', 'notice', 'informational', 'debug']),
        allow_none=True,
    )
    r""" Severity

Valid choices:

* emergency
* alert
* error
* notice
* informational
* debug"""

    snmp_trap_type = marshmallow_fields.Str(
        data_key="snmp_trap_type",
        validate=enum_validation(['standard', 'built_in', 'severity_based']),
        allow_none=True,
    )
    r""" SNMP trap type

Valid choices:

* standard
* built_in
* severity_based"""

    @property
    def resource(self):
        return EmsMessage

    gettable_fields = [
        "links",
        "corrective_action",
        "deprecated",
        "description",
        "name",
        "severity",
        "snmp_trap_type",
    ]
    """links,corrective_action,deprecated,description,name,severity,snmp_trap_type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class EmsMessage(Resource):
    """Allows interaction with EmsMessage objects on the host"""

    _schema = EmsMessageSchema
    _path = "/api/support/ems/messages"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the event catalog definitions.
### Related ONTAP commands
* `event catalog show`

### Learn more
* [`DOC /support/ems/messages`](#docs-support-support_ems_messages)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all EmsMessage resources that match the provided query"""
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
        """Returns a list of RawResources that represent EmsMessage resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the event catalog definitions.
### Related ONTAP commands
* `event catalog show`

### Learn more
* [`DOC /support/ems/messages`](#docs-support-support_ems_messages)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






