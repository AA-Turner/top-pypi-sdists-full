r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterNodesControllerFailedFanMessage", "ClusterNodesControllerFailedFanMessageSchema"]
__pdoc__ = {
    "ClusterNodesControllerFailedFanMessageSchema.resource": False,
    "ClusterNodesControllerFailedFanMessageSchema.opts": False,
    "ClusterNodesControllerFailedFanMessage": False,
}


class ClusterNodesControllerFailedFanMessageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesControllerFailedFanMessage object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Error code describing the current condition of chassis fans.

Example: 111411207 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Message describing the current condition of chassis fans. It is only of use when `failed_fan.count` is not zero.

Example: There are no failed fans. """

    @property
    def resource(self):
        return ClusterNodesControllerFailedFanMessage

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ClusterNodesControllerFailedFanMessage(Resource):

    _schema = ClusterNodesControllerFailedFanMessageSchema
