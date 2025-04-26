r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A portset is a collection of Fibre Channel Protocol and/or iSCSI network interfaces from the portset's SVM.<br/>
Portsets are used to limit the network interfaces through which an initiator can connect to mapped LUNs. When a portset is bound to an initiator group (igroup), and the initiator group is mapped to a LUN, the initiators of the initiator group can only reach the LUN through the network interfaces in the portset.<br/>
Portsets are not recommended for new configurations. With modern releases of ONTAP, it is recommended to use multiple SVMs and initiator groups with no bound portset to load balance applications over multiple ports on a node. Selective LUN mapping will automatically limit the number of visible paths to a LUN from the client host to those required for efficient access and high availability. The REST portset API is primarily intended for legacy use.<br/>
The portset REST API allows you to create, delete, and discover portsets, and to add and remove network interfaces from portsets.<br/>
A portset can be bound to one or more initiator groups. An initiator group (igroup) can be bound to at most one portset.<br/>
When a portset is created, the `protocol` property is used to restrict member network interfaces to Fibre Channel Protocol (_fcp_), iSCSI (_iscsi_), or both (_mixed_).<br/>
Zero or more network interfaces can be supplied when the portset is created. After creation, network interfaces can be added to or removed from the portset using the `/protocols/san/portsets/{portset.uuid}/interfaces` endpoint. See [`POST /protocols/san/portsets/{portset.uuid}/interfaces`](#/SAN/portset_interface_create) and [`DELETE /protocols/san/portsets/{portset.uuid}/interfaces/{name}`](#/SAN/portset_interface_delete) for more details.<br/>
## Examples
### Creating a portset with no network interfaces
The example portset uses the default `mixed` protocol. Note that the `return_records` query parameter is used to obtain the newly created portset in the response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Portset

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Portset()
    resource.svm = {"name": "svm1"}
    resource.name = "portset1"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Portset(
    {
        "protocol": "mixed",
        "name": "portset1",
        "uuid": "5d7b1dfa-1ed7-11eb-8b0f-005056bb3521",
        "_links": {
            "self": {
                "href": "/api/protocols/san/portsets/5d7b1dfa-1ed7-11eb-8b0f-005056bb3521"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/31484775-1e23-11eb-b2a8-005056bb3521"}
            },
            "uuid": "31484775-1e23-11eb-b2a8-005056bb3521",
        },
    }
)

```
</div>
</div>

---
### Creating an iSCSI portset with two network interfaces
Note that the `return_records` query parameter is used to obtain the newly created portset in the response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Portset

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Portset()
    resource.svm = {"name": "svm1"}
    resource.name = "portset2"
    resource.protocol = "iscsi"
    resource.interfaces = [{"ip": {"name": "lif1"}}, {"ip": {"name": "lif2"}}]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Portset(
    {
        "interfaces": [
            {
                "ip": {
                    "name": "lif1",
                    "_links": {
                        "self": {
                            "href": "/api/network/ip/interfaces/f37bfb01-1e2a-11eb-b2a8-005056bb3521"
                        }
                    },
                    "uuid": "f37bfb01-1e2a-11eb-b2a8-005056bb3521",
                    "ip": {"address": "192.168.1.100"},
                },
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/portsets/816c0d49-1ed7-11eb-8b0f-005056bb3521/interfaces/f37bfb01-1e2a-11eb-b2a8-005056bb3521"
                    }
                },
                "uuid": "f37bfb01-1e2a-11eb-b2a8-005056bb3521",
            },
            {
                "ip": {
                    "name": "lif2",
                    "_links": {
                        "self": {
                            "href": "/api/network/ip/interfaces/f92178e7-1e2a-11eb-b2a8-005056bb3521"
                        }
                    },
                    "uuid": "f92178e7-1e2a-11eb-b2a8-005056bb3521",
                    "ip": {"address": "192.168.1.101"},
                },
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/portsets/816c0d49-1ed7-11eb-8b0f-005056bb3521/interfaces/f92178e7-1e2a-11eb-b2a8-005056bb3521"
                    }
                },
                "uuid": "f92178e7-1e2a-11eb-b2a8-005056bb3521",
            },
        ],
        "protocol": "iscsi",
        "name": "portset2",
        "uuid": "816c0d49-1ed7-11eb-8b0f-005056bb3521",
        "_links": {
            "self": {
                "href": "/api/protocols/san/portsets/816c0d49-1ed7-11eb-8b0f-005056bb3521"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/31484775-1e23-11eb-b2a8-005056bb3521"}
            },
            "uuid": "31484775-1e23-11eb-b2a8-005056bb3521",
        },
    }
)

```
</div>
</div>

---
### Retrieving a summary of all portsets
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Portset

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Portset.get_collection()))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    Portset(
        {
            "name": "portset1",
            "uuid": "5d7b1dfa-1ed7-11eb-8b0f-005056bb3521",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/portsets/5d7b1dfa-1ed7-11eb-8b0f-005056bb3521"
                }
            },
        }
    ),
    Portset(
        {
            "name": "portset2",
            "uuid": "816c0d49-1ed7-11eb-8b0f-005056bb3521",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/portsets/816c0d49-1ed7-11eb-8b0f-005056bb3521"
                }
            },
        }
    ),
    Portset(
        {
            "name": "portset3",
            "uuid": "b716b4d2-1ed7-11eb-8b0f-005056bb3521",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/portsets/b716b4d2-1ed7-11eb-8b0f-005056bb3521"
                }
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving details for a specific portset
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Portset

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Portset(uuid="b716b4d2-1ed7-11eb-8b0f-005056bb3521")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Portset(
    {
        "interfaces": [
            {
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/portsets/b716b4d2-1ed7-11eb-8b0f-005056bb3521/interfaces/164eb052-1e2b-11eb-b2a8-005056bb3521"
                    }
                },
                "fc": {
                    "name": "lif5",
                    "uuid": "164eb052-1e2b-11eb-b2a8-005056bb3521",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/interfaces/164eb052-1e2b-11eb-b2a8-005056bb3521"
                        }
                    },
                    "wwpn": "20:01:00:50:56:bb:35:21",
                },
                "uuid": "164eb052-1e2b-11eb-b2a8-005056bb3521",
            },
            {
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/portsets/b716b4d2-1ed7-11eb-8b0f-005056bb3521/interfaces/197ba2b7-1e2b-11eb-b2a8-005056bb3521"
                    }
                },
                "fc": {
                    "name": "lif6",
                    "uuid": "197ba2b7-1e2b-11eb-b2a8-005056bb3521",
                    "_links": {
                        "self": {
                            "href": "/api/network/fc/interfaces/197ba2b7-1e2b-11eb-b2a8-005056bb3521"
                        }
                    },
                    "wwpn": "20:02:00:50:56:bb:35:21",
                },
                "uuid": "197ba2b7-1e2b-11eb-b2a8-005056bb3521",
            },
        ],
        "protocol": "fcp",
        "name": "portset3",
        "uuid": "b716b4d2-1ed7-11eb-8b0f-005056bb3521",
        "_links": {
            "self": {
                "href": "/api/protocols/san/portsets/b716b4d2-1ed7-11eb-8b0f-005056bb3521"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/31484775-1e23-11eb-b2a8-005056bb3521"}
            },
            "uuid": "31484775-1e23-11eb-b2a8-005056bb3521",
        },
    }
)

```
</div>
</div>

---
### Deleting a portset
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Portset

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Portset(uuid="b716b4d2-1ed7-11eb-8b0f-005056bb3521")
    resource.delete()

```

---
### Adding a network interface to a portset
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import PortsetInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = PortsetInterface("5d7b1dfa-1ed7-11eb-8b0f-005056bb3521")
    resource.fc = {"name": "lif4"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Adding multiple network interfaces to a portset in a single call
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import PortsetInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = PortsetInterface("5d7b1dfa-1ed7-11eb-8b0f-005056bb3521")
    resource.records = [
        {"ip": {"name": "lif1"}},
        {"ip": {"name": "lif2"}},
        {"fc": {"name": "lif5"}},
    ]
    resource.post(hydrate=True)
    print(resource)

```

---
### Removing a network interface from a portset
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import PortsetInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = PortsetInterface(
        "5d7b1dfa-1ed7-11eb-8b0f-005056bb3521",
        uuid="f92178e7-1e2a-11eb-b2a8-005056bb3521",
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


__all__ = ["Portset", "PortsetSchema"]
__pdoc__ = {
    "PortsetSchema.resource": False,
    "PortsetSchema.opts": False,
}


class PortsetSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the Portset object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the portset."""

    igroups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.iscsi_session_igroups.IscsiSessionIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="igroups", allow_none=True)
    r""" An array initiator groups to which the portset is bound."""

    interfaces = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.portset_interface_no_records.PortsetInterfaceNoRecordsSchema", unknown=EXCLUDE, allow_none=True), data_key="interfaces", allow_none=True)
    r""" An array of network interfaces that are members of the portset. These are the only network interfaces through which the initiators of a bound igroup can access mapped LUNs.<br/>
Zero or more network interfaces can be supplied when the portset is created. After creation, network interfaces can be added or removed from the portset using the `/protocols/san/portsets/{portset.uuid}/interfaces` endpoint. See [`POST /protocols/san/portsets/{portset.uuid}/interfaces`](#/SAN/portset_interface_create) and [`DELETE /protocols/san/portsets/{portset.uuid}/interfaces/{uuid}`](#/SAN/portset_interface_delete) for more details."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=96),
        allow_none=True,
    )
    r""" The name of the portset. Required in POST.<br/>
The name of a portset cannot be changed after creation.


Example: portset1"""

    protocol = marshmallow_fields.Str(
        data_key="protocol",
        validate=enum_validation(['fcp', 'iscsi', 'mixed']),
        allow_none=True,
    )
    r""" The protocols supported by the portset. This restricts the type of network interfaces that can be added to the portset. Optional in POST; if not supplied, this defaults to _mixed_.<br/>
The protocol of a portset cannot be changed after creation.


Valid choices:

* fcp
* iscsi
* mixed"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the portset."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier for a portset.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return Portset

    gettable_fields = [
        "links",
        "igroups.links",
        "igroups.name",
        "igroups.uuid",
        "interfaces",
        "name",
        "protocol",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,igroups.links,igroups.name,igroups.uuid,interfaces,name,protocol,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "interfaces",
        "name",
        "protocol",
        "svm.name",
        "svm.uuid",
    ]
    """interfaces,name,protocol,svm.name,svm.uuid,"""

class Portset(Resource):
    """Allows interaction with Portset objects on the host"""

    _schema = PortsetSchema
    _path = "/api/protocols/san/portsets"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves portsets.
### Related ONTAP commands
* `lun portset show`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        """Returns a count of all Portset resources that match the provided query"""
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
        """Returns a list of RawResources that represent Portset resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["Portset"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["Portset"], NetAppResponse]:
        r"""Creates a portset.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the portset.
* `name` - Name of the portset.
### Recommended optional properties
* `protocol` - The network protocol of the interfaces in the portset.
* `interfaces` - Network interfaces to include in the portset. This property can be used to create the portset and populate it with network interfaces in a single request.
### Default property values
If not specified in POST, the following default property values are assigned.
* `protocol` - _mixed_ - Data protocol of the portset's network interfaces.
### Related ONTAP commands
* `lun portset create`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        records: Iterable["Portset"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a portset.
### Related ONTAP commands
* `lun portset delete`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves portsets.
### Related ONTAP commands
* `lun portset show`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a portset.
### Related ONTAP commands
* `lun portset show`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        r"""Creates a portset.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the portset.
* `name` - Name of the portset.
### Recommended optional properties
* `protocol` - The network protocol of the interfaces in the portset.
* `interfaces` - Network interfaces to include in the portset. This property can be used to create the portset and populate it with network interfaces in a single request.
### Default property values
If not specified in POST, the following default property values are assigned.
* `protocol` - _mixed_ - Data protocol of the portset's network interfaces.
### Related ONTAP commands
* `lun portset create`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        r"""Deletes a portset.
### Related ONTAP commands
* `lun portset delete`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


