r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to ping the BlueXP cloud service. The POST operation retrieves the details about service reachability, configurability, and ping latency.
## Performing a ping operation
You can perform a ping operation by issuing a POST request on /cluster/mediator-ping. Parameters are provided in the body of the POST request. There is only one required parameter.
### Required configuration fields
These fields are always required for any POST /cluster/mediator-ping request.

* `type`         - Specifies the type of the mediator.
<br/>
---
## Examples
POST request body for a ping to the BlueXP cloud service.
```
# API
/api/cluster/mediator-ping
```
### POST request body from a file
```
ping_post_body.txt:
{
  "type": "cloud"
}
curl -X POST https://<mgmt-ip>/api/cluster/mediator-ping -d "@ping_post_body.txt"
```
### Inline POST request body
```
curl -X POST https://<mgmt-ip>/api/cluste/mediator-ping -d '{"type":"cloud"}'
```
### POST request response
```
HTTP/1.1 200 OK
Cache-Control: no-cache,no-store,must-revalidate
Connection: close
Date: Mon, 03 Mar 2025 16:40:20 GMT
Server: libzapid-httpd
Vary: Accept-Encoding,Origin
Content-Length: 69
Content-Type: application/hal+json
Client-Date: Mon, 03 Mar 2025 16:40:20 GMT
Client-Peer: 10.235.144.44:80
Client-Response-Num: 1
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors: 'self'
X-Content-Type-Options: nosniff
{
  "reachable": true,
  "latency_ms": 50,
  "configurable": true,
  "high_latency": false,
  "proxy_configured": true,
  "proxy_used": true,
  "timeout_occurred": false
}
```"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MediatorPing", "MediatorPingSchema"]
__pdoc__ = {
    "MediatorPingSchema.resource": False,
    "MediatorPingSchema.opts": False,
    "MediatorPing": False,
}


class MediatorPingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MediatorPing object"""

    configurable = marshmallow_fields.Boolean(data_key="configurable", allow_none=True)
    r""" Indicates if the BlueXP cloud mediator is configurable. This depends on whether the ping latency is within a threshold.

Example: true """

    high_latency = marshmallow_fields.Boolean(data_key="high_latency", allow_none=True)
    r""" Indicates if the ping latency of the BlueXP cloud server is greater than a threshold.

Example: false """

    latency_ms = Size(data_key="latency_ms", allow_none=True)
    r""" Ping latency in milliseconds.

Example: 150 """

    proxy_configured = marshmallow_fields.Boolean(data_key="proxy_configured", allow_none=True)
    r""" Indicates if the HTTP proxy is configured on the cluster for the REST API calls to the BlueXP cloud server.

Example: true """

    proxy_used = marshmallow_fields.Boolean(data_key="proxy_used", allow_none=True)
    r""" Indicates if the HTTP proxy is used for the ping to the BlueXP cloud server.

Example: true """

    reachable = marshmallow_fields.Boolean(data_key="reachable", allow_none=True)
    r""" Ping status of the BlueXP cloud service.

Example: true """

    timeout_occurred = marshmallow_fields.Boolean(data_key="timeout_occurred", allow_none=True)
    r""" Indicates if the ping to the BlueXP cloud server failed due to a timeout.

Example: false """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Mediator type.

Valid choices:

* cloud
* on_prem """

    @property
    def resource(self):
        return MediatorPing

    gettable_fields = [
        "configurable",
        "high_latency",
        "latency_ms",
        "proxy_configured",
        "proxy_used",
        "reachable",
        "timeout_occurred",
        "type",
    ]
    """configurable,high_latency,latency_ms,proxy_configured,proxy_used,reachable,timeout_occurred,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "type",
    ]
    """type,"""


class MediatorPing(Resource):

    _schema = MediatorPingSchema
