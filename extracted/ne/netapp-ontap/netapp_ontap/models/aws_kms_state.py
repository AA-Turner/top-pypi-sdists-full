r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AwsKmsState", "AwsKmsStateSchema"]
__pdoc__ = {
    "AwsKmsStateSchema.resource": False,
    "AwsKmsStateSchema.opts": False,
    "AwsKmsState": False,
}


class AwsKmsStateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AwsKmsState object"""

    cluster_state = marshmallow_fields.Boolean(data_key="cluster_state", allow_none=True)
    r""" Set to true when AWS KMS key protection is available on all nodes of the cluster. """

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Code corresponding to the message. Returns a 0 if AWS KMS key protection is available on all nodes of the cluster.

Example: 346758 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message set when cluster_state is false.

Example: AWS KMS key protection is unavailable on the following nodes: node1, node2. """

    @property
    def resource(self):
        return AwsKmsState

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


class AwsKmsState(Resource):

    _schema = AwsKmsStateSchema
