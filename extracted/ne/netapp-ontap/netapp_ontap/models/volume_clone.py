r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["VolumeClone", "VolumeCloneSchema"]
__pdoc__ = {
    "VolumeCloneSchema.resource": False,
    "VolumeCloneSchema.opts": False,
    "VolumeClone": False,
}

class VolumeCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeClone object"""

    has_flexclone = marshmallow_fields.Boolean(data_key="has_flexclone", allow_none=True)
    r""" Specifies whether this volume is a parent of any FlexClone volume. """

    inherited_physical_used = Size(data_key="inherited_physical_used", allow_none=True)
    r""" Inherited physical used from the clone's base snapshot. """

    inherited_savings = Size(data_key="inherited_savings", allow_none=True)
    r""" Inherited savings from the clone's base snapshot. """

    is_flexclone = marshmallow_fields.Boolean(data_key="is_flexclone", allow_none=True)
    r""" Specifies if this volume is a normal FlexVol volume or FlexClone volume. This field needs to be set when creating a FlexClone volume. Valid in POST. """

    lun_name = marshmallow_fields.Str(data_key="lun_name", allow_none=True)
    r""" This optional parameter specifies the name of a LUN that will be non-disruptively migrated to the newly created FlexClone volume. If not specified, no LUNs are migrated. """

    parent_snapshot = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.snapshot", "SnapshotSchema"),
                unknown=EXCLUDE,
                data_key="parent_snapshot",
                allow_none=True
            )
    r""" The parent_snapshot field of the volume_clone. """

    parent_svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="parent_svm",
                allow_none=True
            )
    r""" The parent_svm field of the volume_clone. """

    parent_volume = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.volume", "VolumeSchema"),
                unknown=EXCLUDE,
                data_key="parent_volume",
                allow_none=True
            )
    r""" The parent_volume field of the volume_clone. """

    qtree_name = marshmallow_fields.Str(data_key="qtree_name", allow_none=True)
    r""" This optional parameter specifies the name of the qtree containing the LUN that will be non-disruptively migrated to the newly created FlexClone volume. """

    split_complete_percent = Size(data_key="split_complete_percent", allow_none=True)
    r""" Percentage of FlexClone volume blocks split from its parent volume. """

    split_estimate = Size(data_key="split_estimate", allow_none=True)
    r""" Space required by the containing-aggregate to split the FlexClone volume. """

    split_initiated = marshmallow_fields.Boolean(data_key="split_initiated", allow_none=True)
    r""" This field is set when a split is executed on any FlexClone volume, that is when the FlexClone volume is split from its parent FlexVol volume. Setting this field initiates a split of a FlexClone volume from a FlexVol volume. Valid in PATCH. """

    @property
    def resource(self):
        return VolumeClone

    gettable_fields = [
        "has_flexclone",
        "inherited_physical_used",
        "inherited_savings",
        "is_flexclone",
        "lun_name",
        "parent_snapshot.links",
        "parent_snapshot.name",
        "parent_snapshot.uuid",
        "parent_svm.links",
        "parent_svm.name",
        "parent_svm.uuid",
        "parent_volume.links",
        "parent_volume.name",
        "parent_volume.uuid",
        "qtree_name",
        "split_complete_percent",
        "split_estimate",
        "split_initiated",
    ]
    """has_flexclone,inherited_physical_used,inherited_savings,is_flexclone,lun_name,parent_snapshot.links,parent_snapshot.name,parent_snapshot.uuid,parent_svm.links,parent_svm.name,parent_svm.uuid,parent_volume.links,parent_volume.name,parent_volume.uuid,qtree_name,split_complete_percent,split_estimate,split_initiated,"""

    patchable_fields = [
        "parent_snapshot.name",
        "parent_snapshot.uuid",
        "split_initiated",
    ]
    """parent_snapshot.name,parent_snapshot.uuid,split_initiated,"""

    postable_fields = [
        "is_flexclone",
        "lun_name",
        "parent_snapshot.name",
        "parent_snapshot.uuid",
        "parent_svm.name",
        "parent_svm.uuid",
        "parent_volume.name",
        "parent_volume.uuid",
        "qtree_name",
    ]
    """is_flexclone,lun_name,parent_snapshot.name,parent_snapshot.uuid,parent_svm.name,parent_svm.uuid,parent_volume.name,parent_volume.uuid,qtree_name,"""


class VolumeClone(Resource):

    _schema = VolumeCloneSchema
