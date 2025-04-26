r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeProtocolRawPerformanceStatCreate", "VolumeProtocolRawPerformanceStatCreateSchema"]
__pdoc__ = {
    "VolumeProtocolRawPerformanceStatCreateSchema.resource": False,
    "VolumeProtocolRawPerformanceStatCreateSchema.opts": False,
    "VolumeProtocolRawPerformanceStatCreate": False,
}


class VolumeProtocolRawPerformanceStatCreateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeProtocolRawPerformanceStatCreate object"""

    dir = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="dir", allow_none=True)
    r""" The dir field of the volume_protocol_raw_performance_stat_create. """

    file = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="file", allow_none=True)
    r""" The file field of the volume_protocol_raw_performance_stat_create. """

    other = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="other", allow_none=True)
    r""" The other field of the volume_protocol_raw_performance_stat_create. """

    symlink = marshmallow_fields.Nested("netapp_ontap.models.volume_protocol_raw_performance_stat_other.VolumeProtocolRawPerformanceStatOtherSchema", unknown=EXCLUDE, data_key="symlink", allow_none=True)
    r""" The symlink field of the volume_protocol_raw_performance_stat_create. """

    @property
    def resource(self):
        return VolumeProtocolRawPerformanceStatCreate

    gettable_fields = [
        "dir",
        "file",
        "other",
        "symlink",
    ]
    """dir,file,other,symlink,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class VolumeProtocolRawPerformanceStatCreate(Resource):

    _schema = VolumeProtocolRawPerformanceStatCreateSchema
