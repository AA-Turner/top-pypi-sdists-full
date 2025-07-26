r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BarbicanState", "BarbicanStateSchema"]
__pdoc__ = {
    "BarbicanStateSchema.resource": False,
    "BarbicanStateSchema.opts": False,
    "BarbicanState": False,
}


class BarbicanStateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BarbicanState object"""

    cluster_state = marshmallow_fields.Boolean(data_key="cluster_state", allow_none=True)
    r""" Set to true when an SVM-KEK is present on all nodes of the cluster.

Example: false """

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Code corresponding to the status message. Returns a 0 if the SVM-KEK is available on all nodes in the cluster.

Example: 346758 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message returned when there's no SVM-KEK availability on the cluster.

Example: Top-level internal key encryption key is unavailable on the following nodes with the associated reasons: Node: node1. Reason: No volumes created yet for the SVM. Wrapped KEK status will be available after creating encrypted volumes. """

    @property
    def resource(self):
        return BarbicanState

    gettable_fields = [
        "cluster_state",
        "code",
        "message",
    ]
    """cluster_state,code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class BarbicanState(Resource):

    _schema = BarbicanStateSchema
