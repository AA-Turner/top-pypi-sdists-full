r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BarbicanConnectivity", "BarbicanConnectivitySchema"]
__pdoc__ = {
    "BarbicanConnectivitySchema.resource": False,
    "BarbicanConnectivitySchema.opts": False,
    "BarbicanConnectivity": False,
}


class BarbicanConnectivitySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BarbicanConnectivity object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Code corresponding to the error message. Returns 0 if Barbican KMS is reachable from all nodes in the cluster.

Example: 346758 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Set to the appropriate error message when 'reachable' is false.

Example: Barbican KMS is not reachable from all nodes - <reason>. """

    reachable = marshmallow_fields.Boolean(data_key="reachable", allow_none=True)
    r""" Set to true if the Barbican KMS is reachable from all nodes of the cluster.

Example: false """

    @property
    def resource(self):
        return BarbicanConnectivity

    gettable_fields = [
        "code",
        "message",
        "reachable",
    ]
    """code,message,reachable,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class BarbicanConnectivity(Resource):

    _schema = BarbicanConnectivitySchema
