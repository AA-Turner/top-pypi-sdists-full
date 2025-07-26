r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

## Overview
 The suspects GET API endpoint retrieves the storage units that have a moderate or high probability of a ransomware attack.
 ## Examples
 ### Retrieving storage units that have a moderate or high probability of a ransomware attack
 In this example, the API returns the details of the storage units.
 ```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StorageUnitAntiRansomwareSuspect

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StorageUnitAntiRansomwareSuspect.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StorageUnitAntiRansomwareSuspect(
        {
            "_links": {
                "self": {
                    "href": "/api/security/anti-ransomware/storage-unit/suspects/f48bc3b3-e9e7-11ef-8d5b-005056ae4d2e"
                }
            },
            "storage_unit": {
                "uuid": "f48bc3b3-e9e7-11ef-8d5b-005056ae4d2e",
                "name": "lun_1",
            },
        }
    ),
    StorageUnitAntiRansomwareSuspect(
        {
            "_links": {
                "self": {
                    "href": "/api/security/anti-ransomware/storage-unit/suspects/f48bc74f-e9e7-11ef-8d5b-005056ae4d2e"
                }
            },
            "storage_unit": {
                "uuid": "f48bc74f-e9e7-11ef-8d5b-005056ae4d2e",
                "name": "lun_2",
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


__all__ = ["StorageUnitAntiRansomwareSuspect", "StorageUnitAntiRansomwareSuspectSchema"]
__pdoc__ = {
    "StorageUnitAntiRansomwareSuspectSchema.resource": False,
    "StorageUnitAntiRansomwareSuspectSchema.opts": False,
}


class StorageUnitAntiRansomwareSuspectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitAntiRansomwareSuspect object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the storage_unit_anti_ransomware_suspect."""

    storage_unit = marshmallow_fields.Nested("netapp_ontap.resources.storage_unit.StorageUnitSchema", data_key="storage_unit", unknown=EXCLUDE, allow_none=True)
    r""" The storage_unit field of the storage_unit_anti_ransomware_suspect."""

    @property
    def resource(self):
        return StorageUnitAntiRansomwareSuspect

    gettable_fields = [
        "links",
        "storage_unit.links",
        "storage_unit.name",
        "storage_unit.uuid",
    ]
    """links,storage_unit.links,storage_unit.name,storage_unit.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

class StorageUnitAntiRansomwareSuspect(Resource):
    r""" Storage unit details. """

    _schema = StorageUnitAntiRansomwareSuspectSchema
    _path = "/api/security/anti-ransomware/storage-unit/suspects"
    _keys = ["storage_unit.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves information about the storage units on which a ransomware attack is detected.

### Learn more
* [`DOC /security/anti-ransomware/storage-unit/suspects`](#docs-security-security_anti-ransomware_storage-unit_suspects)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        """Returns a count of all StorageUnitAntiRansomwareSuspect resources that match the provided query"""
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
        """Returns a list of RawResources that represent StorageUnitAntiRansomwareSuspect resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["StorageUnitAntiRansomwareSuspect"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Clear the ransomware attack detected on a storage unit specified by the UUID.

### Learn more
* [`DOC /security/anti-ransomware/storage-unit/suspects`](#docs-security-security_anti-ransomware_storage-unit_suspects)"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves information about the storage units on which a ransomware attack is detected.

### Learn more
* [`DOC /security/anti-ransomware/storage-unit/suspects`](#docs-security-security_anti-ransomware_storage-unit_suspects)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information about the storage unit specified by the UUID.

### Learn more
* [`DOC /security/anti-ransomware/storage-unit/suspects`](#docs-security-security_anti-ransomware_storage-unit_suspects)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)



    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Clear the ransomware attack detected on a storage unit specified by the UUID.

### Learn more
* [`DOC /security/anti-ransomware/storage-unit/suspects`](#docs-security-security_anti-ransomware_storage-unit_suspects)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


