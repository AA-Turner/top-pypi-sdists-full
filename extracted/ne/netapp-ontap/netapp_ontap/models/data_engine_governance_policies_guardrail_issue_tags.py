r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DataEngineGovernancePoliciesGuardrailIssueTags", "DataEngineGovernancePoliciesGuardrailIssueTagsSchema"]
__pdoc__ = {
    "DataEngineGovernancePoliciesGuardrailIssueTagsSchema.resource": False,
    "DataEngineGovernancePoliciesGuardrailIssueTagsSchema.opts": False,
    "DataEngineGovernancePoliciesGuardrailIssueTags": False,
}

class DataEngineGovernancePoliciesGuardrailIssueTagsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DataEngineGovernancePoliciesGuardrailIssueTags object"""

    classification_type = marshmallow_fields.Str(data_key="classification_type", allow_none=True)
    r""" Type of the tag. Possible values are:

* <i>data_classifier</i>: Data classifier tag.
* <i>document_classifier</i>: Document classifier tag.
* <i>data_classifier_category</i>: Data classifier category tag.
* <i>document_classifier_category</i>: Document classifier category tag.


Valid choices:

* data_classifier
* document_classifier
* data_classifier_category
* document_classifier_category """

    tag = marshmallow_fields.Str(data_key="tag", allow_none=True)
    r""" Tag of the classifier or category.

Example: CLS_ENTD00000 """

    @property
    def resource(self):
        return DataEngineGovernancePoliciesGuardrailIssueTags

    gettable_fields = [
        "classification_type",
        "tag",
    ]
    """classification_type,tag,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DataEngineGovernancePoliciesGuardrailIssueTags(Resource):

    _schema = DataEngineGovernancePoliciesGuardrailIssueTagsSchema
