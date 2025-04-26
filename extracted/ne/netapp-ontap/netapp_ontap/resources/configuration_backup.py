r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API retrieves the current settings for the configuration and updates configuration backup settings. The GET operation retrieves the current settings for the configuration and the PATCH operation updates the configuration backup settings.
## Examples
These examples show how to retrieve and update the configuration backup settings.
### Retrieving the configuration backup settings
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConfigurationBackup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConfigurationBackup()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
ConfigurationBackup({"url": "http://10.224.65.198/backups", "username": "me"})

```
</div>
</div>

---
### Updating the configuration backup settings
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ConfigurationBackup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ConfigurationBackup()
    resource.patch()

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


__all__ = ["ConfigurationBackup", "ConfigurationBackupSchema"]
__pdoc__ = {
    "ConfigurationBackupSchema.resource": False,
    "ConfigurationBackupSchema.opts": False,
}


class ConfigurationBackupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConfigurationBackup object"""

    password = marshmallow_fields.Str(
        data_key="password",
        allow_none=True,
    )
    r""" The password field of the configuration_backup.

Example: yourpassword"""

    url = marshmallow_fields.Str(
        data_key="url",
        allow_none=True,
    )
    r""" An external backup location for the cluster configuration. This is mostly required for single node clusters where node and cluster configuration backups cannot be copied to other nodes in the cluster.

Example: http://10.224.65.198/backups"""

    username = marshmallow_fields.Str(
        data_key="username",
        allow_none=True,
    )
    r""" The username field of the configuration_backup.

Example: me"""

    validate_certificate = marshmallow_fields.Boolean(
        data_key="validate_certificate",
        allow_none=True,
    )
    r""" Use this parameter with the value "true" to validate the digital certificate of the remote server. Digital certificate validation is available only when the HTTPS protocol is used in the URL; it is disabled by default."""

    @property
    def resource(self):
        return ConfigurationBackup

    gettable_fields = [
        "url",
        "username",
        "validate_certificate",
    ]
    """url,username,validate_certificate,"""

    patchable_fields = [
        "password",
        "url",
        "username",
        "validate_certificate",
    ]
    """password,url,username,validate_certificate,"""

    postable_fields = [
        "url",
        "username",
        "validate_certificate",
    ]
    """url,username,validate_certificate,"""

class ConfigurationBackup(Resource):
    """Allows interaction with ConfigurationBackup objects on the host"""

    _schema = ConfigurationBackupSchema
    _path = "/api/support/configuration-backup"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster configuration backup information.
### Learn more
* [`DOC /support/configuration-backup`](#docs-support-support_configuration-backup)"""
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
        r"""Updates the cluster configuration backup information.

### Learn more
* [`DOC /support/configuration-backup`](#docs-support-support_configuration-backup)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



