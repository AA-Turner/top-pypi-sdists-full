r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MediatorPingError", "MediatorPingErrorSchema"]
__pdoc__ = {
    "MediatorPingErrorSchema.resource": False,
    "MediatorPingErrorSchema.opts": False,
    "MediatorPingError": False,
}


class MediatorPingErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MediatorPingError object"""

    configurable = marshmallow_fields.Boolean(data_key="configurable", allow_none=True)
    r""" Indicates if the BlueXP cloud mediator is configurable. This depends on whether the ping latency is within a threshold.

Example: false """

    error = marshmallow_fields.Nested("netapp_ontap.models.mediator_ping_error_error.MediatorPingErrorErrorSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the mediator_ping_error. """

    reachable = marshmallow_fields.Boolean(data_key="reachable", allow_none=True)
    r""" Ping status of the BlueXP cloud service.

Example: false """

    @property
    def resource(self):
        return MediatorPingError

    gettable_fields = [
        "configurable",
        "error",
        "reachable",
    ]
    """configurable,error,reachable,"""

    patchable_fields = [
        "error",
    ]
    """error,"""

    postable_fields = [
        "error",
    ]
    """error,"""


class MediatorPingError(Resource):

    _schema = MediatorPingErrorSchema
