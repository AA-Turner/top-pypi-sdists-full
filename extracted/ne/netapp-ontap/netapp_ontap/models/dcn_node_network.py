r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeNetwork", "DcnNodeNetworkSchema"]
__pdoc__ = {
    "DcnNodeNetworkSchema.resource": False,
    "DcnNodeNetworkSchema.opts": False,
    "DcnNodeNetwork": False,
}

class DcnNodeNetworkSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeNetwork object"""

    external_interface = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_network_external_interface", "DcnNodeNetworkExternalInterfaceSchema"),
                unknown=EXCLUDE,
                data_key="external_interface",
                allow_none=True
            )
    r""" Information about the configuration and state of the node's external network interface. """

    @property
    def resource(self):
        return DcnNodeNetwork

    gettable_fields = [
        "external_interface",
    ]
    """external_interface,"""

    patchable_fields = [
        "external_interface",
    ]
    """external_interface,"""

    postable_fields = [
        "external_interface",
    ]
    """external_interface,"""


class DcnNodeNetwork(Resource):

    _schema = DcnNodeNetworkSchema
