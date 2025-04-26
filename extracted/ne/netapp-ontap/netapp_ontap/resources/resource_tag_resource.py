r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this endpoint to list all of the resources in the API that have been tagged with a particular tag value and to create new tags on existing resources. Each resource has a limit of 64 tags that cannot be exceeded. See the section labelled [Tagging Resources for Tracking Purposes](#Tagging_Resources_for_Tracking_Purposes) to find out more information about how to tag a resource.
## Examples
The following examples show some ways that this endpoint can be used.
### List all resources that are tagged for the test environment.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ResourceTagResource

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ResourceTagResource.get_collection("environment:test")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    ResourceTagResource(
        {"href": "/api/storage/volumes/558949d1-d4cf-445e-ada5-e340dee6a581"}
    ),
    ResourceTagResource({"href": "/api/svm/svms/7f97a0b1-fe4f-11e8-b9c5-005056a76061"}),
    ResourceTagResource({"href": "/api/cluster"}),
]

```
</div>
</div>

---
### List all volumes that have been tagged for the accounting team
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ResourceTagResource

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            ResourceTagResource.get_collection(
                "team:accounting", label="storage_volumes"
            )
        )
    )

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    ResourceTagResource(
        {
            "label": "storage_volumes",
            "href": "/api/storage/volumes/558949d1-d4cf-445e-ada5-e340dee6a581",
        }
    ),
    ResourceTagResource(
        {
            "label": "storage_volumes",
            "href": "/api/storage/volumes/64750961-fda7-4327-9f16-00034c3f5ad2",
        }
    ),
    ResourceTagResource(
        {
            "label": "storage_volumes",
            "href": "/api/storage/volumes/bee17b91-f90a-4854-b146-8b102a0a9882",
        }
    ),
]

```
</div>
</div>

---
### Create a new tag on a volume
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ResourceTagResource

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ResourceTagResource("team:accounting")
    resource.href = "/api/storage/volumes/f288168e-bd3e-11ed-9516-005056acd4e8"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
ResourceTagResource(
    {"href": "/api/storage/volumes/f288168e-bd3e-11ed-9516-005056acd4e8"}
)

```
</div>
</div>

---
### Delete a new tag on a volume
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ResourceTagResource

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ResourceTagResource(
        "team:accounting",
        href="/api/storage/volumes/f288168e-bd3e-11ed-9516-005056acd4e8",
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


__all__ = ["ResourceTagResource", "ResourceTagResourceSchema"]
__pdoc__ = {
    "ResourceTagResourceSchema.resource": False,
    "ResourceTagResourceSchema.opts": False,
}


class ResourceTagResourceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ResourceTagResource object"""

    href = marshmallow_fields.Str(
        data_key="href",
        allow_none=True,
    )
    r""" This property provides the address in the API at which the tagged resource is available. Additional queries can be made on this
endpoint to fetch the resource's properties."""

    label = marshmallow_fields.Str(
        data_key="label",
        allow_none=True,
    )
    r""" This is a human-readable classifier representing the type of thing that is pointed to by the href.

Example: volume"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the resource_tag_resource."""

    value = marshmallow_fields.Str(
        data_key="value",
        allow_none=True,
    )
    r""" The text value of the tag formatted as `key:value`."""

    @property
    def resource(self):
        return ResourceTagResource

    gettable_fields = [
        "href",
        "label",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "value",
    ]
    """href,label,svm.links,svm.name,svm.uuid,value,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "href",
        "value",
    ]
    """href,value,"""

class ResourceTagResource(Resource):
    r""" This object provides a pointer to the tagged resource in the API. Details about the tagged object are available by querying
the address of the href property. """

    _schema = ResourceTagResourceSchema
    _path = "/api/resource-tags/{resource_tag[value]}/resources"
    _keys = ["resource_tag.value", "href"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the resources for a specific tag
### Learn more
* [`DOC /resource-tags/{resource_tag.value}/resources`](#docs-cluster-resource-tags_{resource_tag.value}_resources)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ResourceTagResource resources that match the provided query"""
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
        """Returns a list of RawResources that represent ResourceTagResource resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["ResourceTagResource"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["ResourceTagResource"], NetAppResponse]:
        r"""Creates a new tag on a specific resource.
### Learn more
* [`DOC /resource-tags/{resource_tag.value}/resources`](#docs-cluster-resource-tags_{resource_tag.value}_resources)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["ResourceTagResource"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a specific tag on a specific resource.
### Learn more
* [`DOC /resource-tags/{resource_tag.value}/resources`](#docs-cluster-resource-tags_{resource_tag.value}_resources)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the resources for a specific tag
### Learn more
* [`DOC /resource-tags/{resource_tag.value}/resources`](#docs-cluster-resource-tags_{resource_tag.value}_resources)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific resource for a specific tag.
### Learn more
* [`DOC /resource-tags/{resource_tag.value}/resources`](#docs-cluster-resource-tags_{resource_tag.value}_resources)"""
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
        r"""Creates a new tag on a specific resource.
### Learn more
* [`DOC /resource-tags/{resource_tag.value}/resources`](#docs-cluster-resource-tags_{resource_tag.value}_resources)"""
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
        r"""Deletes a specific tag on a specific resource.
### Learn more
* [`DOC /resource-tags/{resource_tag.value}/resources`](#docs-cluster-resource-tags_{resource_tag.value}_resources)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


