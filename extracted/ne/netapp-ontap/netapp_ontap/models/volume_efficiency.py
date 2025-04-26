r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeEfficiency", "VolumeEfficiencySchema"]
__pdoc__ = {
    "VolumeEfficiencySchema.resource": False,
    "VolumeEfficiencySchema.opts": False,
    "VolumeEfficiency": False,
}


class VolumeEfficiencySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeEfficiency object"""

    application_io_size = marshmallow_fields.Str(data_key="application_io_size", allow_none=True)
    r""" Block size to use by compression. 8k and auto are only allowed for POST. Only auto is supported on QAT supported platforms.

Valid choices:

* 8k
* 16k
* 32k
* auto """

    auto_state = marshmallow_fields.Str(data_key="auto_state", allow_none=True)
    r""" Automatic deduplication schedule volume state.<br>auto &dash; Volumes with auto_state set to auto start post-process deduplication automatically.<br>deprioritized &dash; Volumes with auto_state set to deprioritized do not start post-process deduplication automatically.

Valid choices:

* auto
* deprioritized """

    compaction = marshmallow_fields.Str(data_key="compaction", allow_none=True)
    r""" The system can be enabled/disabled compaction.<br>inline &dash; Data will be compacted first and written to the volume.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroup volumes, where some of the constituent volumes are compaction enabled and some are disabled.

Valid choices:

* inline
* none
* mixed """

    compression = marshmallow_fields.Str(data_key="compression", allow_none=True)
    r""" The system can be enabled/disabled compression. Disabling compression is not allowed on Capacity optimized Flash with QAT supported platforms.<br>inline &dash; Data will be compressed first and written to the volume. <br>background &dash; Data will be written to the volume and compressed later. <br>both &dash; Inline compression compresses the data and write to the volume, background compression compresses only the blocks on which inline compression is not run.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroup volumes, where some of the constituent volumes are compression enabled and some are disabled. <br>Note that On volumes with container compression enabled, background compression refers to inactive data compression scan enabled on the volume.

Valid choices:

* inline
* background
* both
* none
* mixed """

    compression_type = marshmallow_fields.Str(data_key="compression_type", allow_none=True)
    r""" Compression type to use by compression. Valid for PATCH and GET.

Valid choices:

* none
* secondary
* adaptive """

    cross_volume_dedupe = marshmallow_fields.Str(data_key="cross_volume_dedupe", allow_none=True)
    r""" The system can be enabled/disabled cross volume dedupe. it can be enabled only when dedupe is enabled. Disabling cross volume dedupe is not allowed on Capacity optimized Flash with QAT supported platforms.<br>inline &dash; Data will be cross volume deduped first and written to the volume.<br>background &dash; Data will be written to the volume and cross volume deduped later.<br>both &dash; Inline cross volume dedupe dedupes the data and write to the volume, background cross volume dedupe dedupes only the blocks on which inline dedupe is not run.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroup volumes, where some of the constituent volumes are cross volume dedupe enabled and some are disabled.

Valid choices:

* inline
* background
* both
* none
* mixed """

    dedupe = marshmallow_fields.Str(data_key="dedupe", allow_none=True)
    r""" The system can be enabled/disabled dedupe. Disabling dedupe is not allowed on Capacity optimized Flash with QAT supported platforms.<br>inline &dash; Data will be deduped first and written to the volume.<br>background &dash; Data will be written to the volume and deduped later.<br>both &dash; Inline dedupe dedupes the data and write to the volume, background dedupe dedupes only the blocks on which inline dedupe is not run.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroup volumes, where some of the constituent volumes are dedupe enabled and some are disabled.

Valid choices:

* inline
* background
* both
* none
* mixed """

    has_savings = marshmallow_fields.Boolean(data_key="has_savings", allow_none=True)
    r""" When true, indicates that the volume contains shared(deduplication, file clones) or compressed data. """

    idcs_scanner = marshmallow_fields.Nested("netapp_ontap.models.volume_efficiency_idcs_scanner.VolumeEfficiencyIdcsScannerSchema", unknown=EXCLUDE, data_key="idcs_scanner", allow_none=True)
    r""" Inactive data compression scan looks and picks up blocks that have not been read for a certain amount of time(threshold_inactive_days). These blocks are then compressed in 32K chunks. All attributes are valid for GET only, except for 'operation_state' which is valid for PATCH and GET, and is used to start/stop the scanner. """

    last_op_begin = marshmallow_fields.Str(data_key="last_op_begin", allow_none=True)
    r""" Last sis operation begin timestamp. """

    last_op_end = marshmallow_fields.Str(data_key="last_op_end", allow_none=True)
    r""" Last sis operation end timestamp. """

    last_op_err = marshmallow_fields.Str(data_key="last_op_err", allow_none=True)
    r""" Last sis operation error text. """

    last_op_size = Size(data_key="last_op_size", allow_none=True)
    r""" Last sis operation size. """

    last_op_state = marshmallow_fields.Str(data_key="last_op_state", allow_none=True)
    r""" Last sis operation state. """

    logging_enabled = marshmallow_fields.Boolean(data_key="logging_enabled", allow_none=True)
    r""" When true, indicates that space savings for any newly-written data are being logged. """

    op_state = marshmallow_fields.Str(data_key="op_state", allow_none=True)
    r""" Sis status of the volume.

Valid choices:

* idle
* initializing
* active
* undoing
* pending
* downgrading
* disabled """

    policy = marshmallow_fields.Nested("netapp_ontap.models.volume_efficiency_policy1.VolumeEfficiencyPolicy1Schema", unknown=EXCLUDE, data_key="policy", allow_none=True)
    r""" The policy field of the volume_efficiency. """

    progress = marshmallow_fields.Str(data_key="progress", allow_none=True)
    r""" Sis progress of the volume. """

    scanner = marshmallow_fields.Nested("netapp_ontap.models.volume_efficiency_scanner.VolumeEfficiencyScannerSchema", unknown=EXCLUDE, data_key="scanner", allow_none=True)
    r""" The scanner field of the volume_efficiency. """

    schedule = marshmallow_fields.Str(data_key="schedule", allow_none=True)
    r""" Schedule associated with volume. """

    space_savings = marshmallow_fields.Nested("netapp_ontap.models.volume_efficiency_space_savings.VolumeEfficiencySpaceSavingsSchema", unknown=EXCLUDE, data_key="space_savings", allow_none=True)
    r""" The space_savings field of the volume_efficiency. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Storage efficiency state of the volume. Currently, this field supports POST/PATCH only for RW (Read-Write) volumes on FSx for ONTAP and Cloud Volumes ONTAP.<br>disabled &dash; All storage efficiency features are disabled.<br>mixed &dash; Read-only field for FlexGroup volumes, storage efficiency is enabled on certain constituents and disabled on others.<br>On FSx for ONTAP and Cloud Volumes ONTAP &dash; <br> &emsp; enabled &dash; All supported storage efficiency features for the volume are enabled.<br> &emsp; custom &dash; Read-only field currently only supported for the FSx for ONTAP and Cloud Volumes ONTAP, user-defined storage efficiency features are enabled.<br>For other platforms &dash; <br> &emsp; enabled &dash; At least one storage efficiency feature for the volume is enabled.

Valid choices:

* disabled
* enabled
* mixed
* custom """

    storage_efficiency_mode = marshmallow_fields.Str(data_key="storage_efficiency_mode", allow_none=True)
    r""" Storage efficiency mode used by volume. This parameter is supported only on AFF platforms. There is no difference between default and efficient modes on QAT supported platforms and auto adaptive compression is set irrespective of the modes.

Valid choices:

* default
* efficient """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Sis Type of the volume.

Valid choices:

* regular
* snapvault """

    volume_path = marshmallow_fields.Str(data_key="volume_path", allow_none=True)
    r""" Absolute volume path of the volume. """

    @property
    def resource(self):
        return VolumeEfficiency

    gettable_fields = [
        "application_io_size",
        "auto_state",
        "compaction",
        "compression",
        "compression_type",
        "cross_volume_dedupe",
        "dedupe",
        "has_savings",
        "idcs_scanner",
        "last_op_begin",
        "last_op_end",
        "last_op_err",
        "last_op_size",
        "last_op_state",
        "logging_enabled",
        "op_state",
        "policy",
        "progress",
        "scanner",
        "schedule",
        "space_savings",
        "state",
        "storage_efficiency_mode",
        "type",
        "volume_path",
    ]
    """application_io_size,auto_state,compaction,compression,compression_type,cross_volume_dedupe,dedupe,has_savings,idcs_scanner,last_op_begin,last_op_end,last_op_err,last_op_size,last_op_state,logging_enabled,op_state,policy,progress,scanner,schedule,space_savings,state,storage_efficiency_mode,type,volume_path,"""

    patchable_fields = [
        "application_io_size",
        "compaction",
        "compression",
        "compression_type",
        "cross_volume_dedupe",
        "dedupe",
        "idcs_scanner",
        "policy",
        "scanner",
        "space_savings",
        "state",
        "storage_efficiency_mode",
    ]
    """application_io_size,compaction,compression,compression_type,cross_volume_dedupe,dedupe,idcs_scanner,policy,scanner,space_savings,state,storage_efficiency_mode,"""

    postable_fields = [
        "application_io_size",
        "compaction",
        "compression",
        "compression_type",
        "cross_volume_dedupe",
        "dedupe",
        "idcs_scanner",
        "policy",
        "scanner",
        "space_savings",
        "state",
        "storage_efficiency_mode",
    ]
    """application_io_size,compaction,compression,compression_type,cross_volume_dedupe,dedupe,idcs_scanner,policy,scanner,space_savings,state,storage_efficiency_mode,"""


class VolumeEfficiency(Resource):

    _schema = VolumeEfficiencySchema
