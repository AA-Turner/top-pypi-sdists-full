r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MultiAdminVerifyApprovalGroupOwner", "MultiAdminVerifyApprovalGroupOwnerSchema"]
__pdoc__ = {
    "MultiAdminVerifyApprovalGroupOwnerSchema.resource": False,
    "MultiAdminVerifyApprovalGroupOwnerSchema.opts": False,
    "MultiAdminVerifyApprovalGroupOwner": False,
}


class MultiAdminVerifyApprovalGroupOwnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MultiAdminVerifyApprovalGroupOwner object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the multi_admin_verify_approval_group_owner. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the SVM. This field cannot be specified in a POST or PATCH method.


Example: svm1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the SVM. This field cannot be specified in a PATCH method.


Example: 02c9e252-41be-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return MultiAdminVerifyApprovalGroupOwner

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class MultiAdminVerifyApprovalGroupOwner(Resource):

    _schema = MultiAdminVerifyApprovalGroupOwnerSchema
