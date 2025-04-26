r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LicenseManagerResponseRecords", "LicenseManagerResponseRecordsSchema"]
__pdoc__ = {
    "LicenseManagerResponseRecordsSchema.resource": False,
    "LicenseManagerResponseRecordsSchema.opts": False,
    "LicenseManagerResponseRecords": False,
}


class LicenseManagerResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LicenseManagerResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the license_manager_response_records. """

    default = marshmallow_fields.Boolean(data_key="default", allow_none=True)
    r""" Flag that indicates whether it's the default license manager instance used by the cluster.'
When a capacity pool is created and if the license manager field is omitted, it is assumed that the license of the capacity pool is installed on the default license manager instance. """

    uri = marshmallow_fields.Nested("netapp_ontap.models.license_manager_uri.LicenseManagerUriSchema", unknown=EXCLUDE, data_key="uri", allow_none=True)
    r""" License manager URI. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the license_manager_response_records.

Example: 4ea7a442-86d1-11e0-ae1c-112233445566 """

    @property
    def resource(self):
        return LicenseManagerResponseRecords

    gettable_fields = [
        "links",
        "default",
        "uri",
        "uuid",
    ]
    """links,default,uri,uuid,"""

    patchable_fields = [
        "uri",
    ]
    """uri,"""

    postable_fields = [
        "uri",
    ]
    """uri,"""


class LicenseManagerResponseRecords(Resource):

    _schema = LicenseManagerResponseRecordsSchema
