r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
ONTAP connected clients show functionality is mainly used to provide a list of currently connected NFS clients. It also provides a potential list of other NFS clients that can be connected but are currently idle and a list of recently unmounted clients. If a client connected to the NFS server is idle for longer than the maximum cache idle time, then the entry will be removed. By default, the maximum cache idle time is 48 hours.<p/>
The following are details of the fields retrieved for the Connected Clients GET API:<p/>
node.name: The node name hosting this record; basically the node hosting the "server_ip".
node.uuid: The node UUID hosting this record; basically the node hosting the "server_ip".
svm.name: The svm name to which the "server_ip" belongs to.
svm.uuid: The svm uuid to which the "server_ip" belongs to.
server_ip: All clients that are connected to this interface are displayed in rows.
client_ip: The IP address of the client that is connected to the interface.
volume.name: The name of the volume the client is accessing.
volume.uuid: The UUID of the volume the client is accessing. This field is expensive field and will be fetched in advance privilege level.
protocol: The NFS protocol version over which client is accessing the volume.
export_policy.id: The export policy ID associated with the volume.
export_policy.name: The export policy name associated with the volume.
idle_duration: The time elapsed since the last request was sent by the client for this volume.
local_request_count: A counter that tracks requests that are sent to the volume with fast-path to local node.
remote_request_count: A counter that tracks requests that are sent to the volume with slow-path to remote node.
trunking_enabled: Flag that indicates the trunking status for the specified SVM connection. True indicates that the trunking feature is enabled while false indicates that the trunking feature is disabled.
## Related CLI command
The CLI command for ONTAP connected clients is: "nfs connected-clients show"
cluster-1::*> nfs connected-clients show
     Node: node1
  Vserver: vs1
  Data-Ip: xxx.xxx.xxx.xxx
                                                   Local Remote
Client-Ip       Protocol Volume    Policy   Idle-Time    Reqs  Reqs   Trunking
--------------- -------- --------- -------- ------------ ----- ------ --------
xxx.xxx.xxx.xxx nfs4.1   root_vol  pol1     6s           9     0      false
xxx.xxx.xxx.xxx nfs3     vol1      pol1     56s          7     0      false
xxx.xxx.xxx.xxx nfs4.1   vol1      pol1     6s           7     0      false
3 entries were displayed.
## Example
### Retrieves connected client information
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NfsClients

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    print(list(NfsClients.get_collection(return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    NfsClients(
        {
            "volume": {"name": "rvol1", "uuid": "c6bbc6f2-b8d0-11e9-9ad1-0050568e8480"},
            "protocol": "nfs4",
            "node": {"name": "vsim1", "uuid": "cc282893-b82f-11e9-a3ad-0050568e8480"},
            "server_ip": "10.140.72.214",
            "client_ip": "10.140.137.57",
            "svm": {"name": "vs1", "uuid": "c642db55-b8d0-11e9-9ad1-0050568e8480"},
        }
    ),
    NfsClients(
        {
            "volume": {"name": "vol1", "uuid": "d28d1999-b8d0-11e9-9ad1-0050568e8480"},
            "protocol": "nfs3",
            "node": {"name": "vsim1", "uuid": "cc282893-b82f-11e9-a3ad-0050568e8480"},
            "server_ip": "10.140.72.214",
            "client_ip": "10.140.137.57",
            "svm": {"name": "vs1", "uuid": "c642db55-b8d0-11e9-9ad1-0050568e8480"},
        }
    ),
    NfsClients(
        {
            "volume": {"name": "vol1", "uuid": "d28d1999-b8d0-11e9-9ad1-0050568e8480"},
            "protocol": "nfs4",
            "node": {"name": "vsim1", "uuid": "cc282893-b82f-11e9-a3ad-0050568e8480"},
            "server_ip": "10.140.72.214",
            "client_ip": "10.140.137.57",
            "svm": {"name": "vs1", "uuid": "c642db55-b8d0-11e9-9ad1-0050568e8480"},
        }
    ),
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


__all__ = ["NfsClients", "NfsClientsSchema"]
__pdoc__ = {
    "NfsClientsSchema.resource": False,
    "NfsClientsSchema.opts": False,
}


class NfsClientsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NfsClients object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nfs_clients."""

    client_ip = marshmallow_fields.Str(
        data_key="client_ip",
        allow_none=True,
    )
    r""" Specifies IP address of the client."""

    export_policy = marshmallow_fields.Nested("netapp_ontap.resources.export_policy.ExportPolicySchema", data_key="export_policy", unknown=EXCLUDE, allow_none=True)
    r""" The export_policy field of the nfs_clients."""

    idle_duration = marshmallow_fields.Str(
        data_key="idle_duration",
        allow_none=True,
    )
    r""" Specifies an ISO-8601 format of date and time to retrieve the idle time duration in hours, minutes, and seconds format.


Example: P4DT84H30M5S"""

    local_request_count = Size(
        data_key="local_request_count",
        allow_none=True,
    )
    r""" A counter that tracks requests that are sent to the volume with fast-path to local node."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the nfs_clients."""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['nfs', 'nfs3', 'nfs4', 'nfs4.1', 'nfs4.2']),
        allow_none=True,
    )
    r""" The NFS protocol version over which client is accessing the volume. The following values are supported:

* nfs - All NFS versions are considered
* nfs3 - NFS version 3 protocol
* nfs4 - NFS version 4 protocol
* nfs4.1 - NFS version 4 minor version 1 protocol
* nfs4.2 - NFS version 4 minor version 2 protocol


Valid choices:

* nfs
* nfs3
* nfs4
* nfs4.1
* nfs4.2"""

    remote_request_count = Size(
        data_key="remote_request_count",
        allow_none=True,
    )
    r""" A counter that tracks requests that are sent to the volume with slow-path to remote node."""

    server_ip = marshmallow_fields.Str(
        data_key="server_ip",
        allow_none=True,
    )
    r""" Specifies the IP address of the server."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nfs_clients."""

    trunking_enabled = marshmallow_fields.Boolean(
        data_key="trunking_enabled",
        allow_none=True,
    )
    r""" Flag that indicates the trunking status for the specified SVM connection. True indicates that the trunking feature is enabled while false indicates that the trunking feature is disabled."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the nfs_clients."""

    @property
    def resource(self):
        return NfsClients

    gettable_fields = [
        "links",
        "client_ip",
        "export_policy.links",
        "export_policy.id",
        "export_policy.name",
        "idle_duration",
        "local_request_count",
        "node.links",
        "node.name",
        "node.uuid",
        "protocol",
        "remote_request_count",
        "server_ip",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "trunking_enabled",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,client_ip,export_policy.links,export_policy.id,export_policy.name,idle_duration,local_request_count,node.links,node.name,node.uuid,protocol,remote_request_count,server_ip,svm.links,svm.name,svm.uuid,trunking_enabled,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "client_ip",
        "export_policy.id",
        "export_policy.name",
        "idle_duration",
        "local_request_count",
        "node.name",
        "node.uuid",
        "remote_request_count",
        "server_ip",
        "svm.name",
        "svm.uuid",
        "trunking_enabled",
        "volume.name",
        "volume.uuid",
    ]
    """client_ip,export_policy.id,export_policy.name,idle_duration,local_request_count,node.name,node.uuid,remote_request_count,server_ip,svm.name,svm.uuid,trunking_enabled,volume.name,volume.uuid,"""

    postable_fields = [
        "client_ip",
        "export_policy.id",
        "export_policy.name",
        "idle_duration",
        "local_request_count",
        "node.name",
        "node.uuid",
        "remote_request_count",
        "server_ip",
        "svm.name",
        "svm.uuid",
        "trunking_enabled",
        "volume.name",
        "volume.uuid",
    ]
    """client_ip,export_policy.id,export_policy.name,idle_duration,local_request_count,node.name,node.uuid,remote_request_count,server_ip,svm.name,svm.uuid,trunking_enabled,volume.name,volume.uuid,"""

class NfsClients(Resource):
    """Allows interaction with NfsClients objects on the host"""

    _schema = NfsClientsSchema
    _path = "/api/protocols/nfs/connected-clients"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the NFS configuration of SVMs.
### Expensive properties
export_policy.id is expensive field. It is not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `export_policy.id`

### Learn more
* [`DOC /protocols/nfs/connected-clients`](#docs-NAS-protocols_nfs_connected-clients)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all NfsClients resources that match the provided query"""
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
        """Returns a list of RawResources that represent NfsClients resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the NFS configuration of SVMs.
### Expensive properties
export_policy.id is expensive field. It is not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `export_policy.id`

### Learn more
* [`DOC /protocols/nfs/connected-clients`](#docs-NAS-protocols_nfs_connected-clients)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






