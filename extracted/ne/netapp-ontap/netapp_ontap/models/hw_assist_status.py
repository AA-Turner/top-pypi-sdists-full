r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["HwAssistStatus", "HwAssistStatusSchema"]
__pdoc__ = {
    "HwAssistStatusSchema.resource": False,
    "HwAssistStatusSchema.opts": False,
    "HwAssistStatus": False,
}


class HwAssistStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the HwAssistStatus object"""

    ip = marshmallow_fields.Str(data_key="ip", allow_none=True)
    r""" The hardware assist IP address. """

    port = Size(data_key="port", allow_none=True)
    r""" The hardware assist port. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The hardware assist monitor status.

Valid choices:

* active
* inactive """

    @property
    def resource(self):
        return HwAssistStatus

    gettable_fields = [
        "ip",
        "port",
        "state",
    ]
    """ip,port,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class HwAssistStatus(Resource):

    _schema = HwAssistStatusSchema
