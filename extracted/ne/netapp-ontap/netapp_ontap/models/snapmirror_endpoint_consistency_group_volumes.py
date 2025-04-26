r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorEndpointConsistencyGroupVolumes", "SnapmirrorEndpointConsistencyGroupVolumesSchema"]
__pdoc__ = {
    "SnapmirrorEndpointConsistencyGroupVolumesSchema.resource": False,
    "SnapmirrorEndpointConsistencyGroupVolumesSchema.opts": False,
    "SnapmirrorEndpointConsistencyGroupVolumes": False,
}


class SnapmirrorEndpointConsistencyGroupVolumesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorEndpointConsistencyGroupVolumes object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the volume.

Example: volume1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier of the volume. This corresponds to the instance-uuid that is exposed in the CLI and ONTAPI. It does not change due to a volume move.

Example: 028baa66-41bd-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return SnapmirrorEndpointConsistencyGroupVolumes

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class SnapmirrorEndpointConsistencyGroupVolumes(Resource):

    _schema = SnapmirrorEndpointConsistencyGroupVolumesSchema
