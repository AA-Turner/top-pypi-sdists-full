r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationLunMappingObject", "ApplicationLunMappingObjectSchema"]
__pdoc__ = {
    "ApplicationLunMappingObjectSchema.resource": False,
    "ApplicationLunMappingObjectSchema.opts": False,
    "ApplicationLunMappingObject": False,
}


class ApplicationLunMappingObjectSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationLunMappingObject object"""

    fcp = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_san_access_fcp_endpoint.ApplicationSanAccessFcpEndpointSchema", unknown=EXCLUDE, allow_none=True), data_key="fcp", allow_none=True)
    r""" All possible Fibre Channel Protocol (FCP) access endpoints for the LUN. """

    igroup = marshmallow_fields.Nested("netapp_ontap.models.application_lun_mapping_object_igroup.ApplicationLunMappingObjectIgroupSchema", unknown=EXCLUDE, data_key="igroup", allow_none=True)
    r""" The igroup field of the application_lun_mapping_object. """

    iscsi = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_san_access_iscsi_endpoint.ApplicationSanAccessIscsiEndpointSchema", unknown=EXCLUDE, allow_none=True), data_key="iscsi", allow_none=True)
    r""" All possible iSCSI access endpoints for the LUN. """

    lun_id = Size(data_key="lun_id", allow_none=True)
    r""" LUN ID """

    @property
    def resource(self):
        return ApplicationLunMappingObject

    gettable_fields = [
        "fcp",
        "igroup",
        "iscsi",
        "lun_id",
    ]
    """fcp,igroup,iscsi,lun_id,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationLunMappingObject(Resource):

    _schema = ApplicationLunMappingObjectSchema
