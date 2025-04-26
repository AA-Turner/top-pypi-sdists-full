r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Configuration of an HTTP proxy for an SVM or a Cluster IPspace.
## Retrieve HTTP proxy information
The HTTP proxy GET operation retrieves all configurations for an SVM or a Cluster IPspace via '/api/cluster'.
## Examples
### Retrieving all fields for all HTTP proxy configurations
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkHttpProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NetworkHttpProxy.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NetworkHttpProxy(
        {
            "uuid": "4133a1fc-7228-11e9-b40c-005056bb4f0c",
            "svm": {"name": "vs1", "uuid": "4133a1fc-7228-11e9-b40c-005056bb4f0c"},
            "port": 3128,
            "authentication_enabled": False,
            "server": "server1.example.com",
        }
    ),
    NetworkHttpProxy(
        {
            "ipspace": {
                "name": "Default",
                "uuid": "7433520f-7214-11e9-828c-005056bb4f0c",
            },
            "uuid": "96219ce3-7214-11e9-828c-005056bb4f0c",
            "svm": {
                "name": "cluster-1",
                "uuid": "96219ce3-7214-11e9-828c-005056bb4f0c",
            },
            "port": 3128,
            "authentication_enabled": True,
            "server": "1.1.1.",
        }
    ),
]

```
</div>
</div>

### Retrieving the HTTP proxy configuration for a specific SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkHttpProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkHttpProxy(uuid="96219ce3-7214-11e9-828c-005056bb4f0c")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
NetworkHttpProxy(
    {
        "ipspace": {"name": "Default", "uuid": "7433520f-7214-11e9-828c-005056bb4f0c"},
        "uuid": "96219ce3-7214-11e9-828c-005056bb4f0c",
        "svm": {"name": "cluster-1", "uuid": "96219ce3-7214-11e9-828c-005056bb4f0c"},
        "port": 3128,
        "authentication_enabled": False,
        "server": "1.1.1.1",
    }
)

```
</div>
</div>

## Creating an HTTP proxy configuration
You can use the HTTP proxy POST operation to create an HTTP proxy configuration for the specified SVM.
## Examples
### Creating an HTTP proxy configuration for a particular SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkHttpProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkHttpProxy()
    resource.port = 3128
    resource.server = "1.1.1.1"
    resource.svm = {"name": "cluster-1"}
    resource.post(hydrate=True)
    print(resource)

```

### Creating an HTTP proxy configuration for a particular IPspace
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkHttpProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkHttpProxy()
    resource.ipspace = {"name": "Default"}
    resource.port = 3128
    resource.server = "1.1.1.1"
    resource.post(hydrate=True)
    print(resource)

```

### Creating an HTTP proxy configuration with authentication enabled
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkHttpProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkHttpProxy()
    resource.ipspace = {"name": "Default"}
    resource.port = 3128
    resource.server = "1.1.1.1"
    resource.authentication_enabled = True
    resource.username = "test"
    resource.password = "test"
    resource.post(hydrate=True)
    print(resource)

```

## Update an HTTP proxy configuration for a specified SVM
You can use the HTTP proxy PATCH operation to update the HTTP proxy configuration for the specified SVM.
## Example
The following example shows how a PATCH operation is used to update an HTTP proxy configuration for a specific SVM:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkHttpProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkHttpProxy(uuid="96219ce3-7214-11e9-828c-005056bb4f0c")
    resource.port = 3128
    resource.server = "server2.example.com"
    resource.patch()

```

## Delete an HTTP proxy configuration for a specified SVM
You can use the HTTP proxy DELETE operation to delete the HTTP proxy configuration for the specified SVM.
## Example
The following example shows how a DELETE operation is used to delete an HTTP proxy configuration for a specific SVM:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NetworkHttpProxy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NetworkHttpProxy(uuid="96219ce3-7214-11e9-828c-005056bb4f0c")
    resource.delete()

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


__all__ = ["NetworkHttpProxy", "NetworkHttpProxySchema"]
__pdoc__ = {
    "NetworkHttpProxySchema.resource": False,
    "NetworkHttpProxySchema.opts": False,
}


class NetworkHttpProxySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NetworkHttpProxy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the network_http_proxy."""

    authentication_enabled = marshmallow_fields.Boolean(
        data_key="authentication_enabled",
        allow_none=True,
    )
    r""" Specifies whether or not authentication with the HTTP proxy server is enabled."""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the network_http_proxy."""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" Password to authenticate with the HTTP proxy server when authentication_enabled is set to "true"."""

    port = Size(
        data_key="port",
        validate=integer_validation(minimum=1, maximum=65535),
        allow_none=True,
    )
    r""" The port number on which the HTTP proxy service is configured on the
proxy server.


Example: 3128"""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
        allow_none=True,
    )
    r""" Set to “svm” for HTTP proxy owned by an SVM. Otherwise, set to "cluster".


Valid choices:

* svm
* cluster"""

    server = marshmallow_fields.Str(
        data_key="server",
        allow_none=True,
    )
    r""" Fully qualified domain name (FQDN) or IP address of the HTTP proxy server."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the network_http_proxy."""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" Username to authenticate with the HTTP proxy server when authentication_enabled is set to "true"."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The UUID that uniquely identifies the HTTP proxy."""

    @property
    def resource(self):
        return NetworkHttpProxy

    gettable_fields = [
        "links",
        "authentication_enabled",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "port",
        "scope",
        "server",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,authentication_enabled,ipspace.links,ipspace.name,ipspace.uuid,port,scope,server,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "authentication_enabled",
        "password",
        "port",
        "server",
        "username",
    ]
    """authentication_enabled,password,port,server,username,"""

    postable_fields = [
        "authentication_enabled",
        "ipspace.name",
        "ipspace.uuid",
        "password",
        "port",
        "server",
        "svm.name",
        "svm.uuid",
        "username",
    ]
    """authentication_enabled,ipspace.name,ipspace.uuid,password,port,server,svm.name,svm.uuid,username,"""

class NetworkHttpProxy(Resource):
    """Allows interaction with NetworkHttpProxy objects on the host"""

    _schema = NetworkHttpProxySchema
    _path = "/api/network/http-proxy"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the HTTP proxy configurations of all the SVMs and Cluster IPspaces.
### Related ONTAP commands
* `vserver http-proxy show`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all NetworkHttpProxy resources that match the provided query"""
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
        """Returns a list of RawResources that represent NetworkHttpProxy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NetworkHttpProxy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the proxy server, port, username, and password parameters.
Important notes:
* IPv6 must be enabled if IPv6 family addresses are specified in the "server" field.
* The server and the port combination specified using the "server" and "port" fields is validated during this operation. The validation will fail in the following scenarios:
  * The HTTP proxy service is not configured on the server.
  * The HTTP proxy service is not running on the specified port.
  * The server is unreachable.
### Related ONTAP commands
* `vserver http-proxy modify`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["NetworkHttpProxy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NetworkHttpProxy"], NetAppResponse]:
        r"""Creates an HTTP proxy configuration for an SVM or a Cluster IPspace.
Important notes:
* IPv6 must be enabled if IPv6 family addresses are specified in the "server" field.
* The server and the port combination specified using the "server" and "port" fields is validated during this operation. The validation will fail in the following scenarios:
  * The HTTP proxy service is not configured on the server.
  * The HTTP proxy service is not running on the specified port.
  * The server is unreachable.
### Required properties
* SVM-scoped HTTP proxy
  * `svm.uuid` or `svm.name` - Existing SVM in which to create the HTTP proxy.
* Cluster-scoped HTTP proxy
  * `ipspace.uuid` or `ipspace.name` - Existing Cluster IPspace in which to create the HTTP proxy.
* `server` - HTTP proxy server FQDN or IP address.
* `port` - HTTP proxy server port.
### Optional properties
* `authentication_enabled` - Specifies if authentication is required for the HTTP proxy server.
* `username` - Username used to authenticate with the HTTP proxy server.
* `password` - Password used to authenticate with the HTTP proxy server.
### Related ONTAP commands
* `vserver http-proxy create`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["NetworkHttpProxy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the HTTP proxy configuration of the specified SVM or Cluster IPspace.
### Related ONTAP commands
* `vserver http-proxy delete`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the HTTP proxy configurations of all the SVMs and Cluster IPspaces.
### Related ONTAP commands
* `vserver http-proxy show`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Displays the HTTP proxy server, port, and IPspace of the specified SVM or Cluster IPspace.
### Related ONTAP commands
* `vserver http-proxy show`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
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
        r"""Creates an HTTP proxy configuration for an SVM or a Cluster IPspace.
Important notes:
* IPv6 must be enabled if IPv6 family addresses are specified in the "server" field.
* The server and the port combination specified using the "server" and "port" fields is validated during this operation. The validation will fail in the following scenarios:
  * The HTTP proxy service is not configured on the server.
  * The HTTP proxy service is not running on the specified port.
  * The server is unreachable.
### Required properties
* SVM-scoped HTTP proxy
  * `svm.uuid` or `svm.name` - Existing SVM in which to create the HTTP proxy.
* Cluster-scoped HTTP proxy
  * `ipspace.uuid` or `ipspace.name` - Existing Cluster IPspace in which to create the HTTP proxy.
* `server` - HTTP proxy server FQDN or IP address.
* `port` - HTTP proxy server port.
### Optional properties
* `authentication_enabled` - Specifies if authentication is required for the HTTP proxy server.
* `username` - Username used to authenticate with the HTTP proxy server.
* `password` - Password used to authenticate with the HTTP proxy server.
### Related ONTAP commands
* `vserver http-proxy create`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
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
        r"""Updates the proxy server, port, username, and password parameters.
Important notes:
* IPv6 must be enabled if IPv6 family addresses are specified in the "server" field.
* The server and the port combination specified using the "server" and "port" fields is validated during this operation. The validation will fail in the following scenarios:
  * The HTTP proxy service is not configured on the server.
  * The HTTP proxy service is not running on the specified port.
  * The server is unreachable.
### Related ONTAP commands
* `vserver http-proxy modify`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
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
        r"""Deletes the HTTP proxy configuration of the specified SVM or Cluster IPspace.
### Related ONTAP commands
* `vserver http-proxy delete`

### Learn more
* [`DOC /network/http-proxy`](#docs-networking-network_http-proxy)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


