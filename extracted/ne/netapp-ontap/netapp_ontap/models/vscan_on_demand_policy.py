r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VscanOnDemandPolicy", "VscanOnDemandPolicySchema"]
__pdoc__ = {
    "VscanOnDemandPolicySchema.resource": False,
    "VscanOnDemandPolicySchema.opts": False,
    "VscanOnDemandPolicy": False,
}


class VscanOnDemandPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanOnDemandPolicy object"""

    log_path = marshmallow_fields.Str(data_key="log_path", allow_none=True)
    r""" The path from the Vserver root where the task report is created.

Example: /vol0/report_dir """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" On-Demand task name

Example: task-1 """

    scan_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="scan_paths", allow_none=True)
    r""" List of paths that need to be scanned.

Example: ["/vol1/","/vol2/cifs/"] """

    schedule = marshmallow_fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", unknown=EXCLUDE, data_key="schedule", allow_none=True)
    r""" The schedule field of the vscan_on_demand_policy. """

    scope = marshmallow_fields.Nested("netapp_ontap.models.vscan_on_demand_scope.VscanOnDemandScopeSchema", unknown=EXCLUDE, data_key="scope", allow_none=True)
    r""" The scope field of the vscan_on_demand_policy. """

    @property
    def resource(self):
        return VscanOnDemandPolicy

    gettable_fields = [
        "log_path",
        "name",
        "scan_paths",
        "schedule.links",
        "schedule.name",
        "schedule.uuid",
        "scope",
    ]
    """log_path,name,scan_paths,schedule.links,schedule.name,schedule.uuid,scope,"""

    patchable_fields = [
        "log_path",
        "scan_paths",
        "schedule.name",
        "schedule.uuid",
        "scope",
    ]
    """log_path,scan_paths,schedule.name,schedule.uuid,scope,"""

    postable_fields = [
        "log_path",
        "name",
        "scan_paths",
        "schedule.name",
        "schedule.uuid",
        "scope",
    ]
    """log_path,name,scan_paths,schedule.name,schedule.uuid,scope,"""


class VscanOnDemandPolicy(Resource):

    _schema = VscanOnDemandPolicySchema
