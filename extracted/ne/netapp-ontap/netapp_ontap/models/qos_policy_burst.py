r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["QosPolicyBurst", "QosPolicyBurstSchema"]
__pdoc__ = {
    "QosPolicyBurstSchema.resource": False,
    "QosPolicyBurstSchema.opts": False,
    "QosPolicyBurst": False,
}

class QosPolicyBurstSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QosPolicyBurst object"""

    duration = Size(data_key="duration", allow_none=True)
    r""" Amount of time in seconds a policy can burst at either the maximum percentage or maximum IOPS above the set limit. """

    iops = Size(data_key="iops", allow_none=True)
    r""" Burst maximum IOPS for a policy max_throughput or peak_iops. Policy max_throughput must have an IOPS component. If burst_iops is less than max_throughput or peak_iops, then max_throughput or peak_iops is used. This is mutually exclusive with burst_percent. """

    percent = Size(data_key="percent", allow_none=True)
    r""" Percentage of IOPS or throughput above policy max_throughput or peak_iops. This is mutually exclusive with burst_iops. """

    @property
    def resource(self):
        return QosPolicyBurst

    gettable_fields = [
        "duration",
        "iops",
        "percent",
    ]
    """duration,iops,percent,"""

    patchable_fields = [
        "duration",
        "iops",
        "percent",
    ]
    """duration,iops,percent,"""

    postable_fields = [
        "duration",
        "iops",
        "percent",
    ]
    """duration,iops,percent,"""


class QosPolicyBurst(Resource):

    _schema = QosPolicyBurstSchema
