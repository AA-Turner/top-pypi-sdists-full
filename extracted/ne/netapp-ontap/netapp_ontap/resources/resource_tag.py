r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

# Overview
You can use this endpoint to list all of the tags that have been used on resources in the API. See the section labelled [Tagging Resources for Tracking Purposes](#Tagging_Resources_for_Tracking_Purposes) to find out more information about how to tag a resource.
## Examples
The following examples show some ways that this endpoint can be used.
### List all of the used tags
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ResourceTag

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ResourceTag.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    ResourceTag({"num_resources": 2, "value": "team:accounting"}),
    ResourceTag({"num_resources": 5, "value": "environment:test"}),
]

```
</div>
</div>

---
### Find tags that are being used by at least 3 resources
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ResourceTag

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ResourceTag.get_collection(num_resources=">=3")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[ResourceTag({"num_resources": 5, "value": "environment:test"})]

```
</div>
</div>
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


__all__ = ["ResourceTag", "ResourceTagSchema"]
__pdoc__ = {
    "ResourceTagSchema.resource": False,
    "ResourceTagSchema.opts": False,
}


class ResourceTagSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ResourceTag object"""

    num_resources = Size(
        data_key="num_resources",
        validate=integer_validation(minimum=1),
        allow_none=True,
    )
    r""" The number of resources that are currently using this tag."""

    value = marshmallow_fields.Str(
        data_key="value",
        validate=len_validation(minimum=0, maximum=200),
        allow_none=True,
    )
    r""" A key:value formatted string representing the tag's name.

Example: team:accounting"""

    @property
    def resource(self):
        return ResourceTag

    gettable_fields = [
        "num_resources",
        "value",
    ]
    """num_resources,value,"""

    patchable_fields = [
        "num_resources",
        "value",
    ]
    """num_resources,value,"""

    postable_fields = [
        "num_resources",
        "value",
    ]
    """num_resources,value,"""

class ResourceTag(Resource):
    r""" A resource tag is a way to group resources in the API together for identification or tracking purposes. """

    _schema = ResourceTagSchema
    _path = "/api/resource-tags"
    _keys = ["value"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the tags currently being used for resources in the API.
### Learn more
* [`DOC /resource-tags`](#docs-cluster-resource-tags)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all ResourceTag resources that match the provided query"""
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
        """Returns a list of RawResources that represent ResourceTag resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the tags currently being used for resources in the API.
### Learn more
* [`DOC /resource-tags`](#docs-cluster-resource-tags)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific resource tag.
### Learn more
* [`DOC /resource-tags`](#docs-cluster-resource-tags)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





