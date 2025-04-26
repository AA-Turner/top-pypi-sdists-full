r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareReferenceMetroclusterProgressDetails", "SoftwareReferenceMetroclusterProgressDetailsSchema"]
__pdoc__ = {
    "SoftwareReferenceMetroclusterProgressDetailsSchema.resource": False,
    "SoftwareReferenceMetroclusterProgressDetailsSchema.opts": False,
    "SoftwareReferenceMetroclusterProgressDetails": False,
}


class SoftwareReferenceMetroclusterProgressDetailsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareReferenceMetroclusterProgressDetails object"""

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" MetroCluster update progress details.

Example: Switchover in progress """

    @property
    def resource(self):
        return SoftwareReferenceMetroclusterProgressDetails

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


class SoftwareReferenceMetroclusterProgressDetails(Resource):

    _schema = SoftwareReferenceMetroclusterProgressDetailsSchema
