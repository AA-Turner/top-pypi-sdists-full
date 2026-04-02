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
    from ..models.open_stack_allowed_address_pair import OpenStackAllowedAddressPair
    from ..models.open_stack_fixed_ip import OpenStackFixedIp
    from ..models.open_stack_port_marketplace_offering_plugin_options_type_0 import (
        OpenStackPortMarketplaceOfferingPluginOptionsType0,
    )
    from ..models.open_stack_port_nested_security_group import OpenStackPortNestedSecurityGroup


T = TypeVar("T", bound="OpenStackPort")


@_attrs_define
class OpenStackPort:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        service_name (Union[Unset, str]):
        service_settings (Union[Unset, str]):
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
        backend_id (Union[None, Unset, str]): Port ID in OpenStack
        access_url (Union[None, Unset, str]):
        fixed_ips (Union[Unset, list['OpenStackFixedIp']]):
        mac_address (Union[Unset, str]): MAC address of the port
        allowed_address_pairs (Union[Unset, list['OpenStackAllowedAddressPair']]):
        tenant (Union[Unset, str]): OpenStack tenant this port belongs to
        tenant_name (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        network (Union[None, Unset, str]): Network to which this port belongs
        network_name (Union[Unset, str]):
        network_uuid (Union[Unset, UUID]):
        floating_ips (Union[Unset, list[str]]):
        device_id (Union[None, Unset, str]): ID of device (instance, router etc) to which this port is connected
        device_owner (Union[None, Unset, str]): Entity that uses this port (e.g. network:router_interface)
        port_security_enabled (Union[Unset, bool]): If True, security groups and rules will be applied to this port
        security_groups (Union[Unset, list['OpenStackPortNestedSecurityGroup']]):
        admin_state_up (Union[None, Unset, bool]): Administrative state of the port. If down, port does not forward
            packets
        status (Union[None, Unset, str]): Port status in OpenStack (e.g. ACTIVE, DOWN)
        marketplace_offering_uuid (Union[None, Unset, str]):
        marketplace_offering_name (Union[None, Unset, str]):
        marketplace_offering_type (Union[None, Unset, str]):
        marketplace_offering_plugin_options (Union['OpenStackPortMarketplaceOfferingPluginOptionsType0', None, Unset]):
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
    access_url: Union[None, Unset, str] = UNSET
    fixed_ips: Union[Unset, list["OpenStackFixedIp"]] = UNSET
    mac_address: Union[Unset, str] = UNSET
    allowed_address_pairs: Union[Unset, list["OpenStackAllowedAddressPair"]] = UNSET
    tenant: Union[Unset, str] = UNSET
    tenant_name: Union[Unset, str] = UNSET
    tenant_uuid: Union[Unset, UUID] = UNSET
    network: Union[None, Unset, str] = UNSET
    network_name: Union[Unset, str] = UNSET
    network_uuid: Union[Unset, UUID] = UNSET
    floating_ips: Union[Unset, list[str]] = UNSET
    device_id: Union[None, Unset, str] = UNSET
    device_owner: Union[None, Unset, str] = UNSET
    port_security_enabled: Union[Unset, bool] = UNSET
    security_groups: Union[Unset, list["OpenStackPortNestedSecurityGroup"]] = UNSET
    admin_state_up: Union[None, Unset, bool] = UNSET
    status: Union[None, Unset, str] = UNSET
    marketplace_offering_uuid: Union[None, Unset, str] = UNSET
    marketplace_offering_name: Union[None, Unset, str] = UNSET
    marketplace_offering_type: Union[None, Unset, str] = UNSET
    marketplace_offering_plugin_options: Union["OpenStackPortMarketplaceOfferingPluginOptionsType0", None, Unset] = (
        UNSET
    )
    marketplace_category_uuid: Union[None, Unset, str] = UNSET
    marketplace_category_name: Union[None, Unset, str] = UNSET
    marketplace_resource_uuid: Union[None, Unset, str] = UNSET
    marketplace_plan_uuid: Union[None, Unset, str] = UNSET
    marketplace_resource_state: Union[None, Unset, str] = UNSET
    is_usage_based: Union[None, Unset, bool] = UNSET
    is_limit_based: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.open_stack_port_marketplace_offering_plugin_options_type_0 import (
            OpenStackPortMarketplaceOfferingPluginOptionsType0,
        )

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

        access_url: Union[None, Unset, str]
        if isinstance(self.access_url, Unset):
            access_url = UNSET
        else:
            access_url = self.access_url

        fixed_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.fixed_ips, Unset):
            fixed_ips = []
            for fixed_ips_item_data in self.fixed_ips:
                fixed_ips_item = fixed_ips_item_data.to_dict()
                fixed_ips.append(fixed_ips_item)

        mac_address = self.mac_address

        allowed_address_pairs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.allowed_address_pairs, Unset):
            allowed_address_pairs = []
            for allowed_address_pairs_item_data in self.allowed_address_pairs:
                allowed_address_pairs_item = allowed_address_pairs_item_data.to_dict()
                allowed_address_pairs.append(allowed_address_pairs_item)

        tenant = self.tenant

        tenant_name = self.tenant_name

        tenant_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.tenant_uuid, Unset):
            tenant_uuid = str(self.tenant_uuid)

        network: Union[None, Unset, str]
        if isinstance(self.network, Unset):
            network = UNSET
        else:
            network = self.network

        network_name = self.network_name

        network_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.network_uuid, Unset):
            network_uuid = str(self.network_uuid)

        floating_ips: Union[Unset, list[str]] = UNSET
        if not isinstance(self.floating_ips, Unset):
            floating_ips = self.floating_ips

        device_id: Union[None, Unset, str]
        if isinstance(self.device_id, Unset):
            device_id = UNSET
        else:
            device_id = self.device_id

        device_owner: Union[None, Unset, str]
        if isinstance(self.device_owner, Unset):
            device_owner = UNSET
        else:
            device_owner = self.device_owner

        port_security_enabled = self.port_security_enabled

        security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = []
            for security_groups_item_data in self.security_groups:
                security_groups_item = security_groups_item_data.to_dict()
                security_groups.append(security_groups_item)

        admin_state_up: Union[None, Unset, bool]
        if isinstance(self.admin_state_up, Unset):
            admin_state_up = UNSET
        else:
            admin_state_up = self.admin_state_up

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

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
        elif isinstance(self.marketplace_offering_plugin_options, OpenStackPortMarketplaceOfferingPluginOptionsType0):
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
        if fixed_ips is not UNSET:
            field_dict["fixed_ips"] = fixed_ips
        if mac_address is not UNSET:
            field_dict["mac_address"] = mac_address
        if allowed_address_pairs is not UNSET:
            field_dict["allowed_address_pairs"] = allowed_address_pairs
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if tenant_name is not UNSET:
            field_dict["tenant_name"] = tenant_name
        if tenant_uuid is not UNSET:
            field_dict["tenant_uuid"] = tenant_uuid
        if network is not UNSET:
            field_dict["network"] = network
        if network_name is not UNSET:
            field_dict["network_name"] = network_name
        if network_uuid is not UNSET:
            field_dict["network_uuid"] = network_uuid
        if floating_ips is not UNSET:
            field_dict["floating_ips"] = floating_ips
        if device_id is not UNSET:
            field_dict["device_id"] = device_id
        if device_owner is not UNSET:
            field_dict["device_owner"] = device_owner
        if port_security_enabled is not UNSET:
            field_dict["port_security_enabled"] = port_security_enabled
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups
        if admin_state_up is not UNSET:
            field_dict["admin_state_up"] = admin_state_up
        if status is not UNSET:
            field_dict["status"] = status
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
        from ..models.open_stack_allowed_address_pair import OpenStackAllowedAddressPair
        from ..models.open_stack_fixed_ip import OpenStackFixedIp
        from ..models.open_stack_port_marketplace_offering_plugin_options_type_0 import (
            OpenStackPortMarketplaceOfferingPluginOptionsType0,
        )
        from ..models.open_stack_port_nested_security_group import OpenStackPortNestedSecurityGroup

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

        def _parse_access_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        access_url = _parse_access_url(d.pop("access_url", UNSET))

        fixed_ips = []
        _fixed_ips = d.pop("fixed_ips", UNSET)
        for fixed_ips_item_data in _fixed_ips or []:
            fixed_ips_item = OpenStackFixedIp.from_dict(fixed_ips_item_data)

            fixed_ips.append(fixed_ips_item)

        mac_address = d.pop("mac_address", UNSET)

        allowed_address_pairs = []
        _allowed_address_pairs = d.pop("allowed_address_pairs", UNSET)
        for allowed_address_pairs_item_data in _allowed_address_pairs or []:
            allowed_address_pairs_item = OpenStackAllowedAddressPair.from_dict(allowed_address_pairs_item_data)

            allowed_address_pairs.append(allowed_address_pairs_item)

        tenant = d.pop("tenant", UNSET)

        tenant_name = d.pop("tenant_name", UNSET)

        _tenant_uuid = d.pop("tenant_uuid", UNSET)
        tenant_uuid: Union[Unset, UUID]
        if isinstance(_tenant_uuid, Unset):
            tenant_uuid = UNSET
        else:
            tenant_uuid = UUID(_tenant_uuid)

        def _parse_network(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        network = _parse_network(d.pop("network", UNSET))

        network_name = d.pop("network_name", UNSET)

        _network_uuid = d.pop("network_uuid", UNSET)
        network_uuid: Union[Unset, UUID]
        if isinstance(_network_uuid, Unset):
            network_uuid = UNSET
        else:
            network_uuid = UUID(_network_uuid)

        floating_ips = cast(list[str], d.pop("floating_ips", UNSET))

        def _parse_device_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        device_id = _parse_device_id(d.pop("device_id", UNSET))

        def _parse_device_owner(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        device_owner = _parse_device_owner(d.pop("device_owner", UNSET))

        port_security_enabled = d.pop("port_security_enabled", UNSET)

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackPortNestedSecurityGroup.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        def _parse_admin_state_up(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        admin_state_up = _parse_admin_state_up(d.pop("admin_state_up", UNSET))

        def _parse_status(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        status = _parse_status(d.pop("status", UNSET))

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
        ) -> Union["OpenStackPortMarketplaceOfferingPluginOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                marketplace_offering_plugin_options_type_0 = (
                    OpenStackPortMarketplaceOfferingPluginOptionsType0.from_dict(data)
                )

                return marketplace_offering_plugin_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OpenStackPortMarketplaceOfferingPluginOptionsType0", None, Unset], data)

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

        open_stack_port = cls(
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
            fixed_ips=fixed_ips,
            mac_address=mac_address,
            allowed_address_pairs=allowed_address_pairs,
            tenant=tenant,
            tenant_name=tenant_name,
            tenant_uuid=tenant_uuid,
            network=network,
            network_name=network_name,
            network_uuid=network_uuid,
            floating_ips=floating_ips,
            device_id=device_id,
            device_owner=device_owner,
            port_security_enabled=port_security_enabled,
            security_groups=security_groups,
            admin_state_up=admin_state_up,
            status=status,
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

        open_stack_port.additional_properties = d
        return open_stack_port

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
