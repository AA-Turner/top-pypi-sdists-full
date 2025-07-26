r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerVolumeFlexcacheRelationship", "ContainerVolumeFlexcacheRelationshipSchema"]
__pdoc__ = {
    "ContainerVolumeFlexcacheRelationshipSchema.resource": False,
    "ContainerVolumeFlexcacheRelationshipSchema.opts": False,
    "ContainerVolumeFlexcacheRelationship": False,
}


class ContainerVolumeFlexcacheRelationshipSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumeFlexcacheRelationship object"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the container_volume_flexcache_relationship. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the container_volume_flexcache_relationship. """

    @property
    def resource(self):
        return ContainerVolumeFlexcacheRelationship

    gettable_fields = [
        "svm.links",
        "svm.name",
        "svm.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """svm.links,svm.name,svm.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "volume.name",
        "volume.uuid",
    ]
    """volume.name,volume.uuid,"""

    postable_fields = [
        "svm.name",
        "svm.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """svm.name,svm.uuid,volume.name,volume.uuid,"""


class ContainerVolumeFlexcacheRelationship(Resource):

    _schema = ContainerVolumeFlexcacheRelationshipSchema
