r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["CifsCharacterMapping", "CifsCharacterMappingSchema"]
__pdoc__ = {
    "CifsCharacterMappingSchema.resource": False,
    "CifsCharacterMappingSchema.opts": False,
    "CifsCharacterMapping": False,
}

class CifsCharacterMappingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the CifsCharacterMapping object"""

    mapping = marshmallow_fields.List(marshmallow_fields.Str, data_key="mapping", allow_none=True)
    r""" The mapping field of the cifs_character_mapping.

Example: ["3c:e17c"] """

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="svm",
                allow_none=True
            )
    r""" The svm field of the cifs_character_mapping. """

    volume = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.volume", "VolumeSchema"),
                unknown=EXCLUDE,
                data_key="volume",
                allow_none=True
            )
    r""" The volume field of the cifs_character_mapping. """

    @property
    def resource(self):
        return CifsCharacterMapping

    gettable_fields = [
        "mapping",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """mapping,svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "mapping",
    ]
    """mapping,"""

    postable_fields = [
        "mapping",
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """mapping,svm.name,svm.uuid,volume.name,volume.uuid,"""


class CifsCharacterMapping(Resource):

    _schema = CifsCharacterMappingSchema
