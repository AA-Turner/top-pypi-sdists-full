r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Displays information about NBT connections for the cluster. Displays the IP address associated with the interfaces, the IP addresses of the WINS servers in use, and information about the registered NetBIOS names for the cluster. You can use this command to troubleshoot NetBIOS name resolution problems.
## Examples
### Retrieving full CIFS NetBIOS information for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Netbios

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Netbios.get_collection(return_timeout=15, fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Netbios(
        {
            "wins_servers": [{"ip": "10.10.10.10", "state": "inactive"}],
            "interfaces": ["172.10.144.44"],
            "name": "CIFSERVER2",
            "time_left": 0,
            "node": {"name": "vsim2", "uuid": "c2179c2c-777f-11ec-95a1-1315568ef5fd"},
            "state": "broadcast",
            "name_registration_type": "",
            "suffix": "00",
            "svm": {"name": "vs1", "uuid": "99a3bd71-777f-11ec-95a1-1315568ef5fd"},
            "mode": "h",
            "scope": "group",
        }
    ),
    Netbios(
        {
            "wins_servers": [{"ip": "10.10.10.10", "state": "inactive"}],
            "interfaces": ["172.10.144.44"],
            "name": "CIFSERVER2",
            "time_left": 0,
            "node": {"name": "vsim2", "uuid": "c2179c2c-777f-11ec-95a1-1315568ef5fd"},
            "state": "broadcast",
            "name_registration_type": "group",
            "suffix": "20",
            "svm": {"name": "vs1", "uuid": "99a3bd71-777f-11ec-95a1-1315568ef5fd"},
            "mode": "h",
            "scope": "",
        }
    ),
]

```
</div>
</div>

---
### Retrieving CIFS NetBIOS Information for a particular SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Netbios

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Netbios.get_collection(
                return_timeout=15,
                fields="*",
                **{"svm.uuid": "45a3bd71-777f-11ec-95a1-1315568ef5fd"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    Netbios(
        {
            "wins_servers": [{"ip": "10.10.10.10", "state": "inactive"}],
            "interfaces": ["172.10.144.44"],
            "name": "CIFSERVER2",
            "time_left": 0,
            "node": {"name": "vsim2", "uuid": "c2179c2c-777f-11ec-95a1-1315568ef5fd"},
            "state": "broadcast",
            "name_registration_type": "",
            "suffix": "00",
            "svm": {"name": "vs1", "uuid": "45a3bd71-777f-11ec-95a1-1315568ef5fd"},
            "mode": "h",
            "scope": "group",
        }
    )
]

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


__all__ = ["Netbios", "NetbiosSchema"]
__pdoc__ = {
    "NetbiosSchema.resource": False,
    "NetbiosSchema.opts": False,
}


class NetbiosSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Netbios object"""

    interfaces = marshmallow_fields.List(marshmallow_fields.Str, data_key="interfaces", allow_none=True)
    r""" The interfaces field of the netbios."""

    mode = marshmallow_fields.Str(
        data_key="mode",
        validate=enum_validation(['p', 'h', 'm', 'b']),
        allow_none=True,
    )
    r""" Specifies the mode in which the NetBIOS name service is configured. The supported values are:

  * p - Point to Point
  * h - Hybrid
  * m - Mixed
  * b - Broadcast


Valid choices:

* p
* h
* m
* b"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Specifies the NetBIOS name.

Example: CLUSTER_1"""

    name_registration_type = marshmallow_fields.Str(
        data_key="name_registration_type",
        validate=enum_validation(['registered', 'active', 'permanent', 'group', '']),
        allow_none=True,
    )
    r""" Specifies the name registration type.

Valid choices:

* registered
* active
* permanent
* group
*"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the netbios."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        allow_none=True,
    )
    r""" Specifies the NetBIOS name scope. Scope is used as a name for the set of NetBIOS nodes that participate in a NetBIOS over TCP (NBT) virtual LAN."""

    state = marshmallow_fields.Str(
        data_key="state",
        validate=enum_validation(['must_register', 'must_unregister', 'wins', 'broadcast', 'name_released', 'wins_conflict', 'broadcast_conflict']),
        allow_none=True,
    )
    r""" Specifies the registration state of the NetBIOS Name.

Valid choices:

* must_register
* must_unregister
* wins
* broadcast
* name_released
* wins_conflict
* broadcast_conflict"""

    suffix = marshmallow_fields.Str(
        data_key="suffix",
        allow_none=True,
    )
    r""" Specifies the NetBIOS suffix. A NetBIOS suffix is the 16th character of the 16-character NetBIOS name. The NetBIOS suffix is used by Microsoft Networking software to identify functionality installed on the registered device."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the netbios."""

    time_left = Size(
        data_key="time_left",
        allow_none=True,
    )
    r""" Specifies the registration time left with WINS, in minutes."""

    wins_servers = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.server.ServerSchema", unknown=EXCLUDE, allow_none=True), data_key="wins_servers", allow_none=True)
    r""" List of WINS"""

    @property
    def resource(self):
        return Netbios

    gettable_fields = [
        "interfaces",
        "mode",
        "name",
        "name_registration_type",
        "node.links",
        "node.name",
        "node.uuid",
        "scope",
        "state",
        "suffix",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "time_left",
        "wins_servers",
    ]
    """interfaces,mode,name,name_registration_type,node.links,node.name,node.uuid,scope,state,suffix,svm.links,svm.name,svm.uuid,time_left,wins_servers,"""

    patchable_fields = [
        "interfaces",
        "mode",
        "name",
        "name_registration_type",
        "node.name",
        "node.uuid",
        "scope",
        "state",
        "suffix",
        "svm.name",
        "svm.uuid",
        "wins_servers",
    ]
    """interfaces,mode,name,name_registration_type,node.name,node.uuid,scope,state,suffix,svm.name,svm.uuid,wins_servers,"""

    postable_fields = [
        "interfaces",
        "mode",
        "name",
        "name_registration_type",
        "node.name",
        "node.uuid",
        "scope",
        "state",
        "suffix",
        "svm.name",
        "svm.uuid",
        "wins_servers",
    ]
    """interfaces,mode,name,name_registration_type,node.name,node.uuid,scope,state,suffix,svm.name,svm.uuid,wins_servers,"""

class Netbios(Resource):
    """Allows interaction with Netbios objects on the host"""

    _schema = NetbiosSchema
    _path = "/api/protocols/cifs/netbios"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NetBIOS information.
### Related ONTAP commands
* `vserver cifs nbtstat`
### Learn more
* [`DOC /protocols/cifs/netbios`](#docs-NAS-protocols_cifs_netbios)
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
        """Returns a count of all Netbios resources that match the provided query"""
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
        """Returns a list of RawResources that represent Netbios resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NetBIOS information.
### Related ONTAP commands
* `vserver cifs nbtstat`
### Learn more
* [`DOC /protocols/cifs/netbios`](#docs-NAS-protocols_cifs_netbios)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






