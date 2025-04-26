r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LicensePackageResponseRecords", "LicensePackageResponseRecordsSchema"]
__pdoc__ = {
    "LicensePackageResponseRecordsSchema.resource": False,
    "LicensePackageResponseRecordsSchema.opts": False,
    "LicensePackageResponseRecords": False,
}


class LicensePackageResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LicensePackageResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the license_package_response_records. """

    description = marshmallow_fields.Str(data_key="description", allow_none=True)
    r""" License description

Example: NFS License """

    entitlement = marshmallow_fields.Nested("netapp_ontap.models.entitlement.EntitlementSchema", unknown=EXCLUDE, data_key="entitlement", allow_none=True)
    r""" The entitlement field of the license_package_response_records. """

    keys = marshmallow_fields.List(marshmallow_fields.Str, data_key="keys", allow_none=True)
    r""" The keys field of the license_package_response_records. """

    licenses = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.license_package_licenses.LicensePackageLicensesSchema", unknown=EXCLUDE, allow_none=True), data_key="licenses", allow_none=True)
    r""" Installed licenses of the package. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the license.

Example: NFS """

    scope = marshmallow_fields.Str(data_key="scope", allow_none=True)
    r""" Scope of the license.

Valid choices:

* not_available
* site
* cluster
* node """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Summary state of package based on all installed licenses.

Valid choices:

* compliant
* noncompliant
* unlicensed
* unknown """

    @property
    def resource(self):
        return LicensePackageResponseRecords

    gettable_fields = [
        "links",
        "description",
        "entitlement",
        "licenses",
        "name",
        "scope",
        "state",
    ]
    """links,description,entitlement,licenses,name,scope,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "keys",
    ]
    """keys,"""


class LicensePackageResponseRecords(Resource):

    _schema = LicensePackageResponseRecordsSchema
