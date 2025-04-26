r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Manages a specific filter instance.
See the documentation for [/support/ems/filters](#/docs/support/support_ems_filters) for details on the various properties.
## Examples
### Retrieving a specific filter instance
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsFilter

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsFilter(name="aggregate-events")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
EmsFilter(
    {
        "name": "aggregate-events",
        "_links": {"self": {"href": "/api/support/ems/filters/aggregate-events"}},
        "rules": [
            {
                "parameter_criteria": [
                    {"name_pattern": "type", "value_pattern": "aggregate"}
                ],
                "_links": {
                    "self": {
                        "href": "/api/support/ems/filters/aggregate-events/rules/1"
                    }
                },
                "index": 1,
                "type": "include",
                "message_criteria": {
                    "name_pattern": "*",
                    "_links": {
                        "related": {
                            "href": "/api/support/ems/messages?name=*&severity=emergency,alert,error,notice&snmp_trap_type=*"
                        }
                    },
                    "snmp_trap_types": "*",
                    "severities": "emergency,alert,error,notice",
                },
            },
            {
                "parameter_criteria": [{"name_pattern": "*", "value_pattern": "*"}],
                "_links": {
                    "self": {
                        "href": "/api/support/ems/filters/aggregate-events/rules/2"
                    }
                },
                "index": 2,
                "type": "exclude",
                "message_criteria": {
                    "name_pattern": "*",
                    "_links": {
                        "related": {
                            "href": "/api/support/ems/messages?name=*&severity=*&snmp_trap_type=*"
                        }
                    },
                    "snmp_trap_types": "*",
                    "severities": "*",
                },
            },
        ],
    }
)

```
</div>
</div>

### Updating an existing filter with a new rule
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsFilter

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsFilter(name="test-filter")
    resource.rules = [
        {
            "type": "include",
            "message_criteria": {"name_pattern": "wafl.*", "severities": "error"},
        }
    ]
    resource.patch()

```

### Deleting an existing filter
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsFilter

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsFilter(name="test-filter")
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


__all__ = ["EmsFilter", "EmsFilterSchema"]
__pdoc__ = {
    "EmsFilterSchema.resource": False,
    "EmsFilterSchema.opts": False,
}


class EmsFilterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsFilter object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_filter."""

    access_control_role = marshmallow_fields.Nested("netapp_ontap.resources.role.RoleSchema", data_key="access_control_role", unknown=EXCLUDE, allow_none=True)
    r""" The access_control_role field of the ems_filter."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Filter name

Example: wafl-critical-events"""

    rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.ems_filter_rule.EmsFilterRuleSchema", unknown=EXCLUDE, allow_none=True), data_key="rules", allow_none=True)
    r""" Array of event filter rules on which to match."""

    system_defined = marshmallow_fields.Boolean(
        data_key="system_defined",
        allow_none=True,
    )
    r""" Flag indicating system-defined filters.

Example: true"""

    @property
    def resource(self):
        return EmsFilter

    gettable_fields = [
        "links",
        "access_control_role.links",
        "access_control_role.name",
        "name",
        "rules",
        "system_defined",
    ]
    """links,access_control_role.links,access_control_role.name,name,rules,system_defined,"""

    patchable_fields = [
        "rules",
    ]
    """rules,"""

    postable_fields = [
        "name",
        "rules",
    ]
    """name,rules,"""

class EmsFilter(Resource):
    """Allows interaction with EmsFilter objects on the host"""

    _schema = EmsFilterSchema
    _path = "/api/support/ems/filters"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of event filters.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all EmsFilter resources that match the provided query"""
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
        """Returns a list of RawResources that represent EmsFilter resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["EmsFilter"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an event filter.
### Recommended optional properties
* `new_name` - New string that uniquely identifies a filter.
* `rules` - New list of criteria used to match the filter with an event. The existing list is discarded.
### Related ONTAP commands
* `event filter rename`
* `event filter rule add`
* `event filter rule delete`
* `event filter rule reorder`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["EmsFilter"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["EmsFilter"], NetAppResponse]:
        r"""Creates an event filter.
### Required properties
* `name` - String that uniquely identifies the filter.
### Recommended optional properties
* `rules` - List of criteria which is used to match a filter with an event.
### Related ONTAP commands
* `event filter create`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["EmsFilter"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an event filter.
### Related ONTAP commands
* `event filter delete`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of event filters.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an event filter.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
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
        r"""Creates an event filter.
### Required properties
* `name` - String that uniquely identifies the filter.
### Recommended optional properties
* `rules` - List of criteria which is used to match a filter with an event.
### Related ONTAP commands
* `event filter create`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
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
        r"""Updates an event filter.
### Recommended optional properties
* `new_name` - New string that uniquely identifies a filter.
* `rules` - New list of criteria used to match the filter with an event. The existing list is discarded.
### Related ONTAP commands
* `event filter rename`
* `event filter rule add`
* `event filter rule delete`
* `event filter rule reorder`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
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
        r"""Deletes an event filter.
### Related ONTAP commands
* `event filter delete`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


