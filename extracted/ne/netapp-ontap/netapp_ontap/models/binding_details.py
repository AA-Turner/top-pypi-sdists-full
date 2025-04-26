r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BindingDetails", "BindingDetailsSchema"]
__pdoc__ = {
    "BindingDetailsSchema.resource": False,
    "BindingDetailsSchema.opts": False,
    "BindingDetails": False,
}


class BindingDetailsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BindingDetails object"""

    server = marshmallow_fields.Str(data_key="server", allow_none=True)
    r""" Hostname/IP address of the NIS server in the domain. """

    status = marshmallow_fields.Nested("netapp_ontap.models.binding_status.BindingStatusSchema", unknown=EXCLUDE, data_key="status", allow_none=True)
    r""" The status field of the binding_details. """

    @property
    def resource(self):
        return BindingDetails

    gettable_fields = [
        "server",
        "status",
    ]
    """server,status,"""

    patchable_fields = [
        "server",
        "status",
    ]
    """server,status,"""

    postable_fields = [
        "server",
        "status",
    ]
    """server,status,"""


class BindingDetails(Resource):

    _schema = BindingDetailsSchema
