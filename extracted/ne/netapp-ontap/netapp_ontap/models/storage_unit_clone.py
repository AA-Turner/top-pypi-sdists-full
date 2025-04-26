r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitClone", "StorageUnitCloneSchema"]
__pdoc__ = {
    "StorageUnitCloneSchema.resource": False,
    "StorageUnitCloneSchema.opts": False,
    "StorageUnitClone": False,
}


class StorageUnitCloneSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitClone object"""

    inherited_physical_used = Size(data_key="inherited_physical_used", allow_none=True)
    r""" Inherited physical used from the clone's base snapshot. """

    inherited_savings = Size(data_key="inherited_savings", allow_none=True)
    r""" Inherited savings from the clone's base snapshot. """

    is_flexclone = marshmallow_fields.Boolean(data_key="is_flexclone", allow_none=True)
    r""" Specifies if this storage unit is a normal FlexVol storage unit or FlexClone storage unit. Valid in POST. """

    source = marshmallow_fields.Nested("netapp_ontap.models.storage_unit_clone_source.StorageUnitCloneSourceSchema", unknown=EXCLUDE, data_key="source", allow_none=True)
    r""" The source field of the storage_unit_clone. """

    split_complete_percent = Size(data_key="split_complete_percent", allow_none=True)
    r""" Percentage of FlexClone storage unit blocks split from its parent storage unit. """

    split_estimate = Size(data_key="split_estimate", allow_none=True)
    r""" Space required by the containing-aggregate to split the FlexClone storage unit. """

    split_initiated = marshmallow_fields.Boolean(data_key="split_initiated", allow_none=True)
    r""" This field is set when a split is executed on a FlexClone storage unit, that is when the FlexClone storage unit is split from its parent FlexVol storage unit. Setting this field initiates a split of a FlexClone storage unit from a FlexVol storage unit. Valid in POST and PATCH. """

    @property
    def resource(self):
        return StorageUnitClone

    gettable_fields = [
        "inherited_physical_used",
        "inherited_savings",
        "is_flexclone",
        "source",
        "split_complete_percent",
        "split_estimate",
        "split_initiated",
    ]
    """inherited_physical_used,inherited_savings,is_flexclone,source,split_complete_percent,split_estimate,split_initiated,"""

    patchable_fields = [
        "source",
        "split_initiated",
    ]
    """source,split_initiated,"""

    postable_fields = [
        "is_flexclone",
        "source",
        "split_initiated",
    ]
    """is_flexclone,source,split_initiated,"""


class StorageUnitClone(Resource):

    _schema = StorageUnitCloneSchema
