r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

You can use this API to update and retrieve the web services security configuration for each data SVM.</br>
## Updating the web services security configuration
The following fields can be used to update the web services security configuration:

* certificate.uuid
* client_enabled
* ocsp_enabled
When updating the certificate, the certificate UUID of an existing certificate known to ONTAP must
be provided. The certificate must be of type "server".</br>
A "client-ca" certificate must be installed on ONTAP to enable "client_enabled".</br>
## Examples
### Retrieving the web services security configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WebSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = WebSvm("3c1b259d-5789-a2eb-9301-10705682b34f")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
WebSvm(
    {
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
        "_links": {
            "self": {"href": "/api/svm/svms/3c1b259d-5789-a2eb-9301-10705682b34f/web"}
        },
        "svm": {
            "name": "svm2",
            "_links": {
                "self": {"href": "/api/svm/svms/3c1b259d-5789-a2eb-9301-10705682b34f"}
            },
            "uuid": "3c1b259d-5789-a2eb-9301-10705682b34f",
        },
    }
)

```
</div>
</div>

### Updating the web services security configuration
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WebSvm

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = WebSvm("3c1b259d-5789-a2eb-9301-10705682b34f")
    resource.certificate = {"uuid": "56da2799-13bc-2ae4-0c16-0c71244ea2ca"}
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


__all__ = ["WebSvm", "WebSvmSchema"]
__pdoc__ = {
    "WebSvmSchema.resource": False,
    "WebSvmSchema.opts": False,
}


class WebSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebSvm object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the web_svm."""

    certificate = marshmallow_fields.Nested("netapp_ontap.models.web_certificate.WebCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" Certificate used by cluster and node management interfaces for TLS connection requests."""

    client_enabled = marshmallow_fields.Boolean(
        data_key="client_enabled",
        allow_none=True,
    )
    r""" Indicates whether client authentication is enabled."""

    ocsp_enabled = marshmallow_fields.Boolean(
        data_key="ocsp_enabled",
        allow_none=True,
    )
    r""" Indicates whether online certificate status protocol verification is enabled."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the web_svm."""

    @property
    def resource(self):
        return WebSvm

    gettable_fields = [
        "links",
        "certificate",
        "client_enabled",
        "ocsp_enabled",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,certificate,client_enabled,ocsp_enabled,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "certificate",
        "client_enabled",
        "ocsp_enabled",
    ]
    """certificate,client_enabled,ocsp_enabled,"""

    postable_fields = [
        "certificate",
        "client_enabled",
        "ocsp_enabled",
    ]
    """certificate,client_enabled,ocsp_enabled,"""

class WebSvm(Resource):
    """Allows interaction with WebSvm objects on the host"""

    _schema = WebSvmSchema
    _path = "/api/svm/svms/{svm[uuid]}/web"
    _keys = ["svm.uuid"]






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the web services security configuration.
### Learn more
* [`DOC /svm/svms/{svm.uuid}/web`](#docs-svm-svm_svms_{svm.uuid}_web)"""
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
        r"""Updates the web services security configuration.
### Learn more
* [`DOC /svm/svms/{svm.uuid}/web`](#docs-svm-svm_svms_{svm.uuid}_web)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



