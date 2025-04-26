r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IpInterfaceResponseRecommend", "IpInterfaceResponseRecommendSchema"]
__pdoc__ = {
    "IpInterfaceResponseRecommendSchema.resource": False,
    "IpInterfaceResponseRecommendSchema.opts": False,
    "IpInterfaceResponseRecommend": False,
}


class IpInterfaceResponseRecommendSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IpInterfaceResponseRecommend object"""

    messages = marshmallow_fields.List(marshmallow_fields.Str, data_key="messages", allow_none=True)
    r""" Messages describing the results of a LIF recommendation request. """

    @property
    def resource(self):
        return IpInterfaceResponseRecommend

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


class IpInterfaceResponseRecommend(Resource):

    _schema = IpInterfaceResponseRecommendSchema
