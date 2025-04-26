r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Cluster wide SNMP configuration. You can configure or retrieve the following SNMP parameters using this endpoint:

* enable or disable SNMP
* enable or disable SNMP authentication traps
* enable or disable SNMP traps
##
This endpoint can also be used to trigger an SNMP test trap.
## Examples
### Disables SNMP protocol in the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.enabled = False
    resource.patch()

```

### Enables SNMP authentication traps in the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.auth_traps_enabled = True
    resource.patch()

```

### Enables SNMP protocol and SNMP authentication traps in the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.enabled = True
    resource.auth_traps_enabled = True
    resource.patch()

```

### Disables the SNMP trap subsystem in the cluster. Once the SNMP trap subsystem is disabled, the cluster stops sending SNMP traps.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.traps_enabled = False
    resource.patch()

```

### Sets the contact and location for the SNMP server
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.contact = "support@company.com"
    resource.location = "Building 1"
    resource.patch()

```

### Triggers an SNMP test trap.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.trigger_test_trap = True
    resource.patch()

```

### Enables the SNMP protocol in the cluster, SNMP traps, and triggers an SNMP test trap.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.enabled = True
    resource.traps_enabled = True
    resource.trigger_test_trap = True
    resource.patch()

```

<br/>"""

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


__all__ = ["Snmp", "SnmpSchema"]
__pdoc__ = {
    "SnmpSchema.resource": False,
    "SnmpSchema.opts": False,
}


class SnmpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Snmp object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snmp."""

    auth_traps_enabled = marshmallow_fields.Boolean(
        data_key="auth_traps_enabled",
        allow_none=True,
    )
    r""" Specifies whether to enable or disable SNMP authentication traps.

Example: true"""

    contact = marshmallow_fields.Str(
        data_key="contact",
        allow_none=True,
    )
    r""" Specifies the contact person for the SNMP server

Example: support@company.com"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Specifies whether to enable or disable SNMP.

Example: true"""

    location = marshmallow_fields.Str(
        data_key="location",
        allow_none=True,
    )
    r""" Specifies the location of the SNMP server

Example: Building 1"""

    traps_enabled = marshmallow_fields.Boolean(
        data_key="traps_enabled",
        allow_none=True,
    )
    r""" Specifies whether to enable or disable SNMP traps.

Example: true"""

    trigger_test_trap = marshmallow_fields.Boolean(
        data_key="trigger_test_trap",
        allow_none=True,
    )
    r""" Trigger a test SNMP trap.

Example: true"""

    @property
    def resource(self):
        return Snmp

    gettable_fields = [
        "links",
        "auth_traps_enabled",
        "contact",
        "enabled",
        "location",
        "traps_enabled",
    ]
    """links,auth_traps_enabled,contact,enabled,location,traps_enabled,"""

    patchable_fields = [
        "auth_traps_enabled",
        "contact",
        "enabled",
        "location",
        "traps_enabled",
        "trigger_test_trap",
    ]
    """auth_traps_enabled,contact,enabled,location,traps_enabled,trigger_test_trap,"""

    postable_fields = [
    ]
    """"""

class Snmp(Resource):
    r""" Cluster-wide SNMP configuration. """

    _schema = SnmpSchema
    _path = "/api/support/snmp"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster wide SNMP configuration.
### Related ONTAP commands
* `options snmp.enable`
* `system snmp show`
### Learn more
* [`DOC /support/snmp`](#docs-support-support_snmp)
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
        r"""Updates the cluster wide SNMP configuration, such as:
* enabling or disabling SNMP
* enabling or disabling SNMP traps
* enabling or disabling authentication traps
* setting the contact and location information for the SNMP server
* triggering an SNMP test trap
### Related ONTAP commands
* `options snmp.enable`
* `system snmp authtrap`
* `system snmp init`
### Learn more
* [`DOC /support/snmp`](#docs-support-support_snmp)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



