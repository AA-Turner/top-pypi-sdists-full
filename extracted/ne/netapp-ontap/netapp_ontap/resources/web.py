r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this API to update web services configurations and to retrieve current configurations.</br>
## Retrieving the current web services configuration
The cluster web GET API retrieves the current cluster-wide configuration.</br>
## Updating the current web services configuration
The cluster web PATCH API updates the current cluster-wide configuration.</br>
Once updated, ONTAP restarts the web services to apply the
changes. </br>
When updating the certificate, the certificate UUID of an existing certificate known to ONTAP must
be provided. The certificate must be of type "server".</br>
A "client-ca" certificate must be installed on ONTAP to enable "client_enabled".</br>
The following fields can be used to update the cluster-wide configuration:

* enabled
* http_port
* https_port
* http_enabled
* csrf.protection_enabled
* csrf.token.concurrent_limit
* csrf.token.idle_timeout
* csrf.token.max_timeout
* certificate.uuid
* client_enabled
* ocsp_enabled
## Examples
### Retrieving the cluster-wide web services configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Web

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Web()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Web(
    {
        "csrf": {
            "token": {"concurrent_limit": 500, "max_timeout": 650, "idle_timeout": 900},
            "protection_enabled": True,
        },
        "certificate": {
            "name": "cert1",
            "_links": {
                "self": {
                    "href": "/api/security/certificates/a3bb219d-4382-1fe0-9c06-1070568ea23d"
                }
            },
            "uuid": "a3bb219d-4382-1fe0-9c06-1070568ea23d",
        },
        "ocsp_enabled": False,
        "client_enabled": False,
        "state": "online",
        "enabled": True,
        "_links": {"self": {"href": "/api/cluster/web"}},
        "http_enabled": False,
        "http_port": 80,
        "https_port": 443,
    }
)

```
</div>
</div>

### Updating the cluster-wide web services configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Web

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Web()
    resource.https_port = 446
    resource.csrf = {"token": {"concurrent_limit": 600}}
    resource.patch()

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


__all__ = ["Web", "WebSchema"]
__pdoc__ = {
    "WebSchema.resource": False,
    "WebSchema.opts": False,
}


class WebSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Web object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the web."""

    certificate = marshmallow_fields.Nested("netapp_ontap.models.web_certificate.WebCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" Certificate used by cluster and node management interfaces for TLS connection requests."""

    client_enabled = marshmallow_fields.Boolean(
        data_key="client_enabled",
        allow_none=True,
    )
    r""" Indicates whether client authentication is enabled."""

    csrf = marshmallow_fields.Nested("netapp_ontap.models.web_csrf.WebCsrfSchema", data_key="csrf", unknown=EXCLUDE, allow_none=True)
    r""" The csrf field of the web."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Indicates whether remote clients can connect to the web services."""

    http_enabled = marshmallow_fields.Boolean(
        data_key="http_enabled",
        allow_none=True,
    )
    r""" Indicates whether HTTP is enabled."""

    http_port = Size(
        data_key="http_port",
        allow_none=True,
    )
    r""" HTTP port for cluster-level web services."""

    https_port = Size(
        data_key="https_port",
        allow_none=True,
    )
    r""" HTTPS port for cluster-level web services."""

    ocsp_enabled = marshmallow_fields.Boolean(
        data_key="ocsp_enabled",
        allow_none=True,
    )
    r""" Indicates whether online certificate status protocol verification is enabled."""

    per_address_limit = Size(
        data_key="per_address_limit",
        validate=integer_validation(minimum=24, maximum=999),
        allow_none=True,
    )
    r""" The number of connections that can be processed concurrently from the same remote address.

Example: 42"""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['offline', 'partial', 'mixed', 'online', 'unclustered']),
        allow_none=True,
    )
    r""" State of the cluster-level web services.

Valid choices:

* offline
* partial
* mixed
* online
* unclustered"""

    wait_queue_capacity = Size(
        data_key="wait_queue_capacity",
        allow_none=True,
    )
    r""" The maximum size of the wait queue for connections exceeding the per-address-limit."""

    @property
    def resource(self):
        return Web

    gettable_fields = [
        "links",
        "certificate",
        "client_enabled",
        "csrf",
        "enabled",
        "http_enabled",
        "http_port",
        "https_port",
        "ocsp_enabled",
        "per_address_limit",
        "state",
        "wait_queue_capacity",
    ]
    """links,certificate,client_enabled,csrf,enabled,http_enabled,http_port,https_port,ocsp_enabled,per_address_limit,state,wait_queue_capacity,"""

    patchable_fields = [
        "certificate",
        "client_enabled",
        "csrf",
        "enabled",
        "http_enabled",
        "http_port",
        "https_port",
        "ocsp_enabled",
        "per_address_limit",
        "wait_queue_capacity",
    ]
    """certificate,client_enabled,csrf,enabled,http_enabled,http_port,https_port,ocsp_enabled,per_address_limit,wait_queue_capacity,"""

    postable_fields = [
        "certificate",
        "client_enabled",
        "csrf",
        "enabled",
        "http_enabled",
        "http_port",
        "https_port",
        "ocsp_enabled",
        "per_address_limit",
        "wait_queue_capacity",
    ]
    """certificate,client_enabled,csrf,enabled,http_enabled,http_port,https_port,ocsp_enabled,per_address_limit,wait_queue_capacity,"""

class Web(Resource):
    """Allows interaction with Web objects on the host"""

    _schema = WebSchema
    _path = "/api/cluster/web"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the web services configuration.
### Learn more
* [`DOC /cluster/web`](#docs-cluster-cluster_web)"""
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
        r"""Updates the web services configuration.
### Related ONTAP commands
* `system services web modify`

### Learn more
* [`DOC /cluster/web`](#docs-cluster-cluster_web)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



