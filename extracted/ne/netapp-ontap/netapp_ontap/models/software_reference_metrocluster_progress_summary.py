r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareReferenceMetroclusterProgressSummary", "SoftwareReferenceMetroclusterProgressSummarySchema"]
__pdoc__ = {
    "SoftwareReferenceMetroclusterProgressSummarySchema.resource": False,
    "SoftwareReferenceMetroclusterProgressSummarySchema.opts": False,
    "SoftwareReferenceMetroclusterProgressSummary": False,
}


class SoftwareReferenceMetroclusterProgressSummarySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareReferenceMetroclusterProgressSummary object"""

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" MetroCluster update progress summary.

Example: MetroCluster updated successfully. """

    @property
    def resource(self):
        return SoftwareReferenceMetroclusterProgressSummary

    gettable_fields = [
        "message",
    ]
    """message,"""

    patchable_fields = [
        "message",
    ]
    """message,"""

    postable_fields = [
        "message",
    ]
    """message,"""


class SoftwareReferenceMetroclusterProgressSummary(Resource):

    _schema = SoftwareReferenceMetroclusterProgressSummarySchema
