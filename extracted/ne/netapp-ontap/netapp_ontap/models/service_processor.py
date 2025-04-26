r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ServiceProcessor", "ServiceProcessorSchema"]
__pdoc__ = {
    "ServiceProcessorSchema.resource": False,
    "ServiceProcessorSchema.opts": False,
    "ServiceProcessor": False,
}


class ServiceProcessorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ServiceProcessor object"""

    api_service = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_service_processor_api_service.ClusterNodesServiceProcessorApiServiceSchema", unknown=EXCLUDE, data_key="api_service", allow_none=True)
    r""" Provides the properties of the service processor (SP) or baseboard management controller (BMC) API service. """

    auto_config = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_service_processor_auto_config.ClusterNodesServiceProcessorAutoConfigSchema", unknown=EXCLUDE, data_key="auto_config", allow_none=True)
    r""" Provides the properties of the service processor auto configuration. """

    autoupdate_enabled = marshmallow_fields.Boolean(data_key="autoupdate_enabled", allow_none=True)
    r""" Indicates whether the service processor can be automatically updated from ONTAP. """

    backup = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_service_processor_backup.ClusterNodesServiceProcessorBackupSchema", unknown=EXCLUDE, data_key="backup", allow_none=True)
    r""" Provides the properties of the service processor backup partition. """

    dhcp_enabled = marshmallow_fields.Boolean(data_key="dhcp_enabled", allow_none=True)
    r""" Set to "true" to use DHCP to configure an IPv4 interface. Do not provide values for address, netmask and gateway when set to "true". """

    firmware_version = marshmallow_fields.Str(data_key="firmware_version", allow_none=True)
    r""" The version of firmware installed. """

    ipv4_interface = marshmallow_fields.Nested("netapp_ontap.models.ipv4_interface.Ipv4InterfaceSchema", unknown=EXCLUDE, data_key="ipv4_interface", allow_none=True)
    r""" Object to set up an interface along with its default router. """

    ipv6_interface = marshmallow_fields.Nested("netapp_ontap.models.ipv6_interface.Ipv6InterfaceSchema", unknown=EXCLUDE, data_key="ipv6_interface", allow_none=True)
    r""" Object to setup an interface along with its default router. """

    is_ip_configured = marshmallow_fields.Boolean(data_key="is_ip_configured", allow_none=True)
    r""" Indicates whether the service processor network is configured. """

    last_update_state = marshmallow_fields.Str(data_key="last_update_state", allow_none=True)
    r""" Provides the "update status" of the last service processor update.

Valid choices:

* failed
* passed """

    link_status = marshmallow_fields.Str(data_key="link_status", allow_none=True)
    r""" The link_status field of the service_processor.

Valid choices:

* up
* down
* disabled
* unknown """

    mac_address = marshmallow_fields.Str(data_key="mac_address", allow_none=True)
    r""" The mac_address field of the service_processor. """

    primary = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_service_processor_primary.ClusterNodesServiceProcessorPrimarySchema", unknown=EXCLUDE, data_key="primary", allow_none=True)
    r""" Provides the properties of the service processor primary partition. """

    ssh_info = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_service_processor_ssh_info.ClusterNodesServiceProcessorSshInfoSchema", unknown=EXCLUDE, data_key="ssh_info", allow_none=True)
    r""" Service processor SSH allowed IP address configuration applied across the cluster. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the service_processor.

Valid choices:

* online
* offline
* degraded
* rebooting
* unknown
* updating
* node_offline
* sp_daemon_offline """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the service_processor.

Valid choices:

* sp
* none
* bmc """

    web_service = marshmallow_fields.Nested("netapp_ontap.models.cluster_nodes_service_processor_web_service.ClusterNodesServiceProcessorWebServiceSchema", unknown=EXCLUDE, data_key="web_service", allow_none=True)
    r""" Provides the properties of SP or BMC web service. """

    @property
    def resource(self):
        return ServiceProcessor

    gettable_fields = [
        "api_service",
        "auto_config",
        "autoupdate_enabled",
        "backup",
        "dhcp_enabled",
        "firmware_version",
        "ipv4_interface",
        "ipv6_interface",
        "is_ip_configured",
        "last_update_state",
        "link_status",
        "mac_address",
        "primary",
        "ssh_info",
        "state",
        "type",
        "web_service",
    ]
    """api_service,auto_config,autoupdate_enabled,backup,dhcp_enabled,firmware_version,ipv4_interface,ipv6_interface,is_ip_configured,last_update_state,link_status,mac_address,primary,ssh_info,state,type,web_service,"""

    patchable_fields = [
        "autoupdate_enabled",
        "dhcp_enabled",
        "ipv4_interface",
        "ipv6_interface",
        "ssh_info",
    ]
    """autoupdate_enabled,dhcp_enabled,ipv4_interface,ipv6_interface,ssh_info,"""

    postable_fields = [
        "ipv4_interface",
        "ssh_info",
    ]
    """ipv4_interface,ssh_info,"""


class ServiceProcessor(Resource):

    _schema = ServiceProcessorSchema
