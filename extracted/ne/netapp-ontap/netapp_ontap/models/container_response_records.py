r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ContainerResponseRecords", "ContainerResponseRecordsSchema"]
__pdoc__ = {
    "ContainerResponseRecordsSchema.resource": False,
    "ContainerResponseRecordsSchema.opts": False,
    "ContainerResponseRecords": False,
}


class ContainerResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerResponseRecords object"""

    svm = marshmallow_fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm", allow_none=True)
    r""" The svm field of the container_response_records. """

    volumes = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.container_volume.ContainerVolumeSchema", unknown=EXCLUDE, allow_none=True), data_key="volumes", allow_none=True)
    r""" A list of NAS volumes to provision.<br/> """

    @property
    def resource(self):
        return ContainerResponseRecords

    gettable_fields = [
        "volumes",
    ]
    """volumes,"""

    patchable_fields = [
        "volumes",
    ]
    """volumes,"""

    postable_fields = [
        "svm.name",
        "svm.uuid",
        "volumes",
    ]
    """svm.name,svm.uuid,volumes,"""


class ContainerResponseRecords(Resource):

    _schema = ContainerResponseRecordsSchema
