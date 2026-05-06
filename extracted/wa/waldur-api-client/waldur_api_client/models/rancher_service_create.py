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
    from ..models.rancher_service_create_marketplace_offering_plugin_options_type_0 import (
        RancherServiceCreateMarketplaceOfferingPluginOptionsType0,
    )
    from ..models.rancher_workload_create import RancherWorkloadCreate


T = TypeVar("T", bound="RancherServiceCreate")


@_attrs_define
class RancherServiceCreate:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        service_name (str):
        service_settings (str):
        service_settings_uuid (UUID):
        service_settings_state (str):
        service_settings_error_message (str):
        project (str):
        project_name (str):
        project_uuid (UUID):
        customer (str):
        customer_uuid (UUID):
        customer_name (str):
        customer_native_name (str):
        customer_abbreviation (str):
        resource_type (str):
        state (CoreStates):
        created (datetime.datetime):
        modified (datetime.datetime):
        access_url (Union[None, list[str], str]):
        namespace_name (str):
        marketplace_offering_uuid (Union[None, str]):
        marketplace_offering_name (Union[None, str]):
        marketplace_offering_type (Union[None, str]):
        marketplace_offering_plugin_options (Union['RancherServiceCreateMarketplaceOfferingPluginOptionsType0', None]):
        marketplace_category_uuid (Union[None, str]):
        marketplace_category_name (Union[None, str]):
        marketplace_resource_uuid (Union[None, str]):
        marketplace_plan_uuid (Union[None, str]):
        marketplace_resource_state (Union[None, str]):
        is_usage_based (Union[None, bool]):
        is_limit_based (Union[None, bool]):
        description (Union[Unset, str]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        runtime_state (Union[Unset, str]):
        namespace (Union[Unset, str]):
        cluster_ip (Union[None, Unset, str]): An IPv4 or IPv6 address.
        selector (Union[Unset, Any]):
        target_workloads (Union[Unset, list['RancherWorkloadCreate']]):
    """

    url: str
    uuid: UUID
    name: str
    service_name: str
    service_settings: str
    service_settings_uuid: UUID
    service_settings_state: str
    service_settings_error_message: str
    project: str
    project_name: str
    project_uuid: UUID
    customer: str
    customer_uuid: UUID
    customer_name: str
    customer_native_name: str
    customer_abbreviation: str
    resource_type: str
    state: CoreStates
    created: datetime.datetime
    modified: datetime.datetime
    access_url: Union[None, list[str], str]
    namespace_name: str
    marketplace_offering_uuid: Union[None, str]
    marketplace_offering_name: Union[None, str]
    marketplace_offering_type: Union[None, str]
    marketplace_offering_plugin_options: Union["RancherServiceCreateMarketplaceOfferingPluginOptionsType0", None]
    marketplace_category_uuid: Union[None, str]
    marketplace_category_name: Union[None, str]
    marketplace_resource_uuid: Union[None, str]
    marketplace_plan_uuid: Union[None, str]
    marketplace_resource_state: Union[None, str]
    is_usage_based: Union[None, bool]
    is_limit_based: Union[None, bool]
    description: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    namespace: Union[Unset, str] = UNSET
    cluster_ip: Union[None, Unset, str] = UNSET
    selector: Union[Unset, Any] = UNSET
    target_workloads: Union[Unset, list["RancherWorkloadCreate"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.rancher_service_create_marketplace_offering_plugin_options_type_0 import (
            RancherServiceCreateMarketplaceOfferingPluginOptionsType0,
        )

        url = self.url

        uuid = str(self.uuid)

        name = self.name

        service_name = self.service_name

        service_settings = self.service_settings

        service_settings_uuid = str(self.service_settings_uuid)

        service_settings_state = self.service_settings_state

        service_settings_error_message = self.service_settings_error_message

        project = self.project

        project_name = self.project_name

        project_uuid = str(self.project_uuid)

        customer = self.customer

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        customer_native_name = self.customer_native_name

        customer_abbreviation = self.customer_abbreviation

        resource_type = self.resource_type

        state = self.state.value

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        access_url: Union[None, list[str], str]
        if isinstance(self.access_url, list):
            access_url = self.access_url

        else:
            access_url = self.access_url

        namespace_name = self.namespace_name

        marketplace_offering_uuid: Union[None, str]
        marketplace_offering_uuid = self.marketplace_offering_uuid

        marketplace_offering_name: Union[None, str]
        marketplace_offering_name = self.marketplace_offering_name

        marketplace_offering_type: Union[None, str]
        marketplace_offering_type = self.marketplace_offering_type

        marketplace_offering_plugin_options: Union[None, dict[str, Any]]
        if isinstance(
            self.marketplace_offering_plugin_options, RancherServiceCreateMarketplaceOfferingPluginOptionsType0
        ):
            marketplace_offering_plugin_options = self.marketplace_offering_plugin_options.to_dict()
        else:
            marketplace_offering_plugin_options = self.marketplace_offering_plugin_options

        marketplace_category_uuid: Union[None, str]
        marketplace_category_uuid = self.marketplace_category_uuid

        marketplace_category_name: Union[None, str]
        marketplace_category_name = self.marketplace_category_name

        marketplace_resource_uuid: Union[None, str]
        marketplace_resource_uuid = self.marketplace_resource_uuid

        marketplace_plan_uuid: Union[None, str]
        marketplace_plan_uuid = self.marketplace_plan_uuid

        marketplace_resource_state: Union[None, str]
        marketplace_resource_state = self.marketplace_resource_state

        is_usage_based: Union[None, bool]
        is_usage_based = self.is_usage_based

        is_limit_based: Union[None, bool]
        is_limit_based = self.is_limit_based

        description = self.description

        error_message = self.error_message

        error_traceback = self.error_traceback

        backend_id = self.backend_id

        runtime_state = self.runtime_state

        namespace = self.namespace

        cluster_ip: Union[None, Unset, str]
        if isinstance(self.cluster_ip, Unset):
            cluster_ip = UNSET
        else:
            cluster_ip = self.cluster_ip

        selector = self.selector

        target_workloads: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.target_workloads, Unset):
            target_workloads = []
            for target_workloads_item_data in self.target_workloads:
                target_workloads_item = target_workloads_item_data.to_dict()
                target_workloads.append(target_workloads_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "service_name": service_name,
                "service_settings": service_settings,
                "service_settings_uuid": service_settings_uuid,
                "service_settings_state": service_settings_state,
                "service_settings_error_message": service_settings_error_message,
                "project": project,
                "project_name": project_name,
                "project_uuid": project_uuid,
                "customer": customer,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "customer_native_name": customer_native_name,
                "customer_abbreviation": customer_abbreviation,
                "resource_type": resource_type,
                "state": state,
                "created": created,
                "modified": modified,
                "access_url": access_url,
                "namespace_name": namespace_name,
                "marketplace_offering_uuid": marketplace_offering_uuid,
                "marketplace_offering_name": marketplace_offering_name,
                "marketplace_offering_type": marketplace_offering_type,
                "marketplace_offering_plugin_options": marketplace_offering_plugin_options,
                "marketplace_category_uuid": marketplace_category_uuid,
                "marketplace_category_name": marketplace_category_name,
                "marketplace_resource_uuid": marketplace_resource_uuid,
                "marketplace_plan_uuid": marketplace_plan_uuid,
                "marketplace_resource_state": marketplace_resource_state,
                "is_usage_based": is_usage_based,
                "is_limit_based": is_limit_based,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if cluster_ip is not UNSET:
            field_dict["cluster_ip"] = cluster_ip
        if selector is not UNSET:
            field_dict["selector"] = selector
        if target_workloads is not UNSET:
            field_dict["target_workloads"] = target_workloads

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_service_create_marketplace_offering_plugin_options_type_0 import (
            RancherServiceCreateMarketplaceOfferingPluginOptionsType0,
        )
        from ..models.rancher_workload_create import RancherWorkloadCreate

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        service_name = d.pop("service_name")

        service_settings = d.pop("service_settings")

        service_settings_uuid = UUID(d.pop("service_settings_uuid"))

        service_settings_state = d.pop("service_settings_state")

        service_settings_error_message = d.pop("service_settings_error_message")

        project = d.pop("project")

        project_name = d.pop("project_name")

        project_uuid = UUID(d.pop("project_uuid"))

        customer = d.pop("customer")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        customer_native_name = d.pop("customer_native_name")

        customer_abbreviation = d.pop("customer_abbreviation")

        resource_type = d.pop("resource_type")

        state = CoreStates(d.pop("state"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_access_url(data: object) -> Union[None, list[str], str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                access_url_type_0 = cast(list[str], data)

                return access_url_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str], str], data)

        access_url = _parse_access_url(d.pop("access_url"))

        namespace_name = d.pop("namespace_name")

        def _parse_marketplace_offering_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_offering_uuid = _parse_marketplace_offering_uuid(d.pop("marketplace_offering_uuid"))

        def _parse_marketplace_offering_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_offering_name = _parse_marketplace_offering_name(d.pop("marketplace_offering_name"))

        def _parse_marketplace_offering_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_offering_type = _parse_marketplace_offering_type(d.pop("marketplace_offering_type"))

        def _parse_marketplace_offering_plugin_options(
            data: object,
        ) -> Union["RancherServiceCreateMarketplaceOfferingPluginOptionsType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                marketplace_offering_plugin_options_type_0 = (
                    RancherServiceCreateMarketplaceOfferingPluginOptionsType0.from_dict(data)
                )

                return marketplace_offering_plugin_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RancherServiceCreateMarketplaceOfferingPluginOptionsType0", None], data)

        marketplace_offering_plugin_options = _parse_marketplace_offering_plugin_options(
            d.pop("marketplace_offering_plugin_options")
        )

        def _parse_marketplace_category_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_category_uuid = _parse_marketplace_category_uuid(d.pop("marketplace_category_uuid"))

        def _parse_marketplace_category_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_category_name = _parse_marketplace_category_name(d.pop("marketplace_category_name"))

        def _parse_marketplace_resource_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_resource_uuid = _parse_marketplace_resource_uuid(d.pop("marketplace_resource_uuid"))

        def _parse_marketplace_plan_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_plan_uuid = _parse_marketplace_plan_uuid(d.pop("marketplace_plan_uuid"))

        def _parse_marketplace_resource_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        marketplace_resource_state = _parse_marketplace_resource_state(d.pop("marketplace_resource_state"))

        def _parse_is_usage_based(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        is_usage_based = _parse_is_usage_based(d.pop("is_usage_based"))

        def _parse_is_limit_based(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        is_limit_based = _parse_is_limit_based(d.pop("is_limit_based"))

        description = d.pop("description", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        namespace = d.pop("namespace", UNSET)

        def _parse_cluster_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster_ip = _parse_cluster_ip(d.pop("cluster_ip", UNSET))

        selector = d.pop("selector", UNSET)

        target_workloads = []
        _target_workloads = d.pop("target_workloads", UNSET)
        for target_workloads_item_data in _target_workloads or []:
            target_workloads_item = RancherWorkloadCreate.from_dict(target_workloads_item_data)

            target_workloads.append(target_workloads_item)

        rancher_service_create = cls(
            url=url,
            uuid=uuid,
            name=name,
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
            resource_type=resource_type,
            state=state,
            created=created,
            modified=modified,
            access_url=access_url,
            namespace_name=namespace_name,
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
            description=description,
            error_message=error_message,
            error_traceback=error_traceback,
            backend_id=backend_id,
            runtime_state=runtime_state,
            namespace=namespace,
            cluster_ip=cluster_ip,
            selector=selector,
            target_workloads=target_workloads,
        )

        rancher_service_create.additional_properties = d
        return rancher_service_create

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
