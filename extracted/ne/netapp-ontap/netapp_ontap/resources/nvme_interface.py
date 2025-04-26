r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
NVMe interfaces are network interfaces configured to support an NVMe over Fabrics (NVMe-oF) protocol. The NVMe interfaces are Fibre Channel (FC) interfaces supporting an NVMe-oF data protocol. Regardless of the underlying physical and data protocol, NVMe interfaces are treated equally for host-side application configuration. This endpoint provides a consolidated view of all NVMe interfaces for the purpose of configuring host-side applications.<br/>
The NVMe interfaces REST API provides NVMe-specific information about network interfaces configured to support an NVMe-oF protocol.<br/>
NVMe interfaces must be created using the protocol-specific endpoints for FC interfaces. See [`POST /network/fc/interfaces`](#/networking/fc_interface_create). After creation, the interfaces are available via this interface.
## Examples
### Retrieving summary information for all NVMe interfaces
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NvmeInterface.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NvmeInterface(
        {
            "name": "nvme1",
            "uuid": "74d69872-0d30-11e9-a684-005056bbdb14",
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/interfaces/74d69872-0d30-11e9-a684-005056bbdb14"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/013e2c44-0d30-11e9-a684-005056bbdb14"
                    }
                },
                "uuid": "013e2c44-0d30-11e9-a684-005056bbdb14",
            },
        }
    ),
    NvmeInterface(
        {
            "name": "nvme2",
            "uuid": "77ded991-0d30-11e9-a684-005056bbdb14",
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/interfaces/77ded991-0d30-11e9-a684-005056bbdb14"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/013e2c44-0d30-11e9-a684-005056bbdb14"
                    }
                },
                "uuid": "013e2c44-0d30-11e9-a684-005056bbdb14",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving detailed information for a specific NVMe interface
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeInterface(uuid="77ded991-0d30-11e9-a684-005056bbdb14")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
NvmeInterface(
    {
        "name": "nvme2",
        "transport_address": "nn-0x2003005056bbdb14:pn-0x2005005056bbdb14",
        "node": {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/cd4d47fd-0d2e-11e9-a684-005056bbdb14"
                }
            },
            "uuid": "cd4d47fd-0d2e-11e9-a684-005056bbdb14",
        },
        "uuid": "77ded991-0d30-11e9-a684-005056bbdb14",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/protocols/nvme/interfaces/77ded991-0d30-11e9-a684-005056bbdb14"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/013e2c44-0d30-11e9-a684-005056bbdb14"}
            },
            "uuid": "013e2c44-0d30-11e9-a684-005056bbdb14",
        },
        "fc_interface": {
            "wwnn": "20:03:00:50:56:bb:db:14",
            "_links": {
                "self": {
                    "href": "/api/network/fc/interfaces/77ded991-0d30-11e9-a684-005056bbdb14"
                }
            },
            "port": {
                "name": "1a",
                "node": {"name": "node1"},
                "uuid": "081ec491-0d2f-11e9-a684-005056bbdb14",
                "_links": {
                    "self": {
                        "href": "/api/network/fc/ports/081ec491-0d2f-11e9-a684-005056bbdb14"
                    }
                },
            },
            "wwpn": "20:05:00:50:56:bb:db:14",
        },
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


__all__ = ["NvmeInterface", "NvmeInterfaceSchema"]
__pdoc__ = {
    "NvmeInterfaceSchema.resource": False,
    "NvmeInterfaceSchema.opts": False,
}


class NvmeInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nvme_interface."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The administrative state of the NVMe interface."""

    fc_interface = marshmallow_fields.Nested("netapp_ontap.models.nvme_interface_fc_interface.NvmeInterfaceFcInterfaceSchema", data_key="fc_interface", unknown=EXCLUDE, allow_none=True)
    r""" The attributes specific to a Fibre Channel-based NVMe interface.<br/>
This is populated when `interface_type` is _fc_interface_."""

    interface_type = marshmallow_fields.Str(
        data_key="interface_type",
        validate=enum_validation(['fc_interface', 'ip_interface']),
        allow_none=True,
    )
    r""" The underlying interface type of the NVMe interface. This property identifies which of _fc_interface_ and _ip_interface_ will be further populated.


Valid choices:

* fc_interface
* ip_interface"""

    ip_interface = marshmallow_fields.Nested("netapp_ontap.models.nvme_interface_ip_interface.NvmeInterfaceIpInterfaceSchema", data_key="ip_interface", unknown=EXCLUDE, allow_none=True)
    r""" The attributes specific to an IP-based NVMe interface.<br/>
This is populated when `interface_type` is _ip_interface_."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The name of the NVMe interface.


Example: lif1"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the nvme_interface."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nvme_interface."""

    transport_address = marshmallow_fields.Str(
        data_key="transport_address",
        allow_none=True,
    )
    r""" The transport address of the NVMe interface.


Example: nn-0x200a00a0989062da:pn-0x200100a0989062da"""

    transport_protocols = marshmallow_fields.List(marshmallow_fields.Str, data_key="transport_protocols", allow_none=True)
    r""" The transport protocols supported by the NVMe interface."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the NVMe interface.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return NvmeInterface

    gettable_fields = [
        "links",
        "enabled",
        "fc_interface",
        "interface_type",
        "ip_interface",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "transport_address",
        "transport_protocols",
        "uuid",
    ]
    """links,enabled,fc_interface,interface_type,ip_interface,name,node.links,node.name,node.uuid,svm.links,svm.name,svm.uuid,transport_address,transport_protocols,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class NvmeInterface(Resource):
    r""" NVMe interfaces are network interfaces configured to support an NVMe over Fabrics (NVMe-oF) protocol. The NVMe interfaces are Fibre Channel interfaces supporting an NVMe-oF data protocol. Regardless of the underlying physical and data protocol, NVMe interfaces are treated equally for host-side application configuration. This endpoint provides a consolidated view of all NVMe interfaces for the purpose of configuring host-side applications.<br/>
NVMe interfaces must be created using the protocol-specific endpoints for Fibre Channel interfaces. See [`POST /network/fc/interfaces`](#/networking/fc_interface_create). After creation, the interfaces are available via this interface. """

    _schema = NvmeInterfaceSchema
    _path = "/api/protocols/nvme/interfaces"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NVMe interfaces.
### Related ONTAP commands
* `vserver nvme show-interface`
### Learn more
* [`DOC /protocols/nvme/interfaces`](#docs-NVMe-protocols_nvme_interfaces)
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
        """Returns a count of all NvmeInterface resources that match the provided query"""
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
        """Returns a list of RawResources that represent NvmeInterface resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NVMe interfaces.
### Related ONTAP commands
* `vserver nvme show-interface`
### Learn more
* [`DOC /protocols/nvme/interfaces`](#docs-NVMe-protocols_nvme_interfaces)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NVMe interface.
### Related ONTAP commands
* `vserver nvme show-interface`
### Learn more
* [`DOC /protocols/nvme/interfaces`](#docs-NVMe-protocols_nvme_interfaces)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





