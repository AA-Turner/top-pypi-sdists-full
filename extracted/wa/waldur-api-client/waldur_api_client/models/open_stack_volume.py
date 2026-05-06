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
    from ..models.open_stack_volume_marketplace_offering_plugin_options_type_0 import (
        OpenStackVolumeMarketplaceOfferingPluginOptionsType0,
    )


T = TypeVar("T", bound="OpenStackVolume")


@_attrs_define
class OpenStackVolume:
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
        backend_id (Union[None, Unset, str]): Volume ID in the OpenStack backend
        access_url (Union[None, Unset, list[str], str]):
        source_snapshot (Union[None, Unset, str]): Snapshot that this volume was created from, if any
        size (Union[None, Unset, int]): Size in MiB
        bootable (Union[Unset, bool]): Indicates if this volume can be used to boot an instance
        metadata (Union[Unset, Any]):
        image (Union[None, Unset, str]): Image that this volume was created from, if any
        image_metadata (Union[Unset, str]): Metadata of the image this volume was created from
        image_name (Union[Unset, str]): Name of the image this volume was created from
        type_ (Union[None, Unset, str]): Type of the volume (e.g. SSD, HDD)
        type_name (Union[Unset, str]):
        runtime_state (Union[Unset, str]):
        availability_zone (Union[None, Unset, str]): Availability zone where this volume is located
        availability_zone_name (Union[Unset, str]):
        device (Union[Unset, str]): Name of volume as instance device e.g. /dev/vdb.
        action (Union[Unset, str]):
        action_details (Union[Unset, Any]):
        instance (Union[None, Unset, str]): Instance that this volume is attached to, if any
        instance_name (Union[Unset, str]):
        instance_marketplace_uuid (Union[Unset, UUID]):
        tenant (Union[Unset, str]):
        tenant_uuid (Union[Unset, UUID]):
        extend_enabled (Union[Unset, bool]):
        marketplace_offering_uuid (Union[None, Unset, str]):
        marketplace_offering_name (Union[None, Unset, str]):
        marketplace_offering_type (Union[None, Unset, str]):
        marketplace_offering_plugin_options (Union['OpenStackVolumeMarketplaceOfferingPluginOptionsType0', None,
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
    source_snapshot: Union[None, Unset, str] = UNSET
    size: Union[None, Unset, int] = UNSET
    bootable: Union[Unset, bool] = UNSET
    metadata: Union[Unset, Any] = UNSET
    image: Union[None, Unset, str] = UNSET
    image_metadata: Union[Unset, str] = UNSET
    image_name: Union[Unset, str] = UNSET
    type_: Union[None, Unset, str] = UNSET
    type_name: Union[Unset, str] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    availability_zone: Union[None, Unset, str] = UNSET
    availability_zone_name: Union[Unset, str] = UNSET
    device: Union[Unset, str] = UNSET
    action: Union[Unset, str] = UNSET
    action_details: Union[Unset, Any] = UNSET
    instance: Union[None, Unset, str] = UNSET
    instance_name: Union[Unset, str] = UNSET
    instance_marketplace_uuid: Union[Unset, UUID] = UNSET
    tenant: Union[Unset, str] = UNSET
    tenant_uuid: Union[Unset, UUID] = UNSET
    extend_enabled: Union[Unset, bool] = UNSET
    marketplace_offering_uuid: Union[None, Unset, str] = UNSET
    marketplace_offering_name: Union[None, Unset, str] = UNSET
    marketplace_offering_type: Union[None, Unset, str] = UNSET
    marketplace_offering_plugin_options: Union["OpenStackVolumeMarketplaceOfferingPluginOptionsType0", None, Unset] = (
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
        from ..models.open_stack_volume_marketplace_offering_plugin_options_type_0 import (
            OpenStackVolumeMarketplaceOfferingPluginOptionsType0,
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

        access_url: Union[None, Unset, list[str], str]
        if isinstance(self.access_url, Unset):
            access_url = UNSET
        elif isinstance(self.access_url, list):
            access_url = self.access_url

        else:
            access_url = self.access_url

        source_snapshot: Union[None, Unset, str]
        if isinstance(self.source_snapshot, Unset):
            source_snapshot = UNSET
        else:
            source_snapshot = self.source_snapshot

        size: Union[None, Unset, int]
        if isinstance(self.size, Unset):
            size = UNSET
        else:
            size = self.size

        bootable = self.bootable

        metadata = self.metadata

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        image_metadata = self.image_metadata

        image_name = self.image_name

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        type_name = self.type_name

        runtime_state = self.runtime_state

        availability_zone: Union[None, Unset, str]
        if isinstance(self.availability_zone, Unset):
            availability_zone = UNSET
        else:
            availability_zone = self.availability_zone

        availability_zone_name = self.availability_zone_name

        device = self.device

        action = self.action

        action_details = self.action_details

        instance: Union[None, Unset, str]
        if isinstance(self.instance, Unset):
            instance = UNSET
        else:
            instance = self.instance

        instance_name = self.instance_name

        instance_marketplace_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.instance_marketplace_uuid, Unset):
            instance_marketplace_uuid = str(self.instance_marketplace_uuid)

        tenant = self.tenant

        tenant_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.tenant_uuid, Unset):
            tenant_uuid = str(self.tenant_uuid)

        extend_enabled = self.extend_enabled

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
        elif isinstance(self.marketplace_offering_plugin_options, OpenStackVolumeMarketplaceOfferingPluginOptionsType0):
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
        if source_snapshot is not UNSET:
            field_dict["source_snapshot"] = source_snapshot
        if size is not UNSET:
            field_dict["size"] = size
        if bootable is not UNSET:
            field_dict["bootable"] = bootable
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if image is not UNSET:
            field_dict["image"] = image
        if image_metadata is not UNSET:
            field_dict["image_metadata"] = image_metadata
        if image_name is not UNSET:
            field_dict["image_name"] = image_name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if type_name is not UNSET:
            field_dict["type_name"] = type_name
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if availability_zone is not UNSET:
            field_dict["availability_zone"] = availability_zone
        if availability_zone_name is not UNSET:
            field_dict["availability_zone_name"] = availability_zone_name
        if device is not UNSET:
            field_dict["device"] = device
        if action is not UNSET:
            field_dict["action"] = action
        if action_details is not UNSET:
            field_dict["action_details"] = action_details
        if instance is not UNSET:
            field_dict["instance"] = instance
        if instance_name is not UNSET:
            field_dict["instance_name"] = instance_name
        if instance_marketplace_uuid is not UNSET:
            field_dict["instance_marketplace_uuid"] = instance_marketplace_uuid
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if tenant_uuid is not UNSET:
            field_dict["tenant_uuid"] = tenant_uuid
        if extend_enabled is not UNSET:
            field_dict["extend_enabled"] = extend_enabled
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
        from ..models.open_stack_volume_marketplace_offering_plugin_options_type_0 import (
            OpenStackVolumeMarketplaceOfferingPluginOptionsType0,
        )

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

        def _parse_source_snapshot(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source_snapshot = _parse_source_snapshot(d.pop("source_snapshot", UNSET))

        def _parse_size(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        size = _parse_size(d.pop("size", UNSET))

        bootable = d.pop("bootable", UNSET)

        metadata = d.pop("metadata", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        image_metadata = d.pop("image_metadata", UNSET)

        image_name = d.pop("image_name", UNSET)

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        type_name = d.pop("type_name", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        def _parse_availability_zone(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        availability_zone = _parse_availability_zone(d.pop("availability_zone", UNSET))

        availability_zone_name = d.pop("availability_zone_name", UNSET)

        device = d.pop("device", UNSET)

        action = d.pop("action", UNSET)

        action_details = d.pop("action_details", UNSET)

        def _parse_instance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instance = _parse_instance(d.pop("instance", UNSET))

        instance_name = d.pop("instance_name", UNSET)

        _instance_marketplace_uuid = d.pop("instance_marketplace_uuid", UNSET)
        instance_marketplace_uuid: Union[Unset, UUID]
        if isinstance(_instance_marketplace_uuid, Unset):
            instance_marketplace_uuid = UNSET
        else:
            instance_marketplace_uuid = UUID(_instance_marketplace_uuid)

        tenant = d.pop("tenant", UNSET)

        _tenant_uuid = d.pop("tenant_uuid", UNSET)
        tenant_uuid: Union[Unset, UUID]
        if isinstance(_tenant_uuid, Unset):
            tenant_uuid = UNSET
        else:
            tenant_uuid = UUID(_tenant_uuid)

        extend_enabled = d.pop("extend_enabled", UNSET)

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
        ) -> Union["OpenStackVolumeMarketplaceOfferingPluginOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                marketplace_offering_plugin_options_type_0 = (
                    OpenStackVolumeMarketplaceOfferingPluginOptionsType0.from_dict(data)
                )

                return marketplace_offering_plugin_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OpenStackVolumeMarketplaceOfferingPluginOptionsType0", None, Unset], data)

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

        open_stack_volume = cls(
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
            source_snapshot=source_snapshot,
            size=size,
            bootable=bootable,
            metadata=metadata,
            image=image,
            image_metadata=image_metadata,
            image_name=image_name,
            type_=type_,
            type_name=type_name,
            runtime_state=runtime_state,
            availability_zone=availability_zone,
            availability_zone_name=availability_zone_name,
            device=device,
            action=action,
            action_details=action_details,
            instance=instance,
            instance_name=instance_name,
            instance_marketplace_uuid=instance_marketplace_uuid,
            tenant=tenant,
            tenant_uuid=tenant_uuid,
            extend_enabled=extend_enabled,
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

        open_stack_volume.additional_properties = d
        return open_stack_volume

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
