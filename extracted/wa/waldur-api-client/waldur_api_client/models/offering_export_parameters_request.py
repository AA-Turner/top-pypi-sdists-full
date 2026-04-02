from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingExportParametersRequest")


@_attrs_define
class OfferingExportParametersRequest:
    """
    Attributes:
        include_components (Union[Unset, bool]): Include offering components in export Default: True.
        include_plans (Union[Unset, bool]): Include offering plans in export Default: True.
        include_screenshots (Union[Unset, bool]): Include offering screenshots in export Default: True.
        include_files (Union[Unset, bool]): Include offering files in export Default: True.
        include_endpoints (Union[Unset, bool]): Include offering access endpoints in export Default: True.
        include_organization_groups (Union[Unset, bool]): Include organization groups associations in export Default:
            True.
        include_terms_of_service (Union[Unset, bool]): Include terms of service configurations in export Default: True.
        include_plugin_options (Union[Unset, bool]): Include plugin options in export Default: True.
        include_secret_options (Union[Unset, bool]): Include secret options in export (WARNING: sensitive data) Default:
            False.
        include_attributes (Union[Unset, bool]): Include offering attributes in export Default: True.
        include_options (Union[Unset, bool]): Include offering options in export Default: True.
        include_resource_options (Union[Unset, bool]): Include resource options in export Default: True.
    """

    include_components: Union[Unset, bool] = True
    include_plans: Union[Unset, bool] = True
    include_screenshots: Union[Unset, bool] = True
    include_files: Union[Unset, bool] = True
    include_endpoints: Union[Unset, bool] = True
    include_organization_groups: Union[Unset, bool] = True
    include_terms_of_service: Union[Unset, bool] = True
    include_plugin_options: Union[Unset, bool] = True
    include_secret_options: Union[Unset, bool] = False
    include_attributes: Union[Unset, bool] = True
    include_options: Union[Unset, bool] = True
    include_resource_options: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        include_components = self.include_components

        include_plans = self.include_plans

        include_screenshots = self.include_screenshots

        include_files = self.include_files

        include_endpoints = self.include_endpoints

        include_organization_groups = self.include_organization_groups

        include_terms_of_service = self.include_terms_of_service

        include_plugin_options = self.include_plugin_options

        include_secret_options = self.include_secret_options

        include_attributes = self.include_attributes

        include_options = self.include_options

        include_resource_options = self.include_resource_options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_components is not UNSET:
            field_dict["include_components"] = include_components
        if include_plans is not UNSET:
            field_dict["include_plans"] = include_plans
        if include_screenshots is not UNSET:
            field_dict["include_screenshots"] = include_screenshots
        if include_files is not UNSET:
            field_dict["include_files"] = include_files
        if include_endpoints is not UNSET:
            field_dict["include_endpoints"] = include_endpoints
        if include_organization_groups is not UNSET:
            field_dict["include_organization_groups"] = include_organization_groups
        if include_terms_of_service is not UNSET:
            field_dict["include_terms_of_service"] = include_terms_of_service
        if include_plugin_options is not UNSET:
            field_dict["include_plugin_options"] = include_plugin_options
        if include_secret_options is not UNSET:
            field_dict["include_secret_options"] = include_secret_options
        if include_attributes is not UNSET:
            field_dict["include_attributes"] = include_attributes
        if include_options is not UNSET:
            field_dict["include_options"] = include_options
        if include_resource_options is not UNSET:
            field_dict["include_resource_options"] = include_resource_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        include_components = d.pop("include_components", UNSET)

        include_plans = d.pop("include_plans", UNSET)

        include_screenshots = d.pop("include_screenshots", UNSET)

        include_files = d.pop("include_files", UNSET)

        include_endpoints = d.pop("include_endpoints", UNSET)

        include_organization_groups = d.pop("include_organization_groups", UNSET)

        include_terms_of_service = d.pop("include_terms_of_service", UNSET)

        include_plugin_options = d.pop("include_plugin_options", UNSET)

        include_secret_options = d.pop("include_secret_options", UNSET)

        include_attributes = d.pop("include_attributes", UNSET)

        include_options = d.pop("include_options", UNSET)

        include_resource_options = d.pop("include_resource_options", UNSET)

        offering_export_parameters_request = cls(
            include_components=include_components,
            include_plans=include_plans,
            include_screenshots=include_screenshots,
            include_files=include_files,
            include_endpoints=include_endpoints,
            include_organization_groups=include_organization_groups,
            include_terms_of_service=include_terms_of_service,
            include_plugin_options=include_plugin_options,
            include_secret_options=include_secret_options,
            include_attributes=include_attributes,
            include_options=include_options,
            include_resource_options=include_resource_options,
        )

        offering_export_parameters_request.additional_properties = d
        return offering_export_parameters_request

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
