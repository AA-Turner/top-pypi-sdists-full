r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsFilterRulesMessageCriteria", "EmsFilterRulesMessageCriteriaSchema"]
__pdoc__ = {
    "EmsFilterRulesMessageCriteriaSchema.resource": False,
    "EmsFilterRulesMessageCriteriaSchema.opts": False,
    "EmsFilterRulesMessageCriteria": False,
}


class EmsFilterRulesMessageCriteriaSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsFilterRulesMessageCriteria object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.related_link.RelatedLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the ems_filter_rules_message_criteria. """

    name_pattern = marshmallow_fields.Str(data_key="name_pattern", allow_none=True)
    r""" Message name filter on which to match. Supports wildcards. Defaults to * if not specified.

Example: wafl.* """

    severities = marshmallow_fields.Str(data_key="severities", allow_none=True)
    r""" A comma-separated list of severities or a wildcard.

Example: emergency,alert,error """

    snmp_trap_types = marshmallow_fields.Str(data_key="snmp_trap_types", allow_none=True)
    r""" A comma separated list of snmp_trap_types or a wildcard.

Example: standard,built_in """

    @property
    def resource(self):
        return EmsFilterRulesMessageCriteria

    gettable_fields = [
        "links",
        "name_pattern",
        "severities",
        "snmp_trap_types",
    ]
    """links,name_pattern,severities,snmp_trap_types,"""

    patchable_fields = [
        "name_pattern",
        "severities",
        "snmp_trap_types",
    ]
    """name_pattern,severities,snmp_trap_types,"""

    postable_fields = [
        "name_pattern",
        "severities",
        "snmp_trap_types",
    ]
    """name_pattern,severities,snmp_trap_types,"""


class EmsFilterRulesMessageCriteria(Resource):

    _schema = EmsFilterRulesMessageCriteriaSchema
