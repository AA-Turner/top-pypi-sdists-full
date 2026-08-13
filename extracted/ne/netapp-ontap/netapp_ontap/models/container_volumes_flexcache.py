r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


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

    global_file_locking_enabled = marshmallow_fields.Boolean(data_key="global_file_locking_enabled", allow_none=True)
    r""" Specifies whether a FlexCache volume has global file locking mode enabled. Global file locking mode is a mode where protocol read locking semantics are enforced across all FlexCaches and origins of a FlexCache volume. When global file locking mode is enabled, cache locks are honored when flexcaches are disconnected from the origin. """

    origins = marshmallow_fields.List(
                marshmallow_fields.Nested(
                    lambda: lazy_import_schema("netapp_ontap.models.container_volume_flexcache_relationship", "ContainerVolumeFlexcacheRelationshipSchema"),
                    unknown=EXCLUDE,
                    allow_none=True
                ),
                data_key="origins",
                allow_none=True
                )
    r""" The origins field of the container_volumes_flexcache. """

    writeback = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.flexcache_writeback", "FlexcacheWritebackSchema"),
                unknown=EXCLUDE,
                data_key="writeback",
                allow_none=True
            )
    r""" The writeback field of the container_volumes_flexcache. """

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
        "global_file_locking_enabled",
        "origins",
        "writeback",
    ]
    """dr_cache,global_file_locking_enabled,origins,writeback,"""


class ContainerVolumesFlexcache(Resource):

    _schema = ContainerVolumesFlexcacheSchema
