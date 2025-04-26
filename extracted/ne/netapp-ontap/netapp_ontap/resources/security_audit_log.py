r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
These APIs return audit log records. The GET requests retrieves all audit log records. An audit log record contains information such as timestamp, node name, index and so on.
<br />
---
## Example
### Retrieving audit log records
The following example shows the audit log records.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAuditLog

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    print(list(SecurityAuditLog.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SecurityAuditLog(
        {
            "location": "172.21.16.89",
            "user": "admin",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/bc9af9da-41bb-11e9-a3db-005056bb27cf"
                    }
                },
                "uuid": "bc9af9da-41bb-11e9-a3db-005056bb27cf",
            },
            "application": "http",
            "state": "pending",
            "input": "GET /api/security/audit/destinations/",
            "index": 4294967299,
            "timestamp": "2019-03-08T11:03:32-05:00",
            "scope": "cluster",
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


__all__ = ["SecurityAuditLog", "SecurityAuditLogSchema"]
__pdoc__ = {
    "SecurityAuditLogSchema.resource": False,
    "SecurityAuditLogSchema.opts": False,
}


class SecurityAuditLogSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityAuditLog object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_audit_log."""

    application = marshmallow_fields.Str(
        data_key="application",
        validate=enum_validation(['internal', 'console', 'rsh', 'telnet', 'ssh', 'ontapi', 'http', 'system']),
        allow_none=True,
    )
    r""" This identifies the "application" by which the request was processed.


Valid choices:

* internal
* console
* rsh
* telnet
* ssh
* ontapi
* http
* system"""

    command_id = marshmallow_fields.Str(
        data_key="command_id",
        allow_none=True,
    )
    r""" This is the command ID for this request.
Each command received on a CLI session is assigned a command ID. This enables you to correlate a request and response."""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Internal index for accessing records with same time/node. This is a 64 bit unsigned value."""

    input = marshmallow_fields.Str(
        data_key="input",
        allow_none=True,
    )
    r""" The request."""

    location = marshmallow_fields.Str(
        data_key="location",
        allow_none=True,
    )
    r""" This identifies the location of the remote user. This is an IP address or "console"."""

    message = marshmallow_fields.Str(
        data_key="message",
        allow_none=True,
    )
    r""" This is an optional field that might contain "error" or "additional information" about the status of a command."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the security_audit_log."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to "svm" when the request is on a data SVM; otherwise set to "cluster".

Valid choices:

* svm
* cluster"""

    session_id = marshmallow_fields.Str(
        data_key="session_id",
        allow_none=True,
    )
    r""" This is the session ID on which the request is received. Each SSH session is assigned a session ID.
Each http/ontapi/snmp request is assigned a unique session ID."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['pending', 'success', 'error']),
        allow_none=True,
    )
    r""" State of of this request.

Valid choices:

* pending
* success
* error"""

    svm = marshmallow_fields.Nested("netapp_ontap.models.security_audit_log_svm.SecurityAuditLogSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" This is the SVM through which the user connected."""

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
        allow_none=True,
    )
    r""" Log entry timestamp. Valid in URL"""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" Username of the remote user."""

    @property
    def resource(self):
        return SecurityAuditLog

    gettable_fields = [
        "links",
        "application",
        "command_id",
        "index",
        "input",
        "location",
        "message",
        "node.links",
        "node.name",
        "node.uuid",
        "scope",
        "session_id",
        "state",
        "svm",
        "timestamp",
        "user",
    ]
    """links,application,command_id,index,input,location,message,node.links,node.name,node.uuid,scope,session_id,state,svm,timestamp,user,"""

    patchable_fields = [
        "scope",
    ]
    """scope,"""

    postable_fields = [
        "scope",
    ]
    """scope,"""

class SecurityAuditLog(Resource):
    """Allows interaction with SecurityAuditLog objects on the host"""

    _schema = SecurityAuditLogSchema
    _path = "/api/security/audit/messages"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the administrative audit log viewer.
### Learn more
* [`DOC /security/audit/messages`](#docs-security-security_audit_messages)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityAuditLog resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityAuditLog resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the administrative audit log viewer.
### Learn more
* [`DOC /security/audit/messages`](#docs-security-security_audit_messages)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






