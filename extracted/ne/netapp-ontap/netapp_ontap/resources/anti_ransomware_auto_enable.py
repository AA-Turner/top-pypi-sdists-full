r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API provides details about the anti-ransomware auto enablement status including information about warm-up periods and auto settings.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AntiRansomwareAutoEnable

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AntiRansomwareAutoEnable()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AntiRansomwareAutoEnable(
    {
        "_links": {"self": {"href": "/security/anti-ransomware/auto-enable"}},
        "warm_up_period_completed": False,
        "new_volume_auto_enable": True,
        "warm_up_period_applicable": True,
    }
)

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
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema
from netapp_ontap.raw_resource import RawResource

from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["AntiRansomwareAutoEnable", "AntiRansomwareAutoEnableSchema"]
__pdoc__ = {
    "AntiRansomwareAutoEnableSchema.resource": False,
    "AntiRansomwareAutoEnableSchema.opts": False,
}

class AntiRansomwareAutoEnableSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AntiRansomwareAutoEnable object"""

    links = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.self_link", "SelfLinkSchema"),
                data_key="_links",
                unknown=EXCLUDE,
                allow_none=True
            )
    r""" The links field of the anti_ransomware_auto_enable."""

    new_volume_auto_enable = marshmallow_fields.Boolean(
        data_key="new_volume_auto_enable",
        allow_none=True,
    )
    r""" Auto Anti-Ransomware Protection (ARP) setting for new volumes."""

    warm_up_period_applicable = marshmallow_fields.Boolean(
        data_key="warm_up_period_applicable",
        allow_none=True,
    )
    r""" Indicates if the warm-up period is applicable."""

    warm_up_period_completed = marshmallow_fields.Boolean(
        data_key="warm_up_period_completed",
        allow_none=True,
    )
    r""" Indicates if warm-up period has completed."""

    warm_up_period_remaining_duration = marshmallow_fields.Str(
        data_key="warm_up_period_remaining_duration",
        allow_none=True,
    )
    r""" Time remaining for warm-up period completion."""

    warm_up_period_total_duration = marshmallow_fields.Str(
        data_key="warm_up_period_total_duration",
        allow_none=True,
    )
    r""" Duration of warm-up period."""

    @property
    def resource(self):
        return AntiRansomwareAutoEnable

    gettable_fields = [
        "links",
        "new_volume_auto_enable",
        "warm_up_period_applicable",
        "warm_up_period_completed",
        "warm_up_period_remaining_duration",
        "warm_up_period_total_duration",
    ]
    """links,new_volume_auto_enable,warm_up_period_applicable,warm_up_period_completed,warm_up_period_remaining_duration,warm_up_period_total_duration,"""

    patchable_fields = [
        "new_volume_auto_enable",
        "warm_up_period_total_duration",
    ]
    """new_volume_auto_enable,warm_up_period_total_duration,"""

    postable_fields = [
    ]
    """"""

class AntiRansomwareAutoEnable(Resource):
    """Allows interaction with AntiRansomwareAutoEnable objects on the host"""

    _schema = AntiRansomwareAutoEnableSchema
    _path = "/api/security/anti-ransomware/auto-enable"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the current anti-ransomware auto enablement values, including details about warm-up period and auto enablement setting for new and existing volumes.

### Learn more
* [`DOC /security/anti-ransomware/auto-enable`](#docs-security-security_anti-ransomware_auto-enable)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""API to modify the anti-ransomware auto enablement setting.

### Learn more
* [`DOC /security/anti-ransomware/auto-enable`](#docs-security-security_anti-ransomware_auto-enable)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)



