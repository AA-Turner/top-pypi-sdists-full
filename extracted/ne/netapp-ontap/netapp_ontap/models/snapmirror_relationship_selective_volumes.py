r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SnapmirrorRelationshipSelectiveVolumes", "SnapmirrorRelationshipSelectiveVolumesSchema"]
__pdoc__ = {
    "SnapmirrorRelationshipSelectiveVolumesSchema.resource": False,
    "SnapmirrorRelationshipSelectiveVolumesSchema.opts": False,
    "SnapmirrorRelationshipSelectiveVolumes": False,
}

class SnapmirrorRelationshipSelectiveVolumesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorRelationshipSelectiveVolumes object"""

    mode = marshmallow_fields.Str(data_key="mode", allow_none=True)
    r""" Indicates whether volumes need to be included or excluded for SnapMirror Active Sync NAS relationship. Default behavior is to protect all volumes under a vserver.

Valid choices:

* include
* exclude """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the volume.

Example: volume1 """

    @property
    def resource(self):
        return SnapmirrorRelationshipSelectiveVolumes

    gettable_fields = [
        "mode",
        "name",
    ]
    """mode,name,"""

    patchable_fields = [
        "mode",
        "name",
    ]
    """mode,name,"""

    postable_fields = [
        "mode",
        "name",
    ]
    """mode,name,"""


class SnapmirrorRelationshipSelectiveVolumes(Resource):

    _schema = SnapmirrorRelationshipSelectiveVolumesSchema
