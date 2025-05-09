r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

You can use this API to manage diagnostic information on NDMP sessions belonging to a specific SVM in the case of SVM-scope or to a specific node in the case of node-scope.
### Examples
Retrieves NDMP session details under node-scope:
<br/>
```
GET "/api/protocols/ndmp/sessions/9b372ce7-3a4b-11e9-a7f8-0050568e3d73/2000"
```
<br/>
Retrieves NDMP session details under SVM-scope:
<br/>
```
GET "/api/protocols/ndmp/sessions/13bb2092-458b-11e9-9c06-0050568ea604/2000:4000"
```
<br/>
Deletes NDMP session details under node-scope:
<br/>
```
DELETE "/api/protocols/ndmp/sessions/9b372ce7-3a4b-11e9-a7f8-0050568e3d73/2000"
```
<br/>
Deletes NDMP session details under SVM-scope:
<br/>
```
DELETE "/api/protocols/ndmp/sessions/13bb2092-458b-11e9-9c06-0050568ea604/2000:4000"
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


__all__ = ["NdmpSession", "NdmpSessionSchema"]
__pdoc__ = {
    "NdmpSessionSchema.resource": False,
    "NdmpSessionSchema.opts": False,
}


class NdmpSessionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NdmpSession object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the ndmp_session."""

    backup_engine = marshmallow_fields.Str(
        data_key="backup_engine",
        validate=enum_validation(['dump', 'smtape']),
        allow_none=True,
    )
    r""" Indicates the NDMP backup engine.

Valid choices:

* dump
* smtape"""

    client_address = marshmallow_fields.Str(
        data_key="client_address",
        allow_none=True,
    )
    r""" Indicates the NDMP client address."""

    client_port = Size(
        data_key="client_port",
        allow_none=True,
    )
    r""" Indicates the NDMP client port."""

    data = marshmallow_fields.Nested("netapp_ontap.models.ndmp_data.NdmpDataSchema", data_key="data", unknown=EXCLUDE, allow_none=True)
    r""" Information about the NDMP data server."""

    data_path = marshmallow_fields.Str(
        data_key="data_path",
        allow_none=True,
    )
    r""" Indicates the NDMP backup or restore path.

Example: /vserver1/vol1"""

    id = marshmallow_fields.Str(
        data_key="id",
        allow_none=True,
    )
    r""" NDMP session identifier."""

    mover = marshmallow_fields.Nested("netapp_ontap.models.ndmp_mover.NdmpMoverSchema", data_key="mover", unknown=EXCLUDE, allow_none=True)
    r""" Information about the NDMP mover."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the ndmp_session."""

    scsi = marshmallow_fields.Nested("netapp_ontap.models.ndmp_scsi.NdmpScsiSchema", data_key="scsi", unknown=EXCLUDE, allow_none=True)
    r""" Information about the NDMP SCSI server."""

    source_address = marshmallow_fields.Str(
        data_key="source_address",
        allow_none=True,
    )
    r""" Indicates the NDMP local address on which connection was established."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the ndmp_session."""

    tape_device = marshmallow_fields.Str(
        data_key="tape_device",
        allow_none=True,
    )
    r""" Indicates the NDMP tape device.

Example: nrst0a"""

    tape_mode = marshmallow_fields.Str(
        data_key="tape_mode",
        allow_none=True,
    )
    r""" Indicates the NDMP tape device mode of operation."""

    uuid = marshmallow_fields.Str(
        data_key="uuid",
        allow_none=True,
    )
    r""" The NDMP node or SVM UUID based on whether NDMP is operating in node-scope or SVM-scope mode."""

    @property
    def resource(self):
        return NdmpSession

    gettable_fields = [
        "links",
        "backup_engine",
        "client_address",
        "client_port",
        "data",
        "data_path",
        "id",
        "mover",
        "node.links",
        "node.name",
        "node.uuid",
        "scsi",
        "source_address",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tape_device",
        "tape_mode",
        "uuid",
    ]
    """links,backup_engine,client_address,client_port,data,data_path,id,mover,node.links,node.name,node.uuid,scsi,source_address,svm.links,svm.name,svm.uuid,tape_device,tape_mode,uuid,"""

    patchable_fields = [
        "backup_engine",
        "client_address",
        "client_port",
        "data",
        "data_path",
        "id",
        "mover",
        "node.name",
        "node.uuid",
        "scsi",
        "source_address",
        "svm.name",
        "svm.uuid",
        "tape_device",
        "tape_mode",
        "uuid",
    ]
    """backup_engine,client_address,client_port,data,data_path,id,mover,node.name,node.uuid,scsi,source_address,svm.name,svm.uuid,tape_device,tape_mode,uuid,"""

    postable_fields = [
        "backup_engine",
        "client_address",
        "client_port",
        "data",
        "data_path",
        "id",
        "mover",
        "node.name",
        "node.uuid",
        "scsi",
        "source_address",
        "svm.name",
        "svm.uuid",
        "tape_device",
        "tape_mode",
        "uuid",
    ]
    """backup_engine,client_address,client_port,data,data_path,id,mover,node.name,node.uuid,scsi,source_address,svm.name,svm.uuid,tape_device,tape_mode,uuid,"""

class NdmpSession(Resource):
    """Allows interaction with NdmpSession objects on the host"""

    _schema = NdmpSessionSchema
    _path = "/api/protocols/ndmp/sessions"
    _keys = ["owner.uuid", "session.id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of NDMP sessions. In the case of SVM-scope, if this API is executed on a data IP, it displays the list of NDMP sessions under the specified SVM; otherwise it displays the list of NDMP sessions for all the SVMs under the cluster. In the case of node-scope, it displays the list of NDMP sessions for all nodes.
### Related ONTAP commands
* `vserver services ndmp probe`
* `system services ndmp probe`
### Learn more
* [`DOC /protocols/ndmp/sessions`](#docs-ndmp-protocols_ndmp_sessions)
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
        """Returns a count of all NdmpSession resources that match the provided query"""
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
        """Returns a list of RawResources that represent NdmpSession resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)



    @classmethod
    def delete_collection(
        cls,
        *args,
        records: Iterable["NdmpSession"] = None,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a specific NDMP session.
### Related ONTAP commands
* `vserver services ndmp kill`
* `system services ndmp kill`
### Learn more
* [`DOC /protocols/ndmp/sessions`](#docs-ndmp-protocols_ndmp_sessions)
"""
        return super()._delete_collection(
            *args, body=body, records=records, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, connection=connection, **kwargs
        )

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of NDMP sessions. In the case of SVM-scope, if this API is executed on a data IP, it displays the list of NDMP sessions under the specified SVM; otherwise it displays the list of NDMP sessions for all the SVMs under the cluster. In the case of node-scope, it displays the list of NDMP sessions for all nodes.
### Related ONTAP commands
* `vserver services ndmp probe`
* `system services ndmp probe`
### Learn more
* [`DOC /protocols/ndmp/sessions`](#docs-ndmp-protocols_ndmp_sessions)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a specific NDMP session.
### Related ONTAP commands
* `vserver services ndmp probe`
* `system services ndmp probe`
### Learn more
* [`DOC /protocols/ndmp/sessions`](#docs-ndmp-protocols_ndmp_sessions)
"""
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
        r"""Deletes a specific NDMP session.
### Related ONTAP commands
* `vserver services ndmp kill`
* `system services ndmp kill`
### Learn more
* [`DOC /protocols/ndmp/sessions`](#docs-ndmp-protocols_ndmp_sessions)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)


