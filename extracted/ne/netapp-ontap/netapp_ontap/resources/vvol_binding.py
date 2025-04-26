r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A VMware virtual volume (vVol) binding is an association between a LUN of class `protocol_endpoint` and a LUN of class `vvol`. Class `protocol_endpoint` LUNs are mapped to igroups and granted access using the same configuration as class `regular` LUNs. When a class `vvol` LUN is bound to a mapped class `protocol_endpoint` LUN, VMware can access the class `vvol` LUN through the class `protocol_endpoint` LUN mapping.</br>
Class `protocol_endpoint` and `vvol` LUNs support many-to-many vVol bindings. A LUN of one class can be bound to zero or more LUNs of the opposite class.</br>
The vVol binding between any two specific LUNs is reference counted. When a REST POST is executed for a vVol binding that already exists, the vVol binding reference count is incremented. When a REST DELETE is executed, the vVol binding reference count is decremented. Only when the vVol binding count reaches zero, or the query parameter `delete_all_references` is supplied, is the vVol binding destroyed.</br>
The vVol binding REST API allows you to create, delete, and discover vVol bindings.
## Examples
### Creating a vVol binding
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VvolBinding

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VvolBinding()
    resource.svm = {"name": "svm1"}
    resource.protocol_endpoint = {"name": "/vol/vol1/pe1"}
    resource.vvol = {"name": "/vol/vol1/vvol1"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Retrieving all vVol bindings
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VvolBinding

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(VvolBinding.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    VvolBinding(
        {
            "vvol": {
                "name": "/vol/vol1/vvol1",
                "_links": {
                    "self": {
                        "href": "/api/storage/luns/28c02623-42fa-4f5f-a984-a02044bfc005"
                    }
                },
                "uuid": "28c02623-42fa-4f5f-a984-a02044bfc005",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/san/vvol-bindings/2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4/28c02623-42fa-4f5f-a984-a02044bfc005"
                }
            },
            "protocol_endpoint": {
                "name": "/vol/vol1/pe1",
                "_links": {
                    "self": {
                        "href": "/api/storage/luns/2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4"
                    }
                },
                "uuid": "2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4",
            },
        }
    ),
    VvolBinding(
        {
            "vvol": {
                "name": "/vol/vol1/vvol2",
                "_links": {
                    "self": {
                        "href": "/api/storage/luns/a8d4ba93-918f-40ad-a1e4-4d7b244bdcdf"
                    }
                },
                "uuid": "a8d4ba93-918f-40ad-a1e4-4d7b244bdcdf",
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/san/vvol-bindings/2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4/a8d4ba93-918f-40ad-a1e4-4d7b244bdcdf"
                }
            },
            "protocol_endpoint": {
                "name": "/vol/vol1/pe1",
                "_links": {
                    "self": {
                        "href": "/api/storage/luns/2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4"
                    }
                },
                "uuid": "2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific vVol binding
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VvolBinding

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VvolBinding(
        **{
            "vvol.uuid": "28c02623-42fa-4f5f-a984-a02044bfc005",
            "protocol_endpoint.uuid": "2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4",
        }
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
VvolBinding(
    {
        "vvol": {
            "name": "/vol/vol1/vvol1",
            "_links": {
                "self": {
                    "href": "/api/storage/luns/28c02623-42fa-4f5f-a984-a02044bfc005"
                }
            },
            "uuid": "28c02623-42fa-4f5f-a984-a02044bfc005",
        },
        "_links": {
            "self": {
                "href": "/api/protocols/san/vvol-bindings/2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4/28c02623-42fa-4f5f-a984-a02044bfc005"
            }
        },
        "id": 2411392,
        "count": 1,
        "is_optimal": True,
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/bf295ccc-a6bb-11eb-93e8-005056bb470f"}
            },
            "uuid": "bf295ccc-a6bb-11eb-93e8-005056bb470f",
        },
        "protocol_endpoint": {
            "name": "/vol/vol1/pe1",
            "_links": {
                "self": {
                    "href": "/api/storage/luns/2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4"
                }
            },
            "uuid": "2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4",
        },
    }
)

```
</div>
</div>

---
### Deleting a vVol binding
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import VvolBinding

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = VvolBinding(
        **{
            "vvol.uuid": "28c02623-42fa-4f5f-a984-a02044bfc005",
            "protocol_endpoint.uuid": "2aab57f3-dc5d-491e-80d2-15c7ed5dd5c4",
        }
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


__all__ = ["VvolBinding", "VvolBindingSchema"]
__pdoc__ = {
    "VvolBindingSchema.resource": False,
    "VvolBindingSchema.opts": False,
}


class VvolBindingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VvolBinding object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the vvol_binding."""

    count = Size(
        data_key="count",
        allow_none=True,
    )
    r""" The vVol binding between any two specific LUNs is reference counted. When a REST POST is executed for a vVol binding that already exists, the vVol binding reference count is incremented. When a REST DELETE is executed, the vVol binding reference count is decremented. Only when the vVol binding count reaches zero, or the query parameter `delete_all_references` is supplied, is the vVol binding destroyed.


Example: 1"""

    id = Size(
        data_key="id",
        allow_none=True,
    )
    r""" The ONTAP internal identifier assigned to the vVol binding. The bind identifier is unique amongst all class `vvol` LUNs bound to the same class `protocol_endpoint` LUN.</br>
This property was included in early releases of the REST API for vVols and is maintained for backward compatibility. See the `secondary_id` property, which replaces `id`.


Example: 1"""

    is_optimal = marshmallow_fields.Boolean(
        data_key="is_optimal",
        allow_none=True,
    )
    r""" Indicates if the class `protocol_endpoint` LUN and the class `vvol` LUN are on the same cluster node.


Example: true"""

    protocol_endpoint = marshmallow_fields.Nested("netapp_ontap.resources.lun.LunSchema", data_key="protocol_endpoint", unknown=EXCLUDE, allow_none=True)
    r""" The protocol_endpoint field of the vvol_binding."""

    secondary_id = marshmallow_fields.Str(
        data_key="secondary_id",
        allow_none=True,
    )
    r""" The identifier assigned to the vVol binding, known as the secondary LUN ID. The identifier is unique amongst all class `vvol` LUNs bound to the same class `protocol_endpoint` LUN.</br>
The format for a secondary LUN ID is 16 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 0000D20000010000h"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the vvol_binding."""

    vvol = marshmallow_fields.Nested("netapp_ontap.resources.lun.LunSchema", data_key="vvol", unknown=EXCLUDE, allow_none=True)
    r""" The vvol field of the vvol_binding."""

    @property
    def resource(self):
        return VvolBinding

    gettable_fields = [
        "links",
        "count",
        "id",
        "is_optimal",
        "protocol_endpoint.links",
        "protocol_endpoint.name",
        "protocol_endpoint.uuid",
        "secondary_id",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "vvol.links",
        "vvol.name",
        "vvol.uuid",
    ]
    """links,count,id,is_optimal,protocol_endpoint.links,protocol_endpoint.name,protocol_endpoint.uuid,secondary_id,svm.links,svm.name,svm.uuid,vvol.links,vvol.name,vvol.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "protocol_endpoint.name",
        "protocol_endpoint.uuid",
        "svm.name",
        "svm.uuid",
        "vvol.name",
        "vvol.uuid",
    ]
    """protocol_endpoint.name,protocol_endpoint.uuid,svm.name,svm.uuid,vvol.name,vvol.uuid,"""

class VvolBinding(Resource):
    r""" A VMware virtual volume (vVol) binding is an association between a LUN of class `protocol_endpoint` and a LUN of class `vvol`. Class `protocol_endpoint` LUNs are mapped to igroups and granted access using the same configuration as class `regular` LUNs. When a class `vvol` LUN is bound to a mapped class `protocol_endpoint` LUN, VMware can access the class `vvol` LUN through the class `protocol_endpoint` LUN mapping.</br>
Class `protocol_endpoint` and `vvol` LUNs support many-to-many vVol bindings. A LUN of one class can be bound to zero or more LUNs of the opposite class.</br>
The vVol binding between any two specific LUNs is reference counted. When a REST POST is executed for a vVol binding that already exists, the vVol binding reference count is incremented. When a REST DELETE is executed, the vVol binding reference count is decremented. Only when the vVol binding count reaches zero, or the query parameter `delete_all_references` is supplied, is the vVol binding destroyed. """

    _schema = VvolBindingSchema
    _path = "/api/protocols/san/vvol-bindings"
    _keys = ["protocol_endpoint.uuid", "vvol.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves vVol bindings.
### Related ONTAP commands
* `lun bind show`
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)

### Learn more
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all VvolBinding resources that match the provided query"""
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
        """Returns a list of RawResources that represent VvolBinding resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["VvolBinding"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["VvolBinding"], NetAppResponse]:
        r"""Creates a vVol binding. The binding between any two specific LUNs is reference counted. When a binding is created that already exists, the binding count is incremented.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the vVol binding.
* `protocol_endpoint.uuid` or `protocol_endpoint.name` - Existing class `protocol_endpoint` LUN to bind to the specified class `vvol` LUN.
* `vvol.uuid` or `vvol.name` - Existing class `vvol` LUN to bind to the specified class `protocol_endpoint` LUN.
### Related ONTAP commands
* `lun bind create`
### Learn more
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)
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
        records: Iterable["VvolBinding"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a vVol binding. The binding between any two specific LUNs is reference counted. When a binding is deleted, the binding count is decremented, but the LUNs remain bound if the resultant reference count is greater than zero. When the binding count reaches zero, the binding is destroyed.
### Related ONTAP commands
* `lun bind destroy`
### Learn more
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves vVol bindings.
### Related ONTAP commands
* `lun bind show`
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)

### Learn more
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a vVol binding.
### Related ONTAP commands
* `lun bind show`
### Learn more
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)
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
        r"""Creates a vVol binding. The binding between any two specific LUNs is reference counted. When a binding is created that already exists, the binding count is incremented.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the vVol binding.
* `protocol_endpoint.uuid` or `protocol_endpoint.name` - Existing class `protocol_endpoint` LUN to bind to the specified class `vvol` LUN.
* `vvol.uuid` or `vvol.name` - Existing class `vvol` LUN to bind to the specified class `protocol_endpoint` LUN.
### Related ONTAP commands
* `lun bind create`
### Learn more
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)
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
        r"""Deletes a vVol binding. The binding between any two specific LUNs is reference counted. When a binding is deleted, the binding count is decremented, but the LUNs remain bound if the resultant reference count is greater than zero. When the binding count reaches zero, the binding is destroyed.
### Related ONTAP commands
* `lun bind destroy`
### Learn more
* [`DOC /protocols/san/vvol-bindings`](#docs-SAN-protocols_san_vvol-bindings)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


