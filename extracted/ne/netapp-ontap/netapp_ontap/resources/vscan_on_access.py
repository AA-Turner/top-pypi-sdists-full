r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Use Vscan On-Access scanning to actively scan file objects for viruses when clients access files over SMB. To control which file operations trigger a vscan, use Vscan File-Operations Profile (vscan-fileop-profile) option in the CIFS share. The Vscan On-Access policy configuration defines the scope and status of On-Access scanning on file objects. Use this API to retrieve and manage Vscan On-Access policy configurations and Vscan On-Access policy statuses for the SVM.
## Examples
### Retrieving all fields for all policies of an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnAccess

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(VscanOnAccess.get_collection("{svm.uuid}", fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    VscanOnAccess(
        {
            "name": "default_CIFS",
            "enabled": True,
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            },
            "mandatory": True,
            "scope": {
                "scan_without_extension": True,
                "include_extensions": ["*"],
                "only_execute_access": False,
                "max_file_size": 2147483648,
                "scan_readonly_volumes": False,
            },
        }
    ),
    VscanOnAccess(
        {
            "name": "on-access-policy",
            "enabled": False,
            "svm": {
                "name": "vs1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
                "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            },
            "mandatory": True,
            "scope": {
                "exclude_paths": ["\\vol\\a b\\", "\\vol\\a,b\\"],
                "scan_without_extension": True,
                "include_extensions": ["mp*", "tx*"],
                "only_execute_access": True,
                "max_file_size": 3221225472,
                "exclude_extensions": ["mp3", "txt"],
                "scan_readonly_volumes": False,
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving the specific On-Access policy associated with the specified SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnAccess

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnAccess(
        "179d3c85-7053-11e8-b9b8-005056b41bd1", name="on-access-policy"
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
VscanOnAccess(
    {
        "name": "on-access-policy",
        "enabled": True,
        "svm": {
            "name": "vs1",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
        },
        "mandatory": True,
        "scope": {
            "exclude_paths": ["\\vol\\a b\\", "\\vol\\a,b\\"],
            "scan_without_extension": True,
            "include_extensions": ["mp*", "tx*"],
            "only_execute_access": True,
            "max_file_size": 3221225472,
            "exclude_extensions": ["mp3", "txt"],
            "scan_readonly_volumes": False,
        },
    }
)

```
</div>
</div>

---
### Creating a Vscan On-Access policy
The Vscan On-Access policy POST endpoint creates an On-Access policy for the specified SVM. Set enabled to "true" to enable scanning on the created policy.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnAccess

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnAccess("86fbc414-f140-11e8-8e22-0050568e0945")
    resource.enabled = False
    resource.mandatory = True
    resource.name = "on-access-policy"
    resource.scope = {
        "exclude_extensions": ["txt", "mp3"],
        "exclude_paths": ["\\dir1\\dir2\\ame", "\\vol\\a b"],
        "include_extensions": ["mp*", "txt"],
        "max_file_size": 3221225472,
        "only_execute_access": True,
        "scan_readonly_volumes": False,
        "scan_without_extension": True,
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
VscanOnAccess(
    {
        "name": "on-access-policy",
        "enabled": False,
        "svm": {"name": "vs1"},
        "mandatory": True,
        "scope": {
            "exclude_paths": ["\\dir1\\dir2\\ame", "\\vol\\a b"],
            "scan_without_extension": True,
            "include_extensions": ["mp*", "txt"],
            "only_execute_access": True,
            "max_file_size": 3221225472,
            "exclude_extensions": ["txt", "mp3"],
            "scan_readonly_volumes": False,
        },
    }
)

```
</div>
</div>

---
### Creating a Vscan On-Access policy where a number of optional fields are not specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnAccess

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnAccess("86fbc414-f140-11e8-8e22-0050568e0945")
    resource.enabled = False
    resource.mandatory = True
    resource.name = "on-access-policy"
    resource.scope = {
        "exclude_paths": ["\\vol\\a b", "\\vol\\a,b\\"],
        "max_file_size": 1073741824,
        "scan_without_extension": True,
    }
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
VscanOnAccess(
    {
        "name": "on-access-policy",
        "enabled": False,
        "svm": {"name": "vs1"},
        "mandatory": True,
        "scope": {
            "exclude_paths": ["\\vol\\a b", "\\vol\\a,b\\"],
            "scan_without_extension": True,
            "max_file_size": 1073741824,
        },
    }
)

```
</div>
</div>

---
### Updating a Vscan On-Access policy
The policy being modified is identified by the UUID of the SVM and the policy name.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnAccess

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnAccess(
        "86fbc414-f140-11e8-8e22-0050568e0945", name="on-access-policy"
    )
    resource.scope = {
        "include_extensions": ["txt"],
        "only_execute_access": True,
        "scan_readonly_volumes": False,
        "scan_without_extension": True,
    }
    resource.patch()

```

---
### Deleting a Vscan On-Access policy
The policy to be deleted is identified by the UUID of the SVM and the policy name.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VscanOnAccess

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VscanOnAccess(
        "86fbc414-f140-11e8-8e22-0050568e0945", name="on-access-policy"
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


__all__ = ["VscanOnAccess", "VscanOnAccessSchema"]
__pdoc__ = {
    "VscanOnAccessSchema.resource": False,
    "VscanOnAccessSchema.opts": False,
}


class VscanOnAccessSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanOnAccess object"""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" Status of the On-Access Vscan policy"""

    mandatory = marshmallow_fields.Boolean(
        data_key="mandatory",
        allow_none=True,
    )
    r""" Specifies if scanning is mandatory. File access is denied if there are no external virus-scanning servers available for virus scanning."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=256),
        allow_none=True,
    )
    r""" On-Access policy name

Example: on-access-test"""

    scope = marshmallow_fields.Nested("netapp_ontap.models.vscan_on_access_scope.VscanOnAccessScopeSchema", data_key="scope", unknown=EXCLUDE, allow_none=True)
    r""" The scope field of the vscan_on_access."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the vscan_on_access."""

    @property
    def resource(self):
        return VscanOnAccess

    gettable_fields = [
        "enabled",
        "mandatory",
        "name",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """enabled,mandatory,name,scope,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "enabled",
        "mandatory",
        "scope",
    ]
    """enabled,mandatory,scope,"""

    postable_fields = [
        "enabled",
        "mandatory",
        "name",
        "scope",
    ]
    """enabled,mandatory,name,scope,"""

class VscanOnAccess(Resource):
    r""" An On-Access policy that defines the scope of an On-Access scan. Use On-Access scanning to check for viruses when clients open, read, rename, or close files over CIFS. By default, ONTAP creates an On-Access policy named "default_CIFS" and enables it for all the SVMs in a cluster. """

    _schema = VscanOnAccessSchema
    _path = "/api/protocols/vscan/{svm[uuid]}/on-access-policies"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the Vscan On-Access policy.
### Related ONTAP commands
* `vserver vscan on-access-policy show`
* `vserver vscan on-access-policy file-ext-to-include show`
* `vserver vscan on-access-policy file-ext-to-exclude show`
* `vserver vscan on-access-policy paths-to-exclude show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
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
        """Returns a count of all VscanOnAccess resources that match the provided query"""
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
        """Returns a list of RawResources that represent VscanOnAccess resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["VscanOnAccess"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the Vscan On-Access policy configuration and/or enables/disables the Vscan On-Access policy of an SVM. You cannot modify the configurations for an On-Access policy associated with a data SVM which was created by SVM owned by the cluster, although you can enable and disable the policy associated with cluster SVM.
### Related ONTAP commands
* `vserver vscan on-access-policy modify`
* `vserver vscan on-access-policy enable`
* `vserver vscan on-access-policy disable`
* `vserver vscan on-access-policy file-ext-to-include add`
* `vserver vscan on-access-policy file-ext-to-exclude add`
* `vserver vscan on-access-policy paths-to-exclude add`
* `vserver vscan on-access-policy file-ext-to-include remove`
* `vserver vscan on-access-policy file-ext-to-exclude remove`
* `vserver vscan on-access-policy paths-to-exclude remove`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["VscanOnAccess"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["VscanOnAccess"], NetAppResponse]:
        r"""Creates a Vscan On-Access policy.
</b>Important notes:
* You must enable the policy on an SVM before its files can be scanned.
* You can enable only one On-Access policy at a time on an SVM. By default, the policy is enabled on creation. * If the Vscan On-Access policy has been created successfully on an SVM but cannot be enabled due to an error, the Vscan On-Access policy configurations are saved. The Vscan On-Access policy is then enabled using the PATCH operation.
### Required properties
* `svm.uuid` - Existing SVM in which to create the Vscan On-Access policy.
* `name` - Name of the Vscan On-Access policy. Maximum length is 256 characters.
### Default property values
If not specified in POST, the following default property values are assigned:
* `enabled` - _true_
* `mandatory` - _true_
* `include_extensions` - _*_
* `max_file_size` - _2147483648_
* `only_execute_access` - _false_
* `scan_readonly_volumes` - _false_
* `scan_without_extension` - _true_
### Related ONTAP commands
* `vserver vscan on-access-policy create`
* `vserver vscan on-access-policy enable`
* `vserver vscan on-access-policy disable`
* `vserver vscan on-access-policy file-ext-to-include add`
* `vserver vscan on-access-policy file-ext-to-exclude add`
* `vserver vscan on-access-policy paths-to-exclude add`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["VscanOnAccess"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the anti-virus On-Access policy configuration.
### Related ONTAP commands
* `vserver vscan on-access-policy delete`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the Vscan On-Access policy.
### Related ONTAP commands
* `vserver vscan on-access-policy show`
* `vserver vscan on-access-policy file-ext-to-include show`
* `vserver vscan on-access-policy file-ext-to-exclude show`
* `vserver vscan on-access-policy paths-to-exclude show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Vscan On-Access policy configuration of an SVM.
### Related ONTAP commands
* `vserver vscan on-access-policy show`
* `vserver vscan on-access-policy file-ext-to-include show`
* `vserver vscan on-access-policy file-ext-to-exclude show`
* `vserver vscan on-access-policy paths-to-exclude show`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
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
        r"""Creates a Vscan On-Access policy.
</b>Important notes:
* You must enable the policy on an SVM before its files can be scanned.
* You can enable only one On-Access policy at a time on an SVM. By default, the policy is enabled on creation. * If the Vscan On-Access policy has been created successfully on an SVM but cannot be enabled due to an error, the Vscan On-Access policy configurations are saved. The Vscan On-Access policy is then enabled using the PATCH operation.
### Required properties
* `svm.uuid` - Existing SVM in which to create the Vscan On-Access policy.
* `name` - Name of the Vscan On-Access policy. Maximum length is 256 characters.
### Default property values
If not specified in POST, the following default property values are assigned:
* `enabled` - _true_
* `mandatory` - _true_
* `include_extensions` - _*_
* `max_file_size` - _2147483648_
* `only_execute_access` - _false_
* `scan_readonly_volumes` - _false_
* `scan_without_extension` - _true_
### Related ONTAP commands
* `vserver vscan on-access-policy create`
* `vserver vscan on-access-policy enable`
* `vserver vscan on-access-policy disable`
* `vserver vscan on-access-policy file-ext-to-include add`
* `vserver vscan on-access-policy file-ext-to-exclude add`
* `vserver vscan on-access-policy paths-to-exclude add`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the Vscan On-Access policy configuration and/or enables/disables the Vscan On-Access policy of an SVM. You cannot modify the configurations for an On-Access policy associated with a data SVM which was created by SVM owned by the cluster, although you can enable and disable the policy associated with cluster SVM.
### Related ONTAP commands
* `vserver vscan on-access-policy modify`
* `vserver vscan on-access-policy enable`
* `vserver vscan on-access-policy disable`
* `vserver vscan on-access-policy file-ext-to-include add`
* `vserver vscan on-access-policy file-ext-to-exclude add`
* `vserver vscan on-access-policy paths-to-exclude add`
* `vserver vscan on-access-policy file-ext-to-include remove`
* `vserver vscan on-access-policy file-ext-to-exclude remove`
* `vserver vscan on-access-policy paths-to-exclude remove`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the anti-virus On-Access policy configuration.
### Related ONTAP commands
* `vserver vscan on-access-policy delete`
### Learn more
* [`DOC /protocols/vscan/{svm.uuid}/on-access-policies`](#docs-NAS-protocols_vscan_{svm.uuid}_on-access-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


