r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to retrieve and display relevant information pertaining to the SAML service provider configuration in the cluster. The POST request creates a SAML service provider configuration if there is none present.  The DELETE request removes the SAML service provider configuration.  The PATCH request enables and disables SAML in the cluster.  Various responses are shown in the examples below.
<br />
---
## Examples
### Retrieving the SAML service provider configuration in the cluster
The following output shows the SAML service provider configuration in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecuritySamlSp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecuritySamlSp()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecuritySamlSp(
    {
        "certificate": {"ca": "cluster1", "serial_number": "156F10C3EB4C51C1"},
        "host": "172.21.74.181",
        "idp_uri": "https://examplelab.customer.com/idp/Metadata",
        "enabled": True,
        "_links": {"self": {"href": "/api/security/authentication/cluster/saml-sp"}},
    }
)

```
</div>
</div>

---
### Creating the SAML service provider configuration
The following output shows how to create a SAML service provider configuration in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecuritySamlSp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecuritySamlSp()
    resource.idp_uri = "https://examplelab.customer.com/idp/Metadata"
    resource.host = "172.21.74.181"
    resource.certificate = {"ca": "cluster1", "serial_number": "156F10C3EB4C51C1"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Updating the SAML service provider configuration
The following output shows how to enable a SAML service provider configuration in the cluster.
<br/>Disabling the configuration requires the client to be authenticated through SAML prior to performing the operation.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecuritySamlSp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecuritySamlSp()
    resource.enabled = True
    resource.patch()

```

---
### Deleting the SAML service provider configuration
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecuritySamlSp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecuritySamlSp()
    resource.delete()

```

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


__all__ = ["SecuritySamlSp", "SecuritySamlSpSchema"]
__pdoc__ = {
    "SecuritySamlSpSchema.resource": False,
    "SecuritySamlSpSchema.opts": False,
}


class SecuritySamlSpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecuritySamlSp object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_saml_sp."""

    certificate = marshmallow_fields.Nested("netapp_ontap.models.security_saml_sp_certificate.SecuritySamlSpCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" The certificate field of the security_saml_sp."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The SAML service provider is enabled.  Valid for PATCH and GET operations only."""

    host = marshmallow_fields.Str(
        data_key="host",
        allow_none=True,
    )
    r""" The SAML service provider host."""

    idp_uri = marshmallow_fields.Str(
        data_key="idp_uri",
        allow_none=True,
    )
    r""" The identity provider (IdP) metadata location. Required for POST operations.

Example: https://idp.example.com/FederationMetadata/2007-06/FederationMetadata.xml"""

    @property
    def resource(self):
        return SecuritySamlSp

    gettable_fields = [
        "links",
        "certificate",
        "enabled",
        "host",
        "idp_uri",
    ]
    """links,certificate,enabled,host,idp_uri,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "certificate",
        "host",
        "idp_uri",
    ]
    """certificate,host,idp_uri,"""

class SecuritySamlSp(Resource):
    """Allows interaction with SecuritySamlSp objects on the host"""

    _schema = SecuritySamlSpSchema
    _path = "/api/security/authentication/cluster/saml-sp"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a SAML service provider configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
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
        r"""Creates a SAML service provider configuration. Note that "common_name" is mutually exclusive with "serial_number" and "ca" in POST. SAML will initially be disabled, requiring a patch to set "enabled" to "true", so that the user has time to complete the setup of the IdP.
### Required properties
* `idp_uri`
### Optional properties
* `certificate`
* `enabled`
* `host`

### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a SAML service provider configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a SAML service provider configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp`](#docs-security-security_authentication_cluster_saml-sp)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


