r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PerformanceFcpMetricSvm", "PerformanceFcpMetricSvmSchema"]
__pdoc__ = {
    "PerformanceFcpMetricSvmSchema.resource": False,
    "PerformanceFcpMetricSvmSchema.opts": False,
    "PerformanceFcpMetricSvm": False,
}


class PerformanceFcpMetricSvmSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PerformanceFcpMetricSvm object"""

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the SVM.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return PerformanceFcpMetricSvm

    gettable_fields = [
        "uuid",
    ]
    """uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class PerformanceFcpMetricSvm(Resource):

    _schema = PerformanceFcpMetricSvmSchema
