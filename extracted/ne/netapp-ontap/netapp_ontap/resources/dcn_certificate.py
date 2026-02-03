r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API endpoint is designed to manage the client certificate during communication between ONTAP and DCN nodes. In this context, ONTAP functions as a client.
The PATCH method is used to update the certificate that ONTAP uses when communicating with DCN (where ONTAP acts as a client), while the GET method retrieves this certificate.
<br />
---
## Examples
### Retrieving the client certificate that ONTAP uses for communication with DCN nodes
The following output shows the client certificate that ONTAP uses for communication with DCN nodes.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnCertificate()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
DcnCertificate(
    {
        "ontap-cert-name": "ontap-cert",
        "_links": {"self": {"href": "/api/dcn/security/client"}},
    }
)

```
</div>
</div>

---
### Modifies the client certificate that ONTAP uses for communication with DCN nodes
The following output shows how to update the client certificate that ONTAP uses for communication with DCN nodes.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnCertificate()
    resource.ontap_cert_name = "new_cert1"
    resource.patch()

```
"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union
from marshmallow import fields as marshmallow_fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["DcnCertificate", "DcnCertificateSchema"]
__pdoc__ = {
    "DcnCertificateSchema.resource": False,
    "DcnCertificateSchema.opts": False,
}

class DcnCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnCertificate object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the dcn_certificate."""

    ontap_cert_name = marshmallow_fields.Str(
        data_key="ontap-cert-name",
        allow_none=True,
    )
    r""" The client certificate used by ONTAP.

Example: ontap-client-certificate"""

    @property
    def resource(self):
        return DcnCertificate

    gettable_fields = [
        "links",
        "ontap_cert_name",
    ]
    """links,ontap_cert_name,"""

    patchable_fields = [
        "ontap_cert_name",
    ]
    """ontap_cert_name,"""

    postable_fields = [
    ]
    """"""

class DcnCertificate(Resource):
    """Allows interaction with DcnCertificate objects on the host"""

    _schema = DcnCertificateSchema
    _path = "/api/dcn/security/client"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the client certificate that ONTAP uses for communication with DCN nodes.
### Related ONTAP commands
* `dcn security client show`

### Learn more
* [`DOC /dcn/security/client`](#docs-security-dcn_security_client)"""
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
        r"""Updates the client certificate that ONTAP uses for communication with DCN nodes.
### Required properties
* `ontap-cert-name` - Name of the client certificate used by ONTAP.
### Related ONTAP commands
* `dcn security client modify`

### Learn more
* [`DOC /dcn/security/client`](#docs-security-dcn_security_client)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



