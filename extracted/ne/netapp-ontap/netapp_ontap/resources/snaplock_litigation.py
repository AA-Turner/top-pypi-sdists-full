r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

Use this API to retain Compliance-mode WORM files for the duration of a litigation. A file under a legal-hold behaves as a WORM file with an indefinite retention period. Litigation ID is a combination of volume UUID and litigation name in the format `<volume UUID>:<litigation name>`. Only a user with the security login role vsadmin-snaplock can perform the operation."""

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


__all__ = ["SnaplockLitigation", "SnaplockLitigationSchema"]
__pdoc__ = {
    "SnaplockLitigationSchema.resource": False,
    "SnaplockLitigationSchema.opts": False,
}


class SnaplockLitigationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnaplockLitigation object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the snaplock_litigation."""

    id = marshmallow_fields.Str(
        data_key="id",
        allow_none=True,
    )
    r""" Specifies the litigation ID."""

    name = marshmallow_fields.Str(
        data_key="name",
        allow_none=True,
    )
    r""" Specifies the legal-hold litigation name.

Example: lit1"""

    operations = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.snaplock_legal_hold_operation.SnaplockLegalHoldOperationSchema", unknown=EXCLUDE, allow_none=True), data_key="operations", allow_none=True)
    r""" The operations field of the snaplock_litigation."""

    path = marshmallow_fields.Str(
        data_key="path",
        allow_none=True,
    )
    r""" Specifies the path on which legal-hold operation has to be applied.

Example: /dir1"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the snaplock_litigation."""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the snaplock_litigation."""

    @property
    def resource(self):
        return SnaplockLitigation

    gettable_fields = [
        "links",
        "id",
        "name",
        "operations",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,id,name,operations,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "name",
        "volume.name",
        "volume.uuid",
    ]
    """name,volume.name,volume.uuid,"""

    postable_fields = [
        "name",
        "path",
        "volume.name",
        "volume.uuid",
    ]
    """name,path,volume.name,volume.uuid,"""

class SnaplockLitigation(Resource):
    """Allows interaction with SnaplockLitigation objects on the host"""

    _schema = SnaplockLitigationSchema
    _path = "/api/storage/snaplock/litigations"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the list of litigations under an SVM.
### Related ONTAP commands
* `snaplock legal-hold show`
### Learn more
* [`DOC /storage/snaplock/litigations`](#docs-snaplock-storage_snaplock_litigations)
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
        """Returns a count of all SnaplockLitigation resources that match the provided query"""
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
        """Returns a list of RawResources that represent SnaplockLitigation resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["SnaplockLitigation"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["SnaplockLitigation"], NetAppResponse]:
        r"""Starts a  Legal-Hold.
### Required properties
* `path` - Path of the file.
* `name` - Litigation name.
* `volume.name` or `volume.uuid` - Name or UUID  of the volume.
### Related ONTAP commands
* `snaplock legal-hold begin`
### Example
<br/>
```
POST "/api/storage/snaplock/litigations" '{"volume.name":"SLC1","name":"l3","path":"/b.txt"}'
```
<br/>
### Learn more
* [`DOC /storage/snaplock/litigations`](#docs-snaplock-storage_snaplock_litigations)
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
        records: Iterable["SnaplockLitigation"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a legal-hold end on all of the files for the specified litigation ID. This is only allowed when an operation is no longer in progress.
### Related ONTAP commands
* `snaplock legal-hold end`
### Example
<br/>
```
DELETE "/api/storage/snaplock/litigations/fd72e138-4bc3-11e9-a85f-0050568eb48f%3Al3"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/litigations`](#docs-snaplock-storage_snaplock_litigations)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the list of litigations under an SVM.
### Related ONTAP commands
* `snaplock legal-hold show`
### Learn more
* [`DOC /storage/snaplock/litigations`](#docs-snaplock-storage_snaplock_litigations)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the list of ongoing operations for the specified litigation ID.
### Related ONTAP commands
* `snaplock legal-hold show`
### Learn more
* [`DOC /storage/snaplock/litigations`](#docs-snaplock-storage_snaplock_litigations)
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
        r"""Starts a  Legal-Hold.
### Required properties
* `path` - Path of the file.
* `name` - Litigation name.
* `volume.name` or `volume.uuid` - Name or UUID  of the volume.
### Related ONTAP commands
* `snaplock legal-hold begin`
### Example
<br/>
```
POST "/api/storage/snaplock/litigations" '{"volume.name":"SLC1","name":"l3","path":"/b.txt"}'
```
<br/>
### Learn more
* [`DOC /storage/snaplock/litigations`](#docs-snaplock-storage_snaplock_litigations)
"""
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
        r"""Creates a legal-hold end on all of the files for the specified litigation ID. This is only allowed when an operation is no longer in progress.
### Related ONTAP commands
* `snaplock legal-hold end`
### Example
<br/>
```
DELETE "/api/storage/snaplock/litigations/fd72e138-4bc3-11e9-a85f-0050568eb48f%3Al3"
```
<br/>
### Learn more
* [`DOC /storage/snaplock/litigations`](#docs-snaplock-storage_snaplock_litigations)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


