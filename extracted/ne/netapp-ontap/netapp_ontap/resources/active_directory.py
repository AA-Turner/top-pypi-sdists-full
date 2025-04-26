r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to display or modify Active Directory account details of the specified SVM.
It can also be used to delete an Active Directory account for the specified SVM.
## Examples
### Retrieving all Active Directory account details of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectory(**{"svm.uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
ActiveDirectory(
    {
        "fqdn": "EXAMPLE.COM",
        "name": "ACCOUNT1",
        "organizational_unit": "CN=Computers",
        "svm": {"name": "vs1", "uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"},
    }
)

```
</div>
</div>

---
### Update the Active Directory account details of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectory(**{"svm.uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"})
    resource.patch()

```

---
### Delete an Active Directory account of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectory

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectory(**{"svm.uuid": "6dd78167-c907-11eb-b2bf-0050568e7324"})
    resource.delete(body={"password": "password", "username": "administrator"})

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


__all__ = ["ActiveDirectory", "ActiveDirectorySchema"]
__pdoc__ = {
    "ActiveDirectorySchema.resource": False,
    "ActiveDirectorySchema.opts": False,
}


class ActiveDirectorySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ActiveDirectory object"""

    discovered_servers = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.active_directory_discovered_server.ActiveDirectoryDiscoveredServerSchema", unknown=EXCLUDE, allow_none=True), data_key="discovered_servers", allow_none=True)
    r""" Specifies the discovered servers records."""

    force_account_overwrite = marshmallow_fields.Boolean(
        data_key="force_account_overwrite",
        allow_none=True,
    )
    r""" If set to true and a machine account exists with the same name as specified in "name" in Active Directory, it will be overwritten and reused.

Example: false"""

    fqdn = marshmallow_fields.Str(
        data_key="fqdn",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" Fully qualified domain name.

Example: server1.com"""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=0, maximum=15),
        allow_none=True,
    )
    r""" Active Directory (AD) account NetBIOS name.

Example: account1"""

    organizational_unit = marshmallow_fields.Str(
        data_key="organizational_unit",
        allow_none=True,
    )
    r""" Organizational unit under which the Active Directory account will be created.

Example: CN=Test"""

    password = marshmallow_fields.Str(
        data_key="password",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" Administrator password required for Active Directory account creation, modification and deletion.

Example: testpwd"""

    preferred_dcs = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.active_directory_preferred_dc.ActiveDirectoryPreferredDcSchema", unknown=EXCLUDE, allow_none=True), data_key="preferred_dcs", allow_none=True)
    r""" Specifies the preferred domain controller (DC) records."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the active_directory."""

    username = marshmallow_fields.Str(
        data_key="username",
        validate=len_validation(minimum=1),
        allow_none=True,
    )
    r""" Administrator username required for Active Directory account creation, modification and deletion.

Example: admin"""

    @property
    def resource(self):
        return ActiveDirectory

    gettable_fields = [
        "discovered_servers",
        "fqdn",
        "name",
        "organizational_unit",
        "preferred_dcs",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """discovered_servers,fqdn,name,organizational_unit,preferred_dcs,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "force_account_overwrite",
        "fqdn",
        "password",
        "username",
    ]
    """force_account_overwrite,fqdn,password,username,"""

    postable_fields = [
        "force_account_overwrite",
        "fqdn",
        "name",
        "organizational_unit",
        "password",
        "svm.name",
        "svm.uuid",
        "username",
    ]
    """force_account_overwrite,fqdn,name,organizational_unit,password,svm.name,svm.uuid,username,"""

class ActiveDirectory(Resource):
    """Allows interaction with ActiveDirectory objects on the host"""

    _schema = ActiveDirectorySchema
    _path = "/api/protocols/active-directory"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Active Directory accounts for all SVMs.
### Related ONTAP commands
* `vserver active-directory show`
* `vserver active-directory preferred-dc show`
* `vserver active-directory discovered-servers show`

### Learn more
* [`DOC /protocols/active-directory`](#docs-NAS-protocols_active-directory)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ActiveDirectory resources that match the provided query"""
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
        """Returns a list of RawResources that represent ActiveDirectory resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["ActiveDirectory"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Modifies the Active Directory account for a given SVM.
### Related ONTAP commands
* `vserver active-directory modify`
### Important notes
* Patching Active Directory account is asynchronous. Response contains Task UUID and Link that can be queried to get the status.

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}`](#docs-NAS-protocols_active-directory_{svm.uuid})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["ActiveDirectory"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ActiveDirectory"], NetAppResponse]:
        r"""Creates an Active Directory account for a given SVM.
### Related ONTAP commands
* `vserver active-directory create`
### Important notes
* Active Directory account creation is asynchronous. Response contains Task UUID and Link that can be queried to get the status.

### Learn more
* [`DOC /protocols/active-directory`](#docs-NAS-protocols_active-directory)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["ActiveDirectory"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the Active Directory account for a given SVM.
### Related ONTAP commands
* `vserver active-directory delete`
### Important notes
* Active Directory account deletion is asynchronous. Response contains Task UUID and Link that can be queried to get the status.

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}`](#docs-NAS-protocols_active-directory_{svm.uuid})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Active Directory accounts for all SVMs.
### Related ONTAP commands
* `vserver active-directory show`
* `vserver active-directory preferred-dc show`
* `vserver active-directory discovered-servers show`

### Learn more
* [`DOC /protocols/active-directory`](#docs-NAS-protocols_active-directory)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Active Directory account for a given SVM.
### Related ONTAP commands
* `vserver active-directory show`
* `vserver active-directory preferred-dc show`
* `vserver active-directory discovered-servers show`
* `vserver active-directory discovered-servers reset-servers`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}`](#docs-NAS-protocols_active-directory_{svm.uuid})"""
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
        r"""Creates an Active Directory account for a given SVM.
### Related ONTAP commands
* `vserver active-directory create`
### Important notes
* Active Directory account creation is asynchronous. Response contains Task UUID and Link that can be queried to get the status.

### Learn more
* [`DOC /protocols/active-directory`](#docs-NAS-protocols_active-directory)"""
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
        r"""Modifies the Active Directory account for a given SVM.
### Related ONTAP commands
* `vserver active-directory modify`
### Important notes
* Patching Active Directory account is asynchronous. Response contains Task UUID and Link that can be queried to get the status.

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}`](#docs-NAS-protocols_active-directory_{svm.uuid})"""
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
        r"""Deletes the Active Directory account for a given SVM.
### Related ONTAP commands
* `vserver active-directory delete`
### Important notes
* Active Directory account deletion is asynchronous. Response contains Task UUID and Link that can be queried to get the status.

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}`](#docs-NAS-protocols_active-directory_{svm.uuid})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


