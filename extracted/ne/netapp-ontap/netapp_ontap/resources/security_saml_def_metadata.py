r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API is used to manage relevant information about the SAML default metadata configuration in the cluster. The POST request creates a SAML default metadata configuration if there is none present.  The DELETE request removes the SAML default metadata configuration.  Various responses are shown in the examples below.
<br />
---
## Examples
### Retrieving the SAML default metadata configuration in the cluster
The following output shows the SAML default metadata configuration in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecuritySamlDefMetadata

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecuritySamlDefMetadata()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecuritySamlDefMetadata(
    {
        "host": "172.21.74.181",
        "certificate": {
            "common_name": "cluster-1",
            "serial_number": "180E3331A0DC5A19",
            "ca": "cluster-1",
        },
        "_links": {
            "self": {
                "href": "/api/security/authentication/cluster/saml-sp/default-metadata"
            }
        },
        "scope": "cluster",
    }
)

```
</div>
</div>

---
### Creating the SAML default metadata configuration in the cluster
The following output shows how to create the SAML default metadata in the cluster.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecuritySamlDefMetadata

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecuritySamlDefMetadata()
    resource.host = "172.21.74.181"
    resource.certificate = {"ca": "cluster1", "serial_number": "156F10C3EB4C51C1"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Deleting the SAML default metadata configuration in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecuritySamlDefMetadata

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecuritySamlDefMetadata()
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


__all__ = ["SecuritySamlDefMetadata", "SecuritySamlDefMetadataSchema"]
__pdoc__ = {
    "SecuritySamlDefMetadataSchema.resource": False,
    "SecuritySamlDefMetadataSchema.opts": False,
}


class SecuritySamlDefMetadataSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecuritySamlDefMetadata object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the security_saml_def_metadata."""

    certificate = marshmallow_fields.Nested("netapp_ontap.models.security_saml_def_metadata_certificate.SecuritySamlDefMetadataCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" The certificate field of the security_saml_def_metadata."""

    host = marshmallow_fields.Str(
        data_key="host",
        allow_none=True,
    )
    r""" The SAML service provider host."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    @property
    def resource(self):
        return SecuritySamlDefMetadata

    gettable_fields = [
        "links",
        "certificate",
        "host",
        "scope",
    ]
    """links,certificate,host,scope,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "certificate",
        "host",
    ]
    """certificate,host,"""

class SecuritySamlDefMetadata(Resource):
    """Allows interaction with SecuritySamlDefMetadata objects on the host"""

    _schema = SecuritySamlDefMetadataSchema
    _path = "/api/security/authentication/cluster/saml-sp/default-metadata"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the SAML default metadata configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp/default-metadata`](#docs-security-security_authentication_cluster_saml-sp_default-metadata)"""
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
        r"""Creates the SAML default metadata configuration. Note that `common_name` is mutually exclusive with `serial_number` and `ca` in POST requests.
### Optional properties
* `certificate`
* `host`

### Learn more
* [`DOC /security/authentication/cluster/saml-sp/default-metadata`](#docs-security-security_authentication_cluster_saml-sp_default-metadata)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the SAML default metadata configuration.
### Learn more
* [`DOC /security/authentication/cluster/saml-sp/default-metadata`](#docs-security-security_authentication_cluster_saml-sp_default-metadata)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


