r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["QosPolicyFixed", "QosPolicyFixedSchema"]
__pdoc__ = {
    "QosPolicyFixedSchema.resource": False,
    "QosPolicyFixedSchema.opts": False,
    "QosPolicyFixed": False,
}


class QosPolicyFixedSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the QosPolicyFixed object"""

    capacity_shared = marshmallow_fields.Boolean(data_key="capacity_shared", allow_none=True)
    r""" Specifies whether the capacities are shared across all objects that use this QoS policy-group. Default is false. """

    max_throughput_iops = Size(data_key="max_throughput_iops", allow_none=True)
    r""" Maximum throughput defined by this policy.  It is specified in terms of IOPS. 0 means no maximum throughput is enforced. """

    max_throughput_mbps = Size(data_key="max_throughput_mbps", allow_none=True)
    r""" Maximum throughput defined by this policy.  It is specified in terms of Mbps. 0 means no maximum throughput is enforced. """

    min_throughput_iops = Size(data_key="min_throughput_iops", allow_none=True)
    r""" Minimum throughput defined by this policy.  It is specified in terms of IOPS. 0 means no minimum throughput is enforced. These floors are not guaranteed on non-AFF platforms or when FabricPool tiering policies are set. """

    min_throughput_mbps = Size(data_key="min_throughput_mbps", allow_none=True)
    r""" Minimum throughput defined by this policy.  It is specified in terms of Mbps. 0 means no minimum throughput is enforced. """

    @property
    def resource(self):
        return QosPolicyFixed

    gettable_fields = [
        "capacity_shared",
        "max_throughput_iops",
        "max_throughput_mbps",
        "min_throughput_iops",
        "min_throughput_mbps",
    ]
    """capacity_shared,max_throughput_iops,max_throughput_mbps,min_throughput_iops,min_throughput_mbps,"""

    patchable_fields = [
        "max_throughput_iops",
        "max_throughput_mbps",
        "min_throughput_iops",
        "min_throughput_mbps",
    ]
    """max_throughput_iops,max_throughput_mbps,min_throughput_iops,min_throughput_mbps,"""

    postable_fields = [
        "capacity_shared",
        "max_throughput_iops",
        "max_throughput_mbps",
        "min_throughput_iops",
        "min_throughput_mbps",
    ]
    """capacity_shared,max_throughput_iops,max_throughput_mbps,min_throughput_iops,min_throughput_mbps,"""


class QosPolicyFixed(Resource):

    _schema = QosPolicyFixedSchema
