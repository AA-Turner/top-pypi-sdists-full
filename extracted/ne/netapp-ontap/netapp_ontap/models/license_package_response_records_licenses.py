r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LicensePackageResponseRecordsLicenses", "LicensePackageResponseRecordsLicensesSchema"]
__pdoc__ = {
    "LicensePackageResponseRecordsLicensesSchema.resource": False,
    "LicensePackageResponseRecordsLicensesSchema.opts": False,
    "LicensePackageResponseRecordsLicenses": False,
}


class LicensePackageResponseRecordsLicensesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LicensePackageResponseRecordsLicenses object"""

    active = marshmallow_fields.Boolean(data_key="active", allow_none=True)
    r""" A flag indicating whether the license is currently being enforced. """

    capacity = marshmallow_fields.Nested("netapp_ontap.models.license_capacity.LicenseCapacitySchema", unknown=EXCLUDE, data_key="capacity", allow_none=True)
    r""" The capacity field of the license_package_response_records_licenses. """

    compliance = marshmallow_fields.Nested("netapp_ontap.models.license_compliance.LicenseComplianceSchema", unknown=EXCLUDE, data_key="compliance", allow_none=True)
    r""" The compliance field of the license_package_response_records_licenses. """

    evaluation = marshmallow_fields.Boolean(data_key="evaluation", allow_none=True)
    r""" A flag indicating whether the license is in evaluation mode. """

    expiry_time = ImpreciseDateTime(data_key="expiry_time", allow_none=True)
    r""" Date and time when the license expires.

Example: 2019-03-02T19:00:00.000+0000 """

    host_id = marshmallow_fields.Str(data_key="host_id", allow_none=True)
    r""" A string that associates the license with a node or cluster.

Example: 456-44-1234 """

    installed_license = marshmallow_fields.Str(data_key="installed_license", allow_none=True)
    r""" Name of license that enabled the feature.

Example: Core Bundle """

    owner = marshmallow_fields.Str(data_key="owner", allow_none=True)
    r""" Cluster, node or license manager that owns the license.

Example: cluster1 """

    serial_number = marshmallow_fields.Str(data_key="serial_number", allow_none=True)
    r""" Serial number of the license.

Example: 123456789 """

    shutdown_imminent = marshmallow_fields.Boolean(data_key="shutdown_imminent", allow_none=True)
    r""" A flag indicating whether the Cloud ONTAP system is going to shutdown as the Cloud platform license has already expired. """

    start_time = ImpreciseDateTime(data_key="start_time", allow_none=True)
    r""" Date and time when the license starts.

Example: 2019-02-02T19:00:00.000+0000 """

    @property
    def resource(self):
        return LicensePackageResponseRecordsLicenses

    gettable_fields = [
        "active",
        "capacity",
        "compliance",
        "evaluation",
        "expiry_time",
        "host_id",
        "installed_license",
        "owner",
        "serial_number",
        "shutdown_imminent",
        "start_time",
    ]
    """active,capacity,compliance,evaluation,expiry_time,host_id,installed_license,owner,serial_number,shutdown_imminent,start_time,"""

    patchable_fields = [
        "compliance",
    ]
    """compliance,"""

    postable_fields = [
        "compliance",
    ]
    """compliance,"""


class LicensePackageResponseRecordsLicenses(Resource):

    _schema = LicensePackageResponseRecordsLicensesSchema
