r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernancePoliciesGuardrailConditions", "DataEngineGovernancePoliciesGuardrailConditionsSchema"]
__pdoc__ = {
    "DataEngineGovernancePoliciesGuardrailConditionsSchema.resource": False,
    "DataEngineGovernancePoliciesGuardrailConditionsSchema.opts": False,
    "DataEngineGovernancePoliciesGuardrailConditions": False,
}

class DataEngineGovernancePoliciesGuardrailConditionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernancePoliciesGuardrailConditions object"""

    items = marshmallow_fields.List(marshmallow_fields.Str, data_key="items", allow_none=True)
    r""" List of classifier or category tags associated with the condition. """

    operator = marshmallow_fields.Str(data_key="operator", allow_none=True)
    r""" specifies operator for condition. Possible values are:

* <i>all</i>: All conditions must be met.
* <i>any</i>: Any one of the conditions must be met.


Valid choices:

* all
* any """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" specifies type of condition. Possible values are:

* <i>data_classifier_category</i>: Condition based on data classifier category.
* <i>document_classifier_category</i>: Condition based on document classifier category.
* <i>data_classifier</i>: Condition based on data classifier.
* <i>document_classifier</i>: Condition based on document classifier.


Valid choices:

* data_classifier_category
* document_classifier_category
* data_classifier
* document_classifier """

    @property
    def resource(self):
        return DataEngineGovernancePoliciesGuardrailConditions

    gettable_fields = [
        "items",
        "operator",
        "type",
    ]
    """items,operator,type,"""

    patchable_fields = [
        "items",
        "operator",
        "type",
    ]
    """items,operator,type,"""

    postable_fields = [
        "items",
        "operator",
        "type",
    ]
    """items,operator,type,"""


class DataEngineGovernancePoliciesGuardrailConditions(Resource):

    _schema = DataEngineGovernancePoliciesGuardrailConditionsSchema
