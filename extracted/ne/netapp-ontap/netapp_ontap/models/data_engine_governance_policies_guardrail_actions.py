r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernancePoliciesGuardrailActions", "DataEngineGovernancePoliciesGuardrailActionsSchema"]
__pdoc__ = {
    "DataEngineGovernancePoliciesGuardrailActionsSchema.resource": False,
    "DataEngineGovernancePoliciesGuardrailActionsSchema.opts": False,
    "DataEngineGovernancePoliciesGuardrailActions": False,
}

class DataEngineGovernancePoliciesGuardrailActionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernancePoliciesGuardrailActions object"""

    action_type = marshmallow_fields.Str(data_key="action_type", allow_none=True)
    r""" specifies type of action. Possible values are:

* <i>exclude</i>: Exclude data.
* <i>exclude_pre_existing</i>: Exclude pre-existing data.
* <i>anonymize</i>: Anonymize data.


Valid choices:

* exclude
* exclude_pre_existing
* anonymize """

    @property
    def resource(self):
        return DataEngineGovernancePoliciesGuardrailActions

    gettable_fields = [
        "action_type",
    ]
    """action_type,"""

    patchable_fields = [
        "action_type",
    ]
    """action_type,"""

    postable_fields = [
        "action_type",
    ]
    """action_type,"""


class DataEngineGovernancePoliciesGuardrailActions(Resource):

    _schema = DataEngineGovernancePoliciesGuardrailActionsSchema
