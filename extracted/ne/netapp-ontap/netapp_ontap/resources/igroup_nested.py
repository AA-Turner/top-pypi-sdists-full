r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

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


__all__ = ["IgroupNested", "IgroupNestedSchema"]
__pdoc__ = {
    "IgroupNestedSchema.resource": False,
    "IgroupNestedSchema.opts": False,
}


class IgroupNestedSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupNested object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the igroup_nested."""

    igroup = marshmallow_fields.Nested("netapp_ontap.models.igroup_nested_igroup.IgroupNestedIgroupSchema", data_key="igroup", unknown=EXCLUDE, allow_none=True)
    r""" The igroup field of the igroup_nested."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=96),
        allow_none=True,
    )
    r""" The name of the initiator group.


Example: igroup1"""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.fc_login_igroups.FcLoginIgroupsSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of initiator groups specified to add multiple nested initiator groups to an initiator group in a single API call. Not allowed when the `name` property is used."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return IgroupNested

    gettable_fields = [
        "links",
        "igroup",
        "name",
        "uuid",
    ]
    """links,igroup,name,uuid,"""

    patchable_fields = [
        "igroup",
        "name",
        "records",
        "uuid",
    ]
    """igroup,name,records,uuid,"""

    postable_fields = [
        "igroup",
        "name",
        "records",
        "uuid",
    ]
    """igroup,name,records,uuid,"""

class IgroupNested(Resource):
    """Allows interaction with IgroupNested objects on the host"""

    _schema = IgroupNestedSchema
    _path = "/api/protocols/san/igroups/{igroup[uuid]}/igroups"
    _keys = ["igroup.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves nested initiator groups of an initiator group.<br/>
This API only reports the nested initiator groups that are direct children of the initiator group. Further nested initiator groups are reported by their direct parent initiator group.
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        """Returns a count of all IgroupNested resources that match the provided query"""
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
        """Returns a list of RawResources that represent IgroupNested resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["IgroupNested"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IgroupNested"], NetAppResponse]:
        r"""Adds one or more nested initiator groups to an initiator group. A single nested initiator group can be added by directly specifying the name or UUID. Multiple nested initiator groups can be added by specifying the names or UUIDs in the records array. Nested initiator groups cannot be added to an initiator group that already directly contains initiators.
### Required properties
* `name` and/or `uuid` or `records` - Nested initiator groups to add to the initiator group.
### Related ONTAP commands
* `lun igroup add`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        records: Iterable["IgroupNested"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Removes a nested initiator group from an initiator group. This API does not delete the nested initiator group itself. It removes the relationship between a parent and child initiator group.<br/>
This API only supports removal of initiator groups owned directly by the initiator group. Further nested initiator groups must be removed from the direct parent initiator group.
### Related ONTAP commands
* `lun igroup remove`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves nested initiator groups of an initiator group.<br/>
This API only reports the nested initiator groups that are direct children of the initiator group. Further nested initiator groups are reported by their direct parent initiator group.
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a nested initiator group of an initiator group.<br/>
This API only reports the nested initiator groups that are direct children of the initiator group. Further nested initiator groups are reported by their direct parent initiator group.
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Adds one or more nested initiator groups to an initiator group. A single nested initiator group can be added by directly specifying the name or UUID. Multiple nested initiator groups can be added by specifying the names or UUIDs in the records array. Nested initiator groups cannot be added to an initiator group that already directly contains initiators.
### Required properties
* `name` and/or `uuid` or `records` - Nested initiator groups to add to the initiator group.
### Related ONTAP commands
* `lun igroup add`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Removes a nested initiator group from an initiator group. This API does not delete the nested initiator group itself. It removes the relationship between a parent and child initiator group.<br/>
This API only supports removal of initiator groups owned directly by the initiator group. Further nested initiator groups must be removed from the direct parent initiator group.
### Related ONTAP commands
* `lun igroup remove`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


