r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Displays and manages local mapping for hostnames.
## Retrieving all hosts table entries
The local-hosts GET endpoint to retrieve all hosts table entries.
## Examples
### Retrieving all the fields of all hosts table entries.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalHost

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LocalHost.get_collection(return_timeout=15, fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    LocalHost(
        {
            "hostname": "host.sales.foo.com",
            "aliases": ["host1.sales.foo.com", "host2.sakes.foo.com"],
            "address": "1.1.1.1",
            "owner": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6cdf045c-87ae-11eb-a56a-0050568e0287"
                    }
                },
                "uuid": "6cdf045c-87ae-11eb-a56a-0050568e0287",
            },
            "_links": {
                "self": {
                    "href": "/api/name-services/local-hosts/6cdf045c-87ae-11eb-a56a-0050568e0287/1.1.1.1"
                }
            },
        }
    ),
    LocalHost(
        {
            "hostname": "samplehost2",
            "address": "2.2.2.2",
            "owner": {
                "name": "svm2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/9d080552-7bff-11eb-a56a-0050568e0287"
                    }
                },
                "uuid": "9d080552-7bff-11eb-a56a-0050568e0287",
            },
            "_links": {
                "self": {
                    "href": "/api/name-services/local-hosts/9d080552-7bff-11eb-a56a-0050568e0287/2.2.2.2"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving the hosts table entry of a given svm and address(ipv4/ipv6).
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalHost

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalHost(
        address="3.3.3.3", **{"owner.uuid": "9d080552-7bff-11eb-a56a-0050568e0287"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
LocalHost(
    {
        "hostname": "samplehost3",
        "aliases": ["host1.sales.foo.com", "host2.sakes.foo.com"],
        "address": "3.3.3.3",
        "owner": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/9d080552-7bff-11eb-a56a-0050568e0287"}
            },
            "uuid": "9d080552-7bff-11eb-a56a-0050568e0287",
        },
        "_links": {
            "self": {
                "href": "/api/name-services/local-hosts/9d080552-7bff-11eb-a56a-0050568e0287/3.3.3.3"
            }
        },
    }
)

```
</div>
</div>

---
## Creating a hosts table entry
The local-hosts POST endpoint creates a new hosts table entry.
## Examples
### Creating a hosts table entry with all fields.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalHost

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalHost()
    resource.address = "3.3.3.3"
    resource.aliases = ["host1.sales.foo.com", "host2.sakes.foo.com"]
    resource.hostname = "samplehost3"
    resource.owner = {"name": "svm2", "uuid": "9d080552-7bff-11eb-a56a-0050568e0287"}
    resource.post(hydrate=True, return_records=False)
    print(resource)

```

---
### Creating a hosts table entry with only required fields.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalHost

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalHost()
    resource.address = "123.123.123.12"
    resource.hostname = "host.sales.foo.com"
    resource.owner = {"name": "svm2", "uuid": "9d080552-7bff-11eb-a56a-0050568e0287"}
    resource.post(hydrate=True, return_records=False)
    print(resource)

```

---
## Updating a hosts table entry
---
The local-hosts PATCH endpoint updates an existing hosts table entry.
## Example
### Updating aliases and hostname of a given svm and address(ipv4/ipv6).
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalHost

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalHost(
        address="123.123.123.123",
        **{"owner.uuid": "9d080552-7bff-11eb-a56a-0050568e0287"}
    )
    resource.aliases = ["host1.sales.foo.com", "host2.sakes.foo.com"]
    resource.hostname = "host.sales.foo.com"
    resource.patch()

```

---
## Deleting a hosts table entry
---
The local-hosts DELETE endpoint deletes an existing hosts table entry.
## Example
### Deleting the hosts table entry of a given svm and address(ipv4/ipv6).
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LocalHost

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LocalHost(
        address="1.1.1.1", **{"owner.uuid": "9d080552-7bff-11eb-a56a-0050568e0287"}
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


__all__ = ["LocalHost", "LocalHostSchema"]
__pdoc__ = {
    "LocalHostSchema.resource": False,
    "LocalHostSchema.opts": False,
}


class LocalHostSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalHost object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the local_host."""

    address = marshmallow_fields.Str(
        data_key="address",
        allow_none=True,
    )
    r""" IPv4/IPv6 address in dotted form.

Example: 123.123.123.123"""

    aliases = marshmallow_fields.List(marshmallow_fields.Str, data_key="aliases", allow_none=True)
    r""" The list of aliases.

Example: ["host1.sales.foo.com","host2.sakes.foo.com"]"""

    hostname = marshmallow_fields.Str(
        data_key="hostname",
        validate=len_validation(minimum=1, maximum=255),
        allow_none=True,
    )
    r""" Canonical hostname.

Example: host.sales.foo.com"""

    owner = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="owner", unknown=EXCLUDE, allow_none=True)
    r""" The owner field of the local_host."""

    scope = marshmallow_fields.Str(
        data_key="scope",
        validate=enum_validation(['cluster', 'svm']),
        allow_none=True,
    )
    r""" Scope of the entity. Set to "cluster" for cluster owned objects and to "svm" for SVM owned objects.

Valid choices:

* cluster
* svm"""

    @property
    def resource(self):
        return LocalHost

    gettable_fields = [
        "links",
        "address",
        "aliases",
        "hostname",
        "owner.links",
        "owner.name",
        "owner.uuid",
        "scope",
    ]
    """links,address,aliases,hostname,owner.links,owner.name,owner.uuid,scope,"""

    patchable_fields = [
        "aliases",
        "hostname",
    ]
    """aliases,hostname,"""

    postable_fields = [
        "address",
        "aliases",
        "hostname",
        "owner.name",
        "owner.uuid",
    ]
    """address,aliases,hostname,owner.name,owner.uuid,"""

class LocalHost(Resource):
    """Allows interaction with LocalHost objects on the host"""

    _schema = LocalHostSchema
    _path = "/api/name-services/local-hosts"
    _keys = ["owner.uuid", "address"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all IP to hostname mappings for all SVMs of the cluster.
### Related ONTAP commands
* `vserver services name-service dns hosts show`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
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
        """Returns a count of all LocalHost resources that match the provided query"""
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
        """Returns a list of RawResources that represent LocalHost resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["LocalHost"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""For a specified SVM and IP address, modifies the corresponding IP to hostname mapping.
### Related ONTAP commands
* `vserver services name-service dns hosts modify`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["LocalHost"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["LocalHost"], NetAppResponse]:
        r"""Creates a new cluster-scoped or SVM-scoped IP to hostname mapping. For SVM-scoped mappings, include either the SVM name as owner.name or the SVM UUID as owner.uuid in the request body, along with other necessary parameters. For cluster-scoped mappings, specifying owner.uuid or owner.name is not required.
### Required properties
* `address` - IPv4/IPv6 address in dotted form.
* `hostname` - Canonical hostname.
### Optional properties
* `owner.uuid` or `owner.name` - Specify the name or UUID of an existing SVM to create an SVM-scoped IP-to-host mapping.
* `aliases` - The list of aliases.
### Related ONTAP commands
* `vserver services name-service dns hosts create`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
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
        records: Iterable["LocalHost"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an existing host object.
### Related ONTAP commands
* `vserver services name-service dns hosts delete`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all IP to hostname mappings for all SVMs of the cluster.
### Related ONTAP commands
* `vserver services name-service dns hosts show`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""For a specified SVM and IP address, returns the corresponding IP to hostname mapping.
### Related ONTAP commands
* `vserver services name-service dns hosts show`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
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
        r"""Creates a new cluster-scoped or SVM-scoped IP to hostname mapping. For SVM-scoped mappings, include either the SVM name as owner.name or the SVM UUID as owner.uuid in the request body, along with other necessary parameters. For cluster-scoped mappings, specifying owner.uuid or owner.name is not required.
### Required properties
* `address` - IPv4/IPv6 address in dotted form.
* `hostname` - Canonical hostname.
### Optional properties
* `owner.uuid` or `owner.name` - Specify the name or UUID of an existing SVM to create an SVM-scoped IP-to-host mapping.
* `aliases` - The list of aliases.
### Related ONTAP commands
* `vserver services name-service dns hosts create`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
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
        r"""For a specified SVM and IP address, modifies the corresponding IP to hostname mapping.
### Related ONTAP commands
* `vserver services name-service dns hosts modify`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
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
        r"""Deletes an existing host object.
### Related ONTAP commands
* `vserver services name-service dns hosts delete`
### Learn more
* [`DOC /name-services/local-hosts`](#docs-name-services-name-services_local-hosts)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


