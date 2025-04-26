r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
A Non-Volatile Memory Express (NVMe) service defines the properties of the NVMe controller target for an SVM. There can be at most one NVMe service for an SVM. An SVM's NVMe service must be created before NVMe host initiators can connect to the SVM.<br/>
The Non-Volatile Memory Express (NVMe) service REST API allows you to create, update, delete, and discover NVMe services for SVMs.
### Platform Specifics

* **ASA r2**: An NVMe service is always present for each data SVM. The service can be disabled, but not created or deleted.
## Performance monitoring
Performance of the SVM can be monitored by the `metric.*` and `statistics.*` properties. These show the performance of the SVM in terms of IOPS, latency and throughput. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
## Examples
### Creating an NVMe service for an SVM
The simplest way to create an NVMe service is to specify only the SVM, either by name or UUID. By default, the new NVMe service is enabled.<br/>
In this example, the `return_records` query parameter is used to retrieve the new NVMe service object in the REST response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeService()
    resource.svm = {"name": "svm1"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
NvmeService(
    {
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"}
            },
            "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
        },
    }
)

```
</div>
</div>

---
### Retrieving the NVMe services for all SVMs in the cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(NvmeService.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    NvmeService(
        {
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/services/ab60c350-dc68-11e8-9711-005056bbe408"
                }
            },
            "svm": {
                "name": "svm0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/ab60c350-dc68-11e8-9711-005056bbe408"
                    }
                },
                "uuid": "ab60c350-dc68-11e8-9711-005056bbe408",
            },
        }
    ),
    NvmeService(
        {
            "_links": {
                "self": {
                    "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"
                    }
                },
                "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving details for a specific NVMe service
The NVMe service is identified by the UUID of its SVM.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeService(**{"svm.uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
NvmeService(
    {
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"}
            },
            "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
        },
    }
)

```
</div>
</div>

---
### Disabling an NVMe service
Disabling an NVMe service shuts down all active NVMe connections for the SVM and prevents the creation of new NVMe connections.<br/>
The NVMe service to update is identified by the UUID of its SVM.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeService(**{"svm.uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341"})
    resource.enabled = False
    resource.patch()

```

<br/>
You can retrieve the NVMe service to confirm the change.<br/>
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeService(**{"svm.uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
NvmeService(
    {
        "enabled": False,
        "_links": {
            "self": {
                "href": "/api/protocols/nvme/services/bfb1beb0-dc69-11e8-b29f-005056bb7341"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/bfb1beb0-dc69-11e8-b29f-005056bb7341"}
            },
            "uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341",
        },
    }
)

```
</div>
</div>

---
### Deleting an NVMe service
The NVMe service must be disabled before it can be deleted. In addition, all NVMe interfaces, subsystems, and subsystem maps associated with the SVM must first be deleted.<br/>
The NVMe service to delete is identified by the UUID of its SVM.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import NvmeService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = NvmeService(**{"svm.uuid": "bfb1beb0-dc69-11e8-b29f-005056bb7341"})
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


__all__ = ["NvmeService", "NvmeServiceSchema"]
__pdoc__ = {
    "NvmeServiceSchema.resource": False,
    "NvmeServiceSchema.opts": False,
}


class NvmeServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeService object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nvme_service."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The administrative state of the NVMe service. The NVMe service can be disabled to block all NVMe connectivity to the SVM.<br/>
This is optional in POST and PATCH. The default setting is _true_ (enabled) in POST."""

    metric = marshmallow_fields.Nested("netapp_ontap.models.nvme_service_metric.NvmeServiceMetricSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" Performance numbers, such as IOPS latency and throughput, for SVM protocols."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.nvme_service_statistics.NvmeServiceStatisticsSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" These are raw performance numbers, such as IOPS latency and throughput for SVM protocols. These numbers are aggregated across all nodes in the cluster and increase with the uptime of the cluster."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the nvme_service."""

    @property
    def resource(self):
        return NvmeService

    gettable_fields = [
        "links",
        "enabled",
        "metric",
        "statistics",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,enabled,metric,statistics,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
        "svm.name",
        "svm.uuid",
    ]
    """enabled,svm.name,svm.uuid,"""

class NvmeService(Resource):
    r""" A Non-Volatile Memory Express (NVMe) service defines the properties of the NVMe controller target for an SVM. There can be at most one NVMe service for an SVM. An SVM's NVMe service must be created before NVMe host initiators can connect to the SVM.<br/>
An NVMe service is identified by the UUID of its SVM. """

    _schema = NvmeServiceSchema
    _path = "/api/protocols/nvme/services"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves NVMe services.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver nvme show`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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
        """Returns a count of all NvmeService resources that match the provided query"""
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
        """Returns a list of RawResources that represent NvmeService resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["NvmeService"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an NVMe service.
### Related ONTAP commands
* `vserver nvme modify`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["NvmeService"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NvmeService"], NetAppResponse]:
        r"""Creates an NVMe service.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the NVMe service for access to the NVMe protocol.
* **ASA r2**: POST and DELETE are not supported. The NVMe service is automatically created and deleted with the SVM.
### Required properties
* `svm.uuid` or `svm.name` - The existing SVM in which to create the NVMe service.
### Related ONTAP commands
* `vserver nvme create`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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
        records: Iterable["NvmeService"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an NVMe service. An NVMe service must be disabled before it can be deleted. In addition, all NVMe interfaces, subsystems, and subsystem maps associated with the SVM must first be deleted.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the NVMe service for access to the NVMe protocol.
* **ASA r2**: POST and DELETE are not supported. The NVMe service is automatically created and deleted with the SVM.
### Related ONTAP commands
* `vserver nvme delete`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves NVMe services.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver nvme show`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NVMe service.
### Related ONTAP commands
* `vserver nvme show`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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
        r"""Creates an NVMe service.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the NVMe service for access to the NVMe protocol.
* **ASA r2**: POST and DELETE are not supported. The NVMe service is automatically created and deleted with the SVM.
### Required properties
* `svm.uuid` or `svm.name` - The existing SVM in which to create the NVMe service.
### Related ONTAP commands
* `vserver nvme create`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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
        r"""Updates an NVMe service.
### Related ONTAP commands
* `vserver nvme modify`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
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
        r"""Deletes an NVMe service. An NVMe service must be disabled before it can be deleted. In addition, all NVMe interfaces, subsystems, and subsystem maps associated with the SVM must first be deleted.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the NVMe service for access to the NVMe protocol.
* **ASA r2**: POST and DELETE are not supported. The NVMe service is automatically created and deleted with the SVM.
### Related ONTAP commands
* `vserver nvme delete`
### Learn more
* [`DOC /protocols/nvme/services`](#docs-NVMe-protocols_nvme_services)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


