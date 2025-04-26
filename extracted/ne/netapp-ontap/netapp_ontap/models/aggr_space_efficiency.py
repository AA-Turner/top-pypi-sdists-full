r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggrSpaceEfficiency", "AggrSpaceEfficiencySchema"]
__pdoc__ = {
    "AggrSpaceEfficiencySchema.resource": False,
    "AggrSpaceEfficiencySchema.opts": False,
    "AggrSpaceEfficiency": False,
}


class AggrSpaceEfficiencySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggrSpaceEfficiency object"""

    auto_adaptive_compression_savings = marshmallow_fields.Boolean(data_key="auto_adaptive_compression_savings", allow_none=True)
    r""" Indicates whether or not aggregate has auto adaptive compression savings. """

    cross_volume_background_dedupe = marshmallow_fields.Boolean(data_key="cross_volume_background_dedupe", allow_none=True)
    r""" Indicates whether or not cross volume background deduplication is enabled. """

    cross_volume_dedupe_savings = marshmallow_fields.Boolean(data_key="cross_volume_dedupe_savings", allow_none=True)
    r""" Indicates whether or not aggregate has cross volume deduplication savings. """

    cross_volume_inline_dedupe = marshmallow_fields.Boolean(data_key="cross_volume_inline_dedupe", allow_none=True)
    r""" Indicates whether or not cross volume inline deduplication is enabled. """

    enable_workload_informed_tsse = marshmallow_fields.Boolean(data_key="enable_workload_informed_tsse", allow_none=True)
    r""" Indicates whether Workload Informed TSSE is enabled on the system. """

    logical_used = Size(data_key="logical_used", allow_none=True)
    r""" Logical used """

    ratio = marshmallow_fields.Number(data_key="ratio", allow_none=True)
    r""" Data reduction ratio (logical_used / used) """

    savings = Size(data_key="savings", allow_none=True)
    r""" Space saved by storage efficiencies (logical_used - used) """

    wise_tsse_min_used_capacity_pct = Size(data_key="wise_tsse_min_used_capacity_pct", allow_none=True)
    r""" Minimum amount of used data in aggregate required to trigger cold compression on TSSE volumes. """

    @property
    def resource(self):
        return AggrSpaceEfficiency

    gettable_fields = [
        "auto_adaptive_compression_savings",
        "cross_volume_background_dedupe",
        "cross_volume_dedupe_savings",
        "cross_volume_inline_dedupe",
        "enable_workload_informed_tsse",
        "logical_used",
        "ratio",
        "savings",
        "wise_tsse_min_used_capacity_pct",
    ]
    """auto_adaptive_compression_savings,cross_volume_background_dedupe,cross_volume_dedupe_savings,cross_volume_inline_dedupe,enable_workload_informed_tsse,logical_used,ratio,savings,wise_tsse_min_used_capacity_pct,"""

    patchable_fields = [
        "enable_workload_informed_tsse",
        "wise_tsse_min_used_capacity_pct",
    ]
    """enable_workload_informed_tsse,wise_tsse_min_used_capacity_pct,"""

    postable_fields = [
        "enable_workload_informed_tsse",
        "wise_tsse_min_used_capacity_pct",
    ]
    """enable_workload_informed_tsse,wise_tsse_min_used_capacity_pct,"""


class AggrSpaceEfficiency(Resource):

    _schema = AggrSpaceEfficiencySchema
