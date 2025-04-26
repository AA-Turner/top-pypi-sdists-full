r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
You can use this API to display the preferred DC configuration of an SVM.
## Retrieving all the preferred DC configurations of an SVM
---
The preferred DC GET endpoint retrieves all the configurations for a specific SVM.
## Examples
### Retrieving all fields for all the preferred DC configurations of an SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            ActiveDirectoryPreferredDc.get_collection(
                "1226670c-abc9-11eb-8de3-0050568eb0c4", fields="*"
            )
        )
    )

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    ActiveDirectoryPreferredDc({"fqdn": "host1", "server_ip": "4.4.4.4"}),
    ActiveDirectoryPreferredDc({"fqdn": "host2", "server_ip": "11.11.11.11"}),
]

```
</div>
</div>

---
### Retrieving the preferred DC configuration of a specific SVM, "fqdn" and "server_ip"
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectoryPreferredDc(
        "1226670c-abc9-11eb-8de3-0050568eb0c4", server_ip="4.4.4.4", fqdn="host1"
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
ActiveDirectoryPreferredDc({"fqdn": "host1", "server_ip": "4.4.4.4"})

```
</div>
</div>

---
## Creating a new preferred DC configuration
The preferred DC POST endpoint creates a new configuration. Both bulk and instance POST is supported.
## Examples
### Creating a single preferred DC configuration
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectoryPreferredDc("1226670c-abc9-11eb-8de3-0050568eb0c4")
    resource.fqdn = "testing.com"
    resource.server_ip = "1.1.1.1"
    resource.post(hydrate=True, skip_config_validation=True, return_records=False)
    print(resource)

```

---
## Deleting an existing preferred DC configuration
The preferred DC DELETE endpoint deletes an existing configuration. Both bulk and instance delete is supported.
## Examples
### Deleting the preferred DC configuration of a specific SVM, "fqdn" and "server_ip"
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectoryPreferredDc(
        "1226670c-abc9-11eb-8de3-0050568eb0c4", server_ip="4.4.4.4", fqdn="sample"
    )
    resource.delete()

```

---
### Deleting the preferred DC configurations of a specific SVM and "fqdn"
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectoryPreferredDc("1226670c-abc9-11eb-8de3-0050568eb0c4")
    resource.delete(fqdn="sampl")

```

---
### Deleting all preferred DC configurations of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectoryPreferredDc("1226670c-abc9-11eb-8de3-0050568eb0c4")
    resource.delete(fqdn="*")

```

---
### Deleting the preferred DC configurations of a specific SVM, "fqdn" and set of "server_ips"
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectoryPreferredDc("1226670c-abc9-11eb-8de3-0050568eb0c4")
    resource.delete(fqdn="sample", server_ip="3.3.3.3|4.4.4.4|1.1.1.1|2.2.2.2")

```

---
### Deleting the preferred DC configurations of a specific SVM and set of "server_ips"
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ActiveDirectoryPreferredDc

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ActiveDirectoryPreferredDc("1226670c-abc9-11eb-8de3-0050568eb0c4")
    resource.delete(server_ip="3.3.3.3|4.4.4.4|1.1.1.1|2.2.2.2")

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


__all__ = ["ActiveDirectoryPreferredDc", "ActiveDirectoryPreferredDcSchema"]
__pdoc__ = {
    "ActiveDirectoryPreferredDcSchema.resource": False,
    "ActiveDirectoryPreferredDcSchema.opts": False,
}


class ActiveDirectoryPreferredDcSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ActiveDirectoryPreferredDc object"""

    fqdn = marshmallow_fields.Str(
        data_key="fqdn",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" Fully Qualified Domain Name.

Example: test.com"""

    server_ip = marshmallow_fields.Str(
        data_key="server_ip",
        allow_none=True,
    )
    r""" IP address of the preferred DC. The address can be either an IPv4 or an IPv6 address.

Example: 4.4.4.4"""

    @property
    def resource(self):
        return ActiveDirectoryPreferredDc

    gettable_fields = [
        "fqdn",
        "server_ip",
    ]
    """fqdn,server_ip,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "fqdn",
        "server_ip",
    ]
    """fqdn,server_ip,"""

class ActiveDirectoryPreferredDc(Resource):
    """Allows interaction with ActiveDirectoryPreferredDc objects on the host"""

    _schema = ActiveDirectoryPreferredDcSchema
    _path = "/api/protocols/active-directory/{svm[uuid]}/preferred-domain-controllers"
    _keys = ["svm.uuid", "fqdn", "server_ip"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the Active Directory preferred DC configuration of an SVM.
### Related ONTAP commands
* `vserver active-directory preferred-dc show`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}/preferred-domain-controllers`](#docs-NAS-protocols_active-directory_{svm.uuid}_preferred-domain-controllers)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ActiveDirectoryPreferredDc resources that match the provided query"""
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
        """Returns a list of RawResources that represent ActiveDirectoryPreferredDc resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["ActiveDirectoryPreferredDc"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ActiveDirectoryPreferredDc"], NetAppResponse]:
        r"""Creates an Active Directory preferred DC configuration for an SVM.
### Required properties
* `svm.uuid` - Existing SVM in which to create the preferred DC.
* `domain` - Fully Qualified Domain Name.
* `server_ip` - IPv4/IPv6 address of the preferred DC.
#### The following parameters are optional:
- skip_config_validation
### Related ONTAP commands
* `vserver active-directory preferred-dc add`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}/preferred-domain-controllers`](#docs-NAS-protocols_active-directory_{svm.uuid}_preferred-domain-controllers)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["ActiveDirectoryPreferredDc"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the Active Directory preferred DC configuration of the specified SVM and domain.
### Related ONTAP commands
* `vserver active-directory preferred-dc delete`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}/preferred-domain-controllers`](#docs-NAS-protocols_active-directory_{svm.uuid}_preferred-domain-controllers)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the Active Directory preferred DC configuration of an SVM.
### Related ONTAP commands
* `vserver active-directory preferred-dc show`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}/preferred-domain-controllers`](#docs-NAS-protocols_active-directory_{svm.uuid}_preferred-domain-controllers)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the Active Directory preferred DC configuration of an SVM.
### Related ONTAP commands
* `vserver active-directory preferred-dc show`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}/preferred-domain-controllers`](#docs-NAS-protocols_active-directory_{svm.uuid}_preferred-domain-controllers)"""
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
        r"""Creates an Active Directory preferred DC configuration for an SVM.
### Required properties
* `svm.uuid` - Existing SVM in which to create the preferred DC.
* `domain` - Fully Qualified Domain Name.
* `server_ip` - IPv4/IPv6 address of the preferred DC.
#### The following parameters are optional:
- skip_config_validation
### Related ONTAP commands
* `vserver active-directory preferred-dc add`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}/preferred-domain-controllers`](#docs-NAS-protocols_active-directory_{svm.uuid}_preferred-domain-controllers)"""
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
        r"""Deletes the Active Directory preferred DC configuration of the specified SVM and domain.
### Related ONTAP commands
* `vserver active-directory preferred-dc delete`

### Learn more
* [`DOC /protocols/active-directory/{svm.uuid}/preferred-domain-controllers`](#docs-NAS-protocols_active-directory_{svm.uuid}_preferred-domain-controllers)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


