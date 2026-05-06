import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.core_states import CoreStates
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_instance_marketplace_offering_plugin_options_type_0 import (
        OpenStackInstanceMarketplaceOfferingPluginOptionsType0,
    )
    from ..models.open_stack_nested_floating_ip import OpenStackNestedFloatingIP
    from ..models.open_stack_nested_port import OpenStackNestedPort
    from ..models.open_stack_nested_security_group import OpenStackNestedSecurityGroup
    from ..models.open_stack_nested_server_group import OpenStackNestedServerGroup
    from ..models.open_stack_nested_volume import OpenStackNestedVolume
    from ..models.rancher_cluster_reference import RancherClusterReference


T = TypeVar("T", bound="OpenStackInstance")


@_attrs_define
class OpenStackInstance:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        service_name (Union[Unset, str]):
        service_settings (Union[Unset, str]): OpenStack provider settings
        service_settings_uuid (Union[Unset, UUID]):
        service_settings_state (Union[Unset, str]):
        service_settings_error_message (Union[Unset, str]):
        project (Union[Unset, str]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_abbreviation (Union[Unset, str]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        resource_type (Union[Unset, str]):
        state (Union[Unset, CoreStates]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        backend_id (Union[None, Unset, str]): Instance ID in the OpenStack backend
        access_url (Union[None, Unset, list[str], str]):
        start_time (Union[None, Unset, datetime.datetime]):
        cores (Union[Unset, int]): Number of cores in a VM
        ram (Union[Unset, int]): Memory size in MiB
        disk (Union[Unset, int]): Disk size in MiB
        min_ram (Union[Unset, int]): Minimum memory size in MiB
        min_disk (Union[Unset, int]): Minimum disk size in MiB
        user_data (Union[Unset, str]): Additional data that will be added to instance on provisioning
        external_ips (Union[Unset, list[str]]):
        internal_ips (Union[Unset, list[str]]):
        latitude (Union[None, Unset, float]):
        longitude (Union[None, Unset, float]):
        key_name (Union[Unset, str]):
        key_fingerprint (Union[Unset, str]):
        image_name (Union[Unset, str]):
        flavor_disk (Union[Unset, int]): Flavor disk size in MiB
        flavor_name (Union[Unset, str]): Name of the flavor used by this instance
        volumes (Union[Unset, list['OpenStackNestedVolume']]): List of volumes attached to the instance
        security_groups (Union[Unset, list['OpenStackNestedSecurityGroup']]):
        server_group (Union[Unset, OpenStackNestedServerGroup]):
        floating_ips (Union[Unset, list['OpenStackNestedFloatingIP']]):
        ports (Union[Unset, list['OpenStackNestedPort']]):
        availability_zone (Union[None, Unset, str]): Availability zone where this instance is located
        availability_zone_name (Union[Unset, str]): Name of the availability zone where instance is located
        connect_directly_to_external_network (Union[Unset, bool]): If True, instance will be connected directly to
            external network
        runtime_state (Union[Unset, str]):
        action (Union[Unset, str]):
        action_details (Union[Unset, Any]): Details about ongoing or completed actions
        tenant_uuid (Union[Unset, UUID]): UUID of the OpenStack tenant
        hypervisor_hostname (Union[Unset, str]): Name of the hypervisor hosting this instance
        tenant (Union[Unset, str]): The OpenStack tenant to create the instance in
        external_address (Union[Unset, list[str]]):
        rancher_cluster (Union['RancherClusterReference', None, Unset]):
        marketplace_offering_uuid (Union[None, Unset, str]):
        marketplace_offering_name (Union[None, Unset, str]):
        marketplace_offering_type (Union[None, Unset, str]):
        marketplace_offering_plugin_options (Union['OpenStackInstanceMarketplaceOfferingPluginOptionsType0', None,
            Unset]):
        marketplace_category_uuid (Union[None, Unset, str]):
        marketplace_category_name (Union[None, Unset, str]):
        marketplace_resource_uuid (Union[None, Unset, str]):
        marketplace_plan_uuid (Union[None, Unset, str]):
        marketplace_resource_state (Union[None, Unset, str]):
        is_usage_based (Union[None, Unset, bool]):
        is_limit_based (Union[None, Unset, bool]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    service_name: Union[Unset, str] = UNSET
    service_settings: Union[Unset, str] = UNSET
    service_settings_uuid: Union[Unset, UUID] = UNSET
    service_settings_state: Union[Unset, str] = UNSET
    service_settings_error_message: Union[Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, UUID] = UNSET
    customer: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_native_name: Union[Unset, str] = UNSET
    customer_abbreviation: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    resource_type: Union[Unset, str] = UNSET
    state: Union[Unset, CoreStates] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    backend_id: Union[None, Unset, str] = UNSET
    access_url: Union[None, Unset, list[str], str] = UNSET
    start_time: Union[None, Unset, datetime.datetime] = UNSET
    cores: Union[Unset, int] = UNSET
    ram: Union[Unset, int] = UNSET
    disk: Union[Unset, int] = UNSET
    min_ram: Union[Unset, int] = UNSET
    min_disk: Union[Unset, int] = UNSET
    user_data: Union[Unset, str] = UNSET
    external_ips: Union[Unset, list[str]] = UNSET
    internal_ips: Union[Unset, list[str]] = UNSET
    latitude: Union[None, Unset, float] = UNSET
    longitude: Union[None, Unset, float] = UNSET
    key_name: Union[Unset, str] = UNSET
    key_fingerprint: Union[Unset, str] = UNSET
    image_name: Union[Unset, str] = UNSET
    flavor_disk: Union[Unset, int] = UNSET
    flavor_name: Union[Unset, str] = UNSET
    volumes: Union[Unset, list["OpenStackNestedVolume"]] = UNSET
    security_groups: Union[Unset, list["OpenStackNestedSecurityGroup"]] = UNSET
    server_group: Union[Unset, "OpenStackNestedServerGroup"] = UNSET
    floating_ips: Union[Unset, list["OpenStackNestedFloatingIP"]] = UNSET
    ports: Union[Unset, list["OpenStackNestedPort"]] = UNSET
    availability_zone: Union[None, Unset, str] = UNSET
    availability_zone_name: Union[Unset, str] = UNSET
    connect_directly_to_external_network: Union[Unset, bool] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    action: Union[Unset, str] = UNSET
    action_details: Union[Unset, Any] = UNSET
    tenant_uuid: Union[Unset, UUID] = UNSET
    hypervisor_hostname: Union[Unset, str] = UNSET
    tenant: Union[Unset, str] = UNSET
    external_address: Union[Unset, list[str]] = UNSET
    rancher_cluster: Union["RancherClusterReference", None, Unset] = UNSET
    marketplace_offering_uuid: Union[None, Unset, str] = UNSET
    marketplace_offering_name: Union[None, Unset, str] = UNSET
    marketplace_offering_type: Union[None, Unset, str] = UNSET
    marketplace_offering_plugin_options: Union[
        "OpenStackInstanceMarketplaceOfferingPluginOptionsType0", None, Unset
    ] = UNSET
    marketplace_category_uuid: Union[None, Unset, str] = UNSET
    marketplace_category_name: Union[None, Unset, str] = UNSET
    marketplace_resource_uuid: Union[None, Unset, str] = UNSET
    marketplace_plan_uuid: Union[None, Unset, str] = UNSET
    marketplace_resource_state: Union[None, Unset, str] = UNSET
    is_usage_based: Union[None, Unset, bool] = UNSET
    is_limit_based: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.open_stack_instance_marketplace_offering_plugin_options_type_0 import (
            OpenStackInstanceMarketplaceOfferingPluginOptionsType0,
        )
        from ..models.rancher_cluster_reference import RancherClusterReference

        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        description = self.description

        service_name = self.service_name

        service_settings = self.service_settings

        service_settings_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.service_settings_uuid, Unset):
            service_settings_uuid = str(self.service_settings_uuid)

        service_settings_state = self.service_settings_state

        service_settings_error_message = self.service_settings_error_message

        project = self.project

        project_name = self.project_name

        project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.project_uuid, Unset):
            project_uuid = str(self.project_uuid)

        customer = self.customer

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        customer_native_name = self.customer_native_name

        customer_abbreviation = self.customer_abbreviation

        error_message = self.error_message

        error_traceback = self.error_traceback

        resource_type = self.resource_type

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        access_url: Union[None, Unset, list[str], str]
        if isinstance(self.access_url, Unset):
            access_url = UNSET
        elif isinstance(self.access_url, list):
            access_url = self.access_url

        else:
            access_url = self.access_url

        start_time: Union[None, Unset, str]
        if isinstance(self.start_time, Unset):
            start_time = UNSET
        elif isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        cores = self.cores

        ram = self.ram

        disk = self.disk

        min_ram = self.min_ram

        min_disk = self.min_disk

        user_data = self.user_data

        external_ips: Union[Unset, list[str]] = UNSET
        if not isinstance(self.external_ips, Unset):
            external_ips = self.external_ips

        internal_ips: Union[Unset, list[str]] = UNSET
        if not isinstance(self.internal_ips, Unset):
            internal_ips = self.internal_ips

        latitude: Union[None, Unset, float]
        if isinstance(self.latitude, Unset):
            latitude = UNSET
        else:
            latitude = self.latitude

        longitude: Union[None, Unset, float]
        if isinstance(self.longitude, Unset):
            longitude = UNSET
        else:
            longitude = self.longitude

        key_name = self.key_name

        key_fingerprint = self.key_fingerprint

        image_name = self.image_name

        flavor_disk = self.flavor_disk

        flavor_name = self.flavor_name

        volumes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.volumes, Unset):
            volumes = []
            for volumes_item_data in self.volumes:
                volumes_item = volumes_item_data.to_dict()
                volumes.append(volumes_item)

        security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = []
            for security_groups_item_data in self.security_groups:
                security_groups_item = security_groups_item_data.to_dict()
                security_groups.append(security_groups_item)

        server_group: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.server_group, Unset):
            server_group = self.server_group.to_dict()

        floating_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.floating_ips, Unset):
            floating_ips = []
            for floating_ips_item_data in self.floating_ips:
                floating_ips_item = floating_ips_item_data.to_dict()
                floating_ips.append(floating_ips_item)

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for ports_item_data in self.ports:
                ports_item = ports_item_data.to_dict()
                ports.append(ports_item)

        availability_zone: Union[None, Unset, str]
        if isinstance(self.availability_zone, Unset):
            availability_zone = UNSET
        else:
            availability_zone = self.availability_zone

        availability_zone_name = self.availability_zone_name

        connect_directly_to_external_network = self.connect_directly_to_external_network

        runtime_state = self.runtime_state

        action = self.action

        action_details = self.action_details

        tenant_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.tenant_uuid, Unset):
            tenant_uuid = str(self.tenant_uuid)

        hypervisor_hostname = self.hypervisor_hostname

        tenant = self.tenant

        external_address: Union[Unset, list[str]] = UNSET
        if not isinstance(self.external_address, Unset):
            external_address = self.external_address

        rancher_cluster: Union[None, Unset, dict[str, Any]]
        if isinstance(self.rancher_cluster, Unset):
            rancher_cluster = UNSET
        elif isinstance(self.rancher_cluster, RancherClusterReference):
            rancher_cluster = self.rancher_cluster.to_dict()
        else:
            rancher_cluster = self.rancher_cluster

        marketplace_offering_uuid: Union[None, Unset, str]
        if isinstance(self.marketplace_offering_uuid, Unset):
            marketplace_offering_uuid = UNSET
        else:
            marketplace_offering_uuid = self.marketplace_offering_uuid

        marketplace_offering_name: Union[None, Unset, str]
        if isinstance(self.marketplace_offering_name, Unset):
            marketplace_offering_name = UNSET
        else:
            marketplace_offering_name = self.marketplace_offering_name

        marketplace_offering_type: Union[None, Unset, str]
        if isinstance(self.marketplace_offering_type, Unset):
            marketplace_offering_type = UNSET
        else:
            marketplace_offering_type = self.marketplace_offering_type

        marketplace_offering_plugin_options: Union[None, Unset, dict[str, Any]]
        if isinstance(self.marketplace_offering_plugin_options, Unset):
            marketplace_offering_plugin_options = UNSET
        elif isinstance(
            self.marketplace_offering_plugin_options, OpenStackInstanceMarketplaceOfferingPluginOptionsType0
        ):
            marketplace_offering_plugin_options = self.marketplace_offering_plugin_options.to_dict()
        else:
            marketplace_offering_plugin_options = self.marketplace_offering_plugin_options

        marketplace_category_uuid: Union[None, Unset, str]
        if isinstance(self.marketplace_category_uuid, Unset):
            marketplace_category_uuid = UNSET
        else:
            marketplace_category_uuid = self.marketplace_category_uuid

        marketplace_category_name: Union[None, Unset, str]
        if isinstance(self.marketplace_category_name, Unset):
            marketplace_category_name = UNSET
        else:
            marketplace_category_name = self.marketplace_category_name

        marketplace_resource_uuid: Union[None, Unset, str]
        if isinstance(self.marketplace_resource_uuid, Unset):
            marketplace_resource_uuid = UNSET
        else:
            marketplace_resource_uuid = self.marketplace_resource_uuid

        marketplace_plan_uuid: Union[None, Unset, str]
        if isinstance(self.marketplace_plan_uuid, Unset):
            marketplace_plan_uuid = UNSET
        else:
            marketplace_plan_uuid = self.marketplace_plan_uuid

        marketplace_resource_state: Union[None, Unset, str]
        if isinstance(self.marketplace_resource_state, Unset):
            marketplace_resource_state = UNSET
        else:
            marketplace_resource_state = self.marketplace_resource_state

        is_usage_based: Union[None, Unset, bool]
        if isinstance(self.is_usage_based, Unset):
            is_usage_based = UNSET
        else:
            is_usage_based = self.is_usage_based

        is_limit_based: Union[None, Unset, bool]
        if isinstance(self.is_limit_based, Unset):
            is_limit_based = UNSET
        else:
            is_limit_based = self.is_limit_based

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if service_name is not UNSET:
            field_dict["service_name"] = service_name
        if service_settings is not UNSET:
            field_dict["service_settings"] = service_settings
        if service_settings_uuid is not UNSET:
            field_dict["service_settings_uuid"] = service_settings_uuid
        if service_settings_state is not UNSET:
            field_dict["service_settings_state"] = service_settings_state
        if service_settings_error_message is not UNSET:
            field_dict["service_settings_error_message"] = service_settings_error_message
        if project is not UNSET:
            field_dict["project"] = project
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if customer is not UNSET:
            field_dict["customer"] = customer
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_native_name is not UNSET:
            field_dict["customer_native_name"] = customer_native_name
        if customer_abbreviation is not UNSET:
            field_dict["customer_abbreviation"] = customer_abbreviation
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if resource_type is not UNSET:
            field_dict["resource_type"] = resource_type
        if state is not UNSET:
            field_dict["state"] = state
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if access_url is not UNSET:
            field_dict["access_url"] = access_url
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if cores is not UNSET:
            field_dict["cores"] = cores
        if ram is not UNSET:
            field_dict["ram"] = ram
        if disk is not UNSET:
            field_dict["disk"] = disk
        if min_ram is not UNSET:
            field_dict["min_ram"] = min_ram
        if min_disk is not UNSET:
            field_dict["min_disk"] = min_disk
        if user_data is not UNSET:
            field_dict["user_data"] = user_data
        if external_ips is not UNSET:
            field_dict["external_ips"] = external_ips
        if internal_ips is not UNSET:
            field_dict["internal_ips"] = internal_ips
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if key_name is not UNSET:
            field_dict["key_name"] = key_name
        if key_fingerprint is not UNSET:
            field_dict["key_fingerprint"] = key_fingerprint
        if image_name is not UNSET:
            field_dict["image_name"] = image_name
        if flavor_disk is not UNSET:
            field_dict["flavor_disk"] = flavor_disk
        if flavor_name is not UNSET:
            field_dict["flavor_name"] = flavor_name
        if volumes is not UNSET:
            field_dict["volumes"] = volumes
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups
        if server_group is not UNSET:
            field_dict["server_group"] = server_group
        if floating_ips is not UNSET:
            field_dict["floating_ips"] = floating_ips
        if ports is not UNSET:
            field_dict["ports"] = ports
        if availability_zone is not UNSET:
            field_dict["availability_zone"] = availability_zone
        if availability_zone_name is not UNSET:
            field_dict["availability_zone_name"] = availability_zone_name
        if connect_directly_to_external_network is not UNSET:
            field_dict["connect_directly_to_external_network"] = connect_directly_to_external_network
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if action is not UNSET:
            field_dict["action"] = action
        if action_details is not UNSET:
            field_dict["action_details"] = action_details
        if tenant_uuid is not UNSET:
            field_dict["tenant_uuid"] = tenant_uuid
        if hypervisor_hostname is not UNSET:
            field_dict["hypervisor_hostname"] = hypervisor_hostname
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if external_address is not UNSET:
            field_dict["external_address"] = external_address
        if rancher_cluster is not UNSET:
            field_dict["rancher_cluster"] = rancher_cluster
        if marketplace_offering_uuid is not UNSET:
            field_dict["marketplace_offering_uuid"] = marketplace_offering_uuid
        if marketplace_offering_name is not UNSET:
            field_dict["marketplace_offering_name"] = marketplace_offering_name
        if marketplace_offering_type is not UNSET:
            field_dict["marketplace_offering_type"] = marketplace_offering_type
        if marketplace_offering_plugin_options is not UNSET:
            field_dict["marketplace_offering_plugin_options"] = marketplace_offering_plugin_options
        if marketplace_category_uuid is not UNSET:
            field_dict["marketplace_category_uuid"] = marketplace_category_uuid
        if marketplace_category_name is not UNSET:
            field_dict["marketplace_category_name"] = marketplace_category_name
        if marketplace_resource_uuid is not UNSET:
            field_dict["marketplace_resource_uuid"] = marketplace_resource_uuid
        if marketplace_plan_uuid is not UNSET:
            field_dict["marketplace_plan_uuid"] = marketplace_plan_uuid
        if marketplace_resource_state is not UNSET:
            field_dict["marketplace_resource_state"] = marketplace_resource_state
        if is_usage_based is not UNSET:
            field_dict["is_usage_based"] = is_usage_based
        if is_limit_based is not UNSET:
            field_dict["is_limit_based"] = is_limit_based

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_instance_marketplace_offering_plugin_options_type_0 import (
            OpenStackInstanceMarketplaceOfferingPluginOptionsType0,
        )
        from ..models.open_stack_nested_floating_ip import OpenStackNestedFloatingIP
        from ..models.open_stack_nested_port import OpenStackNestedPort
        from ..models.open_stack_nested_security_group import OpenStackNestedSecurityGroup
        from ..models.open_stack_nested_server_group import OpenStackNestedServerGroup
        from ..models.open_stack_nested_volume import OpenStackNestedVolume
        from ..models.rancher_cluster_reference import RancherClusterReference

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        service_name = d.pop("service_name", UNSET)

        service_settings = d.pop("service_settings", UNSET)

        _service_settings_uuid = d.pop("service_settings_uuid", UNSET)
        service_settings_uuid: Union[Unset, UUID]
        if isinstance(_service_settings_uuid, Unset):
            service_settings_uuid = UNSET
        else:
            service_settings_uuid = UUID(_service_settings_uuid)

        service_settings_state = d.pop("service_settings_state", UNSET)

        service_settings_error_message = d.pop("service_settings_error_message", UNSET)

        project = d.pop("project", UNSET)

        project_name = d.pop("project_name", UNSET)

        _project_uuid = d.pop("project_uuid", UNSET)
        project_uuid: Union[Unset, UUID]
        if isinstance(_project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = UUID(_project_uuid)

        customer = d.pop("customer", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        customer_native_name = d.pop("customer_native_name", UNSET)

        customer_abbreviation = d.pop("customer_abbreviation", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        resource_type = d.pop("resource_type", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, CoreStates]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = CoreStates(_state)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        def _parse_access_url(data: object) -> Union[None, Unset, list[str], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                access_url_type_0 = cast(list[str], data)

                return access_url_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str], str], data)

        access_url = _parse_access_url(d.pop("access_url", UNSET))

        def _parse_start_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("start_time", UNSET))

        cores = d.pop("cores", UNSET)

        ram = d.pop("ram", UNSET)

        disk = d.pop("disk", UNSET)

        min_ram = d.pop("min_ram", UNSET)

        min_disk = d.pop("min_disk", UNSET)

        user_data = d.pop("user_data", UNSET)

        external_ips = cast(list[str], d.pop("external_ips", UNSET))

        internal_ips = cast(list[str], d.pop("internal_ips", UNSET))

        def _parse_latitude(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        latitude = _parse_latitude(d.pop("latitude", UNSET))

        def _parse_longitude(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        longitude = _parse_longitude(d.pop("longitude", UNSET))

        key_name = d.pop("key_name", UNSET)

        key_fingerprint = d.pop("key_fingerprint", UNSET)

        image_name = d.pop("image_name", UNSET)

        flavor_disk = d.pop("flavor_disk", UNSET)

        flavor_name = d.pop("flavor_name", UNSET)

        volumes = []
        _volumes = d.pop("volumes", UNSET)
        for volumes_item_data in _volumes or []:
            volumes_item = OpenStackNestedVolume.from_dict(volumes_item_data)

            volumes.append(volumes_item)

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackNestedSecurityGroup.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        _server_group = d.pop("server_group", UNSET)
        server_group: Union[Unset, OpenStackNestedServerGroup]
        if isinstance(_server_group, Unset):
            server_group = UNSET
        else:
            server_group = OpenStackNestedServerGroup.from_dict(_server_group)

        floating_ips = []
        _floating_ips = d.pop("floating_ips", UNSET)
        for floating_ips_item_data in _floating_ips or []:
            floating_ips_item = OpenStackNestedFloatingIP.from_dict(floating_ips_item_data)

            floating_ips.append(floating_ips_item)

        ports = []
        _ports = d.pop("ports", UNSET)
        for ports_item_data in _ports or []:
            ports_item = OpenStackNestedPort.from_dict(ports_item_data)

            ports.append(ports_item)

        def _parse_availability_zone(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        availability_zone = _parse_availability_zone(d.pop("availability_zone", UNSET))

        availability_zone_name = d.pop("availability_zone_name", UNSET)

        connect_directly_to_external_network = d.pop("connect_directly_to_external_network", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        action = d.pop("action", UNSET)

        action_details = d.pop("action_details", UNSET)

        _tenant_uuid = d.pop("tenant_uuid", UNSET)
        tenant_uuid: Union[Unset, UUID]
        if isinstance(_tenant_uuid, Unset):
            tenant_uuid = UNSET
        else:
            tenant_uuid = UUID(_tenant_uuid)

        hypervisor_hostname = d.pop("hypervisor_hostname", UNSET)

        tenant = d.pop("tenant", UNSET)

        external_address = cast(list[str], d.pop("external_address", UNSET))

        def _parse_rancher_cluster(data: object) -> Union["RancherClusterReference", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rancher_cluster_type_1 = RancherClusterReference.from_dict(data)

                return rancher_cluster_type_1
            except:  # noqa: E722
                pass
            return cast(Union["RancherClusterReference", None, Unset], data)

        rancher_cluster = _parse_rancher_cluster(d.pop("rancher_cluster", UNSET))

        def _parse_marketplace_offering_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_offering_uuid = _parse_marketplace_offering_uuid(d.pop("marketplace_offering_uuid", UNSET))

        def _parse_marketplace_offering_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_offering_name = _parse_marketplace_offering_name(d.pop("marketplace_offering_name", UNSET))

        def _parse_marketplace_offering_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_offering_type = _parse_marketplace_offering_type(d.pop("marketplace_offering_type", UNSET))

        def _parse_marketplace_offering_plugin_options(
            data: object,
        ) -> Union["OpenStackInstanceMarketplaceOfferingPluginOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                marketplace_offering_plugin_options_type_0 = (
                    OpenStackInstanceMarketplaceOfferingPluginOptionsType0.from_dict(data)
                )

                return marketplace_offering_plugin_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OpenStackInstanceMarketplaceOfferingPluginOptionsType0", None, Unset], data)

        marketplace_offering_plugin_options = _parse_marketplace_offering_plugin_options(
            d.pop("marketplace_offering_plugin_options", UNSET)
        )

        def _parse_marketplace_category_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_category_uuid = _parse_marketplace_category_uuid(d.pop("marketplace_category_uuid", UNSET))

        def _parse_marketplace_category_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_category_name = _parse_marketplace_category_name(d.pop("marketplace_category_name", UNSET))

        def _parse_marketplace_resource_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_resource_uuid = _parse_marketplace_resource_uuid(d.pop("marketplace_resource_uuid", UNSET))

        def _parse_marketplace_plan_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_plan_uuid = _parse_marketplace_plan_uuid(d.pop("marketplace_plan_uuid", UNSET))

        def _parse_marketplace_resource_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_resource_state = _parse_marketplace_resource_state(d.pop("marketplace_resource_state", UNSET))

        def _parse_is_usage_based(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_usage_based = _parse_is_usage_based(d.pop("is_usage_based", UNSET))

        def _parse_is_limit_based(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_limit_based = _parse_is_limit_based(d.pop("is_limit_based", UNSET))

        open_stack_instance = cls(
            url=url,
            uuid=uuid,
            name=name,
            description=description,
            service_name=service_name,
            service_settings=service_settings,
            service_settings_uuid=service_settings_uuid,
            service_settings_state=service_settings_state,
            service_settings_error_message=service_settings_error_message,
            project=project,
            project_name=project_name,
            project_uuid=project_uuid,
            customer=customer,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            customer_native_name=customer_native_name,
            customer_abbreviation=customer_abbreviation,
            error_message=error_message,
            error_traceback=error_traceback,
            resource_type=resource_type,
            state=state,
            created=created,
            modified=modified,
            backend_id=backend_id,
            access_url=access_url,
            start_time=start_time,
            cores=cores,
            ram=ram,
            disk=disk,
            min_ram=min_ram,
            min_disk=min_disk,
            user_data=user_data,
            external_ips=external_ips,
            internal_ips=internal_ips,
            latitude=latitude,
            longitude=longitude,
            key_name=key_name,
            key_fingerprint=key_fingerprint,
            image_name=image_name,
            flavor_disk=flavor_disk,
            flavor_name=flavor_name,
            volumes=volumes,
            security_groups=security_groups,
            server_group=server_group,
            floating_ips=floating_ips,
            ports=ports,
            availability_zone=availability_zone,
            availability_zone_name=availability_zone_name,
            connect_directly_to_external_network=connect_directly_to_external_network,
            runtime_state=runtime_state,
            action=action,
            action_details=action_details,
            tenant_uuid=tenant_uuid,
            hypervisor_hostname=hypervisor_hostname,
            tenant=tenant,
            external_address=external_address,
            rancher_cluster=rancher_cluster,
            marketplace_offering_uuid=marketplace_offering_uuid,
            marketplace_offering_name=marketplace_offering_name,
            marketplace_offering_type=marketplace_offering_type,
            marketplace_offering_plugin_options=marketplace_offering_plugin_options,
            marketplace_category_uuid=marketplace_category_uuid,
            marketplace_category_name=marketplace_category_name,
            marketplace_resource_uuid=marketplace_resource_uuid,
            marketplace_plan_uuid=marketplace_plan_uuid,
            marketplace_resource_state=marketplace_resource_state,
            is_usage_based=is_usage_based,
            is_limit_based=is_limit_based,
        )

        open_stack_instance.additional_properties = d
        return open_stack_instance

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
