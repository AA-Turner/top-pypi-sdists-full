r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
This API returns the percentage of data classified as encrypted using an entropy
algorithm, measured at various time intervals at the storage unit level. If no storage unit UUID
is specified, entropy statistics for all storage units are be returned.
The entropy_stats_type parameter can be used to retrieve statistics with sub_hourly,
hourly, or daily granularity. Additionally, it can be used to identify intervals that
exhibited high (high_enc_pct) percentages of encrypted data. If no type is specified,
all types of entropy statistics are returned for the storage units.
## Examples
### Retrieving storage units stats
In this example, the API returns the data-entropy statistics for the
storage units.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitAntiRansomwareEntropyStats

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageUnitAntiRansomwareEntropyStats.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StorageUnitAntiRansomwareEntropyStats(
        {
            "timestamp": "2024-12-13T03:36:24-05:00",
            "entropy_stats_type": "sub_hourly",
            "encryption_percentage": 51,
            "data_written_in_bytes": 13249687,
            "storage_unit": {
                "uuid": "61edb8bb-b7d1-11ef-932d-005056bbaeff",
                "name": "lun1",
            },
            "duration": "PT10M21S",
            "_links": {
                "self": {
                    "href": "/api/security/anti-ransomware/storage-unit/entropy-stats/61edb8bb-b7d1-11ef-932d-005056bbaeff/sub_hourly/2024-12-13T03%3A36%3A24-05%3A00"
                }
            },
        }
    ),
    StorageUnitAntiRansomwareEntropyStats(
        {
            "timestamp": "2024-12-13T04:16:06-05:00",
            "entropy_stats_type": "hourly",
            "encryption_percentage": 51,
            "data_written_in_bytes": 13249687,
            "storage_unit": {
                "uuid": "61edb8bb-b7d1-11ef-932d-005056bbaeff",
                "name": "lun2",
            },
            "duration": "PT10M21S",
            "_links": {
                "self": {
                    "href": "/api/security/anti-ransomware/storage-unit/entropy-stats/61edb8bb-b7d1-11ef-932d-005056bbaeff/hourly/2024-12-13T04%3A16%3A06-05%3A00"
                }
            },
        }
    ),
]

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


__all__ = ["StorageUnitAntiRansomwareEntropyStats", "StorageUnitAntiRansomwareEntropyStatsSchema"]
__pdoc__ = {
    "StorageUnitAntiRansomwareEntropyStatsSchema.resource": False,
    "StorageUnitAntiRansomwareEntropyStatsSchema.opts": False,
}


class StorageUnitAntiRansomwareEntropyStatsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitAntiRansomwareEntropyStats object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the storage_unit_anti_ransomware_entropy_stats."""

    data_written_in_bytes = Size(
        data_key="data_written_in_bytes",
        allow_none=True,
    )
    r""" The amount of data written."""

    duration = marshmallow_fields.Str(
        data_key="duration",
        allow_none=True,
    )
    r""" The duration of the interval associated with this statistic. The duration is represented in ISO-8601 standard format.

Example: PT15M"""

    encryption_percentage = Size(
        data_key="encryption_percentage",
        allow_none=True,
    )
    r""" The percentage of data that is encrypted."""

    entropy_stats_type = marshmallow_fields.Str(
        data_key="entropy_stats_type",
        validate=enum_validation(['sub_hourly', 'hourly', 'daily', 'high_enc_pct']),
        allow_none=True,
    )
    r""" Storage unit metrics are retrieved based on this statistic type.

Valid choices:

* sub_hourly
* hourly
* daily
* high_enc_pct"""

    storage_unit = marshmallow_fields.Nested("netapp_ontap.resources.storage_unit.StorageUnitSchema", data_key="storage_unit", unknown=EXCLUDE, allow_none=True)
    r""" The storage_unit field of the storage_unit_anti_ransomware_entropy_stats."""

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
        allow_none=True,
    )
    r""" Start time in date-time format."""

    @property
    def resource(self):
        return StorageUnitAntiRansomwareEntropyStats

    gettable_fields = [
        "links",
        "data_written_in_bytes",
        "duration",
        "encryption_percentage",
        "entropy_stats_type",
        "storage_unit.links",
        "storage_unit.name",
        "storage_unit.uuid",
        "timestamp",
    ]
    """links,data_written_in_bytes,duration,encryption_percentage,entropy_stats_type,storage_unit.links,storage_unit.name,storage_unit.uuid,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class StorageUnitAntiRansomwareEntropyStats(Resource):
    r""" Storage unit data-entropy statistics derived from block analysis. """

    _schema = StorageUnitAntiRansomwareEntropyStatsSchema
    _path = "/api/security/anti-ransomware/storage-unit/entropy-stats"
    _keys = ["storage_unit.uuid", "entropy_stats_type", "timestamp"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the data-entropy statistics for the storage units.
### Learn more
* [`DOC /security/anti-ransomware/storage-unit/entropy-stats`](#docs-security-security_anti-ransomware_storage-unit_entropy-stats)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all StorageUnitAntiRansomwareEntropyStats resources that match the provided query"""
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
        """Returns a list of RawResources that represent StorageUnitAntiRansomwareEntropyStats resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the data-entropy statistics for the storage units.
### Learn more
* [`DOC /security/anti-ransomware/storage-unit/entropy-stats`](#docs-security-security_anti-ransomware_storage-unit_entropy-stats)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a data-entropy statistic for the storage unit.
### Learn more
* [`DOC /security/anti-ransomware/storage-unit/entropy-stats`](#docs-security-security_anti-ransomware_storage-unit_entropy-stats)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





