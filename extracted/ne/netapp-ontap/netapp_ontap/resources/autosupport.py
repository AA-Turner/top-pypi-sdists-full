r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
AutoSupport is the NetApp *call home* mechanism. AutoSupport sends configuration details, status details, and error reporting details to NetApp.<p/>
This endpoint supports both GET and PATCH calls. GET is used to retrieve AutoSupport configuration details for the cluster and PATCH is used to modify the AutoSupport configuration of the cluster. You can also use GET calls to check AutoSupport connectivity.
---
## Examples
### Configuring 'to' addresses
The following example configures AutoSupport to send emails to 'to' addresses.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Autosupport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Autosupport()
    resource.to = ["abc@netapp.com", "xyz@netapp.com"]
    resource.patch()

```

---
### Configuring 'SMTP' transport
The following example configures AutoSupport to use 'SMTP' transport. The default transport is 'HTTPS'.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Autosupport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Autosupport()
    resource.transport = "smtp"
    resource.patch()

```

---
### Configuring 'start_tls' SMTP encryption
The following example configures AutoSupport to use 'start_tls' SMTP encryption. The default value for the smtp_encryption field is 'none'.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Autosupport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Autosupport()
    resource.smtp_encryption = "start_tls"
    resource.patch()

```

---
### Retrieving the AutoSupport configuration
The following example retrieves AutoSupport configuration for the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Autosupport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Autosupport()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Autosupport(
    {
        "mail_hosts": ["mailhost"],
        "from": "Postmaster",
        "smtp_encryption": "none",
        "transport": "smtp",
        "ondemand_enabled": True,
        "enabled": True,
        "proxy_url": "",
        "to": ["abc@netapp.com", "xyz@netapp.com"],
        "is_minimal": False,
        "contact_support": True,
    }
)

```
</div>
</div>

---
### Retrieving AutoSupport connectivity issues
The following example retrieves AutoSupport connectivity issues for the cluster. The `fields=issues` parameter must be specified, for the response to return connectivity issues. The `corrective_action` section might contain commands which needs to be executed on the ONTAP CLI.<p/>
Note that the connectivity check can take up to 10 seconds to complete.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Autosupport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Autosupport()
    resource.get(fields="issues")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
Autosupport(
    {
        "issues": [
            {
                "destination": "mailhost",
                "issue": {
                    "message": "SMTP connectivity check failed for destination: mailhost. Error: Could not resolve host - 'mailhost'",
                    "code": "53149746",
                },
                "node": {
                    "name": "node3",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc"
                        }
                    },
                    "uuid": "0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc",
                },
                "component": "mail_server",
                "corrective_action": {
                    "message": "Check the hostname of the SMTP server",
                    "code": "53149746",
                },
            },
            {
                "destination": "https://support.netapp.com/aods/asupmessage",
                "issue": {
                    "message": 'AutoSupport OnDemand is disabled when "-transport" is not set to "https".',
                    "code": "53149740",
                },
                "node": {
                    "name": "node3",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc"
                        }
                    },
                    "uuid": "0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc",
                },
                "component": "ondemand_server",
                "corrective_action": {
                    "message": 'Run "system node autosupport modify -transport https -node <node name>" to set "-transport" to "https".',
                    "code": "53149740",
                },
            },
        ]
    }
)

```
</div>
</div>

---
### Retrieving AutoSupport configuration and connectivity issues
The following example retrieves AutoSupport configuration and connectivity issues on the cluster. Use `fields=*,issues` parameter to return both configuration and connectivity issues.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Autosupport

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Autosupport()
    resource.get(fields="*,issues")
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
Autosupport(
    {
        "mail_hosts": ["mailhost"],
        "from": "Postmaster",
        "smtp_encryption": "none",
        "transport": "smtp",
        "ondemand_enabled": True,
        "enabled": True,
        "proxy_url": "",
        "to": ["abc@netapp.com", "xyz@netapp.com"],
        "is_minimal": False,
        "contact_support": True,
        "issues": [
            {
                "destination": "mailhost",
                "issue": {
                    "message": "SMTP connectivity check failed for destination: mailhost. Error: Could not resolve host - 'mailhost'",
                    "code": "53149746",
                },
                "node": {
                    "name": "node3",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc"
                        }
                    },
                    "uuid": "0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc",
                },
                "component": "mail_server",
                "corrective_action": {
                    "message": "Check the hostname of the SMTP server",
                    "code": "53149746",
                },
            },
            {
                "destination": "https://support.netapp.com/aods/asupmessage",
                "issue": {
                    "message": 'AutoSupport OnDemand is disabled when "-transport" is not set to "https".',
                    "code": "53149740",
                },
                "node": {
                    "name": "node3",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc"
                        }
                    },
                    "uuid": "0ecfd0a6-f1b3-11e8-9d9f-005056bbaadc",
                },
                "component": "ondemand_server",
                "corrective_action": {
                    "message": 'Run "system node autosupport modify -transport https -node <node name>" to set "-transport" to "https".',
                    "code": "53149740",
                },
            },
        ],
    }
)

```
</div>
</div>

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


__all__ = ["Autosupport", "AutosupportSchema"]
__pdoc__ = {
    "AutosupportSchema.resource": False,
    "AutosupportSchema.opts": False,
}


class AutosupportSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Autosupport object"""

    contact_support = marshmallow_fields.Boolean(
        data_key="contact_support",
        allow_none=True,
    )
    r""" Specifies whether to send the AutoSupport messages to vendor support.

Example: true"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies whether the AutoSupport daemon is enabled.  When this setting is disabled, delivery of all AutoSupport messages is turned off.

Example: true"""

    from_ = marshmallow_fields.Str(
        data_key="from",
        allow_none=True,
    )
    r""" The e-mail address from which the AutoSupport messages are sent. To generate node-specific 'from' addresses, enable '-node-specific-from' parameter via ONTAP CLI.

Example: postmaster@example.com"""

    is_minimal = marshmallow_fields.Boolean(
        data_key="is_minimal",
        allow_none=True,
    )
    r""" Specifies whether the system information is collected in compliant form, to remove private data or in complete form, to enhance diagnostics.

Example: true"""

    issues = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.autosupport_issues.AutosupportIssuesSchema", unknown=EXCLUDE, allow_none=True), data_key="issues", allow_none=True)
    r""" A list of connectivity issues to the HTTPS/SMTP/AOD AutoSupport destinations on the nodes in the cluster along with the corrective actions."""

    mail_hosts = marshmallow_fields.List(marshmallow_fields.Str, data_key="mail_hosts", allow_none=True)
    r""" The names of the mail servers used to deliver AutoSupport messages via SMTP.

Example: ["mailhost1.example.com","mailhost2.example.com"]"""

    ondemand_enabled = marshmallow_fields.Boolean(
        data_key="ondemand_enabled",
        allow_none=True,
    )
    r""" Specifies whether the AutoSupport OnDemand feature is enabled. When AutoSupport OnDemand is enabled, support personnel can remotely trigger new AutoSupport messages, resend existing AutoSupport messages, and decline the delivery of unwanted AutoSupport messages. When this option is disabled, the cluster does not respond to any AutoSupport OnDemand requests from support personnel.


Example: true"""

    partner_addresses = marshmallow_fields.List(marshmallow_fields.Str, data_key="partner_addresses", allow_none=True)
    r""" The list of partner addresses.

Example: ["user1@partner.com","user2@partner.com"]"""

    proxy_url = marshmallow_fields.Str(
        data_key="proxy_url",
        allow_none=True,
    )
    r""" Proxy server for AutoSupport message delivery via HTTPS. Optionally specify a username/password for authentication with the proxy server.

Example: proxy.company.com"""

    smtp_encryption = marshmallow_fields.Str(
        data_key="smtp_encryption",
        validate=enum_validation(['none', 'start_tls']),
        allow_none=True,
    )
    r""" The encryption protocol used to deliver AutoSupport messages via SMTP to the configured mail_hosts.


Valid choices:

* none
* start_tls"""

    to = marshmallow_fields.List(marshmallow_fields.Str, data_key="to", allow_none=True)
    r""" The e-mail addresses to which the AutoSupport messages are sent.

Example: ["user1@example.com","user2@example.com"]"""

    transport = marshmallow_fields.Str(
        data_key="transport",
        validate=enum_validation(['smtp', 'https']),
        allow_none=True,
    )
    r""" The name of the transport protocol used to deliver AutoSupport messages. Note: 'http' transport is no longer supported by AutoSupport servers.


Valid choices:

* smtp
* https"""

    @property
    def resource(self):
        return Autosupport

    gettable_fields = [
        "contact_support",
        "enabled",
        "from_",
        "is_minimal",
        "issues",
        "mail_hosts",
        "ondemand_enabled",
        "partner_addresses",
        "proxy_url",
        "smtp_encryption",
        "to",
        "transport",
    ]
    """contact_support,enabled,from_,is_minimal,issues,mail_hosts,ondemand_enabled,partner_addresses,proxy_url,smtp_encryption,to,transport,"""

    patchable_fields = [
        "contact_support",
        "enabled",
        "from_",
        "is_minimal",
        "mail_hosts",
        "ondemand_enabled",
        "partner_addresses",
        "proxy_url",
        "smtp_encryption",
        "to",
        "transport",
    ]
    """contact_support,enabled,from_,is_minimal,mail_hosts,ondemand_enabled,partner_addresses,proxy_url,smtp_encryption,to,transport,"""

    postable_fields = [
        "contact_support",
        "enabled",
        "from_",
        "is_minimal",
        "mail_hosts",
        "ondemand_enabled",
        "partner_addresses",
        "proxy_url",
        "smtp_encryption",
        "to",
        "transport",
    ]
    """contact_support,enabled,from_,is_minimal,mail_hosts,ondemand_enabled,partner_addresses,proxy_url,smtp_encryption,to,transport,"""

class Autosupport(Resource):
    """Allows interaction with Autosupport objects on the host"""

    _schema = AutosupportSchema
    _path = "/api/support/autosupport"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the AutoSupport configuration of the cluster and if requested, returns connectivity issues with the AutoSupport configuration.<p/>
</br>Important note:
* The **issues** field consists of a list of objects containing details of the node that has a connectivity issue, the issue description, and corrective action you can take to address the issue. When not empty, this indicates a connection issue to the **HTTPS**, **SMTP**, or **AutoSupport On Demand** server.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `issues`
### Related ONTAP commands
* `system node autosupport show -instance`
* `system node autosupport check show-details`
### Learn more
* [`DOC /support/autosupport`](#docs-support-support_autosupport)
"""
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
        r"""Updates the AutoSupport configuration for the entire cluster.
### Related ONTAP commands
* `system node autosupport modify`
### Learn more
* [`DOC /support/autosupport`](#docs-support-support_autosupport)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



