r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
The FPolicy engine allows you to configure the external servers to which the file access notifications are sent. As part of FPolicy engine configuration, you can configure a server(s) to which the notification is sent, an optional set of secondary server(s) to which the notification is sent in the case of a primary server(s) failure, the port number for FPolicy application, the type of the engine, which is either synchronous or asynchronous and the format of the notifications, which is either xml or protobuf. </br>
For the synchronous engine, ONTAP will wait for a response from the FPolicy application before it allows the operation. With an asynchronous engine, ONTAP proceeds with the operation processing after sending the notification to the FPolicy application. An engine can belong to multiple FPolicy policies. If the format is not specified, the default format, xml, is configured.
## Examples
### Creating an FPolicy engine
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEngine

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEngine("4f643fb4-fd21-11e8-ae49-0050568e2c1e")
    resource.name = "engine0"
    resource.port = 9876
    resource.primary_servers = ["10.132.145.22", "10.140.101.109"]
    resource.secondary_servers = ["10.132.145.20", "10.132.145.21"]
    resource.type = "synchronous"
    resource.format = "xml"
    resource.request_abort_timeout = "PT3M"
    resource.request_cancel_timeout = "PT29S"
    resource.server_progress_timeout = "PT1M"
    resource.status_request_interval = "PT23S"
    resource.keep_alive_interval = "PT2M"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
FpolicyEngine(
    {
        "type": "synchronous",
        "format": "xml",
        "name": "engine0",
        "primary_servers": ["10.132.145.22", "10.140.101.109"],
        "port": 9876,
        "secondary_servers": ["10.132.145.20", "10.132.145.21"],
    }
)

```
</div>
</div>

---
### Creating an FPolicy engine with the minimum required fields
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEngine

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEngine("4f643fb4-fd21-11e8-ae49-0050568e2c1e")
    resource.name = "engine0"
    resource.port = 9876
    resource.primary_servers = ["10.132.145.22", "10.140.101.109"]
    resource.type = "synchronous"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
FpolicyEngine(
    {
        "type": "synchronous",
        "format": "xml",
        "name": "engine0",
        "primary_servers": ["10.132.145.22", "10.140.101.109"],
        "port": 9876,
    }
)

```
</div>
</div>

---
### Retrieving an FPolicy engine configuration for a particular SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEngine

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            FpolicyEngine.get_collection(
                "4f643fb4-fd21-11e8-ae49-0050568e2c1e", fields="*", return_timeout=15
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    FpolicyEngine(
        {
            "type": "synchronous",
            "name": "cifs",
            "primary_servers": ["10.20.20.10"],
            "svm": {"uuid": "4f643fb4-fd21-11e8-ae49-0050568e2c1e"},
            "port": 9876,
        }
    ),
    FpolicyEngine(
        {
            "request_cancel_timeout": "PT29S",
            "type": "synchronous",
            "resiliency": {"enabled": False, "retention_duration": "PT3M"},
            "format": "xml",
            "request_abort_timeout": "PT3M",
            "keep_alive_interval": "PT2M",
            "name": "nfs",
            "buffer_size": {"recv_buffer": 262144, "send_buffer": 1048576},
            "max_server_requests": 500,
            "ssl_option": "no_auth",
            "server_progress_timeout": "PT1M",
            "primary_servers": ["10.23.140.64", "10.140.101.109"],
            "svm": {"uuid": "4f643fb4-fd21-11e8-ae49-0050568e2c1e"},
            "status_request_interval": "PT23S",
            "port": 9876,
            "secondary_servers": ["10.132.145.20", "10.132.145.22"],
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific FPolicy engine configuration for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEngine

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEngine("4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="cifs")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
FpolicyEngine(
    {
        "type": "synchronous",
        "format": "xml",
        "name": "cifs",
        "primary_servers": ["10.20.20.10"],
        "svm": {"uuid": "4f643fb4-fd21-11e8-ae49-0050568e2c1e"},
        "port": 9876,
    }
)

```
</div>
</div>

---
### Updating an FPolicy engine for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEngine

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEngine("4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="cifs")
    resource.port = 6666
    resource.secondary_servers = ["10.132.145.20", "10.132.145.21"]
    resource.type = "synchronous"
    resource.patch()

```

---
### Updating all the attributes of a specific FPolicy engine for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEngine

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEngine("4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="cifs")
    resource.port = 9876
    resource.primary_servers = ["10.132.145.20", "10.140.101.109"]
    resource.secondary_servers = ["10.132.145.23", "10.132.145.21"]
    resource.type = "synchronous"
    resource.format = "protobuf"
    resource.patch()

```

---
### Deleting a specific FPolicy engine for an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FpolicyEngine

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FpolicyEngine("4f643fb4-fd21-11e8-ae49-0050568e2c1e", name="cifs")
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


__all__ = ["FpolicyEngine", "FpolicyEngineSchema"]
__pdoc__ = {
    "FpolicyEngineSchema.resource": False,
    "FpolicyEngineSchema.opts": False,
}


class FpolicyEngineSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEngine object"""

    buffer_size = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_buffer_size.FpolicyEngineBufferSizeSchema", data_key="buffer_size", unknown=EXCLUDE, allow_none=True)
    r""" Specifies the send and receive buffer size of the connected socket for the FPolicy server."""

    certificate = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_certificate.FpolicyEngineCertificateSchema", data_key="certificate", unknown=EXCLUDE, allow_none=True)
    r""" Provides details about certificate used to authenticate the FPolicy server."""

    format = marshmallow_fields.Str(
        data_key="format",
        validate=enum_validation(['xml', 'protobuf']),
        allow_none=True,
    )
    r""" The format for the notification messages sent to the FPolicy servers.
  The possible values are:

    * xml  - Notifications sent to the FPolicy server will be formatted using the XML schema.
    * protobuf - Notifications sent to the FPolicy server will be formatted using Protobuf schema, which is a binary form.


Valid choices:

* xml
* protobuf"""

    keep_alive_interval = marshmallow_fields.Str(
        data_key="keep_alive_interval",
        allow_none=True,
    )
    r""" Specifies the ISO-8601 interval time for a storage appliance to send Keep Alive message to an FPolicy server. The allowed range is between 10 to 600 seconds.

Example: PT2M"""

    max_server_requests = Size(
        data_key="max_server_requests",
        validate=integer_validation(minimum=1, maximum=10000),
        allow_none=True,
    )
    r""" Specifies the maximum number of outstanding requests for the FPolicy server. It is used to specify maximum outstanding requests that will be queued up for the FPolicy server. The value for this field must be between 1 and 10000.  The default values are 500, 1000 or 2000 for Low-end(<64 GB memory), Mid-end(>=64 GB memory) and High-end(>=128 GB memory) Platforms respectively.

Example: 500"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Specifies the name to assign to the external server configuration.

Example: fp_ex_eng"""

    port = Size(
        data_key="port",
        allow_none=True,
    )
    r""" Port number of the FPolicy server application.

Example: 9876"""

    primary_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="primary_servers", allow_none=True)
    r""" The primary_servers field of the fpolicy_engine.

Example: ["10.132.145.20","10.140.101.109"]"""

    request_abort_timeout = marshmallow_fields.Str(
        data_key="request_abort_timeout",
        allow_none=True,
    )
    r""" Specifies the ISO-8601 timeout duration for a screen request to be aborted by a storage appliance. The allowed range is between 0 to 200 seconds.

Example: PT40S"""

    request_cancel_timeout = marshmallow_fields.Str(
        data_key="request_cancel_timeout",
        allow_none=True,
    )
    r""" Specifies the ISO-8601 timeout duration for a screen request to be processed by an FPolicy server. The allowed range is between 0 to 100 seconds.

Example: PT20S"""

    resiliency = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_resiliency.FpolicyEngineResiliencySchema", data_key="resiliency", unknown=EXCLUDE, allow_none=True)
    r""" If all primary and secondary servers are down, or if no response is received from the FPolicy servers, file access events are stored inside the storage controller under the specified resiliency-directory-path."""

    secondary_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="secondary_servers", allow_none=True)
    r""" The secondary_servers field of the fpolicy_engine.

Example: ["10.132.145.20","10.132.145.21"]"""

    server_progress_timeout = marshmallow_fields.Str(
        data_key="server_progress_timeout",
        allow_none=True,
    )
    r""" Specifies the ISO-8601 timeout duration in which a throttled FPolicy server must complete at least one screen request. If no request is processed within the timeout, connection to the FPolicy server is terminated. The allowed range is between 0 to 100 seconds.

Example: PT1M"""

    ssl_option = marshmallow_fields.Str(
        data_key="ssl_option",
        validate=enum_validation(['no_auth', 'server_auth', 'mutual_auth']),
        allow_none=True,
    )
    r""" Specifies the SSL option for external communication with the FPolicy server. Possible values include the following:

* no_auth       When set to "no_auth", no authentication takes place.
* server_auth   When set to "server_auth", only the FPolicy server is authenticated by the SVM. With this option, before creating the FPolicy external engine, the administrator must install the public certificate of the certificate authority (CA) that signed the FPolicy server certificate.
* mutual_auth   When set to "mutual_auth", mutual authentication takes place between the SVM and the FPolicy server. This means authentication of the FPolicy server by the SVM along with authentication of the SVM by the FPolicy server. With this option, before creating the FPolicy external engine, the administrator must install the public certificate of the certificate authority (CA) that signed the FPolicy server certificate along with the public certificate and key file for authentication of the SVM.


Valid choices:

* no_auth
* server_auth
* mutual_auth"""

    status_request_interval = marshmallow_fields.Str(
        data_key="status_request_interval",
        allow_none=True,
    )
    r""" Specifies the ISO-8601 interval time for a storage appliance to query a status request from an FPolicy server. The allowed range is between 0 to 50 seconds.

Example: PT10S"""

    svm = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_svm.FpolicyEngineSvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the fpolicy_engine."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['synchronous', 'asynchronous']),
        allow_none=True,
    )
    r""" The notification mode determines what ONTAP does after sending notifications to FPolicy servers.
  The possible values are:

    * synchronous  - After sending a notification, wait for a response from the FPolicy server.
    * asynchronous - After sending a notification, file request processing continues.


Valid choices:

* synchronous
* asynchronous"""

    @property
    def resource(self):
        return FpolicyEngine

    gettable_fields = [
        "buffer_size",
        "certificate",
        "format",
        "keep_alive_interval",
        "max_server_requests",
        "name",
        "port",
        "primary_servers",
        "request_abort_timeout",
        "request_cancel_timeout",
        "resiliency",
        "secondary_servers",
        "server_progress_timeout",
        "ssl_option",
        "status_request_interval",
        "svm",
        "type",
    ]
    """buffer_size,certificate,format,keep_alive_interval,max_server_requests,name,port,primary_servers,request_abort_timeout,request_cancel_timeout,resiliency,secondary_servers,server_progress_timeout,ssl_option,status_request_interval,svm,type,"""

    patchable_fields = [
        "buffer_size",
        "certificate",
        "format",
        "keep_alive_interval",
        "max_server_requests",
        "port",
        "primary_servers",
        "request_abort_timeout",
        "request_cancel_timeout",
        "resiliency",
        "secondary_servers",
        "server_progress_timeout",
        "ssl_option",
        "status_request_interval",
        "type",
    ]
    """buffer_size,certificate,format,keep_alive_interval,max_server_requests,port,primary_servers,request_abort_timeout,request_cancel_timeout,resiliency,secondary_servers,server_progress_timeout,ssl_option,status_request_interval,type,"""

    postable_fields = [
        "buffer_size",
        "certificate",
        "format",
        "keep_alive_interval",
        "max_server_requests",
        "name",
        "port",
        "primary_servers",
        "request_abort_timeout",
        "request_cancel_timeout",
        "resiliency",
        "secondary_servers",
        "server_progress_timeout",
        "ssl_option",
        "status_request_interval",
        "type",
    ]
    """buffer_size,certificate,format,keep_alive_interval,max_server_requests,name,port,primary_servers,request_abort_timeout,request_cancel_timeout,resiliency,secondary_servers,server_progress_timeout,ssl_option,status_request_interval,type,"""

class FpolicyEngine(Resource):
    r""" Defines how ONTAP makes and manages connections to external FPolicy servers. """

    _schema = FpolicyEngineSchema
    _path = "/api/protocols/fpolicy/{svm[uuid]}/engines"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FPolicy engine configurations of all the engines for a specified SVM. ONTAP allows creation of cluster-level FPolicy engines that act as a template for all the SVMs belonging to the cluster. These cluster-level FPolicy engines are also retrieved for the specified SVM.
### Related ONTAP commands
* `fpolicy policy external-engine show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all FpolicyEngine resources that match the provided query"""
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
        """Returns a list of RawResources that represent FpolicyEngine resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["FpolicyEngine"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a specific FPolicy engine configuration of an SVM. Modification of an FPolicy engine that is attached to one or more enabled FPolicy policies is not allowed.
### Related ONTAP commands
* `fpolicy policy external-engine modify`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["FpolicyEngine"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["FpolicyEngine"], NetAppResponse]:
        r"""Creates an FPolicy engine configuration for a specified SVM. FPolicy engine creation is allowed only on data SVMs.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy engine.
* `name` - Name of external engine.
* `port` - Port number of the FPolicy server application.
* `primary_servers` - List of primary FPolicy servers to which the node will send notifications.
### Recommended optional properties
* `secondary_servers` - It is recommended to configure secondary FPolicy server to which the node will send notifications when the primary server is down.
### Default property values
* `type` - _synchronous_
* `format` - _xml_
### Related ONTAP commands
* `fpolicy policy external-engine create`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["FpolicyEngine"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the FPolicy external engine configuration. Deletion of an FPolicy engine that is attached to one or more FPolicy policies is not allowed.
### Related ONTAP commands
* `fpolicy policy external-engine delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FPolicy engine configurations of all the engines for a specified SVM. ONTAP allows creation of cluster-level FPolicy engines that act as a template for all the SVMs belonging to the cluster. These cluster-level FPolicy engines are also retrieved for the specified SVM.
### Related ONTAP commands
* `fpolicy policy external-engine show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a particular FPolicy engine configuration of a specified SVM. A cluster-level FPolicy engine configuration cannot be retrieved for a data SVM.
### Related ONTAP commands
* `fpolicy policy external-engine show`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
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
        r"""Creates an FPolicy engine configuration for a specified SVM. FPolicy engine creation is allowed only on data SVMs.
### Required properties
* `svm.uuid` - Existing SVM in which to create the FPolicy engine.
* `name` - Name of external engine.
* `port` - Port number of the FPolicy server application.
* `primary_servers` - List of primary FPolicy servers to which the node will send notifications.
### Recommended optional properties
* `secondary_servers` - It is recommended to configure secondary FPolicy server to which the node will send notifications when the primary server is down.
### Default property values
* `type` - _synchronous_
* `format` - _xml_
### Related ONTAP commands
* `fpolicy policy external-engine create`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
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
        r"""Updates a specific FPolicy engine configuration of an SVM. Modification of an FPolicy engine that is attached to one or more enabled FPolicy policies is not allowed.
### Related ONTAP commands
* `fpolicy policy external-engine modify`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
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
        r"""Deletes the FPolicy external engine configuration. Deletion of an FPolicy engine that is attached to one or more FPolicy policies is not allowed.
### Related ONTAP commands
* `fpolicy policy external-engine delete`
### Learn more
* [`DOC /protocols/fpolicy/{svm.uuid}/engines`](#docs-NAS-protocols_fpolicy_{svm.uuid}_engines)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


