r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeProtocolRawPerformanceStats", "VolumeProtocolRawPerformanceStatsSchema"]
__pdoc__ = {
    "VolumeProtocolRawPerformanceStatsSchema.resource": False,
    "VolumeProtocolRawPerformanceStatsSchema.opts": False,
    "VolumeProtocolRawPerformanceStats": False,
}


class VolumeProtocolRawPerformanceStatsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeProtocolRawPerformanceStats object"""

    access = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="access", allow_none=True)
    r""" The access field of the volume_protocol_raw_performance_stats. """

    audit = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="audit", allow_none=True)
    r""" The audit field of the volume_protocol_raw_performance_stats. """

    create = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_create.VolumeProtocolRawPerformanceStatCreateSchema", unknown=EXCLUDE, data_key="create", allow_none=True)
    r""" The create field of the volume_protocol_raw_performance_stats. """

    getattr = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="getattr", allow_none=True)
    r""" The getattr field of the volume_protocol_raw_performance_stats. """

    link = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="link", allow_none=True)
    r""" The link field of the volume_protocol_raw_performance_stats. """

    lock = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="lock", allow_none=True)
    r""" The lock field of the volume_protocol_raw_performance_stats. """

    lookup = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="lookup", allow_none=True)
    r""" The lookup field of the volume_protocol_raw_performance_stats. """

    open = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="open", allow_none=True)
    r""" The open field of the volume_protocol_raw_performance_stats. """

    read = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_rw.VolumeProtocolRawPerformanceStatRwSchema", unknown=EXCLUDE, data_key="read", allow_none=True)
    r""" The read field of the volume_protocol_raw_performance_stats. """

    readdir = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="readdir", allow_none=True)
    r""" The readdir field of the volume_protocol_raw_performance_stats. """

    readlink = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="readlink", allow_none=True)
    r""" The readlink field of the volume_protocol_raw_performance_stats. """

    rename = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="rename", allow_none=True)
    r""" The rename field of the volume_protocol_raw_performance_stats. """

    setattr = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="setattr", allow_none=True)
    r""" The setattr field of the volume_protocol_raw_performance_stats. """

    unlink = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="unlink", allow_none=True)
    r""" The unlink field of the volume_protocol_raw_performance_stats. """

    watch = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="watch", allow_none=True)
    r""" The watch field of the volume_protocol_raw_performance_stats. """

    write = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_rw.VolumeProtocolRawPerformanceStatRwSchema", unknown=EXCLUDE, data_key="write", allow_none=True)
    r""" The write field of the volume_protocol_raw_performance_stats. """

    @property
    def resource(self):
        return VolumeProtocolRawPerformanceStats

    gettable_fields = [
        "access",
        "audit",
        "create",
        "getattr",
        "link",
        "lock",
        "lookup",
        "open",
        "read",
        "readdir",
        "readlink",
        "rename",
        "setattr",
        "unlink",
        "watch",
        "write",
    ]
    """access,audit,create,getattr,link,lock,lookup,open,read,readdir,readlink,rename,setattr,unlink,watch,write,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class VolumeProtocolRawPerformanceStats(Resource):

    _schema = VolumeProtocolRawPerformanceStatsSchema
