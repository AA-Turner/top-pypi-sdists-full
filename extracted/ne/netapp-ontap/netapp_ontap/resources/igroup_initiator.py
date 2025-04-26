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


__all__ = ["IgroupInitiator", "IgroupInitiatorSchema"]
__pdoc__ = {
    "IgroupInitiatorSchema.resource": False,
    "IgroupInitiatorSchema.opts": False,
}


class IgroupInitiatorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiator object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the igroup_initiator."""

    comment = marshmallow_fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=254),
        allow_none=True,
    )
    r""" A comment available for use by the administrator. Valid in POST and PATCH."""

    connectivity_tracking = marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_connectivity_tracking.IgroupInitiatorConnectivityTrackingSchema", data_key="connectivity_tracking", unknown=EXCLUDE, allow_none=True)
    r""" Overview of the initiator's connections to ONTAP."""

    igroup = marshmallow_fields.Nested("netapp_ontap.resources.igroup.IgroupSchema", data_key="igroup", unknown=EXCLUDE, allow_none=True)
    r""" The igroup field of the igroup_initiator."""

    name = marshmallow_fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=96),
        allow_none=True,
    )
    r""" The FC WWPN, iSCSI IQN, or iSCSI EUI that identifies the host initiator. Valid in POST only and not allowed when the `records` property is used.<br/>
An FC WWPN consists of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters.


Example: iqn.1998-01.com.corp.iscsi:name1"""

    proximity = marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_proximity.IgroupInitiatorProximitySchema", data_key="proximity", unknown=EXCLUDE, allow_none=True)
    r""" Properties that define to what SVMs the initiator is proximal. This information is used to properly report active optimized and active non-optimized network paths via ALUA. If no configuration has been specified for an initiator, the sub-object will not be present in GET.<br/>
These properties can be set via initiator group POST and PATCH and apply to all instances of the initiator in all initiator groups in the SVM and its peers. The `proximity` sub-object for an initiator is set in POST and PATCH in its entirety and replaces any previously set proximity for the initiator within the SVM for the initiator within the SVM. The `local_svm` property must always be set to `true` or `false` when setting the `proximity` property. To clear any previously set proximity, POST or PATCH the `proximity` object to `null`."""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_no_records.IgroupInitiatorNoRecordsSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of initiators specified to add multiple initiators to an initiator group in a single API call. Not allowed when the `name` property is used."""

    @property
    def resource(self):
        return IgroupInitiator

    gettable_fields = [
        "links",
        "comment",
        "connectivity_tracking",
        "igroup.links",
        "igroup.name",
        "igroup.uuid",
        "name",
        "proximity",
    ]
    """links,comment,connectivity_tracking,igroup.links,igroup.name,igroup.uuid,name,proximity,"""

    patchable_fields = [
        "comment",
        "igroup.name",
        "igroup.uuid",
        "proximity",
        "records",
    ]
    """comment,igroup.name,igroup.uuid,proximity,records,"""

    postable_fields = [
        "comment",
        "igroup.name",
        "igroup.uuid",
        "name",
        "proximity",
        "records",
    ]
    """comment,igroup.name,igroup.uuid,name,proximity,records,"""

class IgroupInitiator(Resource):
    """Allows interaction with IgroupInitiator objects on the host"""

    _schema = IgroupInitiatorSchema
    _path = "/api/protocols/san/igroups/{igroup[uuid]}/initiators"
    _keys = ["igroup.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves initiators of an initiator group.<br/>
This API only reports initiators owned directly by the initiator group. Initiators of nested initiator groups are not included in this collection.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity_tracking.*`
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
        """Returns a count of all IgroupInitiator resources that match the provided query"""
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
        """Returns a list of RawResources that represent IgroupInitiator resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        records: Iterable["IgroupInitiator"] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an initiator of an initiator group.<br/>
This API only supports modification of initiators owned directly by the initiator group. Initiators of nested initiator groups must be modified on the initiator group that directly owns the initiator.
### Related ONTAP commands
* `lun igroup initiator modify`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._patch_collection(
            body, *args, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def post_collection(
        cls,
        records: Iterable["IgroupInitiator"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["IgroupInitiator"], NetAppResponse]:
        r"""Adds one or more initiators to an initiator group.<br/>
This API does not support adding initiators to an initiator group that already contains nested initiator groups.
### Required properties
* `name` or `records.name` - Initiator name(s) to add to the initiator group.
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
        records: Iterable["IgroupInitiator"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an initiator from an initiator group.<br/>
This API only supports removal of initiators owned directly by the initiator group. Initiators of nested initiator groups must be removed on the initiator group that directly owns the initiator.
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
        r"""Retrieves initiators of an initiator group.<br/>
This API only reports initiators owned directly by the initiator group. Initiators of nested initiator groups are not included in this collection.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity_tracking.*`
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an initiator of an initiator group.<br/>
This API only reports initiators owned directly by the initiator group. Initiators of nested initiator groups are not part of this collection.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `connectivity_tracking.*`
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
        r"""Adds one or more initiators to an initiator group.<br/>
This API does not support adding initiators to an initiator group that already contains nested initiator groups.
### Required properties
* `name` or `records.name` - Initiator name(s) to add to the initiator group.
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

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an initiator of an initiator group.<br/>
This API only supports modification of initiators owned directly by the initiator group. Initiators of nested initiator groups must be modified on the initiator group that directly owns the initiator.
### Related ONTAP commands
* `lun igroup initiator modify`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Deletes an initiator from an initiator group.<br/>
This API only supports removal of initiators owned directly by the initiator group. Initiators of nested initiator groups must be removed on the initiator group that directly owns the initiator.
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


