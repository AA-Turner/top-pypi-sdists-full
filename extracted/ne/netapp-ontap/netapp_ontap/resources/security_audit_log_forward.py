r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API controls the forwarding of audit log information to remote syslog/splunk servers. Multiple destinations can be configured and all audit records are forwarded to all destinations.</br>
A GET operation retrieves information about remote syslog/splunk server destinations.
A POST operation creates a remote syslog/splunk server destination.
A GET operation on /security/audit/destinations/{address}/{port} retrieves information about the syslog/splunk server destination given its address and port number.
A PATCH operation on /security/audit/destinations/{address}/{port} updates information about the syslog/splunk server destination given its address and port number.
A DELETE operation on /security/audit/destinations/{address}/{port} deletes a syslog/splunk server destination given its address and port number.
### Overview of fields used for creating a remote syslog/splunk destination
The fields used for creating a remote syslog/splunk destination fall into the following categories
#### Required properties
All of the following fields are required for creating a remote syslog/splunk destination

* `address`
#### Optional properties
All of the following fields are optional for creating a remote syslog/splunk destination

* `port`
* `ipspace`
* `protocol`
* `facility`
* `verify_server`
* `message_format` (Can be either "legacy_netapp" or "rfc_5424")
* `timestamp_format_override` (Can be either "no_override", "rfc_3164", "iso_8601_utc" or "iso_8601_local_time")
* `hostname_format_override` (Can be either "no_override", "fqdn" or "hostname_only")
<br />
---
## Examples
### Retrieving remote syslog/splunk server destinations
The following example shows remote syslog/splunk server destinations
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAuditLogForward

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    print(list(SecurityAuditLogForward.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[SecurityAuditLogForward({"address": "1.1.1.1", "port": 514})]

```
</div>
</div>

---
### Creating remote syslog/splunk server destinations
The following example creates remote syslog/splunk server destinations.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAuditLogForward

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = SecurityAuditLogForward()
    resource.address = "1.1.1.1"
    resource.port = 514
    resource.protocol = "udp_unencrypted"
    resource.facility = "kern"
    resource.post(hydrate=True, force=True)
    print(resource)

```

---
### Retrieving a remote syslog/splunk server destination given its destination address and port number
The following example retrieves a remote syslog/splunk server destination given its destination address and port number.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAuditLogForward

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = SecurityAuditLogForward(port=514, address="1.1.1.1")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
SecurityAuditLogForward(
    {
        "timestamp_format_override": "no_override",
        "facility": "kern",
        "verify_server": False,
        "protocol": "udp_unencrypted",
        "ipspace": {"name": "Default", "uuid": "a97a3549-f7ae-11ec-b6bc-005056a7c8ff"},
        "address": "1.1.1.1",
        "message_format": "legacy_netapp",
        "hostname_format_override": "no_override",
        "port": 514,
    }
)

```
</div>
</div>

---
### Updating a remote syslog/splunk server destination given its destination address and port number
The following example updates a remote syslog/splunk server destination configuration given its destination address and port number.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAuditLogForward

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = SecurityAuditLogForward(port=514, address="1.1.1.1")
    resource.facility = "user"
    resource.patch()

```

---
### Deleting a remote syslog/splunk server destination given its destination address and port number
The following example deletes a remote syslog/splunk server destination configuration given its destination address and port number.
<br />
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityAuditLogForward

with HostConnection(
    "<cluster-ip>", username="admin", password="password", verify=False
):
    resource = SecurityAuditLogForward(port=514, address="1.1.1.1")
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


__all__ = ["SecurityAuditLogForward", "SecurityAuditLogForwardSchema"]
__pdoc__ = {
    "SecurityAuditLogForwardSchema.resource": False,
    "SecurityAuditLogForwardSchema.opts": False,
}


class SecurityAuditLogForwardSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityAuditLogForward object"""

    address = marshmallow_fields.Str(
        data_key="address",
        allow_none=True,
    )
    r""" Destination syslog|splunk host to forward audit records to. This can be an IP address (IPv4|IPv6) or a hostname.

Example: 1.1.1.1"""

    facility = marshmallow_fields.Str(
        data_key="facility",
        validate=enum_validation(['kern', 'user', 'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7']),
        allow_none=True,
    )
    r""" This is the standard Syslog Facility value that is used when sending audit records to a remote server.

Valid choices:

* kern
* user
* local0
* local1
* local2
* local3
* local4
* local5
* local6
* local7"""

    hostname_format_override = marshmallow_fields.Str(
        data_key="hostname_format_override",
        validate=enum_validation(['no_override', 'fqdn', 'hostname_only']),
        allow_none=True,
    )
    r""" Syslog Hostname Format Override

Valid choices:

* no_override
* fqdn
* hostname_only"""

    ipspace = marshmallow_fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE, allow_none=True)
    r""" The ipspace field of the security_audit_log_forward."""

    message_format = marshmallow_fields.Str(
        data_key="message_format",
        validate=enum_validation(['legacy_netapp', 'rfc_5424']),
        allow_none=True,
    )
    r""" Syslog message format to be used. legacy_netapp format (variation of RFC-3164) is default message format.

Valid choices:

* legacy_netapp
* rfc_5424"""

    port = Size(
        data_key="port",
        allow_none=True,
    )
    r""" Destination Port. The default port depends on the protocol chosen:
For un-encrypted destinations the default port is 514.
For encrypted destinations the default port is 6514.


Example: 514"""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['udp_unencrypted', 'tcp_unencrypted', 'tcp_encrypted']),
        allow_none=True,
    )
    r""" Log forwarding protocol

Valid choices:

* udp_unencrypted
* tcp_unencrypted
* tcp_encrypted"""

    timestamp_format_override = marshmallow_fields.Str(
        data_key="timestamp_format_override",
        validate=enum_validation(['no_override', 'rfc_3164', 'iso_8601_utc', 'iso_8601_local_time']),
        allow_none=True,
    )
    r""" Syslog Timestamp Format Override.

Valid choices:

* no_override
* rfc_3164
* iso_8601_utc
* iso_8601_local_time"""

    verify_server = marshmallow_fields.Boolean(
        data_key="verify_server",
        allow_none=True,
    )
    r""" This is only applicable when the protocol is tcp_encrypted. This controls whether the remote server's certificate is validated. Setting "verify_server" to "true" will enforce validation of remote server's certificate. Setting "verify_server" to "false" will not enforce validation of remote server's certificate."""

    @property
    def resource(self):
        return SecurityAuditLogForward

    gettable_fields = [
        "address",
        "facility",
        "hostname_format_override",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "message_format",
        "port",
        "protocol",
        "timestamp_format_override",
        "verify_server",
    ]
    """address,facility,hostname_format_override,ipspace.links,ipspace.name,ipspace.uuid,message_format,port,protocol,timestamp_format_override,verify_server,"""

    patchable_fields = [
        "facility",
        "hostname_format_override",
        "ipspace.name",
        "ipspace.uuid",
        "message_format",
        "timestamp_format_override",
        "verify_server",
    ]
    """facility,hostname_format_override,ipspace.name,ipspace.uuid,message_format,timestamp_format_override,verify_server,"""

    postable_fields = [
        "address",
        "facility",
        "hostname_format_override",
        "ipspace.name",
        "ipspace.uuid",
        "message_format",
        "port",
        "protocol",
        "timestamp_format_override",
        "verify_server",
    ]
    """address,facility,hostname_format_override,ipspace.name,ipspace.uuid,message_format,port,protocol,timestamp_format_override,verify_server,"""

class SecurityAuditLogForward(Resource):
    """Allows interaction with SecurityAuditLogForward objects on the host"""

    _schema = SecurityAuditLogForwardSchema
    _path = "/api/security/audit/destinations"
    _keys = ["address", "port"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Defines a remote syslog/splunk server for sending audit information to.
### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all SecurityAuditLogForward resources that match the provided query"""
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
        """Returns a list of RawResources that represent SecurityAuditLogForward resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SecurityAuditLogForward"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates remote syslog/splunk server information.
### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SecurityAuditLogForward"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SecurityAuditLogForward"], NetAppResponse]:
        r"""Configures remote syslog/splunk server information.
### Required properties
All of the following fields are required for creating a remote syslog/splunk destination
* `address`
### Optional properties
All of the following fields are optional for creating a remote syslog/splunk destination
* `port` (1 - 65535)
* `ipspace`
* `protocol`
* `facility`
* `verify_server` (Can only be "true" when protocol is "tcp_encrypted")
* `message_format` (Can be either "legacy-netapp" or "rfc-5424")
* `timestamp_format_override` (Can be either "no-override", "rfc-3164", "iso-8601-utc" or "iso-8601-local-time")
* `hostname_format_override` (Can be either "no-override", "fqdn" or "hostname-only")

### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["SecurityAuditLogForward"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes remote syslog/splunk server information.
### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Defines a remote syslog/splunk server for sending audit information to.
### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Defines a remote syslog/splunk server for sending audit information to.
### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
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
        r"""Configures remote syslog/splunk server information.
### Required properties
All of the following fields are required for creating a remote syslog/splunk destination
* `address`
### Optional properties
All of the following fields are optional for creating a remote syslog/splunk destination
* `port` (1 - 65535)
* `ipspace`
* `protocol`
* `facility`
* `verify_server` (Can only be "true" when protocol is "tcp_encrypted")
* `message_format` (Can be either "legacy-netapp" or "rfc-5424")
* `timestamp_format_override` (Can be either "no-override", "rfc-3164", "iso-8601-utc" or "iso-8601-local-time")
* `hostname_format_override` (Can be either "no-override", "fqdn" or "hostname-only")

### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
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
        r"""Updates remote syslog/splunk server information.
### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
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
        r"""Deletes remote syslog/splunk server information.
### Learn more
* [`DOC /security/audit/destinations`](#docs-security-security_audit_destinations)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


