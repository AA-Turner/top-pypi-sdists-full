r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
ONTAP connected clients map functionality is mainly used by the System Manager to display client information.<p/>
The following are details of the fields retrieved for the Connected Clients MAP GET API:<p/>
node.name: Node name hosting this record, essentially the node hosting the "server_ip".
node.uuid: Node UUID hosting this record, essentially the node hosting the "server_ip".
svm.name: SVM name to which the "server_ip" belongs to.
svm.uuid: SVM UUID to which the "server_ip" belongs to.
server_ip: All clients that are connected to this interface are displayed in rows.
client_ips: List of client IP addresses connected to the interface.
## Example
### Retrieving connected client Map information
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsClientsMap

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    print(list(NfsClientsMap.get_collection(return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NfsClientsMap(
        {
            "node": {"name": "vsim1", "uuid": "cc282893-b82f-11e9-a3ad-0050568e8480"},
            "client_ips": ["127.0.0.1"],
            "server_ip": "10.140.72.214",
            "svm": {"name": "vs1", "uuid": "c642db55-b8d0-11e9-9ad1-0050568e8480"},
        }
    )
]

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


__all__ = ["NfsClientsMap", "NfsClientsMapSchema"]
__pdoc__ = {
    "NfsClientsMapSchema.resource": False,
    "NfsClientsMapSchema.opts": False,
}


class NfsClientsMapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsClientsMap object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nfs_clients_map."""

    client_ips = marshmallow_fields.List(marshmallow_fields.Str, data_key="client_ips", allow_none=True)
    r""" Specifies the IP address of the client.


Example: ["127.0.0.1"]"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the nfs_clients_map."""

    server_ip = marshmallow_fields.Str(
        data_key="server_ip",
        allow_none=True,
    )
    r""" Specifies the IP address of the server."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nfs_clients_map."""

    @property
    def resource(self):
        return NfsClientsMap

    gettable_fields = [
        "links",
        "client_ips",
        "node.links",
        "node.name",
        "node.uuid",
        "server_ip",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,client_ips,node.links,node.name,node.uuid,server_ip,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "client_ips",
        "node.name",
        "node.uuid",
        "server_ip",
        "svm.name",
        "svm.uuid",
    ]
    """client_ips,node.name,node.uuid,server_ip,svm.name,svm.uuid,"""

    postable_fields = [
        "client_ips",
        "node.name",
        "node.uuid",
        "server_ip",
        "svm.name",
        "svm.uuid",
    ]
    """client_ips,node.name,node.uuid,server_ip,svm.name,svm.uuid,"""

class NfsClientsMap(Resource):
    """Allows interaction with NfsClientsMap objects on the host"""

    _schema = NfsClientsMapSchema
    _path = "/api/protocols/nfs/connected-client-maps"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NFS clients information.

### Learn more
* [`DOC /protocols/nfs/connected-client-maps`](#docs-NAS-protocols_nfs_connected-client-maps)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all NfsClientsMap resources that match the provided query"""
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
        """Returns a list of RawResources that represent NfsClientsMap resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NFS clients information.

### Learn more
* [`DOC /protocols/nfs/connected-client-maps`](#docs-NAS-protocols_nfs_connected-client-maps)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






