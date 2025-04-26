r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["CifsSessionVolumes", "CifsSessionVolumesSchema"]
__pdoc__ = {
    "CifsSessionVolumesSchema.resource": False,
    "CifsSessionVolumesSchema.opts": False,
    "CifsSessionVolumes": False,
}


class CifsSessionVolumesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsSessionVolumes object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the cifs_session_volumes. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the volume. This field cannot be specified in a PATCH method.

Example: volume1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier for the volume. This corresponds to the instance-uuid that is exposed in the CLI and ONTAPI. It does not change due to a volume move.

Example: 028baa66-41bd-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return CifsSessionVolumes

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class CifsSessionVolumes(Resource):

    _schema = CifsSessionVolumesSchema
