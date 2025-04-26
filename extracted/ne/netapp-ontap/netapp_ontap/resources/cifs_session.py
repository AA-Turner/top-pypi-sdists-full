r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
ONTAP CIFS sessions `show` functionality is used to provide a list of currently established CIFS sessions with SMB Clients.<p/>
### Information on the CIFS session

* List all the SMB sessions for SVM and the clients along with volume information on which the clients are using.
## Example
### Retrieves established sessions information
To retrieve the list of CIFS sessions, use the following API. Note that <i>return_records=true</i>.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSession

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    print(list(CifsSession.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    CifsSession(
        {
            "idle_duration": "PT3M15S",
            "user": "example_user",
            "open_other": 0,
            "server_ip": "172.29.212.166",
            "smb_signing": True,
            "identifier": 10878444899913433000,
            "svm": {"name": "vs0", "uuid": "80e795f4-3553-11ee-9f97-005056ae78de"},
            "node": {
                "name": "sti220-vsim-sr050u",
                "uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
            },
            "smb_encryption": "unencrypted",
            "open_shares": 1,
            "protocol": "smb3_1",
            "large_mtu": True,
            "authentication": "ntlmv2",
            "continuous_availability": "unavailable",
            "open_files": 5,
            "volumes": [
                {"name": "root_vs0", "uuid": "5015c99b-3554-11ee-9f97-005056ae78de"},
                {"name": "vol_test", "uuid": "84b94bb8-3553-11ee-a3c3-005056ae0dd5"},
            ],
            "connection_id": 103985,
            "connection_count": 1,
            "mapped_unix_user": "example_user",
            "client_ip": "10.249.30.206",
            "connected_duration": "PT37M53S",
        }
    ),
    CifsSession(
        {
            "idle_duration": "PT5S",
            "user": "example_user",
            "open_other": 0,
            "server_ip": "172.29.212.166",
            "smb_signing": False,
            "identifier": 10878444899913433000,
            "svm": {"name": "vs0", "uuid": "80e795f4-3553-11ee-9f97-005056ae78de"},
            "node": {
                "name": "sti220-vsim-sr050u",
                "uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
            },
            "smb_encryption": "unencrypted",
            "open_shares": 1,
            "protocol": "smb3_1",
            "large_mtu": True,
            "authentication": "ntlmv2",
            "continuous_availability": "unavailable",
            "open_files": 1,
            "volumes": [
                {"name": "root_vs0", "uuid": "84b94bb8-3553-11ee-a3c3-005056ae0dd5"}
            ],
            "connection_id": 103986,
            "connection_count": 1,
            "mapped_unix_user": "example_user",
            "client_ip": "10.234.157.109",
            "connected_duration": "PT15S",
        }
    ),
]

```
</div>
</div>

---
### Retrieving CIFS server configuration details for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSession

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    resource = CifsSession(
        connection_id=103985,
        identifier=10878444899913433090,
        **{
            "svm.uuid": "80e795f4-3553-11ee-9f97-005056ae78de",
            "node.uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
        }
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
CifsSession(
    {
        "idle_duration": "PT5M41S",
        "user": "example_user",
        "open_other": 0,
        "server_ip": "172.29.212.166",
        "smb_signing": True,
        "identifier": 10878444899913433000,
        "svm": {"name": "vs0", "uuid": "80e795f4-3553-11ee-9f97-005056ae78de"},
        "node": {
            "name": "sti220-vsim-sr050u",
            "uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
        },
        "smb_encryption": "unencrypted",
        "open_shares": 1,
        "protocol": "smb3_1",
        "large_mtu": True,
        "authentication": "ntlmv2",
        "continuous_availability": "unavailable",
        "open_files": 5,
        "volumes": [
            {"name": "root_vs0", "uuid": "5015c99b-3554-11ee-9f97-005056ae78de"},
            {"name": "vol_test", "uuid": "84b94bb8-3553-11ee-a3c3-005056ae0dd5"},
        ],
        "connection_id": 103985,
        "connection_count": 1,
        "mapped_unix_user": "example_user",
        "client_ip": "10.249.30.206",
        "connected_duration": "PT50M20S",
    }
)

```
</div>
</div>

---
### Removing all existing CIFS sessions for a specific node on a specific SVM
To delete all the existing CIFS session, pass the identifier and connection ID as zero (0) in the following API. This will delete all of the CIFS sessions for the given SVM on the node.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSession

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    resource = CifsSession(
        connection_id=0,
        identifier=0,
        **{
            "svm.uuid": "80e795f4-3553-11ee-9f97-005056ae78de",
            "node.uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
        }
    )
    resource.delete()

```

---
### Removing all CIFS sessions for a specific connection on a specific node on a specific SVM
To delete a CIFS session, use the following API. This will delete the CIFS sessions for a given SVM on the node.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSession

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    resource = CifsSession(
        connection_id=103985,
        identifier=0,
        **{
            "svm.uuid": "80e795f4-3553-11ee-9f97-005056ae78de",
            "node.uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
        }
    )
    resource.delete()

```

---
### Removing a specific CIFS session for a specific Node on a specific SVM
To delete a specific CIFS session, use the following API. This will delete the specific CIFS session for the given SVM on the node.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSession

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    resource = CifsSession(
        connection_id=103985,
        identifier=10878444899913433090,
        **{
            "svm.uuid": "80e795f4-3553-11ee-9f97-005056ae78de",
            "node.uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
        }
    )
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


__all__ = ["CifsSession", "CifsSessionSchema"]
__pdoc__ = {
    "CifsSessionSchema.resource": False,
    "CifsSessionSchema.opts": False,
}


class CifsSessionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsSession object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cifs_session."""

    authentication = marshmallow_fields.Str(
        data_key="authentication",
        validate=enum_validation(['none', 'ntlmv1', 'ntlmv2', 'kerberos', 'anonymous']),
        allow_none=True,
    )
    r""" SMB authentication over which the client accesses the share. The following values are supported:

* none - No authentication
* ntlmv1 - Ntlm version 1 mechanism
* ntlmv2 - Ntlm version 2 mechanism
* kerberos - Kerberos authentication
* anonymous - Anonymous mechanism


Valid choices:

* none
* ntlmv1
* ntlmv2
* kerberos
* anonymous"""

    client_ip = marshmallow_fields.Str(
        data_key="client_ip",
        allow_none=True,
    )
    r""" Specifies IP address of the client.


Example: 10.74.7.182"""

    connected_duration = marshmallow_fields.Str(
        data_key="connected_duration",
        allow_none=True,
    )
    r""" Specifies an ISO-8601 format of date and time used to retrieve the connected time duration in hours, minutes, and seconds format.


Example: P4DT84H30M5S"""

    connection_count = Size(
        data_key="connection_count",
        allow_none=True,
    )
    r""" A counter used to track requests that are sent to the volumes to the node.


Example: 0"""

    connection_id = Size(
        data_key="connection_id",
        allow_none=True,
    )
    r""" A unique 32-bit unsigned number used to represent each SMB session's connection ID.


Example: 22802"""

    continuous_availability = marshmallow_fields.Str(
        data_key="continuous_availability",
        validate=enum_validation(['unavailable', 'available', 'partial']),
        allow_none=True,
    )
    r""" The level of continuous availability protection provided to the SMB sessions and/or files.

* unavailable - Open file is not continuously available. For sessions, it contains one or more open files but none of them are continuously available.
* available - open file is continuously available. For sessions, it contains one or more open files and all of them are continuously available.
* partial - Sessions only. Contains at least one continuously available open file with other files open but not continuously available.


Valid choices:

* unavailable
* available
* partial"""

    identifier = Size(
        data_key="identifier",
        allow_none=True,
    )
    r""" A unique 64-bit unsigned number used to represent each SMB session's identifier.


Example: 4622663542519103507"""

    idle_duration = marshmallow_fields.Str(
        data_key="idle_duration",
        allow_none=True,
    )
    r""" Specifies an ISO-8601 format of date and time used to retrieve the idle time duration in hours, minutes, and seconds format.


Example: P4DT84H30M5S"""

    large_mtu = marshmallow_fields.Boolean(
        data_key="large_mtu",
        allow_none=True,
    )
    r""" Specifies whether the large MTU is enabled or not for an SMB session.


Example: true"""

    mapped_unix_user = marshmallow_fields.Str(
        data_key="mapped_unix_user",
        allow_none=True,
    )
    r""" Indicated that a mapped UNIX user has logged in.


Example: root"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the cifs_session."""

    open_files = Size(
        data_key="open_files",
        allow_none=True,
    )
    r""" Number of files the SMB session has opened."""

    open_other = Size(
        data_key="open_other",
        allow_none=True,
    )
    r""" Number of other files the SMB session has opened."""

    open_shares = Size(
        data_key="open_shares",
        allow_none=True,
    )
    r""" Number of shares the SMB session has opened."""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['smb1', 'smb2', 'smb2_1', 'smb3', 'smb3_1']),
        allow_none=True,
    )
    r""" The SMB protocol version over which the client accesses the volumes. The following values are supported:

* smb1 - SMB version 1
* smb2 - SMB version 2
* smb2_1 - SMB version 2 minor version 1
* smb3 - SMB version 3
* smb3_1 - SMB version 3 minor version 1


Valid choices:

* smb1
* smb2
* smb2_1
* smb3
* smb3_1"""

    server_ip = marshmallow_fields.Str(
        data_key="server_ip",
        allow_none=True,
    )
    r""" Specifies the IP address of the SVM.


Example: 10.140.78.248"""

    smb_encryption = marshmallow_fields.Str(
        data_key="smb_encryption",
        validate=enum_validation(['unencrypted', 'encrypted', 'partially_encrypted']),
        allow_none=True,
    )
    r""" Indicates an SMB encryption state. The following values are supported:

* unencrypted - SMB session is not encrypted
* encrypted - SMB session is fully encrypted. SVM level encryption is enabled and encryption occurs for the entire session.
* partially_encrypted - SMB session is partially encrypted. Share level encryption is enabled and encryption is initiated when the tree-connect occurs.


Valid choices:

* unencrypted
* encrypted
* partially_encrypted"""

    smb_signing = marshmallow_fields.Boolean(
        data_key="smb_signing",
        allow_none=True,
    )
    r""" Specifies whether or not SMB signing is enabled.

Example: false"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cifs_session."""

    user = marshmallow_fields.Str(
        data_key="user",
        allow_none=True,
    )
    r""" Indicates that a Windows user has logged in.


Example: NBCIFSQA2\administrator"""

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" A group of volumes, the client is accessing."""

    @property
    def resource(self):
        return CifsSession

    gettable_fields = [
        "links",
        "authentication",
        "client_ip",
        "connected_duration",
        "connection_count",
        "connection_id",
        "continuous_availability",
        "identifier",
        "idle_duration",
        "large_mtu",
        "mapped_unix_user",
        "node.links",
        "node.name",
        "node.uuid",
        "open_files",
        "open_other",
        "open_shares",
        "protocol",
        "server_ip",
        "smb_encryption",
        "smb_signing",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "user",
        "volumes.links",
        "volumes.name",
        "volumes.uuid",
    ]
    """links,authentication,client_ip,connected_duration,connection_count,connection_id,continuous_availability,identifier,idle_duration,large_mtu,mapped_unix_user,node.links,node.name,node.uuid,open_files,open_other,open_shares,protocol,server_ip,smb_encryption,smb_signing,svm.links,svm.name,svm.uuid,user,volumes.links,volumes.name,volumes.uuid,"""

    patchable_fields = [
        "node.name",
        "node.uuid",
        "svm.name",
        "svm.uuid",
        "volumes.name",
        "volumes.uuid",
    ]
    """node.name,node.uuid,svm.name,svm.uuid,volumes.name,volumes.uuid,"""

    postable_fields = [
        "node.name",
        "node.uuid",
        "svm.name",
        "svm.uuid",
        "volumes.name",
        "volumes.uuid",
    ]
    """node.name,node.uuid,svm.name,svm.uuid,volumes.name,volumes.uuid,"""

class CifsSession(Resource):
    """Allows interaction with CifsSession objects on the host"""

    _schema = CifsSessionSchema
    _path = "/api/protocols/cifs/sessions"
    _keys = ["node.uuid", "svm.uuid", "identifier", "connection_id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the CIFS sessions information for all SVMs.
### Related ONTAP commands
  * `vserver cifs session show -active-volumes`
### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)
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
        """Returns a count of all CifsSession resources that match the provided query"""
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
        """Returns a list of RawResources that represent CifsSession resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["CifsSession"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes SMB session information on a node for an SVM.
* To delete the specific SMB session information, pass the relevant SMB session's identifier and connection Id.
* To delete all the SMB session information on specific node and SVM, pass the both SMB session's identifier and connection Id as zero(0)
* To delete all the SMB session information on specific connection, pass the specific SMB session's Identifier value as zero(0).
* To delete all the SMB session information on specific Identifier alone is not allowed.
### Related ONTAP commands
  * `vserver cifs session close`
### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the CIFS sessions information for all SVMs.
### Related ONTAP commands
  * `vserver cifs session show -active-volumes`
### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves specific SMB session information for a specific SMB connection in a node on an SVM.
### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)



    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes SMB session information on a node for an SVM.
* To delete the specific SMB session information, pass the relevant SMB session's identifier and connection Id.
* To delete all the SMB session information on specific node and SVM, pass the both SMB session's identifier and connection Id as zero(0)
* To delete all the SMB session information on specific connection, pass the specific SMB session's Identifier value as zero(0).
* To delete all the SMB session information on specific Identifier alone is not allowed.
### Related ONTAP commands
  * `vserver cifs session close`
### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


