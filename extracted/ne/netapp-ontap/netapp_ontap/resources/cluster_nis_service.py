r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
NIS servers are used to authenticate user and client computers. NIS domain name and NIS server information is required to configure NIS. This API retrieves and manages NIS server configurations.
## Examples
### Retrieving cluster NIS information
The cluster NIS GET request retrieves the NIS configuration of the cluster.<br>
The following example shows how a GET request is used to retrieve the cluster NIS configuration:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterNisService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterNisService()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
ClusterNisService(
    {
        "servers": ["10.10.10.10", "example.com"],
        "bound_servers": ["10.10.10.10"],
        "domain": "domainA.example.com",
    }
)

```
</div>
</div>

### Creating the cluster NIS configuration
The cluster NIS POST request creates a NIS configuration for the cluster.<br>
The following example shows how a POST request is used to create a cluster NIS configuration:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterNisService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterNisService()
    resource.domain = "domainA.example.com"
    resource.servers = ["10.10.10.10", "example.com"]
    resource.post(hydrate=True)
    print(resource)

```

### Updating the cluster NIS configuration
The cluster NIS PATCH request updates the NIS configuration of the cluster.<br>
The following example shows how to update the domain:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterNisService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterNisService()
    resource.domain = "domainC.example.com"
    resource.servers = ["13.13.13.13"]
    resource.patch()

```

The following example shows how to update the server:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterNisService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterNisService()
    resource.servers = ["14.14.14.14"]
    resource.patch()

```

## Deleting the cluster NIS configuration
The cluster NIS DELETE request deletes the NIS configuration of the cluster.<br>
The following example shows how a DELETE request is used to delete the cluster NIS configuration:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterNisService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterNisService()
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


__all__ = ["ClusterNisService", "ClusterNisServiceSchema"]
__pdoc__ = {
    "ClusterNisServiceSchema.resource": False,
    "ClusterNisServiceSchema.opts": False,
}


class ClusterNisServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNisService object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cluster_nis_service."""

    binding_details = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.binding_details.BindingDetailsSchema", unknown=EXCLUDE, allow_none=True), data_key="binding_details", allow_none=True)
    r""" An array of objects where each object represents the NIS server and it's status for a given NIS domain. It is an advanced field."""

    bound_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="bound_servers", allow_none=True)
    r""" The bound_servers field of the cluster_nis_service."""

    domain = marshmallow_fields.Str(
        data_key="domain",
        validate=len_validation(minimum=1, maximum=64),
        allow_none=True,
    )
    r""" The NIS domain to which this configuration belongs."""

    servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="servers", allow_none=True)
    r""" A list of hostnames or IP addresses of NIS servers used
by the NIS domain configuration."""

    @property
    def resource(self):
        return ClusterNisService

    gettable_fields = [
        "links",
        "binding_details",
        "bound_servers",
        "domain",
        "servers",
    ]
    """links,binding_details,bound_servers,domain,servers,"""

    patchable_fields = [
        "domain",
        "servers",
    ]
    """domain,servers,"""

    postable_fields = [
        "domain",
        "servers",
    ]
    """domain,servers,"""

class ClusterNisService(Resource):
    """Allows interaction with ClusterNisService objects on the host"""

    _schema = ClusterNisServiceSchema
    _path = "/api/security/authentication/cluster/nis"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the NIS configuration of the cluster. Both NIS domain and servers are displayed by default.
The `bound_servers` property indicates the successfully bound NIS servers.

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
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
        r"""The cluster can have one NIS server configuration. Specify the NIS domain and NIS servers as input. The servers field cannot be empty.
Both FQDNs and IP addresses are supported for the `server` property. IPv6 must be enabled if IPv6 family addresses are specified in the `server` property. A maximum of ten NIS servers are supported.
### Required properties
* `domain` - NIS domain to which this configuration belongs.
* `servers` - List of hostnames or IP addresses of NIS servers used by the NIS domain configuration.

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
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
        r"""Both NIS domain and servers can be updated. Domains and servers cannot be empty. Both FQDNs and IP addresses are supported for the 'servers' field. If the domain is updated, NIS servers must also be specified. IPv6 must be enabled if IPv6 family addresses are specified for the `servers` property.<br/>

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
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
        r"""Deletes the NIS configuration of the cluster. NIS can be removed as a source from ns-switch if NIS is not used for lookups.

### Learn more
* [`DOC /security/authentication/cluster/nis`](#docs-security-security_authentication_cluster_nis)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


