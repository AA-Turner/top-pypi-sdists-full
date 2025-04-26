r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeTiering", "VolumeTieringSchema"]
__pdoc__ = {
    "VolumeTieringSchema.resource": False,
    "VolumeTieringSchema.opts": False,
    "VolumeTiering": False,
}


class VolumeTieringSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeTiering object"""

    min_cooling_days = Size(data_key="min_cooling_days", allow_none=True)
    r""" This parameter specifies the minimum number of days that user data blocks of the volume must be cooled before they can be considered cold and tiered out to the cloud tier. Note that this parameter is only used for tiering purposes and does not affect the reporting of inactive data. The value specified should be greater than the frequency with which applications in the volume shift between different sets of data. This parameter cannot be set when volume tiering policy is either "none" or "all". The default value of this parameter depends on the volume's tiering policy. See the tiering policy section of this documentation for corresponding default values. If the tiering policy on the volume gets changed, then this parameter will be reset to the default value corresponding to the new tiering policy. """

    object_tags = marshmallow_fields.List(marshmallow_fields.Str, data_key="object_tags", allow_none=True)
    r""" This parameter specifies tags of a volume for objects stored on a FabricPool-enabled aggregate. Each tag is a key,value pair and should be in the format "key=value". """

    policy = marshmallow_fields.Str(data_key="policy", allow_none=True)
    r""" Policy that determines whether the user data blocks of a volume in a FabricPool will be tiered to the cloud store when they become cold. FabricPool combines flash (performance tier) with a cloud store into a single aggregate. Temperature of a volume block increases if it is accessed frequently and decreases when it is not. Valid in POST or PATCH.<br>all &dash; This policy allows tiering of both snapshots and active file system user data to the cloud store as soon as possible by ignoring the temperature on the volume blocks.<br>auto &dash; This policy allows tiering of both snapshot and active file system user data to the cloud store<br>none &dash; Volume blocks will not be tiered to the cloud store.<br>snapshot_only &dash; This policy allows tiering of only the volume snapshots not associated with the active file system. The default tiering policy is "snapshot-only" for a FlexVol volume and "none" for a FlexGroup volume. The default minimum cooling period for the "snapshot-only" tiering policy is 2 days and for the "auto" tiering policy is 31 days.

Valid choices:

* all
* auto
* none
* snapshot_only """

    supported = marshmallow_fields.Boolean(data_key="supported", allow_none=True)
    r""" This parameter specifies whether or not FabricPools are selected when provisioning a FlexGroup volume without specifying "aggregates.name" or "aggregates.uuid". Only FabricPool aggregates are used if this parameter is set to true and only non FabricPool aggregates are used if this parameter is set to false. Tiering support for a FlexGroup volume can be changed by moving all of the constituents to the required aggregates. Note that in order to tier data, not only does the volume need to support tiering by using FabricPools, the tiering "policy" must not be 'none'. A volume that uses FabricPools but has a tiering "policy" of 'none' supports tiering, but will not tier any data. """

    @property
    def resource(self):
        return VolumeTiering

    gettable_fields = [
        "min_cooling_days",
        "object_tags",
        "policy",
    ]
    """min_cooling_days,object_tags,policy,"""

    patchable_fields = [
        "min_cooling_days",
        "object_tags",
        "policy",
    ]
    """min_cooling_days,object_tags,policy,"""

    postable_fields = [
        "min_cooling_days",
        "object_tags",
        "policy",
        "supported",
    ]
    """min_cooling_days,object_tags,policy,supported,"""


class VolumeTiering(Resource):

    _schema = VolumeTieringSchema
