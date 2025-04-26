r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PoliciesAndRulesToBeAppliedToBeApplied", "PoliciesAndRulesToBeAppliedToBeAppliedSchema"]
__pdoc__ = {
    "PoliciesAndRulesToBeAppliedToBeAppliedSchema.resource": False,
    "PoliciesAndRulesToBeAppliedToBeAppliedSchema.opts": False,
    "PoliciesAndRulesToBeAppliedToBeApplied": False,
}


class PoliciesAndRulesToBeAppliedToBeAppliedSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PoliciesAndRulesToBeAppliedToBeApplied object"""

    access_policies = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.group_policy_object_central_access_policy.GroupPolicyObjectCentralAccessPolicySchema", unknown=EXCLUDE, allow_none=True), data_key="access_policies", allow_none=True)
    r""" The access_policies field of the policies_and_rules_to_be_applied_to_be_applied. """

    access_rules = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.group_policy_object_central_access_rule.GroupPolicyObjectCentralAccessRuleSchema", unknown=EXCLUDE, allow_none=True), data_key="access_rules", allow_none=True)
    r""" The access_rules field of the policies_and_rules_to_be_applied_to_be_applied. """

    objects = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.group_policy_object.GroupPolicyObjectSchema", unknown=EXCLUDE, allow_none=True), data_key="objects", allow_none=True)
    r""" The objects field of the policies_and_rules_to_be_applied_to_be_applied. """

    restricted_groups = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.resources.group_policy_object_restricted_group.GroupPolicyObjectRestrictedGroupSchema", unknown=EXCLUDE, allow_none=True), data_key="restricted_groups", allow_none=True)
    r""" The restricted_groups field of the policies_and_rules_to_be_applied_to_be_applied. """

    @property
    def resource(self):
        return PoliciesAndRulesToBeAppliedToBeApplied

    gettable_fields = [
        "access_policies",
        "access_rules",
        "objects",
        "restricted_groups",
    ]
    """access_policies,access_rules,objects,restricted_groups,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class PoliciesAndRulesToBeAppliedToBeApplied(Resource):

    _schema = PoliciesAndRulesToBeAppliedToBeAppliedSchema
