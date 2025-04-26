r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

An event retention policy consists of a policy-name and a retention-period. The policy can be applied to a single file or files in a directory. Only a user with the security login role vsadmin-snaplock can perform the operation. EBR policies cannot be applied to files under a Legal-Hold.
### Examples
1. Creates an EBR policy policy_name with a retention period of "10 years":
   <br/>
   ```
   POST "/api/storage/snaplock/event-retention/policies/" '{"name": "policy_name","retention_period": "P10Y"}'
   ```
   <br/>
2. Creates an EBR policy policy_name1 with a retention period of "infinite":
   <br/>
   ```
   POST "/api/storage/snaplock/event-retention/policies/" '{"name": "policy_name1","retention_period": "infinite"}'
   ```
   <br/>"""

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


__all__ = ["SnaplockRetentionPolicy", "SnaplockRetentionPolicySchema"]
__pdoc__ = {
    "SnaplockRetentionPolicySchema.resource": False,
    "SnaplockRetentionPolicySchema.opts": False,
}


class SnaplockRetentionPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockRetentionPolicy object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snaplock_retention_policy."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Specifies the EBR policy name"""

    retention_period = marshmallow_fields.Str(
        data_key="retention_period",
        allow_none=True,
    )
    r""" Specifies the retention period of an event based retention policy. The retention period value represents a duration and must be specified in the ISO-8601 duration format. The retention period can be in years, months, days, hours or minutes. A period specified for years, months and days is represented in the ISO-8601 format as "P<num>Y", "P<num>M", "P<num>D" respectively. For example "P10Y" represents a duration of 10 years. Similarly, a duration in hours, minutes is represented by "PT<num>H", "PT<num>M" respectively. The period string must contain only a single time element i.e. either years, months, days, hours or minutes. A duration which combines different periods is not supported, example "P1Y10M" is not supported. Apart from the duration specified in the ISO-8601 format, the retention period field also accepts the strings "infinite" and "unspecified".

Example: P30M"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the snaplock_retention_policy."""

    @property
    def resource(self):
        return SnaplockRetentionPolicy

    gettable_fields = [
        "links",
        "name",
        "retention_period",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,name,retention_period,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "retention_period",
    ]
    """retention_period,"""

    postable_fields = [
        "name",
        "retention_period",
    ]
    """name,retention_period,"""

class SnaplockRetentionPolicy(Resource):
    """Allows interaction with SnaplockRetentionPolicy objects on the host"""

    _schema = SnaplockRetentionPolicySchema
    _path = "/api/storage/snaplock/event-retention/policies"
    _keys = ["policy.name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves all event retention policies for an SVM.
### Related ONTAP commands
* `snaplock event-retention policy show`
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
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
        """Returns a count of all SnaplockRetentionPolicy resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnaplockRetentionPolicy resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["SnaplockRetentionPolicy"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the retention period of an Event Based Retention (EBR) policy.
### Related ONTAP commands
* `snaplock event-retention policy modify`
### Example
Updates the retention period of an EBR policy "policy_name":
<br/>
```
PATCH "/api/storage/snaplock/event-retention/policies/{policy.name}" '{"retention_period": "P20Y"}'
```
<br/>
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnaplockRetentionPolicy"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnaplockRetentionPolicy"], NetAppResponse]:
        r"""Creates an Event Based Retention (EBR) policy for an SVM. The input parameter retention_period expects the duration in ISO 8601 format or infinite.
### Required properties
* `name` - Event retention policy name.
* `retention_period` - Retention period of the EBR policy.
### Related ONTAP commands
* `snaplock event-retention policy create`
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
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
        records: Iterable["SnaplockRetentionPolicy"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the specified Event Based Retention (EBR) policy.
### Related ONTAP commands
* `snaplock event-retention policy delete`
### Example
Delete the specified Event Based Retention policy "policy_name":
<br/>
```
DELETE "/api/storage/snaplock/event-retention/policies/{policy.name}"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves all event retention policies for an SVM.
### Related ONTAP commands
* `snaplock event-retention policy show`
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a list of attributes of the specified Event Based Retention (EBR) policy.
### Related ONTAP commands
* `snaplock event-retention policy show`
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
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
        r"""Creates an Event Based Retention (EBR) policy for an SVM. The input parameter retention_period expects the duration in ISO 8601 format or infinite.
### Required properties
* `name` - Event retention policy name.
* `retention_period` - Retention period of the EBR policy.
### Related ONTAP commands
* `snaplock event-retention policy create`
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
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
        r"""Updates the retention period of an Event Based Retention (EBR) policy.
### Related ONTAP commands
* `snaplock event-retention policy modify`
### Example
Updates the retention period of an EBR policy "policy_name":
<br/>
```
PATCH "/api/storage/snaplock/event-retention/policies/{policy.name}" '{"retention_period": "P20Y"}'
```
<br/>
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
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
        r"""Deletes the specified Event Based Retention (EBR) policy.
### Related ONTAP commands
* `snaplock event-retention policy delete`
### Example
Delete the specified Event Based Retention policy "policy_name":
<br/>
```
DELETE "/api/storage/snaplock/event-retention/policies/{policy.name}"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/event-retention/policies`](#docs-snaplock-storage_snaplock_event-retention_policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


