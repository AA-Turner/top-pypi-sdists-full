r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["GroupPolicyObjectRestrictAnonymous", "GroupPolicyObjectRestrictAnonymousSchema"]
__pdoc__ = {
    "GroupPolicyObjectRestrictAnonymousSchema.resource": False,
    "GroupPolicyObjectRestrictAnonymousSchema.opts": False,
    "GroupPolicyObjectRestrictAnonymous": False,
}


class GroupPolicyObjectRestrictAnonymousSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupPolicyObjectRestrictAnonymous object"""

    anonymous_access_to_shares_and_named_pipes_restricted = marshmallow_fields.Boolean(data_key="anonymous_access_to_shares_and_named_pipes_restricted", allow_none=True)
    r""" Restrict anonymous access to shares and named pipes. """

    combined_restriction_for_anonymous_user = marshmallow_fields.Str(data_key="combined_restriction_for_anonymous_user", allow_none=True)
    r""" Combined restriction for anonymous user.

Valid choices:

* no_restriction
* no_enumeration
* no_access """

    no_enumeration_of_sam_accounts = marshmallow_fields.Boolean(data_key="no_enumeration_of_sam_accounts", allow_none=True)
    r""" No enumeration of SAM accounts. """

    no_enumeration_of_sam_accounts_and_shares = marshmallow_fields.Boolean(data_key="no_enumeration_of_sam_accounts_and_shares", allow_none=True)
    r""" No enumeration of SAM accounts and shares. """

    @property
    def resource(self):
        return GroupPolicyObjectRestrictAnonymous

    gettable_fields = [
        "anonymous_access_to_shares_and_named_pipes_restricted",
        "combined_restriction_for_anonymous_user",
        "no_enumeration_of_sam_accounts",
        "no_enumeration_of_sam_accounts_and_shares",
    ]
    """anonymous_access_to_shares_and_named_pipes_restricted,combined_restriction_for_anonymous_user,no_enumeration_of_sam_accounts,no_enumeration_of_sam_accounts_and_shares,"""

    patchable_fields = [
        "anonymous_access_to_shares_and_named_pipes_restricted",
        "combined_restriction_for_anonymous_user",
        "no_enumeration_of_sam_accounts",
        "no_enumeration_of_sam_accounts_and_shares",
    ]
    """anonymous_access_to_shares_and_named_pipes_restricted,combined_restriction_for_anonymous_user,no_enumeration_of_sam_accounts,no_enumeration_of_sam_accounts_and_shares,"""

    postable_fields = [
        "anonymous_access_to_shares_and_named_pipes_restricted",
        "combined_restriction_for_anonymous_user",
        "no_enumeration_of_sam_accounts",
        "no_enumeration_of_sam_accounts_and_shares",
    ]
    """anonymous_access_to_shares_and_named_pipes_restricted,combined_restriction_for_anonymous_user,no_enumeration_of_sam_accounts,no_enumeration_of_sam_accounts_and_shares,"""


class GroupPolicyObjectRestrictAnonymous(Resource):

    _schema = GroupPolicyObjectRestrictAnonymousSchema
