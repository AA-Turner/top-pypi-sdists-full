r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FcInterfaceResponseRecommend", "FcInterfaceResponseRecommendSchema"]
__pdoc__ = {
    "FcInterfaceResponseRecommendSchema.resource": False,
    "FcInterfaceResponseRecommendSchema.opts": False,
    "FcInterfaceResponseRecommend": False,
}


class FcInterfaceResponseRecommendSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcInterfaceResponseRecommend object"""

    messages = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.fc_interface_recommend_message.FcInterfaceRecommendMessageSchema", unknown=EXCLUDE, allow_none=True), data_key="messages", allow_none=True)
    r""" Messages describing the results of a FC network interface placement operation or evaluation of caller-proposed locations. """

    @property
    def resource(self):
        return FcInterfaceResponseRecommend

    gettable_fields = [
        "messages",
    ]
    """messages,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FcInterfaceResponseRecommend(Resource):

    _schema = FcInterfaceResponseRecommendSchema
