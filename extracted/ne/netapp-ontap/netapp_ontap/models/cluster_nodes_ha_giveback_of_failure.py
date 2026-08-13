r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ClusterNodesHaGivebackOfFailure", "ClusterNodesHaGivebackOfFailureSchema"]
__pdoc__ = {
    "ClusterNodesHaGivebackOfFailureSchema.resource": False,
    "ClusterNodesHaGivebackOfFailureSchema.opts": False,
    "ClusterNodesHaGivebackOfFailure": False,
}

class ClusterNodesHaGivebackOfFailureSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaGivebackOfFailure object"""

    code = Size(data_key="code", allow_none=True)
    r""" Message code

Example: 852126 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Detailed message based on the state.

Example: Failed to initiate giveback. Run the "storage failover" command for more information. """

    @property
    def resource(self):
        return ClusterNodesHaGivebackOfFailure

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    postable_fields = [
        "code",
        "message",
    ]
    """code,message,"""


class ClusterNodesHaGivebackOfFailure(Resource):

    _schema = ClusterNodesHaGivebackOfFailureSchema
