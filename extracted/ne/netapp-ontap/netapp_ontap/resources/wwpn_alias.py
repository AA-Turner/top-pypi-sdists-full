r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A worldwide port name (WWPN) is a unique 64-bit identifier for a Fibre Channel (FC) initiator. It is displayed as a 16-character hexadecimal value. SAN administrators might find it easier to identify FC initiators using an alias, especially in larger SANs.<br/>
The WWPN alias REST API allows you to create, delete, and discover aliases for WWPNs.<br/>
Multiple aliases can be created for a WWPN, but you cannot use the same alias for multiple WWPNs.<br/>
An alias can consist of up to 32 characters. Valid characters are:

* A through Z
* a through z
* numbers 0 through 9
* hyphen ("-")
* underscore ("_")
* left and right braces ("{", "}")
* period (".")
## Examples
### Creating a WWPN alias
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WwpnAlias

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = WwpnAlias()
    resource.svm = {"name": "svm1"}
    resource.wwpn = "50:0a:09:82:b4:30:25:05"
    resource.alias = "alias3"
    resource.post(hydrate=True)
    print(resource)

```

### Retrieving all properties of all WWPN aliases
The `fields` query parameter is used to request that all properties be returned.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WwpnAlias

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(WwpnAlias.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    WwpnAlias(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/68589d3d-7efa-11e8-9eed-005056b43025"
                    }
                },
                "uuid": "68589d3d-7efa-11e8-9eed-005056b43025",
            },
            "alias": "alias1",
            "_links": {
                "self": {
                    "href": "/api/network/fc/wwpn-aliases/68589d3d-7efa-11e8-9eed-005056b43025/alias1"
                }
            },
            "wwpn": "20:00:00:50:56:b4:30:25",
        }
    ),
    WwpnAlias(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/68589d3d-7efa-11e8-9eed-005056b43025"
                    }
                },
                "uuid": "68589d3d-7efa-11e8-9eed-005056b43025",
            },
            "alias": "alias2",
            "_links": {
                "self": {
                    "href": "/api/network/fc/wwpn-aliases/68589d3d-7efa-11e8-9eed-005056b43025/alias2"
                }
            },
            "wwpn": "50:0a:09:82:b4:30:25:00",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all WWPN aliases named "alias1"
The `alias` query parameter is used to specify a query for the value "alias1".
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WwpnAlias

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(WwpnAlias.get_collection(alias="alias1")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    WwpnAlias(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/68589d3d-7efa-11e8-9eed-005056b43025"
                    }
                },
                "uuid": "68589d3d-7efa-11e8-9eed-005056b43025",
            },
            "alias": "alias1",
            "_links": {
                "self": {
                    "href": "/api/network/fc/wwpn-aliases/68589d3d-7efa-11e8-9eed-005056b43025/alias1"
                }
            },
            "wwpn": "20:00:00:50:56:b4:30:25",
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific WWPN alias
The alias to be returned is identified by the UUID of its SVM and the alias name.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WwpnAlias

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = WwpnAlias(
        alias="alias2", **{"svm.uuid": "68589d3d-7efa-11e8-9eed-005056b43025"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    WwpnAlias(
        {
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/68589d3d-7efa-11e8-9eed-005056b43025"
                    }
                },
                "uuid": "68589d3d-7efa-11e8-9eed-005056b43025",
            },
            "alias": "alias2",
            "_links": {
                "self": {
                    "href": "/api/network/fc/wwpn-aliases/68589d3d-7efa-11e8-9eed-005056b43025/alias1"
                }
            },
            "wwpn": "50:0a:09:82:b4:30:25:00",
        }
    )
]

```
</div>
</div>

---
### Deleting a WWPN alias
The alias to delete is identified by the UUID of its SVM and the alias name.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import WwpnAlias

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = WwpnAlias(
        alias="alias2", **{"svm.uuid": "68589d3d-7efa-11e8-9eed-005056b43025"}
    )
    resource.delete()

```
"""

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


__all__ = ["WwpnAlias", "WwpnAliasSchema"]
__pdoc__ = {
    "WwpnAliasSchema.resource": False,
    "WwpnAliasSchema.opts": False,
}


class WwpnAliasSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WwpnAlias object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the wwpn_alias."""

    alias = marshmallow_fields.Str(
        data_key="alias",
        allow_none=True,
    )
    r""" The FC WWPN alias. Required in POST.


Example: host1"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the wwpn_alias."""

    wwpn = marshmallow_fields.Str(
        data_key="wwpn",
        allow_none=True,
    )
    r""" The FC initiator WWPN. Required in POST.


Example: 2f:a0:00:a0:98:0b:56:13"""

    @property
    def resource(self):
        return WwpnAlias

    gettable_fields = [
        "links",
        "alias",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "wwpn",
    ]
    """links,alias,svm.links,svm.name,svm.uuid,wwpn,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "alias",
        "svm.name",
        "svm.uuid",
        "wwpn",
    ]
    """alias,svm.name,svm.uuid,wwpn,"""

class WwpnAlias(Resource):
    r""" A Fibre Channel (FC) world wide port name (WWPN) alias. A WWPN is a unique 64-bit identifier for an FC initiator. It is displayed as a 16-character hexadecimal value. SAN administrators may find it easier to identify FC initiators using an alias, especially in larger SANs. """

    _schema = WwpnAliasSchema
    _path = "/api/network/fc/wwpn-aliases"
    _keys = ["svm.uuid", "alias"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves FC WWPN aliases.
### Related ONTAP commands
* `vserver fcp wwpn-alias show`
### Learn more
* [`DOC /network/fc/wwpn-aliases`](#docs-SAN-network_fc_wwpn-aliases)
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
        """Returns a count of all WwpnAlias resources that match the provided query"""
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
        """Returns a list of RawResources that represent WwpnAlias resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["WwpnAlias"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["WwpnAlias"], NetAppResponse]:
        r"""Creates an FC WWPN alias.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the FC alias.
* `alias` - Name of the FC alias.
* `wwpn` - FC WWPN for which to create the alias.
### Related ONTAP commands
* `vserver fcp wwpn-alias set`
### Learn more
* [`DOC /network/fc/wwpn-aliases`](#docs-SAN-network_fc_wwpn-aliases)
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
        records: Iterable["WwpnAlias"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an FC WWPN alias.
### Related ONTAP commands
* `vserver fcp wwpn-alias remove`
### Learn more
* [`DOC /network/fc/wwpn-aliases`](#docs-SAN-network_fc_wwpn-aliases)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves FC WWPN aliases.
### Related ONTAP commands
* `vserver fcp wwpn-alias show`
### Learn more
* [`DOC /network/fc/wwpn-aliases`](#docs-SAN-network_fc_wwpn-aliases)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an FC WWPN alias.
### Related ONTAP commands
* `vserver fcp wwpn-alias show`
### Learn more
* [`DOC /network/fc/wwpn-aliases`](#docs-SAN-network_fc_wwpn-aliases)
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
        r"""Creates an FC WWPN alias.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the FC alias.
* `alias` - Name of the FC alias.
* `wwpn` - FC WWPN for which to create the alias.
### Related ONTAP commands
* `vserver fcp wwpn-alias set`
### Learn more
* [`DOC /network/fc/wwpn-aliases`](#docs-SAN-network_fc_wwpn-aliases)
"""
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
        r"""Deletes an FC WWPN alias.
### Related ONTAP commands
* `vserver fcp wwpn-alias remove`
### Learn more
* [`DOC /network/fc/wwpn-aliases`](#docs-SAN-network_fc_wwpn-aliases)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


