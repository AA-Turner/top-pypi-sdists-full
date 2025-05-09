r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API supports creating, deleting and retrieving configuration backup files.
Configuration backups can be 'cluster' or 'node' type. A 'cluster' backup contains cluster-wide configuration in addition to the configuration of each node in the cluster. A 'node' backup contains only node-specific configuration such as configuration files on the root volume and the boot variables. For creating a cluster backup, a cluster-wide job is queued. For creating a node backup, a private job local to the node is queued.
In addition to the backups created using this API, ONTAP creates configuration backups automatically based on job schedules. This API supports creating configuration backups on demand only. It supports deleting and retrieving configuration backups that are created automatically or on demand.
For information on configuration backup settings for automatically created backups, see [`DOC /support/configuration-backup`](#docs-support-support_configuration-backup)
## Examples
### Retrieving a list of configuration backup files
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConfigurationBackupFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ConfigurationBackupFile.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    ConfigurationBackupFile(
        {
            "name": "backup1.7z",
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/5cafe0f6-499f-11e9-b644-005056bbcf93"
                    }
                },
                "uuid": "5cafe0f6-499f-11e9-b644-005056bbcf93",
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving details of the specified configuration backup file
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConfigurationBackupFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConfigurationBackupFile(
        name="backup1.7z", **{"node.uuid": "bc2f15d0-8b93-11e9-90e9-005056bb6a30"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
ConfigurationBackupFile(
    {
        "download_link": "https://10.224.66.113/backups/backup1.7z",
        "backup_nodes": [{"name": "node1"}, {"name": "node2"}],
        "auto": False,
        "name": "backup1.7z",
        "version": "9.7.0",
        "node": {
            "name": "node1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/bc2f15d0-8b93-11e9-90e9-005056bb6a30"
                }
            },
            "uuid": "bc2f15d0-8b93-11e9-90e9-005056bb6a30",
        },
        "time": "2019-06-10T13:35:06-04:00",
        "type": "cluster",
        "size": 6058408,
    }
)

```
</div>
</div>

---
### Creating a configuration backup file
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConfigurationBackupFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConfigurationBackupFile()
    resource.node = {"uuid": "ac13c636-4fc9-11e9-94c2-005056bb2516", "name": "node1"}
    resource.name = "backup3.7z"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
ConfigurationBackupFile(
    {
        "name": "backup3.7z",
        "node": {"name": "node1", "uuid": "ac13c636-4fc9-11e9-94c2-005056bb2516"},
    }
)

```
</div>
</div>

---
### Deleting a configuration backup file
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConfigurationBackupFile

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConfigurationBackupFile(
        name="backup1.7z", **{"node.uuid": "5cafe0f6-499f-11e9-b644-005056bbcf93"}
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


__all__ = ["ConfigurationBackupFile", "ConfigurationBackupFileSchema"]
__pdoc__ = {
    "ConfigurationBackupFileSchema.resource": False,
    "ConfigurationBackupFileSchema.opts": False,
}


class ConfigurationBackupFileSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConfigurationBackupFile object"""

    auto = marshmallow_fields.Boolean(
        data_key="auto",
        allow_none=True,
    )
    r""" Indicates if the backup was created automatically."""

    backup_nodes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.backup_node.BackupNodeSchema", unknown=EXCLUDE, allow_none=True), data_key="backup_nodes", allow_none=True)
    r""" The list of nodes included in the backup."""

    download_link = marshmallow_fields.Str(
        data_key="download_link",
        allow_none=True,
    )
    r""" The link to download the backup file.

Example: https://10.224.65.198/backups/backup_file.7z"""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" The backup name.

Example: backup_file.7z"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the configuration_backup_file."""

    size = Size(
        data_key="size",
        allow_none=True,
    )
    r""" The size of the backup in bytes.

Example: 4787563"""

    time = ImpreciseDateTime(
        data_key="time",
        allow_none=True,
    )
    r""" The backup creation time.

Example: 2019-02-04T18:33:48.000+0000"""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['node', 'cluster']),
        allow_none=True,
    )
    r""" The backup type.

Valid choices:

* node
* cluster"""

    version = marshmallow_fields.Str(
        data_key="version",
        allow_none=True,
    )
    r""" The software version.

Example: 9.7.0"""

    @property
    def resource(self):
        return ConfigurationBackupFile

    gettable_fields = [
        "auto",
        "backup_nodes",
        "download_link",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "size",
        "time",
        "type",
        "version",
    ]
    """auto,backup_nodes,download_link,name,node.links,node.name,node.uuid,size,time,type,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "node.name",
        "node.uuid",
    ]
    """name,node.name,node.uuid,"""

class ConfigurationBackupFile(Resource):
    r""" The configuration backup file. """

    _schema = ConfigurationBackupFileSchema
    _path = "/api/support/configuration-backup/backups"
    _keys = ["node.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of configuration backup files.
### Related ONTAP commands
* `system configuration backup show`

### Learn more
* [`DOC /support/configuration-backup/backups`](#docs-support-support_configuration-backup_backups)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ConfigurationBackupFile resources that match the provided query"""
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
        """Returns a list of RawResources that represent ConfigurationBackupFile resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["ConfigurationBackupFile"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ConfigurationBackupFile"], NetAppResponse]:
        r"""Creates a configuration backup. The required backup file name must end with .7z extension.
### Required properties
* `node.uuid` or `node.name` - The node UUID or node name on which the configuration backup will be created.
* `name` - The backup file name
### Related ONTAP commands
* `system configuration backup create`

### Learn more
* [`DOC /support/configuration-backup/backups`](#docs-support-support_configuration-backup_backups)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["ConfigurationBackupFile"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a configuration backup.
### Related ONTAP commands
* `system configuration backup delete`

### Learn more
* [`DOC /support/configuration-backup/backups`](#docs-support-support_configuration-backup_backups)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of configuration backup files.
### Related ONTAP commands
* `system configuration backup show`

### Learn more
* [`DOC /support/configuration-backup/backups`](#docs-support-support_configuration-backup_backups)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details of the specified configuration backup file.
### Related ONTAP commands
* `system configuration backup show`

### Learn more
* [`DOC /support/configuration-backup/backups`](#docs-support-support_configuration-backup_backups)"""
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
        r"""Creates a configuration backup. The required backup file name must end with .7z extension.
### Required properties
* `node.uuid` or `node.name` - The node UUID or node name on which the configuration backup will be created.
* `name` - The backup file name
### Related ONTAP commands
* `system configuration backup create`

### Learn more
* [`DOC /support/configuration-backup/backups`](#docs-support-support_configuration-backup_backups)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a configuration backup.
### Related ONTAP commands
* `system configuration backup delete`

### Learn more
* [`DOC /support/configuration-backup/backups`](#docs-support-support_configuration-backup_backups)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


