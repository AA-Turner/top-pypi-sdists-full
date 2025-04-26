r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsFilterRuleResponseRecords", "EmsFilterRuleResponseRecordsSchema"]
__pdoc__ = {
    "EmsFilterRuleResponseRecordsSchema.resource": False,
    "EmsFilterRuleResponseRecordsSchema.opts": False,
    "EmsFilterRuleResponseRecords": False,
}


class EmsFilterRuleResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsFilterRuleResponseRecords object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_filter_rule_response_records. """

    index = Size(data_key="index", allow_none=True)
    r""" Rule index. Rules are evaluated in ascending order. If a rule's index order is not specified during creation, the rule is appended to the end of the list.

Example: 1 """

    message_criteria = marshmallow_fields.Nested("netapp_ontap.models.ems_filter_rules_message_criteria.EmsFilterRulesMessageCriteriaSchema", unknown=EXCLUDE, data_key="message_criteria", allow_none=True)
    r""" Matching message definitions for the filter. A property must be specified. """

    parameter_criteria = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.ems_filter_rule_parameter_criteria.EmsFilterRuleParameterCriteriaSchema", unknown=EXCLUDE, allow_none=True), data_key="parameter_criteria", allow_none=True)
    r""" Parameter criteria used to match against events' parameters. Each parameter consists of a name and a value. When multiple parameter criteria are provided in a rule, all must match for the rule to be considered matched. A pattern can include one or more wildcard '*' characters. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Rule type

Valid choices:

* include
* exclude """

    @property
    def resource(self):
        return EmsFilterRuleResponseRecords

    gettable_fields = [
        "links",
        "index",
        "message_criteria",
        "parameter_criteria",
        "type",
    ]
    """links,index,message_criteria,parameter_criteria,type,"""

    patchable_fields = [
        "index",
        "message_criteria",
        "parameter_criteria",
        "type",
    ]
    """index,message_criteria,parameter_criteria,type,"""

    postable_fields = [
        "index",
        "message_criteria",
        "parameter_criteria",
        "type",
    ]
    """index,message_criteria,parameter_criteria,type,"""


class EmsFilterRuleResponseRecords(Resource):

    _schema = EmsFilterRuleResponseRecordsSchema
