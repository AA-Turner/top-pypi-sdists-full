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


__all__ = ["PortsetInterface", "PortsetInterfaceSchema"]
__pdoc__ = {
    "PortsetInterfaceSchema.resource": False,
    "PortsetInterfaceSchema.opts": False,
}


class PortsetInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PortsetInterface object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the portset_interface."""

    fc = marshmallow_fields.Nested("netapp_ontap.resources.fc_interface.FcInterfaceSchema", data_key="fc", unknown=EXCLUDE, allow_none=True)
    r""" The fc field of the portset_interface."""

    ip = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", data_key="ip", unknown=EXCLUDE, allow_none=True)
    r""" The ip field of the portset_interface."""

    portset = marshmallow_fields.Nested("netapp_ontap.models.portset_interface_portset.PortsetInterfacePortsetSchema", data_key="portset", unknown=EXCLUDE, allow_none=True)
    r""" The portset in which the network interface is found.<br/>
Note that this does not mean that the network interface cannot also be found in other portsets."""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.portset_interfaces.PortsetInterfacesSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of network interfaces specified to add multiple interfaces to a portset in a single API call. Valid in POST only and not allowed when the `fc` or `ip` property is used."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The unique identifier of the network interface.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412"""

    @property
    def resource(self):
        return PortsetInterface

    gettable_fields = [
        "links",
        "fc.links",
        "fc.name",
        "fc.uuid",
        "fc.wwpn",
        "ip.links",
        "ip.ip",
        "ip.name",
        "ip.uuid",
        "portset",
        "uuid",
    ]
    """links,fc.links,fc.name,fc.uuid,fc.wwpn,ip.links,ip.ip,ip.name,ip.uuid,portset,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "fc.name",
        "fc.uuid",
        "ip.name",
        "ip.uuid",
        "records",
    ]
    """fc.name,fc.uuid,ip.name,ip.uuid,records,"""

class PortsetInterface(Resource):
    """Allows interaction with PortsetInterface objects on the host"""

    _schema = PortsetInterfaceSchema
    _path = "/api/protocols/san/portsets/{portset[uuid]}/interfaces"
    _keys = ["portset.uuid", "uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves interfaces of a portset.
### Related ONTAP commands
* `lun portset show`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        """Returns a count of all PortsetInterface resources that match the provided query"""
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
        """Returns a list of RawResources that represent PortsetInterface resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["PortsetInterface"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["PortsetInterface"], NetAppResponse]:
        r"""Adds one or more interfaces to a portset.
### Required properties
* `fc`, `ip` or `records` - Network interface(s) to add to the portset.
### Related ONTAP commands
* `lun portset add`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        records: Iterable["PortsetInterface"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a network interface from a portset.
### Related ONTAP commands
* `lun portset remove`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves interfaces of a portset.
### Related ONTAP commands
* `lun portset show`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a network interface of a portset.
### Related ONTAP commands
* `lun portset show`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        r"""Adds one or more interfaces to a portset.
### Required properties
* `fc`, `ip` or `records` - Network interface(s) to add to the portset.
### Related ONTAP commands
* `lun portset add`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
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
        r"""Deletes a network interface from a portset.
### Related ONTAP commands
* `lun portset remove`
### Learn more
* [`DOC /protocols/san/portsets`](#docs-SAN-protocols_san_portsets)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


