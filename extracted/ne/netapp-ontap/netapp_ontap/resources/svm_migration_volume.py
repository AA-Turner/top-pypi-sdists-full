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


__all__ = ["SvmMigrationVolume", "SvmMigrationVolumeSchema"]
__pdoc__ = {
    "SvmMigrationVolumeSchema.resource": False,
    "SvmMigrationVolumeSchema.opts": False,
}


class SvmMigrationVolumeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SvmMigrationVolume object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE, allow_none=True)
    r""" The links field of the svm_migration_volume."""

    errors = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.svm_migration_messages.SvmMigrationMessagesSchema", unknown=EXCLUDE, allow_none=True), data_key="errors", allow_none=True)
    r""" List of transfer errors"""

    healthy = marshmallow_fields.Boolean(
        data_key="healthy",
        allow_none=True,
    )
    r""" Indicates whether the volume transfer relationship is healthy."""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE, allow_none=True)
    r""" The node field of the svm_migration_volume."""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE, allow_none=True)
    r""" The svm field of the svm_migration_volume."""

    transfer_state = marshmallow_fields.Str(
        data_key="transfer_state",
        validate=enum_validation(['Idle', 'Transferring', 'Aborting', 'OutOfSync', 'InSync', 'Transitioning', 'ReadyForCutoverPreCommit', 'CutoverPreCommitting', 'CuttingOver']),
        allow_none=True,
    )
    r""" Status of the transfer.

Valid choices:

* Idle
* Transferring
* Aborting
* OutOfSync
* InSync
* Transitioning
* ReadyForCutoverPreCommit
* CutoverPreCommitting
* CuttingOver"""

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE, allow_none=True)
    r""" The volume field of the svm_migration_volume."""

    @property
    def resource(self):
        return SvmMigrationVolume

    gettable_fields = [
        "links",
        "errors",
        "healthy",
        "node.links",
        "node.name",
        "node.uuid",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "transfer_state",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,errors,healthy,node.links,node.name,node.uuid,svm.links,svm.name,svm.uuid,transfer_state,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "healthy",
    ]
    """healthy,"""

    postable_fields = [
        "healthy",
    ]
    """healthy,"""

class SvmMigrationVolume(Resource):
    r""" Volume transfer information """

    _schema = SvmMigrationVolumeSchema
    _path = "/api/svm/migrations/{svm_migration[uuid]}/volumes"
    _keys = ["svm_migration.uuid", "volume.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the transfer status of the volumes in the SVM.
### Related ONTAP commands
* `vserver migrate show-volume`
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
        """Returns a count of all SvmMigrationVolume resources that match the provided query"""
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
        """Returns a list of RawResources that represent SvmMigrationVolume resources that match the provided query"""
        return super()._get_collection(
            *args, connection=connection, max_records=max_records, raw=True, **kwargs
        )

    fast_get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)




    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the transfer status of the volumes in the SVM.
### Related ONTAP commands
* `vserver migrate show-volume`
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the volume transfer status of the specified volume.uuid.
### Related ONTAP commands
* `vserver migrate show-volume`
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





