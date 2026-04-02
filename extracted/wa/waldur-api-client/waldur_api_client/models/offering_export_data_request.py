from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.export_component_data_request import ExportComponentDataRequest
    from ..models.export_endpoint_data_request import ExportEndpointDataRequest
    from ..models.export_file_data_request import ExportFileDataRequest
    from ..models.export_offering_data_request import ExportOfferingDataRequest
    from ..models.export_organization_group_data_request import ExportOrganizationGroupDataRequest
    from ..models.export_plan_data_request import ExportPlanDataRequest
    from ..models.export_screenshot_data_request import ExportScreenshotDataRequest
    from ..models.export_terms_of_service_data_request import ExportTermsOfServiceDataRequest


T = TypeVar("T", bound="OfferingExportDataRequest")


@_attrs_define
class OfferingExportDataRequest:
    """
    Attributes:
        offering (ExportOfferingDataRequest):
        components (Union[Unset, list['ExportComponentDataRequest']]):
        plans (Union[Unset, list['ExportPlanDataRequest']]):
        screenshots (Union[Unset, list['ExportScreenshotDataRequest']]):
        files (Union[Unset, list['ExportFileDataRequest']]):
        endpoints (Union[Unset, list['ExportEndpointDataRequest']]):
        organization_groups (Union[Unset, list['ExportOrganizationGroupDataRequest']]):
        terms_of_service (Union[Unset, list['ExportTermsOfServiceDataRequest']]):
        plugin_options (Union[Unset, Any]):
        secret_options (Union[Unset, Any]):
        resource_options (Union[Unset, Any]):
    """

    offering: "ExportOfferingDataRequest"
    components: Union[Unset, list["ExportComponentDataRequest"]] = UNSET
    plans: Union[Unset, list["ExportPlanDataRequest"]] = UNSET
    screenshots: Union[Unset, list["ExportScreenshotDataRequest"]] = UNSET
    files: Union[Unset, list["ExportFileDataRequest"]] = UNSET
    endpoints: Union[Unset, list["ExportEndpointDataRequest"]] = UNSET
    organization_groups: Union[Unset, list["ExportOrganizationGroupDataRequest"]] = UNSET
    terms_of_service: Union[Unset, list["ExportTermsOfServiceDataRequest"]] = UNSET
    plugin_options: Union[Unset, Any] = UNSET
    secret_options: Union[Unset, Any] = UNSET
    resource_options: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering = self.offering.to_dict()

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()
                components.append(components_item)

        plans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.plans, Unset):
            plans = []
            for plans_item_data in self.plans:
                plans_item = plans_item_data.to_dict()
                plans.append(plans_item)

        screenshots: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.screenshots, Unset):
            screenshots = []
            for screenshots_item_data in self.screenshots:
                screenshots_item = screenshots_item_data.to_dict()
                screenshots.append(screenshots_item)

        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        endpoints: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.endpoints, Unset):
            endpoints = []
            for endpoints_item_data in self.endpoints:
                endpoints_item = endpoints_item_data.to_dict()
                endpoints.append(endpoints_item)

        organization_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = []
            for organization_groups_item_data in self.organization_groups:
                organization_groups_item = organization_groups_item_data.to_dict()
                organization_groups.append(organization_groups_item)

        terms_of_service: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.terms_of_service, Unset):
            terms_of_service = []
            for terms_of_service_item_data in self.terms_of_service:
                terms_of_service_item = terms_of_service_item_data.to_dict()
                terms_of_service.append(terms_of_service_item)

        plugin_options = self.plugin_options

        secret_options = self.secret_options

        resource_options = self.resource_options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering": offering,
            }
        )
        if components is not UNSET:
            field_dict["components"] = components
        if plans is not UNSET:
            field_dict["plans"] = plans
        if screenshots is not UNSET:
            field_dict["screenshots"] = screenshots
        if files is not UNSET:
            field_dict["files"] = files
        if endpoints is not UNSET:
            field_dict["endpoints"] = endpoints
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if terms_of_service is not UNSET:
            field_dict["terms_of_service"] = terms_of_service
        if plugin_options is not UNSET:
            field_dict["plugin_options"] = plugin_options
        if secret_options is not UNSET:
            field_dict["secret_options"] = secret_options
        if resource_options is not UNSET:
            field_dict["resource_options"] = resource_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export_component_data_request import ExportComponentDataRequest
        from ..models.export_endpoint_data_request import ExportEndpointDataRequest
        from ..models.export_file_data_request import ExportFileDataRequest
        from ..models.export_offering_data_request import ExportOfferingDataRequest
        from ..models.export_organization_group_data_request import ExportOrganizationGroupDataRequest
        from ..models.export_plan_data_request import ExportPlanDataRequest
        from ..models.export_screenshot_data_request import ExportScreenshotDataRequest
        from ..models.export_terms_of_service_data_request import ExportTermsOfServiceDataRequest

        d = dict(src_dict)
        offering = ExportOfferingDataRequest.from_dict(d.pop("offering"))

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = ExportComponentDataRequest.from_dict(components_item_data)

            components.append(components_item)

        plans = []
        _plans = d.pop("plans", UNSET)
        for plans_item_data in _plans or []:
            plans_item = ExportPlanDataRequest.from_dict(plans_item_data)

            plans.append(plans_item)

        screenshots = []
        _screenshots = d.pop("screenshots", UNSET)
        for screenshots_item_data in _screenshots or []:
            screenshots_item = ExportScreenshotDataRequest.from_dict(screenshots_item_data)

            screenshots.append(screenshots_item)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = ExportFileDataRequest.from_dict(files_item_data)

            files.append(files_item)

        endpoints = []
        _endpoints = d.pop("endpoints", UNSET)
        for endpoints_item_data in _endpoints or []:
            endpoints_item = ExportEndpointDataRequest.from_dict(endpoints_item_data)

            endpoints.append(endpoints_item)

        organization_groups = []
        _organization_groups = d.pop("organization_groups", UNSET)
        for organization_groups_item_data in _organization_groups or []:
            organization_groups_item = ExportOrganizationGroupDataRequest.from_dict(organization_groups_item_data)

            organization_groups.append(organization_groups_item)

        terms_of_service = []
        _terms_of_service = d.pop("terms_of_service", UNSET)
        for terms_of_service_item_data in _terms_of_service or []:
            terms_of_service_item = ExportTermsOfServiceDataRequest.from_dict(terms_of_service_item_data)

            terms_of_service.append(terms_of_service_item)

        plugin_options = d.pop("plugin_options", UNSET)

        secret_options = d.pop("secret_options", UNSET)

        resource_options = d.pop("resource_options", UNSET)

        offering_export_data_request = cls(
            offering=offering,
            components=components,
            plans=plans,
            screenshots=screenshots,
            files=files,
            endpoints=endpoints,
            organization_groups=organization_groups,
            terms_of_service=terms_of_service,
            plugin_options=plugin_options,
            secret_options=secret_options,
            resource_options=resource_options,
        )

        offering_export_data_request.additional_properties = d
        return offering_export_data_request

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
