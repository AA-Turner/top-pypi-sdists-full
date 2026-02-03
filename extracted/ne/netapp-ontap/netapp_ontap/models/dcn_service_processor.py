r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnServiceProcessor", "DcnServiceProcessorSchema"]
__pdoc__ = {
    "DcnServiceProcessorSchema.resource": False,
    "DcnServiceProcessorSchema.opts": False,
    "DcnServiceProcessor": False,
}

class DcnServiceProcessorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnServiceProcessor object"""

    autoupdate_enabled = marshmallow_fields.Boolean(data_key="autoupdate_enabled", allow_none=True)
    r""" Indicates whether the service processor can be automatically updated from ONTAP. """

    dhcp_enabled = marshmallow_fields.Boolean(data_key="dhcp_enabled", allow_none=True)
    r""" Set to "true" to use DHCP to configure an IPv4 interface. Do not provide values for address, netmask and gateway when set to "true". """

    firmware_version = marshmallow_fields.Str(data_key="firmware_version", allow_none=True)
    r""" The version of firmware installed. """

    ipv4_interface = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.ipv4_interface", "Ipv4InterfaceSchema"),
                unknown=EXCLUDE,
                data_key="ipv4_interface",
                allow_none=True
            )
    r""" Object to set up an interface along with its default router. """

    ipv6_interface = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.ipv6_interface", "Ipv6InterfaceSchema"),
                unknown=EXCLUDE,
                data_key="ipv6_interface",
                allow_none=True
            )
    r""" Object to setup an interface along with its default router. """

    is_ip_configured = marshmallow_fields.Boolean(data_key="is_ip_configured", allow_none=True)
    r""" Indicates whether the service processor network is configured. """

    last_update_state = marshmallow_fields.Str(data_key="last_update_state", allow_none=True)
    r""" Provides the "update status" of the last service processor update.

Valid choices:

* failed
* passed """

    link_state = marshmallow_fields.Str(data_key="link_state", allow_none=True)
    r""" The link_state field of the dcn_service_processor.

Valid choices:

* up
* down
* disabled
* unknown """

    mac_address = marshmallow_fields.Str(data_key="mac_address", allow_none=True)
    r""" The mac_address field of the dcn_service_processor. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the dcn_service_processor.

Valid choices:

* online
* offline
* degraded
* rebooting
* unknown
* updating
* node_offline
* sp_daemon_offline """

    @property
    def resource(self):
        return DcnServiceProcessor

    gettable_fields = [
        "autoupdate_enabled",
        "dhcp_enabled",
        "firmware_version",
        "ipv4_interface",
        "ipv6_interface",
        "is_ip_configured",
        "last_update_state",
        "link_state",
        "mac_address",
        "state",
    ]
    """autoupdate_enabled,dhcp_enabled,firmware_version,ipv4_interface,ipv6_interface,is_ip_configured,last_update_state,link_state,mac_address,state,"""

    patchable_fields = [
        "autoupdate_enabled",
        "dhcp_enabled",
        "ipv4_interface",
        "ipv6_interface",
    ]
    """autoupdate_enabled,dhcp_enabled,ipv4_interface,ipv6_interface,"""

    postable_fields = [
        "ipv4_interface",
    ]
    """ipv4_interface,"""


class DcnServiceProcessor(Resource):

    _schema = DcnServiceProcessorSchema
