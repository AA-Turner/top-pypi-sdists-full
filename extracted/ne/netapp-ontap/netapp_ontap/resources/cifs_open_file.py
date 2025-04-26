r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
<h2> ONTAP `cifs sessions file show` functionality is used to provide a list of currently opened files.<h2/>
### Information on the open files

* Lists all files opened in current session.
## Example
### Retrieving established open file information
To retrieve the list of open files, use the following API. Note that <i>return_records=true</i>.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsOpenFile

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    print(list(CifsOpenFile.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    CifsOpenFile(
        {
            "volume": {
                "name": "root_vs0",
                "uuid": "8384f6ae-3553-11ee-a3c3-005056ae0dd5",
            },
            "continuously_available": "no",
            "type": "regular",
            "open_mode": "r",
            "range_locks_count": 0,
            "node": {
                "name": "sti220-vsim-sr050u",
                "uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
            },
            "session": {"identifier": 10878444899913433090},
            "identifier": 109,
            "svm": {"name": "vs0", "uuid": "80e795f4-3553-11ee-9f97-005056ae78de"},
            "connection": {"count": 1, "identifier": 103985},
            "path": "first_file.txt",
            "share": {"mode": "r", "name": "sh1"},
        }
    ),
    CifsOpenFile(
        {
            "volume": {
                "name": "root_vs0",
                "uuid": "8384f6ae-3553-11ee-a3c3-005056ae0dd5",
            },
            "continuously_available": "no",
            "type": "regular",
            "open_mode": "r",
            "range_locks_count": 0,
            "node": {
                "name": "sti220-vsim-sr050u",
                "uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
            },
            "session": {"identifier": 10878444899913433090},
            "identifier": 110,
            "svm": {"name": "vs0", "uuid": "80e795f4-3553-11ee-9f97-005056ae78de"},
            "connection": {"count": 1, "identifier": 103985},
            "path": "second_file.txt",
            "share": {"mode": "r", "name": "sh1"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving specific open file Information
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsOpenFile

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    resource = CifsOpenFile(
        identifier=109,
        **{
            "session.identifier": "10878444899913433090",
            "connection.identifier": "103985",
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
CifsOpenFile(
    {
        "volume": {"name": "root_vs0", "uuid": "8384f6ae-3553-11ee-a3c3-005056ae0dd5"},
        "continuously_available": "no",
        "type": "regular",
        "open_mode": "r",
        "range_locks_count": 0,
        "node": {
            "name": "sti220-vsim-sr050u",
            "uuid": "a5f65ec0-3550-11ee-93c5-005056ae78de",
        },
        "session": {"identifier": 10878444899913433000},
        "identifier": 109,
        "svm": {"name": "vs0", "uuid": "80e795f4-3553-11ee-9f97-005056ae78de"},
        "connection": {"count": 1, "identifier": 103985},
        "path": "first_file.txt",
        "share": {"mode": "r", "name": "sh1"},
    }
)

```
</div>
</div>

---
### Closing a specific file based on `file.identifier`, `connection.identifier` and `session_id`
The file being closed is identified by the UUID of its SVM, the corresponding file.identifier, connection.identifier and session_id.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsOpenFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsOpenFile(
        identifier=109,
        **{
            "session.identifier": "10878444899913433090",
            "connection.identifier": "103985",
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


__all__ = ["CifsOpenFile", "CifsOpenFileSchema"]
__pdoc__ = {
    "CifsOpenFileSchema.resource": False,
    "CifsOpenFileSchema.opts": False,
}


class CifsOpenFileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsOpenFile object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the cifs_open_file."""

    connection = marshmallow_fields.Nested("netapp_ontap.models.cifs_open_file_connection.CifsOpenFileConnectionSchema", data_key="connection", unknown=EXCLUDE, allow_none=True)
    r""" The connection field of the cifs_open_file."""

    continuously_available = marshmallow_fields.Str(
        data_key="continuously_available",
        validate=enum_validation(['no', 'yes']),
        allow_none=True,
    )
    r""" The type of continuous availability protection provided to the file.
Opened files are continuously available if there are opened through a SMB3 client through a share with "continuously_available" set to yes.
These open files are capable of non-disruptively recovering from take over and giveback as well as general aggregate relocation.
- no: the open file is not continuously available.
- yes: the open file is continuously available.


Valid choices:

* no
* yes"""

    identifier = Size(
        data_key="identifier",
        allow_none=True,
    )
    r""" The unique identifier for the opened file.

Example: 17"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the cifs_open_file."""

    open_mode = marshmallow_fields.Str(
        data_key="open_mode",
        validate=enum_validation(['r', 'w', 'd']),
        allow_none=True,
    )
    r""" Open mode corresponding to the opened file
- r: Opened for read
- w: Opened for write
- d: Opened for Delete


Valid choices:

* r
* w
* d"""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Path from CIFS share.

Example: sub1\sub2\f4"""

    range_locks_count = Size(
        data_key="range_locks_count",
        allow_none=True,
    )
    r""" The number of range locks granted on the file.

Example: 4"""

    session = marshmallow_fields.Nested("netapp_ontap.models.cifs_open_file_session.CifsOpenFileSessionSchema", data_key="session", unknown=EXCLUDE, allow_none=True)
    r""" The session field of the cifs_open_file."""

    share = marshmallow_fields.Nested("netapp_ontap.models.cifs_open_file_share.CifsOpenFileShareSchema", data_key="share", unknown=EXCLUDE, allow_none=True)
    r""" The share field of the cifs_open_file."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the cifs_open_file."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['directory', 'regular', 'stream', 'symlink']),
        allow_none=True,
    )
    r""" The type of opened file.
The file can be a regular file, directory, a symbolic link to an existing file/directory, or an alternate data stream.


Valid choices:

* directory
* regular
* stream
* symlink"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the cifs_open_file."""

    @property
    def resource(self):
        return CifsOpenFile

    gettable_fields = [
        "links",
        "connection",
        "continuously_available",
        "identifier",
        "node.links",
        "node.name",
        "node.uuid",
        "open_mode",
        "path",
        "range_locks_count",
        "session",
        "share",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,connection,continuously_available,identifier,node.links,node.name,node.uuid,open_mode,path,range_locks_count,session,share,svm.links,svm.name,svm.uuid,type,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "identifier",
        "node.name",
        "node.uuid",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """identifier,node.name,node.uuid,svm.name,svm.uuid,volume.name,volume.uuid,"""

    postable_fields = [
        "identifier",
        "node.name",
        "node.uuid",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """identifier,node.name,node.uuid,svm.name,svm.uuid,volume.name,volume.uuid,"""

class CifsOpenFile(Resource):
    r""" Manage opened files over CIFS. """

    _schema = CifsOpenFileSchema
    _path = "/api/protocols/cifs/session/files"
    _keys = ["node.uuid", "svm.uuid", "identifier", "connection.identifier", "session.identifier"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the CIFS sessions Open Files information for all SVMs.
### Related ONTAP commands
  * `vserver cifs session file show`
### Learn more
* [`DOC /protocols/cifs/session/files`](#docs-NAS-protocols_cifs_session_files)
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
        """Returns a count of all CifsOpenFile resources that match the provided query"""
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
        """Returns a list of RawResources that represent CifsOpenFile resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["CifsOpenFile"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Closes open files identified by svm.uuid, file.identifier, connection.identifier and session_id.
### Related ONTAP commands
  * `vserver cifs session file close`
### Learn more
* [`DOC /protocols/cifs/session/files`](#docs-NAS-protocols_cifs_session_files)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the CIFS sessions Open Files information for all SVMs.
### Related ONTAP commands
  * `vserver cifs session file show`
### Learn more
* [`DOC /protocols/cifs/session/files`](#docs-NAS-protocols_cifs_session_files)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves specific CIFS session Open Files information.
### Learn more
* [`DOC /protocols/cifs/session/files`](#docs-NAS-protocols_cifs_session_files)
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
        r"""Closes open files identified by svm.uuid, file.identifier, connection.identifier and session_id.
### Related ONTAP commands
  * `vserver cifs session file close`
### Learn more
* [`DOC /protocols/cifs/session/files`](#docs-NAS-protocols_cifs_session_files)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


