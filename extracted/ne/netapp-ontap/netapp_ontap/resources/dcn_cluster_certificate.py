r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API endpoint is designed to manage the certificate that is used by the Kubernetes cluster. The PATCH method is used to update the certificate of the Kubernetes cluster, while the GET method retrieves the certificate of the Kubernetes cluster.
<br />
---
## Examples
### Retrieving the certificate that is used by the Kubernetes cluster
The following output shows the certificate that is used by the Kubernetes cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnClusterCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnClusterCertificate()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
DcnClusterCertificate(
    {
        "_links": {"self": {"href": "/api/dcn/security/cluster/certificate/"}},
        "dcn-k8s-cert-name": "DCN",
    }
)

```
</div>
</div>

---
### Modifies the certificate that is used by the Kubernetes cluster
The following output shows how to modify the certificate that is used by the Kubernetes cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnClusterCertificate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnClusterCertificate()
    resource.dcn_k8s_cert_name = "k8s-cert"
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


__all__ = ["DcnClusterCertificate", "DcnClusterCertificateSchema"]
__pdoc__ = {
    "DcnClusterCertificateSchema.resource": False,
    "DcnClusterCertificateSchema.opts": False,
}

class DcnClusterCertificateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnClusterCertificate object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the dcn_cluster_certificate."""

    dcn_k8s_cert_name = marshmallow_fields.Str(
        data_key="dcn-k8s-cert-name",
        allow_none=True,
    )
    r""" DCN cluster certificate name.

Example: dcn-k8s-cert"""

    @property
    def resource(self):
        return DcnClusterCertificate

    gettable_fields = [
        "links",
        "dcn_k8s_cert_name",
    ]
    """links,dcn_k8s_cert_name,"""

    patchable_fields = [
        "dcn_k8s_cert_name",
    ]
    """dcn_k8s_cert_name,"""

    postable_fields = [
    ]
    """"""

class DcnClusterCertificate(Resource):
    """Allows interaction with DcnClusterCertificate objects on the host"""

    _schema = DcnClusterCertificateSchema
    _path = "/api/dcn/security/cluster/certificate"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the certificate that is used by the Kubernetes cluster.
### Related ONTAP commands
* `dcn security certificate k8s show`

### Learn more
* [`DOC /dcn/security/cluster/certificate`](#docs-security-dcn_security_cluster_certificate)"""
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
        r"""Updates the certificate that is used by the Kubernetes cluster.
### Required properties
* `dcn-k8s-cert-name` - Name of the DCN Kubernetes cluster certificate.
### Related ONTAP commands
* `dcn security certificate k8s modify`

### Learn more
* [`DOC /dcn/security/cluster/certificate`](#docs-security-dcn_security_cluster_certificate)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



