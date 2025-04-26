r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
Manages a specific instance of a rule within a filter.
See the documentation for [/support/ems/filters](#/docs/support/support_ems_filters) for details on the various properties in a rule.
## Examples
### Retrieving a single instance of a rule
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsFilterRule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsFilterRule("no-info-debug-events", index=1)
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
EmsFilterRule(
    {
        "parameter_criteria": [{"name_pattern": "*", "value_pattern": "*"}],
        "_links": {
            "self": {"href": "/api/support/ems/filters/no-info-debug-events/rules/1"}
        },
        "index": 1,
        "type": "include",
        "message_criteria": {
            "name_pattern": "*",
            "_links": {},
            "snmp_trap_types": "*",
            "severities": "emergency,alert,error,notice",
        },
    }
)

```
</div>
</div>

### Updating an existing rule to use severity emergency
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsFilterRule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsFilterRule("test-filter", index=1)
    resource.message_criteria = {"severities": "emergency"}
    resource.patch()

```

### Deleting a rule from an existing filter
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import EmsFilterRule

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = EmsFilterRule("test-filter", index=1)
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


__all__ = ["EmsFilterRule", "EmsFilterRuleSchema"]
__pdoc__ = {
    "EmsFilterRuleSchema.resource": False,
    "EmsFilterRuleSchema.opts": False,
}


class EmsFilterRuleSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsFilterRule object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ems_filter_rule."""

    index = Size(
        data_key="index",
        allow_none=True,
    )
    r""" Rule index. Rules are evaluated in ascending order. If a rule's index order is not specified during creation, the rule is appended to the end of the list.

Example: 1"""

    message_criteria = marshmallow_fields.Nested("netapp_ontap.models.ems_filter_rules_message_criteria.EmsFilterRulesMessageCriteriaSchema", data_key="message_criteria", unknown=EXCLUDE, allow_none=True)
    r""" Matching message definitions for the filter. A property must be specified."""

    parameter_criteria = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_filter_response_records_rules_parameter_criteria.EmsFilterResponseRecordsRulesParameterCriteriaSchema", unknown=EXCLUDE, allow_none=True), data_key="parameter_criteria", allow_none=True)
    r""" Parameter criteria used to match against events' parameters. Each parameter consists of a name and a value. When multiple parameter criteria are provided in a rule, all must match for the rule to be considered matched. A pattern can include one or more wildcard '*' characters."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['include', 'exclude']),
        allow_none=True,
    )
    r""" Rule type

Valid choices:

* include
* exclude"""

    @property
    def resource(self):
        return EmsFilterRule

    gettable_fields = [
        "links",
        "index",
        "message_criteria",
        "parameter_criteria",
        "type",
    ]
    """links,index,message_criteria,parameter_criteria,type,"""

    patchable_fields = [
        "index",
        "message_criteria",
        "parameter_criteria",
        "type",
    ]
    """index,message_criteria,parameter_criteria,type,"""

    postable_fields = [
        "index",
        "message_criteria",
        "parameter_criteria",
        "type",
    ]
    """index,message_criteria,parameter_criteria,type,"""

class EmsFilterRule(Resource):
    r""" Rule for an event filter """

    _schema = EmsFilterRuleSchema
    _path = "/api/support/ems/filters/{ems_filter[name]}/rules"
    _keys = ["ems_filter.name", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves event filter rules.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters/{name}/rules`](#docs-support-support_ems_filters_{name}_rules)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all EmsFilterRule resources that match the provided query"""
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
        """Returns a list of RawResources that represent EmsFilterRule resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["EmsFilterRule"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an event filter rule.
### Recommended optional properties
* `message_criteria` - Message criteria used by a rule to match an event.
* `parameter_criteria` - Parameter criteria used by a rule to match an event.
### Related ONTAP commands
* `event filter rule add`
* `event filter rule delete`

### Learn more
* [`DOC /support/ems/filters/{name}/rules/{index}`](#docs-support-support_ems_filters_{name}_rules_{index})"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["EmsFilterRule"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["EmsFilterRule"], NetAppResponse]:
        r"""Creates an event filter rule.
### Required properties
* `type` - Enumeration indicating whether the rule is for include or exclude.
* `message_criteria` - Message criteria used by a rule to match an event.
* `parameter_criteria` - Parameter criteria used by a rule to match an event.
Note: At least one pattern needs to be provided for message_criteria and / or
parameter_criteria.
### Recommended optional properties
* `index` - One-based position index of the new rule.
### Related ONTAP commands
* `event filter rule add`

### Learn more
* [`DOC /support/ems/filters/{name}/rules`](#docs-support-support_ems_filters_{name}_rules)"""
        return super()._post_collection(
            records, *args, hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    post_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["EmsFilterRule"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an event filter rule.
### Related ONTAP commands
* `event filter rule delete`

### Learn more
* [`DOC /support/ems/filters/{name}/rules/{index}`](#docs-support-support_ems_filters_{name}_rules_{index})"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves event filter rules.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters/{name}/rules`](#docs-support-support_ems_filters_{name}_rules)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an event filter rule.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters/{name}/rules/{index}`](#docs-support-support_ems_filters_{name}_rules_{index})"""
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
        r"""Creates an event filter rule.
### Required properties
* `type` - Enumeration indicating whether the rule is for include or exclude.
* `message_criteria` - Message criteria used by a rule to match an event.
* `parameter_criteria` - Parameter criteria used by a rule to match an event.
Note: At least one pattern needs to be provided for message_criteria and / or
parameter_criteria.
### Recommended optional properties
* `index` - One-based position index of the new rule.
### Related ONTAP commands
* `event filter rule add`

### Learn more
* [`DOC /support/ems/filters/{name}/rules`](#docs-support-support_ems_filters_{name}_rules)"""
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
        r"""Updates an event filter rule.
### Recommended optional properties
* `message_criteria` - Message criteria used by a rule to match an event.
* `parameter_criteria` - Parameter criteria used by a rule to match an event.
### Related ONTAP commands
* `event filter rule add`
* `event filter rule delete`

### Learn more
* [`DOC /support/ems/filters/{name}/rules/{index}`](#docs-support-support_ems_filters_{name}_rules_{index})"""
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
        r"""Deletes an event filter rule.
### Related ONTAP commands
* `event filter rule delete`

### Learn more
* [`DOC /support/ems/filters/{name}/rules/{index}`](#docs-support-support_ems_filters_{name}_rules_{index})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


