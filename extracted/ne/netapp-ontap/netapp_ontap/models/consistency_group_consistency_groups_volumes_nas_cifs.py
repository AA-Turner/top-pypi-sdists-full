r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsVolumesNasCifs", "ConsistencyGroupConsistencyGroupsVolumesNasCifsSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsVolumesNasCifsSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsVolumesNasCifsSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsVolumesNasCifs": False,
}


class ConsistencyGroupConsistencyGroupsVolumesNasCifsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsVolumesNasCifs object"""

    shares = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.consistency_group_cifs_share.ConsistencyGroupCifsShareSchema", unknown=EXCLUDE, allow_none=True), data_key="shares", allow_none=True)
    r""" CIFS share is a named access point in a volume. Before users and applications can access data on the CIFS server over SMB,
a CIFS share must be created with sufficient share permission. CIFS shares are tied to the CIFS server on the SVM.
When a CIFS share is created, ONTAP creates a default ACL for the share with Full Control permissions for Everyone. """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsVolumesNasCifs

    gettable_fields = [
        "shares",
    ]
    """shares,"""

    patchable_fields = [
        "shares",
    ]
    """shares,"""

    postable_fields = [
        "shares",
    ]
    """shares,"""


class ConsistencyGroupConsistencyGroupsVolumesNasCifs(Resource):

    _schema = ConsistencyGroupConsistencyGroupsVolumesNasCifsSchema
