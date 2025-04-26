r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Retrieves or modifies the key management configuration options. The following operations are supported:

* GET
* PATCH
## Examples
### Retrieving cluster-level key manager configurations
The following example shows how to retrieve cluster-level manager configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyManagerConfig()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
KeyManagerConfig(
    {
        "health_monitor_policy": {
            "aws": {"enabled": True, "manage_volume_offline": True},
            "akv": {"enabled": True, "manage_volume_offline": True},
            "kmip": {"enabled": True, "manage_volume_offline": True},
            "ikp": {"enabled": True, "manage_volume_offline": True},
            "okm": {"enabled": True, "manage_volume_offline": True},
            "gcp": {"enabled": True, "manage_volume_offline": True},
        },
        "cc_mode_enabled": False,
        "_links": {"self": {"href": "/api/security/key-manager-configs"}},
        "health_monitor_polling_interval": 15,
        "cloud_kms_retry_count": 3,
    }
)

```
</div>
</div>

---
### Updating the cluster-level key manager configurations
The following example shows how to modify the "health_monitor_polling_interval" and "cloud_kms_retry_count" fields.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyManagerConfig()
    resource.health_monitor_polling_interval = "20"
    resource.cloud_kms_retry_count = "5"
    resource.patch()

```

---
### Updating the cluster-level key manager configurations
The following example shows how to modify the "cc_mode" and "passphrase" fields.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyManagerConfig()
    resource.cc_mode_enabled = True
    resource.passphrase = "current_passphrase"
    resource.patch()

```

---
### Shows the keystore level health monitor policy
The following example shows how to retrieve the health monitor policies for Amazon Web Services and Google Cloud.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyManagerConfig()
    resource.get(fields="health_monitor_policy.aws,health_monitor_policy.gcp")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
KeyManagerConfig(
    {
        "health_monitor_policy": {
            "aws": {"enabled": False, "manage_volume_offline": False},
            "gcp": {"enabled": False, "manage_volume_offline": False},
        },
        "_links": {"self": {"href": "/api/security/key-manager-configs"}},
    }
)

```
</div>
</div>

---
### Updates the keytore level health monitor policy
The following example shows how to modify the Amazon Web Services "enabled" field and the Google Cloud "manage_volume_offline" field of the health monitor policy.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import KeyManagerConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = KeyManagerConfig()
    resource.health_monitor_policy = {
        "aws": {"enabled": "false"},
        "gcp": {"manage_volume_offline": "false"},
    }
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


__all__ = ["KeyManagerConfig", "KeyManagerConfigSchema"]
__pdoc__ = {
    "KeyManagerConfigSchema.resource": False,
    "KeyManagerConfigSchema.opts": False,
}


class KeyManagerConfigSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KeyManagerConfig object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the key_manager_config."""

    cc_mode_enabled = marshmallow_fields.Boolean(
        data_key="cc_mode_enabled",
        allow_none=True,
    )
    r""" Indicates whether the Common Criteria Mode configuration is enabled."""

    cloud_kms_retry_count = Size(
        data_key="cloud_kms_retry_count",
        allow_none=True,
    )
    r""" Cloud key manager connection retry count. Supported value range of 0-10.

Example: 3"""

    health_monitor_policy = marshmallow_fields.Nested("netapp_ontap.models.key_manager_config_health_monitor_policy.KeyManagerConfigHealthMonitorPolicySchema", data_key="health_monitor_policy", unknown=EXCLUDE, allow_none=True)
    r""" Manages the keystore configurations."""

    health_monitor_polling_interval = Size(
        data_key="health_monitor_polling_interval",
        allow_none=True,
    )
    r""" Health Monitor Polling Period, in minutes. Supported value range of 15-30 minutes.

Example: 20"""

    passphrase = marshmallow_fields.Str(
        data_key="passphrase",
        allow_none=True,
    )
    r""" Current cluster-wide passphrase. This is a required field when setting the cc_mode_enabled field value to true. This is not audited.

Example: The cluster passphrase of length 64-256 ASCII characters."""

    @property
    def resource(self):
        return KeyManagerConfig

    gettable_fields = [
        "links",
        "cc_mode_enabled",
        "cloud_kms_retry_count",
        "health_monitor_policy",
        "health_monitor_polling_interval",
    ]
    """links,cc_mode_enabled,cloud_kms_retry_count,health_monitor_policy,health_monitor_polling_interval,"""

    patchable_fields = [
        "cc_mode_enabled",
        "cloud_kms_retry_count",
        "health_monitor_policy",
        "health_monitor_polling_interval",
        "passphrase",
    ]
    """cc_mode_enabled,cloud_kms_retry_count,health_monitor_policy,health_monitor_polling_interval,passphrase,"""

    postable_fields = [
    ]
    """"""

class KeyManagerConfig(Resource):
    r""" Manages the various key manager configuration options. """

    _schema = KeyManagerConfigSchema
    _path = "/api/security/key-manager-configs"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves key manager configurations.
Retrieves the key manager health monitor policy (fields=health_monitor_policy).
### Related ONTAP commands
* `security key-manager config show`
* `security key-manager health policy show`

### Learn more
* [`DOC /security/key-manager-configs`](#docs-security-security_key-manager-configs)"""
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
        r"""Updates key manager configurations.
Updates the key manager health monitor policy.
### Related ONTAP commands
* `security key-manager config modify`
* `security key-manager health policy modify`

### Learn more
* [`DOC /security/key-manager-configs`](#docs-security-security_key-manager-configs)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



