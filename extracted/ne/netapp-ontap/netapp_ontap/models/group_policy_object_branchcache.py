r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["GroupPolicyObjectBranchcache", "GroupPolicyObjectBranchcacheSchema"]
__pdoc__ = {
    "GroupPolicyObjectBranchcacheSchema.resource": False,
    "GroupPolicyObjectBranchcacheSchema.opts": False,
    "GroupPolicyObjectBranchcache": False,
}


class GroupPolicyObjectBranchcacheSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the GroupPolicyObjectBranchcache object"""

    hash_publication_mode = marshmallow_fields.Str(data_key="hash_publication_mode", allow_none=True)
    r""" Hash publication mode.

Valid choices:

* per_share
* disabled
* all_shares """

    supported_hash_version = marshmallow_fields.Str(data_key="supported_hash_version", allow_none=True)
    r""" Hash version.

Valid choices:

* version1
* version2
* all_versions """

    @property
    def resource(self):
        return GroupPolicyObjectBranchcache

    gettable_fields = [
        "hash_publication_mode",
        "supported_hash_version",
    ]
    """hash_publication_mode,supported_hash_version,"""

    patchable_fields = [
        "hash_publication_mode",
        "supported_hash_version",
    ]
    """hash_publication_mode,supported_hash_version,"""

    postable_fields = [
        "hash_publication_mode",
        "supported_hash_version",
    ]
    """hash_publication_mode,supported_hash_version,"""


class GroupPolicyObjectBranchcache(Resource):

    _schema = GroupPolicyObjectBranchcacheSchema
