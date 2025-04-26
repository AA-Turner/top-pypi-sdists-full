r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareReferenceMetrocluster", "SoftwareReferenceMetroclusterSchema"]
__pdoc__ = {
    "SoftwareReferenceMetroclusterSchema.resource": False,
    "SoftwareReferenceMetroclusterSchema.opts": False,
    "SoftwareReferenceMetrocluster": False,
}


class SoftwareReferenceMetroclusterSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareReferenceMetrocluster object"""

    clusters = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.software_mcc.SoftwareMccSchema", unknown=EXCLUDE, allow_none=True), data_key="clusters", allow_none=True)
    r""" List of MetroCluster sites, statuses, and active ONTAP versions. """

    progress_details = marshmallow_fields.Nested("netapp_ontap.models.software_reference_metrocluster_progress_details.SoftwareReferenceMetroclusterProgressDetailsSchema", unknown=EXCLUDE, data_key="progress_details", allow_none=True)
    r""" The progress_details field of the software_reference_metrocluster. """

    progress_summary = marshmallow_fields.Nested("netapp_ontap.models.software_reference_metrocluster_progress_summary.SoftwareReferenceMetroclusterProgressSummarySchema", unknown=EXCLUDE, data_key="progress_summary", allow_none=True)
    r""" The progress_summary field of the software_reference_metrocluster. """

    @property
    def resource(self):
        return SoftwareReferenceMetrocluster

    gettable_fields = [
        "clusters",
        "progress_details",
        "progress_summary",
    ]
    """clusters,progress_details,progress_summary,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SoftwareReferenceMetrocluster(Resource):

    _schema = SoftwareReferenceMetroclusterSchema
