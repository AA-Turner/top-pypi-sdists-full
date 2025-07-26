r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This endpoint manages Ethernet switches used by ONTAP for monitoring and configuration. You can retrieve, configure, add, or delete Ethernet switches, as well as change SNMP credentials and monitor their status.
## Examples
### Retrieving a list of Ethernet switches
The following example shows the response with a list of monitored Ethernet switches.  Note that if the <i>fields=*</i> parameter is not specified, the fields snmp.version, snmp.user, version, monitoring.enabled, and monitoring.reason are not returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Switch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Switch.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Switch(
        {
            "serial_number": "Unknown",
            "address": "172.26.207.77",
            "snmp": {"user": "cshm1!", "version": "snmpv2c"},
            "version": "Cisco Nexus Operating System (NX-OS) Software, Version 9.2(3)",
            "role": "cluster",
            "rcf_version": "RCF NX3232C v1.13 1-CLUSTER",
            "network": "cluster",
            "discovered": True,
            "model": "NX3232C",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switches/RTP-CS01-510R11%28FOC22092K12%29"
                }
            },
            "monitoring": {"reason": "None", "monitored": True, "enabled": True},
            "name": "RTP-CS01-510R11(FOC22092K12)",
        }
    ),
    Switch(
        {
            "serial_number": "FOC22373C3P",
            "address": "172.26.207.82",
            "snmp": {"user": "cshm1!", "version": "snmpv2c"},
            "version": "Cisco Nexus Operating System (NX-OS) Software, Version 9.2(3)",
            "role": "cluster",
            "rcf_version": "RCF NX3232C v1.13 1-CLUSTER",
            "network": "cluster",
            "discovered": True,
            "model": "NX3232C",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switches/RTP-CS01-510R12%28FOC22373C3P%29"
                }
            },
            "monitoring": {"reason": "None", "monitored": True, "enabled": True},
            "name": "RTP-CS01-510R12(FOC22373C3P)",
        }
    ),
    Switch(
        {
            "serial_number": "FOC22170DFR",
            "address": "172.26.207.65",
            "snmp": {"user": "cshm1!", "version": "snmpv2c"},
            "version": "Cisco Nexus Operating System (NX-OS) Software, Version 9.3(3)",
            "role": "storage",
            "rcf_version": "RCF NX3232C v1.13 1-STORAGE",
            "network": "storage",
            "discovered": True,
            "model": "NX3232C",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switches/RTP-SS01-510R10%28FOC22170DFR%29"
                }
            },
            "monitoring": {"reason": "None", "monitored": True, "enabled": True},
            "name": "RTP-SS01-510R10(FOC22170DFR)",
        }
    ),
    Switch(
        {
            "serial_number": "FOC22131U6T",
            "address": "172.26.207.66",
            "snmp": {"user": "cshm1!", "version": "snmpv2c"},
            "version": "Cisco Nexus Operating System (NX-OS) Software, Version 9.3(3)",
            "role": "storage",
            "rcf_version": "RCF NX3232C v1.13 1-STORAGE",
            "network": "storage",
            "discovered": True,
            "model": "NX3232C",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switches/RTP-SS02-510R10%28FOC22131U6T%29"
                }
            },
            "monitoring": {"reason": "None", "monitored": True, "enabled": True},
            "name": "RTP-SS02-510R10(FOC22131U6T)",
        }
    ),
]

```
</div>
</div>

### Retrieving an Ethernet switch
The following example shows the response of the requested Ethernet switch. If there is no Ethernet switch with the requested name, an error is returned.
 ```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Switch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Switch(name="RTP-SS02-510R10(FOC22131U6T)")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Switch(
    {
        "serial_number": "FOC22131U6T",
        "address": "172.26.207.66",
        "snmp": {"user": "cshm1!", "version": "snmpv2c"},
        "version": "Cisco Nexus Operating System (NX-OS) Software, Version 9.3(3)",
        "role": "storage",
        "rcf_version": "RCF NX3232C v1.13 1-STORAGE",
        "network": "storage",
        "discovered": True,
        "model": "NX3232C",
        "_links": {
            "self": {
                "href": "/api/network/ethernet/switches/RTP-SS02-510R10(FOC22131U6T)"
            }
        },
        "monitoring": {"reason": "None", "monitored": True, "enabled": True},
        "name": "RTP-SS02-510R10(FOC22131U6T)",
    }
)

```
</div>
</div>

### Configuring monitoring settings for an Ethernet switch
The following example configures SNMP credential and version settings for an Ethernet switch. If the provided information is not valid, an error is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Switch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Switch(name="sconqa-corduroyl-03")
    resource.snmp = {"version": "snmpv2c", "user": "cshm1!"}
    resource.patch()

```

### Adding an Ethernet switch
The following example adds an Ethernet switch for monitoring. If the provided information is not valid, an error is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Switch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Switch()
    resource.name = "RTP-SS02-510R10(FOC22131U6T)"
    resource.address = "172.26.207.66"
    resource.model = "NX3232C"
    resource.monitoring = {"enabled": "true"}
    resource.network = "storage"
    resource.snmp = {"version": "snmpv2c", "user": "cshm1!"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Switch(
    {
        "address": "172.26.207.66",
        "snmp": {"user": "cshm1!", "version": "snmpv2c"},
        "network": "storage",
        "model": "NX3232C",
        "monitoring": {"enabled": True},
        "name": "RTP-SS02-510R10(FOC22131U6T)",
    }
)

```
</div>
</div>

### Deleting an Ethernet switch
The following example deletes an Ethernet switch. If there is no Ethernet switch with the requested name, an error is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Switch

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Switch(name="sconqa-corduroyl-03")
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


__all__ = ["Switch", "SwitchSchema"]
__pdoc__ = {
    "SwitchSchema.resource": False,
    "SwitchSchema.opts": False,
}


class SwitchSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Switch object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the switch."""

    address = marshmallow_fields.Str(
        data_key="address",
        allow_none=True,
    )
    r""" IP Address."""

    discovered = marshmallow_fields.Boolean(
        data_key="discovered",
        allow_none=True,
    )
    r""" Discovered By ONTAP CDP/LLDP"""

    model = marshmallow_fields.Str(
        data_key="model",
        allow_none=True,
    )
    r""" Model Number."""

    monitoring = marshmallow_fields.Nested("netapp_ontap.models.switch_monitoring.SwitchMonitoringSchema", data_key="monitoring", unknown=EXCLUDE, allow_none=True)
    r""" The monitoring field of the switch."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Name."""

    network = marshmallow_fields.Str(
        data_key="network",
        validate=enum_validation(['cluster', 'storage']),
        allow_none=True,
    )
    r""" Switch Network.

Valid choices:

* cluster
* storage"""

    rcf_version = marshmallow_fields.Str(
        data_key="rcf_version",
        allow_none=True,
    )
    r""" The switch reference configuration file (RCF) version.

Example: RCF NX9336C-FX2 v1.13 1-CLUSTER"""

    role = marshmallow_fields.Str(
        data_key="role",
        allow_none=True,
    )
    r""" Switch role based on the interface configurations. Using '+' to combine multiple roles.
Available role types are: cluster, multicluster, storage, multistorage, metrocluster.


Example:"""

    serial_number = marshmallow_fields.Str(
        data_key="serial_number",
        allow_none=True,
    )
    r""" Serial Number."""

    snmp = marshmallow_fields.Nested("netapp_ontap.models.switch_snmp.SwitchSnmpSchema", data_key="snmp", unknown=EXCLUDE, allow_none=True)
    r""" The snmp field of the switch."""

    version = marshmallow_fields.Str(
        data_key="version",
        allow_none=True,
    )
    r""" Software Version."""

    @property
    def resource(self):
        return Switch

    gettable_fields = [
        "links",
        "address",
        "discovered",
        "model",
        "monitoring",
        "name",
        "network",
        "rcf_version",
        "role",
        "serial_number",
        "snmp",
        "version",
    ]
    """links,address,discovered,model,monitoring,name,network,rcf_version,role,serial_number,snmp,version,"""

    patchable_fields = [
        "address",
        "monitoring",
        "snmp",
    ]
    """address,monitoring,snmp,"""

    postable_fields = [
        "address",
        "model",
        "monitoring",
        "name",
        "network",
        "snmp",
    ]
    """address,model,monitoring,name,network,snmp,"""

class Switch(Resource):
    r""" Ethernet Switch REST API """

    _schema = SwitchSchema
    _path = "/api/network/ethernet/switches"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of Ethernet switches.
### Related ONTAP commands
* `system switch ethernet show`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
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
        """Returns a count of all Switch resources that match the provided query"""
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
        """Returns a list of RawResources that represent Switch resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Switch"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Configures monitoring settings for an Ethernet switch.
### Related ONTAP commands
* `system switch ethernet modify`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["Switch"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Switch"], NetAppResponse]:
        r"""Adds an Ethernet switch.
### Required properties
* `name` - Name of the switch to create.
* `address` - Switch IP address.
* `model` - Switch model number.
* `monitoring.enabled` - Whether the switch should be monitored by CSHM.
* `network`
  * _cluster_ for cluster or shared switches.
  * _storage_ for storage switches.
* `snmp.version` - SNMP version.
* `snmp.user` - SNMP user.
### Related ONTAP commands
* `system switch ethernet create`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
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
        records: Iterable["Switch"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an Ethernet switch.
### Related ONTAP commands
* `system switch ethernet delete`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of Ethernet switches.
### Related ONTAP commands
* `system switch ethernet show`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of an Ethernet switch.
### Related ONTAP commands
* `system switch ethernet show`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
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
        r"""Adds an Ethernet switch.
### Required properties
* `name` - Name of the switch to create.
* `address` - Switch IP address.
* `model` - Switch model number.
* `monitoring.enabled` - Whether the switch should be monitored by CSHM.
* `network`
  * _cluster_ for cluster or shared switches.
  * _storage_ for storage switches.
* `snmp.version` - SNMP version.
* `snmp.user` - SNMP user.
### Related ONTAP commands
* `system switch ethernet create`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
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
        r"""Configures monitoring settings for an Ethernet switch.
### Related ONTAP commands
* `system switch ethernet modify`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
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
        r"""Deletes an Ethernet switch.
### Related ONTAP commands
* `system switch ethernet delete`
### Learn more
* [`DOC /network/ethernet/switches`](#docs-networking-network_ethernet_switches)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


