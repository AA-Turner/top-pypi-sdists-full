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


__all__ = ["VscanEvent", "VscanEventSchema"]
__pdoc__ = {
    "VscanEventSchema.resource": False,
    "VscanEventSchema.opts": False,
}


class VscanEventSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanEvent object"""

    disconnect_reason = marshmallow_fields.Str(
        data_key="disconnect_reason",
        validate=enum_validation(['na', 'vscan_disabled', 'no_data_lif', 'session_uninitialized', 'remote_closed', 'invalid_protocol_msg', 'invalid_session_id', 'inactive_connection', 'invalid_user', 'server_removed']),
        allow_none=True,
    )
    r""" Specifies the reason of the Vscan server disconnection.
The available values are:

* na                        Not applicable
* vscan_disabled            Vscan disabled on the SVM
* no_data_lif               SVM does not have data lif on the node
* session_uninitialized     Session not initialized
* remote_closed             Closure from Server
* invalid_protocol_msg      Invalid protocol-message received
* invalid_session_id        Invalid session-id received
* inactive_connection       No activity on connection
* invalid_user              Connection request by invalid user
* server_removed            Server removed from the active scanner-pool


Valid choices:

* na
* vscan_disabled
* no_data_lif
* session_uninitialized
* remote_closed
* invalid_protocol_msg
* invalid_session_id
* inactive_connection
* invalid_user
* server_removed"""

    event_time = ImpreciseDateTime(
        data_key="event_time",
        allow_none=True,
    )
    r""" Specifies the Timestamp of the event.

Example: 2021-11-25T04:29:41.606+0000"""

    file_path = marshmallow_fields.Str(
        data_key="file_path",
        allow_none=True,
    )
    r""" Specifies the file for which event happened.

Example: /1"""

    interface = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", data_key="interface", unknown=EXCLUDE, allow_none=True)
    r""" The interface field of the vscan_event."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the vscan_event."""

    server = marshmallow_fields.Str(
        data_key="server",
        allow_none=True,
    )
    r""" Specifies the IP address of the Vscan server.

Example: 192.168.1.1"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the vscan_event."""

    type = marshmallow_fields.Str(
        data_key="type",
        validate=enum_validation(['scanner_connected', 'scanner_disconnected', 'scanner_updated', 'scan_internal_error', 'scan_failed', 'scan_timedout', 'file_infected', 'file_renamed', 'file_quarantined', 'file_deleted', 'scanner_busy']),
        allow_none=True,
    )
    r""" Specifies the event type.

Valid choices:

* scanner_connected
* scanner_disconnected
* scanner_updated
* scan_internal_error
* scan_failed
* scan_timedout
* file_infected
* file_renamed
* file_quarantined
* file_deleted
* scanner_busy"""

    vendor = marshmallow_fields.Str(
        data_key="vendor",
        allow_none=True,
    )
    r""" Specifies the scan-engine vendor.

Example: mighty master anti-evil scanner"""

    version = marshmallow_fields.Str(
        data_key="version",
        allow_none=True,
    )
    r""" Specifies the scan-engine version.

Example: 1.0"""

    @property
    def resource(self):
        return VscanEvent

    gettable_fields = [
        "disconnect_reason",
        "event_time",
        "file_path",
        "interface.links",
        "interface.ip",
        "interface.name",
        "interface.uuid",
        "node.links",
        "node.name",
        "node.uuid",
        "server",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "vendor",
        "version",
    ]
    """disconnect_reason,event_time,file_path,interface.links,interface.ip,interface.name,interface.uuid,node.links,node.name,node.uuid,server,svm.links,svm.name,svm.uuid,type,vendor,version,"""

    patchable_fields = [
        "event_time",
        "file_path",
        "interface.name",
        "interface.uuid",
        "server",
        "type",
        "vendor",
        "version",
    ]
    """event_time,file_path,interface.name,interface.uuid,server,type,vendor,version,"""

    postable_fields = [
        "event_time",
        "file_path",
        "interface.name",
        "interface.uuid",
        "server",
        "type",
        "vendor",
        "version",
    ]
    """event_time,file_path,interface.name,interface.uuid,server,type,vendor,version,"""

class VscanEvent(Resource):
    """Allows interaction with VscanEvent objects on the host"""

    _schema = VscanEventSchema
    _path = "/api/protocols/vscan/{svm[uuid]}/events"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves Vscan events, which are generated by the cluster to capture important events.
### Related ONTAP commands
* `vserver vscan show-events`
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
        """Returns a count of all VscanEvent resources that match the provided query"""
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
        """Returns a list of RawResources that represent VscanEvent resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves Vscan events, which are generated by the cluster to capture important events.
### Related ONTAP commands
* `vserver vscan show-events`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






