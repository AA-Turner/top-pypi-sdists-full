r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupQos", "ConsistencyGroupQosSchema"]
__pdoc__ = {
    "ConsistencyGroupQosSchema.resource": False,
    "ConsistencyGroupQosSchema.opts": False,
    "ConsistencyGroupQos": False,
}


class ConsistencyGroupQosSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupQos object"""

    policy = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_qos_policy.ConsistencyGroupQosPolicySchema", unknown=EXCLUDE, data_key="policy", allow_none=True)
    r""" When "min_throughput_iops", "min_throughput_mbps", "max_throughput_iops" or "max_throughput_mbps" attributes are specified, the storage object is assigned to an auto-generated QoS policy group. If the attributes are later modified, the auto-generated QoS policy-group attributes are modified. Attributes can be removed by specifying "0" and policy group by specifying "none". Upon deletion of the storage object or if the attributes are removed, then the QoS policy-group is also removed. """

    @property
    def resource(self):
        return ConsistencyGroupQos

    gettable_fields = [
        "policy",
    ]
    """policy,"""

    patchable_fields = [
        "policy",
    ]
    """policy,"""

    postable_fields = [
        "policy",
    ]
    """policy,"""


class ConsistencyGroupQos(Resource):

    _schema = ConsistencyGroupQosSchema
