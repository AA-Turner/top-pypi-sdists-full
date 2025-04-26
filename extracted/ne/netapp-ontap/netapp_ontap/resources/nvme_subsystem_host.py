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


__all__ = ["NvmeSubsystemHost", "NvmeSubsystemHostSchema"]
__pdoc__ = {
    "NvmeSubsystemHostSchema.resource": False,
    "NvmeSubsystemHostSchema.opts": False,
}


class NvmeSubsystemHostSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NvmeSubsystemHost object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the nvme_subsystem_host."""

    dh_hmac_chap = marshmallow_fields.Nested("netapp_ontap.models.nvme_dh_hmac_chap_authentication.NvmeDhHmacChapAuthenticationSchema", data_key="dh_hmac_chap", unknown=EXCLUDE, allow_none=True)
    r""" A container for the configuration of NVMe in-band authentication using the DH-HMAC-CHAP protocol for a host."""

    io_queue = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_host_io_queue.NvmeSubsystemHostIoQueueSchema", data_key="io_queue", unknown=EXCLUDE, allow_none=True)
    r""" The properties of the submission queue used to submit I/O commands for execution by the NVMe controller."""

    nqn = marshmallow_fields.Str(
        data_key="nqn",
        allow_none=True,
    )
    r""" The NVMe qualified name (NQN) used to identify the NVMe storage target.


Example: nqn.1992-01.example.com:string"""

    priority = marshmallow_fields.Str(
        data_key="priority",
        validate=enum_validation(['regular', 'high']),
        allow_none=True,
    )
    r""" The host priority setting allocates appropriate NVMe I/O queues (count and depth) for the host to submit I/O commands. Absence of this property in GET implies io_queue count and I/O queue depth are being used.


Valid choices:

* regular
* high"""

    records = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_host_no_records.NvmeSubsystemHostNoRecordsSchema", unknown=EXCLUDE, allow_none=True), data_key="records", allow_none=True)
    r""" An array of NVMe hosts specified to add multiple NVMe hosts to an NVMe subsystem in a single API call. Valid in POST only."""

    subsystem = marshmallow_fields.Nested("netapp_ontap.models.nvme_subsystem_host_records_subsystem.NvmeSubsystemHostRecordsSubsystemSchema", data_key="subsystem", unknown=EXCLUDE, allow_none=True)
    r""" The NVMe subsystem to which the NVMe host has been provisioned."""

    tls = marshmallow_fields.Nested("netapp_ontap.models.nvme_tcp_tls.NvmeTcpTlsSchema", data_key="tls", unknown=EXCLUDE, allow_none=True)
    r""" A container for the configuration for NVMe/TCP-TLS transport session for the host."""

    @property
    def resource(self):
        return NvmeSubsystemHost

    gettable_fields = [
        "links",
        "dh_hmac_chap",
        "io_queue",
        "nqn",
        "priority",
        "subsystem",
        "tls",
    ]
    """links,dh_hmac_chap,io_queue,nqn,priority,subsystem,tls,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "dh_hmac_chap",
        "nqn",
        "priority",
        "records",
        "tls",
    ]
    """dh_hmac_chap,nqn,priority,records,tls,"""

class NvmeSubsystemHost(Resource):
    r""" The NVMe host provisioned to access NVMe namespaces mapped to a subsystem. """

    _schema = NvmeSubsystemHostSchema
    _path = "/api/protocols/nvme/subsystems/{subsystem[uuid]}/hosts"
    _keys = ["subsystem.uuid", "nqn"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the NVMe subsystem hosts of an NVMe subsystem.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `subsystem_maps.*`
### Related ONTAP commands
* `vserver nvme subsystem map show`
* `vserver nvme subsystem show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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
        """Returns a count of all NvmeSubsystemHost resources that match the provided query"""
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
        """Returns a list of RawResources that represent NvmeSubsystemHost resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)


    @classmethod
    def post_collection(
        cls,
        records: Iterable["NvmeSubsystemHost"],
        *args,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> Union[List["NvmeSubsystemHost"], NetAppResponse]:
        r"""Adds NVMe subsystem host(s) to an NVMe subsystem.
### Required properties
* `nqn` or `records.nqn` - NVMe host(s) NQN(s) to add to the NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host add`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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
        records: Iterable["NvmeSubsystemHost"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an NVMe subsystem host from an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host remove`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the NVMe subsystem hosts of an NVMe subsystem.
### Expensive properties
There is an added computational cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `subsystem_maps.*`
### Related ONTAP commands
* `vserver nvme subsystem map show`
* `vserver nvme subsystem show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an NVMe subsystem host of an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host show`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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
        r"""Adds NVMe subsystem host(s) to an NVMe subsystem.
### Required properties
* `nqn` or `records.nqn` - NVMe host(s) NQN(s) to add to the NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host add`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
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
        r"""Deletes an NVMe subsystem host from an NVMe subsystem.
### Related ONTAP commands
* `vserver nvme subsystem host remove`
### Learn more
* [`DOC /protocols/nvme/subsystems`](#docs-NVMe-protocols_nvme_subsystems)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


