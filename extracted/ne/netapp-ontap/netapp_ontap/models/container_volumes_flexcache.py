r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerVolumesFlexcache", "ContainerVolumesFlexcacheSchema"]
__pdoc__ = {
    "ContainerVolumesFlexcacheSchema.resource": False,
    "ContainerVolumesFlexcacheSchema.opts": False,
    "ContainerVolumesFlexcache": False,
}


class ContainerVolumesFlexcacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesFlexcache object"""

    dr_cache = marshmallow_fields.Boolean(data_key="dr_cache", allow_none=True)
    r""" If set to true, a DR cache is created. """

    origins = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.container_volume_flexcache_relationship.ContainerVolumeFlexcacheRelationshipSchema", unknown=EXCLUDE, allow_none=True), data_key="origins", allow_none=True)
    r""" The origins field of the container_volumes_flexcache. """

    @property
    def resource(self):
        return ContainerVolumesFlexcache

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "dr_cache",
        "origins",
    ]
    """dr_cache,origins,"""


class ContainerVolumesFlexcache(Resource):

    _schema = ContainerVolumesFlexcacheSchema
