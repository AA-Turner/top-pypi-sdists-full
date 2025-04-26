r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
An iSCSI service defines the properties of the iSCSI target for an SVM. There can be at most one iSCSI service for an SVM. An SVM's iSCSI service must be created before iSCSI initiators can log in to the SVM.<br/>
The iSCSI service REST API allows you to create, update, delete, and discover iSCSI services for SVMs.
### Platform Specifics

* **ASA r2**: An iSCSI service is always present for each data SVM. The service can be disabled, but not created or deleted.
## Performance monitoring
Performance of the SVM can be monitored by the `metric.*` and `statistics.*` properties. These show the performance of the SVM in terms of IOPS, latency and throughput. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
## Examples
### Creating an iSCSI service for an SVM
The simplest way to create an iSCSI service is to specify only the SVM, either by name or UUID. By default, the new iSCSI service is enabled and uses the SVM name as its target alias.<br/>
In this example, the `return_records` query parameter is used to retrieve the new iSCSI service object in the REST response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IscsiService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IscsiService()
    resource.svm = {"name": "svm1"}
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
IscsiService(
    {
        "enabled": True,
        "target": {
            "alias": "svm1",
            "name": "iqn.1992-08.com.netapp:sn.19d04b8e94d711e88370005056b48fd2:vs.4",
        },
        "_links": {
            "self": {
                "href": "/api/protocols/san/iscsi/services/19d04b8e-94d7-11e8-8370-005056b48fd2"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/19d04b8e-94d7-11e8-8370-005056b48fd2"}
            },
            "uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2",
        },
    }
)

```
</div>
</div>

---
### Retrieving the iSCSI services for all SVMs in the cluster
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IscsiService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(IscsiService.get_collection()))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    IscsiService(
        {
            "_links": {
                "self": {
                    "href": "/api/protocols/san/iscsi/services/19d04b8e-94d7-11e8-8370-005056b48fd2"
                }
            },
            "svm": {
                "name": "svm1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/19d04b8e-94d7-11e8-8370-005056b48fd2"
                    }
                },
                "uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2",
            },
        }
    ),
    IscsiService(
        {
            "_links": {
                "self": {
                    "href": "/api/protocols/san/iscsi/services/25f617cf-94d7-11e8-8370-005056b48fd2"
                }
            },
            "svm": {
                "name": "svm2",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/25f617cf-94d7-11e8-8370-005056b48fd2"
                    }
                },
                "uuid": "25f617cf-94d7-11e8-8370-005056b48fd2",
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving details for a specific iSCSI service
The iSCSI service is identified by the UUID of its SVM.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IscsiService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IscsiService(**{"svm.uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
IscsiService(
    {
        "enabled": True,
        "target": {
            "alias": "svm1",
            "name": "iqn.1992-08.com.netapp:sn.19d04b8e94d711e88370005056b48fd2:vs.4",
        },
        "_links": {
            "self": {
                "href": "/api/protocols/san/iscsi/services/19d04b8e-94d7-11e8-8370-005056b48fd2"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/19d04b8e-94d7-11e8-8370-005056b48fd2"}
            },
            "uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2",
        },
    }
)

```
</div>
</div>

---
### Disabling an iSCSI service
Disabling an iSCSI service shuts down all active iSCSI sessions for the SVM and prevents the creation of new iSCSI sessions.<br/>
The iSCSI service to update is identified by the UUID of its SVM.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IscsiService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IscsiService(**{"svm.uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2"})
    resource.enabled = False
    resource.patch()

```

<br/>
You can retrieve the iSCSI service to confirm the change.<br/>
In this example, the `fields` query parameter is used to limit the response to the `enabled` property and iSCSI service identifiers.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IscsiService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IscsiService(**{"svm.uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2"})
    resource.get(fields="enabled")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
IscsiService(
    {
        "enabled": False,
        "_links": {
            "self": {
                "href": "/api/protocols/san/iscsi/services/19d04b8e-94d7-11e8-8370-005056b48fd2"
            }
        },
        "svm": {
            "name": "svm1",
            "_links": {
                "self": {"href": "/api/svm/svms/19d04b8e-94d7-11e8-8370-005056b48fd2"}
            },
            "uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2",
        },
    }
)

```
</div>
</div>

---
### Deleting an iSCSI service
The iSCSI service must be disabled before it can be deleted.<br/>
The iSCSI service to be deleted is identified by the UUID of its SVM.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IscsiService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IscsiService(**{"svm.uuid": "19d04b8e-94d7-11e8-8370-005056b48fd2"})
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


__all__ = ["IscsiService", "IscsiServiceSchema"]
__pdoc__ = {
    "IscsiServiceSchema.resource": False,
    "IscsiServiceSchema.opts": False,
}


class IscsiServiceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiService object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the iscsi_service."""

    enabled = marshmallow_fields.Boolean(
        data_key="enabled",
        allow_none=True,
    )
    r""" The administrative state of the iSCSI service. The iSCSI service can be disabled to block all iSCSI connectivity to the SVM.<br/>
Optional in POST and PATCH. The default setting is _true_ (enabled) in POST."""

    metric = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_svm.PerformanceMetricSvmSchema", data_key="metric", unknown=EXCLUDE, allow_none=True)
    r""" The metric field of the iscsi_service."""

    statistics = marshmallow_fields.Nested("netapp_ontap.models.performance_metric_raw_svm.PerformanceMetricRawSvmSchema", data_key="statistics", unknown=EXCLUDE, allow_none=True)
    r""" The statistics field of the iscsi_service."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the iscsi_service."""

    target = marshmallow_fields.Nested("netapp_ontap.models.iscsi_service_target.IscsiServiceTargetSchema", data_key="target", unknown=EXCLUDE, allow_none=True)
    r""" The target field of the iscsi_service."""

    @property
    def resource(self):
        return IscsiService

    gettable_fields = [
        "links",
        "enabled",
        "metric.links",
        "metric.duration",
        "metric.iops",
        "metric.latency",
        "metric.status",
        "metric.throughput",
        "metric.timestamp",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "target",
    ]
    """links,enabled,metric.links,metric.duration,metric.iops,metric.latency,metric.status,metric.throughput,metric.timestamp,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,svm.links,svm.name,svm.uuid,target,"""

    patchable_fields = [
        "enabled",
        "target",
    ]
    """enabled,target,"""

    postable_fields = [
        "enabled",
        "svm.name",
        "svm.uuid",
        "target",
    ]
    """enabled,svm.name,svm.uuid,target,"""

class IscsiService(Resource):
    r""" An iSCSI service defines the properties of the iSCSI target for an SVM. There can be at most one iSCSI service for an SVM. An SVM's iSCSI service must be created before iSCSI initiators can log in to the SVM.<br/>
An iSCSI service is identified by the UUID of its SVM. """

    _schema = IscsiServiceSchema
    _path = "/api/protocols/san/iscsi/services"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves iSCSI services.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver iscsi show`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
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
        """Returns a count of all IscsiService resources that match the provided query"""
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
        """Returns a list of RawResources that represent IscsiService resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["IscsiService"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an iSCSI service.
### Related ONTAP commands
* `vserver iscsi modify`
* `vserver iscsi start`
* `vserver iscsi stop`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["IscsiService"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IscsiService"], NetAppResponse]:
        r"""Creates an iSCSI service.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the iSCSI service for access to the iSCSI protocol.
* **ASA r2**: POST and DELETE are not supported. The iSCSI service is automatically created and deleted with the SVM.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the iSCSI service.
### Related ONTAP commands
* `vserver iscsi create`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
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
        records: Iterable["IscsiService"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an iSCSI service. An iSCSI service must be disabled before it can be deleted.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the iSCSI service for access to the iSCSI protocol.
* **ASA r2**: POST and DELETE are not supported. The iSCSI service is automatically created and deleted with the SVM.
### Related ONTAP commands
* `vserver iscsi delete`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves iSCSI services.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver iscsi show`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an iSCSI service.
### Related ONTAP commands
* `vserver iscsi show`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
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
        r"""Creates an iSCSI service.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the iSCSI service for access to the iSCSI protocol.
* **ASA r2**: POST and DELETE are not supported. The iSCSI service is automatically created and deleted with the SVM.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the iSCSI service.
### Related ONTAP commands
* `vserver iscsi create`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
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
        r"""Updates an iSCSI service.
### Related ONTAP commands
* `vserver iscsi modify`
* `vserver iscsi start`
* `vserver iscsi stop`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
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
        r"""Deletes an iSCSI service. An iSCSI service must be disabled before it can be deleted.
### Platform Specifics
* **Unified ONTAP**: POST and DELETE must be used to manage the iSCSI service for access to the iSCSI protocol.
* **ASA r2**: POST and DELETE are not supported. The iSCSI service is automatically created and deleted with the SVM.
### Related ONTAP commands
* `vserver iscsi delete`
### Learn more
* [`DOC /protocols/san/iscsi/services`](#docs-SAN-protocols_san_iscsi_services)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


