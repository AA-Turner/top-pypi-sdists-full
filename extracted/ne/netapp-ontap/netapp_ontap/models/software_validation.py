r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareValidation", "SoftwareValidationSchema"]
__pdoc__ = {
    "SoftwareValidationSchema.resource": False,
    "SoftwareValidationSchema.opts": False,
    "SoftwareValidation": False,
}


class SoftwareValidationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareValidation object"""

    action = marshmallow_fields.Nested("netapp_ontap.models.software_validation_reference_action.SoftwareValidationReferenceActionSchema", unknown=EXCLUDE, data_key="action", allow_none=True)
    r""" The action field of the software_validation. """

    issue = marshmallow_fields.Nested("netapp_ontap.models.software_validation_reference_issue.SoftwareValidationReferenceIssueSchema", unknown=EXCLUDE, data_key="issue", allow_none=True)
    r""" The issue field of the software_validation. """

    status = marshmallow_fields.Str(data_key="status", allow_none=True)
    r""" Status of the update check.

Valid choices:

* warning
* error """

    update_check = marshmallow_fields.Str(data_key="update_check", allow_none=True)
    r""" Name of the update check.

Example: nfs_mounts """

    @property
    def resource(self):
        return SoftwareValidation

    gettable_fields = [
        "action",
        "issue",
        "status",
        "update_check",
    ]
    """action,issue,status,update_check,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SoftwareValidation(Resource):

    _schema = SoftwareValidationSchema
