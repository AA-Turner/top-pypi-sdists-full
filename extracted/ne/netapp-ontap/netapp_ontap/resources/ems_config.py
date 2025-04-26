r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This endpoint is used to configure general parameters of the Event Management System (EMS).
## Examples
### Configuring the system-wide email parameters
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsConfig()
    resource.mail_from = "administrator@mycompany.com"
    resource.mail_server = "mycompany.com"
    resource.mail_server_user = "smtp"
    resource.patch()

```

### Retrieving the EMS configuration
The following example retrieves EMS configuration for the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsConfig()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
EmsConfig(
    {
        "pubsub_enabled": True,
        "mail_from": "admin@localhost",
        "_links": {"self": {"href": "/api/support/ems"}},
        "mail_server": "localhost",
    }
)

```
</div>
</div>
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


__all__ = ["EmsConfig", "EmsConfigSchema"]
__pdoc__ = {
    "EmsConfigSchema.resource": False,
    "EmsConfigSchema.opts": False,
}


class EmsConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsConfig object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_config."""

    mail_from = marshmallow_fields.Str(
        data_key="mail_from",
        allow_none=True,
    )
    r""" Mail from

Example: administrator@mycompany.com"""

    mail_server = marshmallow_fields.Str(
        data_key="mail_server",
        allow_none=True,
    )
    r""" Mail server (SMTP)

Example: mail.mycompany.com"""

    mail_server_password = marshmallow_fields.Str(
        data_key="mail_server_password",
        allow_none=True,
    )
    r""" Password for Mail server (SMTP)

Example: password"""

    mail_server_user = marshmallow_fields.Str(
        data_key="mail_server_user",
        allow_none=True,
    )
    r""" Username for Mail server (SMTP)

Example: user"""

    proxy_password = marshmallow_fields.Str(
        data_key="proxy_password",
        allow_none=True,
    )
    r""" Password for HTTP/HTTPS proxy

Example: password"""

    proxy_url = marshmallow_fields.Str(
        data_key="proxy_url",
        allow_none=True,
    )
    r""" HTTP/HTTPS proxy URL

Example: https://proxyserver.mycompany.com"""

    proxy_user = marshmallow_fields.Str(
        data_key="proxy_user",
        allow_none=True,
    )
    r""" User name for HTTP/HTTPS proxy

Example: proxy_user"""

    pubsub_enabled = marshmallow_fields.Boolean(
        data_key="pubsub_enabled",
        allow_none=True,
    )
    r""" Is Publish/Subscribe Messaging Enabled?

Example: true"""

    @property
    def resource(self):
        return EmsConfig

    gettable_fields = [
        "links",
        "mail_from",
        "mail_server",
        "mail_server_user",
        "proxy_url",
        "proxy_user",
        "pubsub_enabled",
    ]
    """links,mail_from,mail_server,mail_server_user,proxy_url,proxy_user,pubsub_enabled,"""

    patchable_fields = [
        "mail_from",
        "mail_server",
        "mail_server_password",
        "mail_server_user",
        "proxy_password",
        "proxy_url",
        "proxy_user",
        "pubsub_enabled",
    ]
    """mail_from,mail_server,mail_server_password,mail_server_user,proxy_password,proxy_url,proxy_user,pubsub_enabled,"""

    postable_fields = [
    ]
    """"""

class EmsConfig(Resource):
    """Allows interaction with EmsConfig objects on the host"""

    _schema = EmsConfigSchema
    _path = "/api/support/ems"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the EMS configuration.
### Related ONTAP commands
* `event config show`

### Learn more
* [`DOC /support/ems`](#docs-support-support_ems)"""
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
        r"""Updates the EMS configuration.
### Related ONTAP commands
* `event config modify`

### Learn more
* [`DOC /support/ems`](#docs-support-support_ems)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



