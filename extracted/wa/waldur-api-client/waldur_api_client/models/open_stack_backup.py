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
    from ..models.open_stack_backup_marketplace_offering_plugin_options_type_0 import (
        OpenStackBackupMarketplaceOfferingPluginOptionsType0,
    )
    from ..models.open_stack_backup_restoration import OpenStackBackupRestoration
    from ..models.open_stack_nested_floating_ip import OpenStackNestedFloatingIP
    from ..models.open_stack_nested_port import OpenStackNestedPort
    from ..models.open_stack_nested_security_group import OpenStackNestedSecurityGroup


T = TypeVar("T", bound="OpenStackBackup")


@_attrs_define
class OpenStackBackup:
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
        backend_id (Union[Unset, str]):
        access_url (Union[None, Unset, list[str], str]):
        kept_until (Union[None, Unset, datetime.datetime]): Guaranteed time of backup retention. If null - keep forever.
        metadata (Union[Unset, Any]):
        instance (Union[Unset, str]): Instance that this backup is created from
        instance_name (Union[Unset, str]):
        instance_marketplace_uuid (Union[Unset, UUID]):
        restorations (Union[Unset, list['OpenStackBackupRestoration']]):
        instance_security_groups (Union[Unset, list['OpenStackNestedSecurityGroup']]):
        instance_ports (Union[Unset, list['OpenStackNestedPort']]):
        instance_floating_ips (Union[Unset, list['OpenStackNestedFloatingIP']]):
        tenant_uuid (Union[Unset, UUID]):
        marketplace_offering_uuid (Union[None, Unset, str]):
        marketplace_offering_name (Union[None, Unset, str]):
        marketplace_offering_type (Union[None, Unset, str]):
        marketplace_offering_plugin_options (Union['OpenStackBackupMarketplaceOfferingPluginOptionsType0', None,
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
    backend_id: Union[Unset, str] = UNSET
    access_url: Union[None, Unset, list[str], str] = UNSET
    kept_until: Union[None, Unset, datetime.datetime] = UNSET
    metadata: Union[Unset, Any] = UNSET
    instance: Union[Unset, str] = UNSET
    instance_name: Union[Unset, str] = UNSET
    instance_marketplace_uuid: Union[Unset, UUID] = UNSET
    restorations: Union[Unset, list["OpenStackBackupRestoration"]] = UNSET
    instance_security_groups: Union[Unset, list["OpenStackNestedSecurityGroup"]] = UNSET
    instance_ports: Union[Unset, list["OpenStackNestedPort"]] = UNSET
    instance_floating_ips: Union[Unset, list["OpenStackNestedFloatingIP"]] = UNSET
    tenant_uuid: Union[Unset, UUID] = UNSET
    marketplace_offering_uuid: Union[None, Unset, str] = UNSET
    marketplace_offering_name: Union[None, Unset, str] = UNSET
    marketplace_offering_type: Union[None, Unset, str] = UNSET
    marketplace_offering_plugin_options: Union["OpenStackBackupMarketplaceOfferingPluginOptionsType0", None, Unset] = (
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
        from ..models.open_stack_backup_marketplace_offering_plugin_options_type_0 import (
            OpenStackBackupMarketplaceOfferingPluginOptionsType0,
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

        backend_id = self.backend_id

        access_url: Union[None, Unset, list[str], str]
        if isinstance(self.access_url, Unset):
            access_url = UNSET
        elif isinstance(self.access_url, list):
            access_url = self.access_url

        else:
            access_url = self.access_url

        kept_until: Union[None, Unset, str]
        if isinstance(self.kept_until, Unset):
            kept_until = UNSET
        elif isinstance(self.kept_until, datetime.datetime):
            kept_until = self.kept_until.isoformat()
        else:
            kept_until = self.kept_until

        metadata = self.metadata

        instance = self.instance

        instance_name = self.instance_name

        instance_marketplace_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.instance_marketplace_uuid, Unset):
            instance_marketplace_uuid = str(self.instance_marketplace_uuid)

        restorations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.restorations, Unset):
            restorations = []
            for restorations_item_data in self.restorations:
                restorations_item = restorations_item_data.to_dict()
                restorations.append(restorations_item)

        instance_security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.instance_security_groups, Unset):
            instance_security_groups = []
            for instance_security_groups_item_data in self.instance_security_groups:
                instance_security_groups_item = instance_security_groups_item_data.to_dict()
                instance_security_groups.append(instance_security_groups_item)

        instance_ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.instance_ports, Unset):
            instance_ports = []
            for instance_ports_item_data in self.instance_ports:
                instance_ports_item = instance_ports_item_data.to_dict()
                instance_ports.append(instance_ports_item)

        instance_floating_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.instance_floating_ips, Unset):
            instance_floating_ips = []
            for instance_floating_ips_item_data in self.instance_floating_ips:
                instance_floating_ips_item = instance_floating_ips_item_data.to_dict()
                instance_floating_ips.append(instance_floating_ips_item)

        tenant_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.tenant_uuid, Unset):
            tenant_uuid = str(self.tenant_uuid)

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
        elif isinstance(self.marketplace_offering_plugin_options, OpenStackBackupMarketplaceOfferingPluginOptionsType0):
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
        if kept_until is not UNSET:
            field_dict["kept_until"] = kept_until
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if instance is not UNSET:
            field_dict["instance"] = instance
        if instance_name is not UNSET:
            field_dict["instance_name"] = instance_name
        if instance_marketplace_uuid is not UNSET:
            field_dict["instance_marketplace_uuid"] = instance_marketplace_uuid
        if restorations is not UNSET:
            field_dict["restorations"] = restorations
        if instance_security_groups is not UNSET:
            field_dict["instance_security_groups"] = instance_security_groups
        if instance_ports is not UNSET:
            field_dict["instance_ports"] = instance_ports
        if instance_floating_ips is not UNSET:
            field_dict["instance_floating_ips"] = instance_floating_ips
        if tenant_uuid is not UNSET:
            field_dict["tenant_uuid"] = tenant_uuid
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
        from ..models.open_stack_backup_marketplace_offering_plugin_options_type_0 import (
            OpenStackBackupMarketplaceOfferingPluginOptionsType0,
        )
        from ..models.open_stack_backup_restoration import OpenStackBackupRestoration
        from ..models.open_stack_nested_floating_ip import OpenStackNestedFloatingIP
        from ..models.open_stack_nested_port import OpenStackNestedPort
        from ..models.open_stack_nested_security_group import OpenStackNestedSecurityGroup

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

        backend_id = d.pop("backend_id", UNSET)

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

        def _parse_kept_until(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kept_until_type_0 = isoparse(data)

                return kept_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        kept_until = _parse_kept_until(d.pop("kept_until", UNSET))

        metadata = d.pop("metadata", UNSET)

        instance = d.pop("instance", UNSET)

        instance_name = d.pop("instance_name", UNSET)

        _instance_marketplace_uuid = d.pop("instance_marketplace_uuid", UNSET)
        instance_marketplace_uuid: Union[Unset, UUID]
        if isinstance(_instance_marketplace_uuid, Unset):
            instance_marketplace_uuid = UNSET
        else:
            instance_marketplace_uuid = UUID(_instance_marketplace_uuid)

        restorations = []
        _restorations = d.pop("restorations", UNSET)
        for restorations_item_data in _restorations or []:
            restorations_item = OpenStackBackupRestoration.from_dict(restorations_item_data)

            restorations.append(restorations_item)

        instance_security_groups = []
        _instance_security_groups = d.pop("instance_security_groups", UNSET)
        for instance_security_groups_item_data in _instance_security_groups or []:
            instance_security_groups_item = OpenStackNestedSecurityGroup.from_dict(instance_security_groups_item_data)

            instance_security_groups.append(instance_security_groups_item)

        instance_ports = []
        _instance_ports = d.pop("instance_ports", UNSET)
        for instance_ports_item_data in _instance_ports or []:
            instance_ports_item = OpenStackNestedPort.from_dict(instance_ports_item_data)

            instance_ports.append(instance_ports_item)

        instance_floating_ips = []
        _instance_floating_ips = d.pop("instance_floating_ips", UNSET)
        for instance_floating_ips_item_data in _instance_floating_ips or []:
            instance_floating_ips_item = OpenStackNestedFloatingIP.from_dict(instance_floating_ips_item_data)

            instance_floating_ips.append(instance_floating_ips_item)

        _tenant_uuid = d.pop("tenant_uuid", UNSET)
        tenant_uuid: Union[Unset, UUID]
        if isinstance(_tenant_uuid, Unset):
            tenant_uuid = UNSET
        else:
            tenant_uuid = UUID(_tenant_uuid)

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
        ) -> Union["OpenStackBackupMarketplaceOfferingPluginOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                marketplace_offering_plugin_options_type_0 = (
                    OpenStackBackupMarketplaceOfferingPluginOptionsType0.from_dict(data)
                )

                return marketplace_offering_plugin_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OpenStackBackupMarketplaceOfferingPluginOptionsType0", None, Unset], data)

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

        open_stack_backup = cls(
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
            kept_until=kept_until,
            metadata=metadata,
            instance=instance,
            instance_name=instance_name,
            instance_marketplace_uuid=instance_marketplace_uuid,
            restorations=restorations,
            instance_security_groups=instance_security_groups,
            instance_ports=instance_ports,
            instance_floating_ips=instance_floating_ips,
            tenant_uuid=tenant_uuid,
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

        open_stack_backup.additional_properties = d
        return open_stack_backup

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
