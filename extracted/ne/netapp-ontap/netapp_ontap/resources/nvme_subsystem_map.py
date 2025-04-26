r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An NVMe subsystem map is an association of an NVMe namespace with an NVMe subsystem. When an NVMe namespace is mapped to an NVMe subsystem, the NVMe subsystem's hosts are granted access to the NVMe namespace. The relationship between an NVMe subsystem and an NVMe namespace is one subsystem to many namespaces.<br/>
The NVMe subsystem map REST API allows you to create, delete and discover NVMe subsystem maps.
## Examples
### Creating an NVMe subsystem map
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemMap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeSubsystemMap()
    resource.svm = {"name": "svm1"}
    resource.subsystem = {"name": "subsystem1"}
    resource.namespace = {"name": "/vol/vol1/namespace1"}
    resource.post(hydrate=True)
    print(resource)

```

---
### Retrieving all of the NVMe subsystem maps
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemMap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NvmeSubsystemMap.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    NvmeSubsystemMap(
        {
            "subsystem": {
                "name": "subsystem1",
                "uuid": "580a6b1e-fe43-11e8-91a0-005056a79967",
                "_links": {
                    "self": {
                        "href": "/api/protocols/nvme/subsystems/580a6b1e-fe43-11e8-91a0-005056a79967"
                    }
                },
            },
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystem-maps/580a6b1e-fe43-11e8-91a0-005056a79967/3ccdedc6-2519-4206-bc1f-b0f4adab6f89"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/0e91b214-fe40-11e8-91a0-005056a79967"
                    }
                },
                "uuid": "0e91b214-fe40-11e8-91a0-005056a79967",
            },
            "namespace": {
                "name": "/vol/vol1/namespace1",
                "_links": {
                    "self": {
                        "href": "/api/storage/namespaces/3ccdedc6-2519-4206-bc1f-b0f4adab6f89"
                    }
                },
                "uuid": "3ccdedc6-2519-4206-bc1f-b0f4adab6f89",
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific NVMe subsystem map
The NVMe subsystem map is identified by the UUID of the NVMe subsystem followed by the UUID of the NVMe namespace.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemMap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeSubsystemMap(
        **{
            "namespace.uuid": "3ccdedc6-2519-4206-bc1f-b0f4adab6f89",
            "subsystem.uuid": "580a6b1e-fe43-11e8-91a0-005056a79967",
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
NvmeSubsystemMap(
    {
        "subsystem": {
            "name": "subsystem1",
            "uuid": "580a6b1e-fe43-11e8-91a0-005056a79967",
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/subsystems/580a6b1e-fe43-11e8-91a0-005056a79967"
                }
            },
        },
        "_links": {
            "self": {
                "href": "/api/protocols/nvme/subsystem-maps/580a6b1e-fe43-11e8-91a0-005056a79967/3ccdedc6-2519-4206-bc1f-b0f4adab6f89"
            }
        },
        "nsid": "00000001h",
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/0e91b214-fe40-11e8-91a0-005056a79967"}
            },
            "uuid": "0e91b214-fe40-11e8-91a0-005056a79967",
        },
        "namespace": {
            "name": "/vol/vol1/namespace1",
            "_links": {
                "self": {
                    "href": "/api/storage/namespaces/3ccdedc6-2519-4206-bc1f-b0f4adab6f89"
                }
            },
            "node": {
                "name": "node1",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/012b4508-67d6-4788-8c2d-801f254ce976"
                    }
                },
                "uuid": "012b4508-67d6-4788-8c2d-801f254ce976",
            },
            "uuid": "3ccdedc6-2519-4206-bc1f-b0f4adab6f89",
        },
    }
)

```
</div>
</div>

---
### Deleting an NVMe subsystem map
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeSubsystemMap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeSubsystemMap(
        **{
            "namespace.uuid": "3ccdedc6-2519-4206-bc1f-b0f4adab6f89",
            "subsystem.uuid": "580a6b1e-fe43-11e8-91a0-005056a79967",
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


__all__ = ["NvmeSubsystemMap", "NvmeSubsystemMapSchema"]
__pdoc__ = {
    "NvmeSubsystemMapSchema.resource": False,
    "NvmeSubsystemMapSchema.opts": False,
}


class NvmeSubsystemMapSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemMap object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nvme_subsystem_map."""

    anagrpid = marshmallow_fields.Str(
        data_key="anagrpid",
        allow_none=True,
    )
    r""" The Asymmetric Namespace Access Group ID (ANAGRPID) of the NVMe namespace.<br/>
The format for an ANAGRPID is 8 hexadecimal digits (zero-filled) followed by a lower case "h".<br/>
There is an added computational cost to retrieving this property's value. It is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.


Example: 00103050h"""

    namespace = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_map_namespace.NvmeSubsystemMapNamespaceSchema", data_key="namespace", unknown=EXCLUDE, allow_none=True)
    r""" The NVMe namespace to which the NVMe subsystem is mapped. Required in POST by supplying either the UUID, name, or both."""

    nsid = marshmallow_fields.Str(
        data_key="nsid",
        allow_none=True,
    )
    r""" The NVMe namespace identifier. This is an identifier used by an NVMe controller to provide access to the NVMe namespace.<br/>
The format for an NVMe namespace identifier is 8 hexadecimal digits (zero-filled) followed by a lower case "h".


Example: 00000001h"""

    subsystem = marshmallow_fields.Nested("netapp_ontap.resources.nvme_subsystem.NvmeSubsystemSchema", data_key="subsystem", unknown=EXCLUDE, allow_none=True)
    r""" The subsystem field of the nvme_subsystem_map."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nvme_subsystem_map."""

    @property
    def resource(self):
        return NvmeSubsystemMap

    gettable_fields = [
        "links",
        "anagrpid",
        "namespace",
        "nsid",
        "subsystem.links",
        "subsystem.name",
        "subsystem.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,anagrpid,namespace,nsid,subsystem.links,subsystem.name,subsystem.uuid,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "namespace",
        "subsystem.name",
        "subsystem.uuid",
        "svm.name",
        "svm.uuid",
    ]
    """namespace,subsystem.name,subsystem.uuid,svm.name,svm.uuid,"""

class NvmeSubsystemMap(Resource):
    r""" An NVMe subsystem map is an association of an NVMe namespace with an NVMe subsystem. When an NVMe namespace is mapped to an NVMe subsystem, the NVMe subsystem's hosts are granted access to the NVMe namespace. The relationship between an NVMe subsystem and an NVMe namespace is one subsystem to many namespaces. """

    _schema = NvmeSubsystemMapSchema
    _path = "/api/protocols/nvme/subsystem-maps"
    _keys = ["subsystem.uuid", "namespace.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NVMe subsystem maps.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `anagrpid`
### Related ONTAP commands
* `vserver nvme subsystem map show`
### Learn more
* [`DOC /protocols/nvme/subsystem-maps`](#docs-NVMe-protocols_nvme_subsystem-maps)
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
        """Returns a count of all NvmeSubsystemMap resources that match the provided query"""
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
        """Returns a list of RawResources that represent NvmeSubsystemMap resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["NvmeSubsystemMap"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NvmeSubsystemMap"], NetAppResponse]:
        r"""Creates an NVMe subsystem map.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the NVMe subsystem map.
* `namespace.uuid` or `namespace.name` - Existing NVMe namespace to map to the specified NVme subsystem.
* `subsystem.uuid` or `subsystem.name` - Existing NVMe subsystem to map to the specified NVMe namespace.
### Related ONTAP commands
* `vserver nvme subsystem map add`
### Learn more
* [`DOC /protocols/nvme/subsystem-maps`](#docs-NVMe-protocols_nvme_subsystem-maps)
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
        records: Iterable["NvmeSubsystemMap"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an NVMe subsystem map.
### Related ONTAP commands
* `vserver nvme subsystem map remove`
### Learn more
* [`DOC /protocols/nvme/subsystem-maps`](#docs-NVMe-protocols_nvme_subsystem-maps)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NVMe subsystem maps.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `anagrpid`
### Related ONTAP commands
* `vserver nvme subsystem map show`
### Learn more
* [`DOC /protocols/nvme/subsystem-maps`](#docs-NVMe-protocols_nvme_subsystem-maps)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NVMe subsystem map.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `anagrpid`
### Related ONTAP commands
* `vserver nvme subsystem map show`
### Learn more
* [`DOC /protocols/nvme/subsystem-maps`](#docs-NVMe-protocols_nvme_subsystem-maps)
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
        r"""Creates an NVMe subsystem map.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the NVMe subsystem map.
* `namespace.uuid` or `namespace.name` - Existing NVMe namespace to map to the specified NVme subsystem.
* `subsystem.uuid` or `subsystem.name` - Existing NVMe subsystem to map to the specified NVMe namespace.
### Related ONTAP commands
* `vserver nvme subsystem map add`
### Learn more
* [`DOC /protocols/nvme/subsystem-maps`](#docs-NVMe-protocols_nvme_subsystem-maps)
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
        r"""Deletes an NVMe subsystem map.
### Related ONTAP commands
* `vserver nvme subsystem map remove`
### Learn more
* [`DOC /protocols/nvme/subsystem-maps`](#docs-NVMe-protocols_nvme_subsystem-maps)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


