r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Microsoft Remote Volume Shadow Copy Services (VSS) is an extension of the existing Microsoft VSS infrastructure. Previously, VSS could be used for backup services only for data stored on the local disk. This limited the use of VSS to applications that stored data either on a local disk or on SAN-based storage. With Remote VSS, Microsoft has extended the VSS infrastructure to support the shadow copying of SMB shares. Server applications, such as, Hyper-V are now storing VHD files on SMB file shares. With these new extensions, it is possible to take application consistent shadow copies for virtual machines that store data and configuration files on shares.
### Retrieving Shadow copy sets for all SVMs
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ShadowcopySet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ShadowcopySet.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    ShadowcopySet(
        {
            "svm": {"name": "vs1", "uuid": "dfb8e00d-9498-11ec-9f9d-0050568e57be"},
            "keep_snapshots": True,
            "uuid": "27ed1b79-97f6-11ec-8ad1-0050568e57be",
        }
    ),
    ShadowcopySet(
        {
            "svm": {"name": "vs1", "uuid": "dfb8e00d-9498-11ec-9f9d-0050568e57be"},
            "keep_snapshots": False,
            "uuid": "388be551-97f6-11ec-8ad1-0050568e57be",
        }
    ),
    ShadowcopySet(
        {
            "svm": {"name": "vs2", "uuid": "fdb5bd8b-9498-11ec-9f9d-0050568e57be"},
            "keep_snapshots": False,
            "uuid": "525104ef-9f96-11ec-82fd-0050568e57be",
        }
    ),
    ShadowcopySet(
        {
            "svm": {"name": "vs2", "uuid": "fdb5bd8b-9498-11ec-9f9d-0050568e57be"},
            "keep_snapshots": True,
            "uuid": "66f8f723-9f96-11ec-82fd-0050568e57be",
        }
    ),
]

```
</div>
</div>

---
### Retrieving information for a specific shadow copy set
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ShadowcopySet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ShadowcopySet(uuid="525104ef-9f96-11ec-82fd-0050568e57be")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
ShadowcopySet(
    {
        "svm": {"name": "vs2", "uuid": "fdb5bd8b-9498-11ec-9f9d-0050568e57be"},
        "keep_snapshots": False,
        "uuid": "525104ef-9f96-11ec-82fd-0050568e57be",
    }
)

```
</div>
</div>

---
### Updating the keep-snapshot property of a specific shadow copy set
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ShadowcopySet

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ShadowcopySet(uuid="525104ef-9f96-11ec-82fd-0050568e57be")
    resource.keep_snapshots = True
    resource.patch()

```

---
### Retrieving shadow copy information for all SVMs
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shadowcopy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Shadowcopy.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    Shadowcopy(
        {
            "volume": {"name": "vol1", "uuid": "e117c8f6-9498-11ec-9f9d-0050568e57be"},
            "shadowcopy_set": {"uuid": "9169cd4a-a421-11ec-b82e-0050568e57be"},
            "uuid": "919fbc80-a421-11ec-b82e-0050568e57be",
            "client_uuid": "(uuid)",
            "svm": {"name": "vs1", "uuid": "dfb8e00d-9498-11ec-9f9d-0050568e57be"},
            "share": {"name": "sh1"},
        }
    ),
    Shadowcopy(
        {
            "volume": {"name": "vol1", "uuid": "e117c8f6-9498-11ec-9f9d-0050568e57be"},
            "shadowcopy_set": {"uuid": "9169cd4a-a421-11ec-b82e-0050568e57be"},
            "uuid": "91ac5a5f-a421-11ec-b82e-0050568e57be",
            "client_uuid": "(uuid)",
            "svm": {"name": "vs1", "uuid": "dfb8e00d-9498-11ec-9f9d-0050568e57be"},
            "share": {"name": "sh2"},
        }
    ),
    Shadowcopy(
        {
            "volume": {"name": "vol1", "uuid": "e117c8f6-9498-11ec-9f9d-0050568e57be"},
            "shadowcopy_set": {"uuid": "9169cd4a-a421-11ec-b82e-0050568e57be"},
            "uuid": "91b14098-a421-11ec-b82e-0050568e57be",
            "client_uuid": "(uuid)",
            "svm": {"name": "vs1", "uuid": "dfb8e00d-9498-11ec-9f9d-0050568e57be"},
            "share": {"name": "sh3"},
        }
    ),
    Shadowcopy(
        {
            "volume": {"name": "vol1", "uuid": "e117c8f6-9498-11ec-9f9d-0050568e57be"},
            "shadowcopy_set": {"uuid": "9169cd4a-a421-11ec-b82e-0050568e57be"},
            "uuid": "91b63309-a421-11ec-b82e-0050568e57be",
            "client_uuid": "(uuid)",
            "svm": {"name": "vs1", "uuid": "dfb8e00d-9498-11ec-9f9d-0050568e57be"},
            "share": {"name": "sh4"},
        }
    ),
]

```
</div>
</div>

---
### Retrieving information for a specific shadow copy
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shadowcopy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Shadowcopy(client_uuid="(uuid)")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
Shadowcopy(
    {
        "volume": {"name": "vol1", "uuid": "e117c8f6-9498-11ec-9f9d-0050568e57be"},
        "shadowcopy_set": {"uuid": "9169cd4a-a421-11ec-b82e-0050568e57be"},
        "uuid": "91b14098-a421-11ec-b82e-0050568e57be",
        "client_uuid": "(uuid)",
        "svm": {"name": "vs1", "uuid": "dfb8e00d-9498-11ec-9f9d-0050568e57be"},
        "share": {"name": "sh3"},
    }
)

```
</div>
</div>

---
### Updating the list of files to be shadowcopied in a particular share
Use this endpoint to update the list of files to be shadow copied in a particular share. Set "restore" field as false to perform this operation.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shadowcopy

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Shadowcopy(client_uuid="(uuid)")
    resource.files = ["/vhd1", "/vhd2"]
    resource.patch(hydrate=True, restore=False)

```

---
### Requesting the storage system to restore a directory
You set restore field to true to perform this operation. Only users with the security login role "vsadmin" can perform the operation.
---
```
# The API:
PATCH /protocols/cifs/shadow-copies?restore=true
# The call:
PATCH "api/protocols/cifs/shadow-copies?restore=true" -d "{  \"destination_dir\": \"/dir2\",  \"source_dir\": \"/src_dir\",  \"volume\": {    \"name\": \"test_vol\"  },  \"with_content\": false}"
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


__all__ = ["Shadowcopy", "ShadowcopySchema"]
__pdoc__ = {
    "ShadowcopySchema.resource": False,
    "ShadowcopySchema.opts": False,
}


class ShadowcopySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Shadowcopy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the shadowcopy."""

    client_uuid = marshmallow_fields.Str(
        data_key="client_uuid",
        allow_none=True,
    )
    r""" The universally-unique identifier of the client's shadow copy.

Example: abc13450-1f19-40ba-9b82-ebf277517e7e"""

    destination_dir = marshmallow_fields.Str(
        data_key="destination_dir",
        allow_none=True,
    )
    r""" The path of the destination directory. The path is in UTF8 and uses forward
slash as a directory separator. The path is relative to the root of the volume.


Example: /dir2"""

    files = marshmallow_fields.List(marshmallow_fields.Str, data_key="files", allow_none=True)
    r""" The list of files to shadow copy in the share. The path is in UTF8 and uses forward
slash as a directory separator. The path is relative to the root of the share.


Example: ["/vhd1","/vhd2"]"""

    shadowcopy_set = marshmallow_fields.Nested("netapp_ontap.resources.shadowcopy_set.ShadowcopySetSchema", data_key="shadowcopy_set", unknown=EXCLUDE, allow_none=True)
    r""" The shadowcopy_set field of the shadowcopy."""

    share = marshmallow_fields.Nested("netapp_ontap.resources.cifs_share.CifsShareSchema", data_key="share", unknown=EXCLUDE, allow_none=True)
    r""" The share field of the shadowcopy."""

    source_dir = marshmallow_fields.Str(
        data_key="source_dir",
        allow_none=True,
    )
    r""" The path of the source directory. The path is in UTF8 and uses forward slash
as a directory separator. The path is relative to the root of the volume.


Example: /dir1"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the shadowcopy."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The universally-unique identifier of the storage's shadow copy.

Example: fef32805-1f19-40ba-9b82-ebf277517e7e"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the shadowcopy."""

    with_content = marshmallow_fields.Boolean(
        data_key="with_content",
        allow_none=True,
    )
    r""" Specifies what needs to be restored. False specifies the directory only.
True indicates the directory and its content."""

    @property
    def resource(self):
        return Shadowcopy

    gettable_fields = [
        "links",
        "client_uuid",
        "files",
        "shadowcopy_set.links",
        "shadowcopy_set.uuid",
        "share.links",
        "share.name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,client_uuid,files,shadowcopy_set.links,shadowcopy_set.uuid,share.links,share.name,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "destination_dir",
        "files",
        "source_dir",
        "volume.name",
        "volume.uuid",
        "with_content",
    ]
    """destination_dir,files,source_dir,volume.name,volume.uuid,with_content,"""

    postable_fields = [
        "files",
    ]
    """files,"""

class Shadowcopy(Resource):
    """Allows interaction with Shadowcopy objects on the host"""

    _schema = ShadowcopySchema
    _path = "/api/protocols/cifs/shadow-copies"
    _keys = ["client_uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Shadowcopies
### Related ONTAP commands
* `vserver cifs shadowcopy show-shares`
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
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
        """Returns a count of all Shadowcopy resources that match the provided query"""
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
        """Returns a list of RawResources that represent Shadowcopy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["Shadowcopy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Specify list Files to be added as a part of Shadowcopy creation
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Shadowcopies
### Related ONTAP commands
* `vserver cifs shadowcopy show-shares`
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a Shadowcopy
### Related ONTAP commands
* `vserver cifs shadowcopy show-shares`
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
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
        r"""Specify list Files to be added as a part of Shadowcopy creation
### Learn more
* [`DOC /protocols/cifs/shadow-copies`](#docs-NAS-protocols_cifs_shadow-copies)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



