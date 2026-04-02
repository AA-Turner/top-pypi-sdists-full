from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_export_data_request import OfferingExportDataRequest


T = TypeVar("T", bound="OfferingImportParametersRequest")


@_attrs_define
class OfferingImportParametersRequest:
    """
    Attributes:
        offering_data (OfferingExportDataRequest):
        customer (Union[None, UUID, Unset]): Target customer for imported offering. If not provided, uses current user's
            customer
        category (Union[None, Unset, str]): Target category name for imported offering. If not provided, uses category
            from export data
        project (Union[None, UUID, Unset]): Target project for imported offering (optional)
        import_components (Union[Unset, bool]): Import offering components Default: True.
        import_plans (Union[Unset, bool]): Import offering plans Default: True.
        import_screenshots (Union[Unset, bool]): Import offering screenshots Default: True.
        import_files (Union[Unset, bool]): Import offering files Default: True.
        import_endpoints (Union[Unset, bool]): Import offering access endpoints Default: True.
        import_organization_groups (Union[Unset, bool]): Import organization groups associations (may fail if groups
            don't exist) Default: False.
        import_terms_of_service (Union[Unset, bool]): Import terms of service configurations Default: True.
        import_plugin_options (Union[Unset, bool]): Import plugin options Default: True.
        import_secret_options (Union[Unset, bool]): Import secret options (WARNING: will overwrite existing secrets)
            Default: False.
        overwrite_existing (Union[Unset, bool]): Overwrite existing offering if one with the same name exists Default:
            False.
    """

    offering_data: "OfferingExportDataRequest"
    customer: Union[None, UUID, Unset] = UNSET
    category: Union[None, Unset, str] = UNSET
    project: Union[None, UUID, Unset] = UNSET
    import_components: Union[Unset, bool] = True
    import_plans: Union[Unset, bool] = True
    import_screenshots: Union[Unset, bool] = True
    import_files: Union[Unset, bool] = True
    import_endpoints: Union[Unset, bool] = True
    import_organization_groups: Union[Unset, bool] = False
    import_terms_of_service: Union[Unset, bool] = True
    import_plugin_options: Union[Unset, bool] = True
    import_secret_options: Union[Unset, bool] = False
    overwrite_existing: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_data = self.offering_data.to_dict()

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        elif isinstance(self.customer, UUID):
            customer = str(self.customer)
        else:
            customer = self.customer

        category: Union[None, Unset, str]
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        elif isinstance(self.project, UUID):
            project = str(self.project)
        else:
            project = self.project

        import_components = self.import_components

        import_plans = self.import_plans

        import_screenshots = self.import_screenshots

        import_files = self.import_files

        import_endpoints = self.import_endpoints

        import_organization_groups = self.import_organization_groups

        import_terms_of_service = self.import_terms_of_service

        import_plugin_options = self.import_plugin_options

        import_secret_options = self.import_secret_options

        overwrite_existing = self.overwrite_existing

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_data": offering_data,
            }
        )
        if customer is not UNSET:
            field_dict["customer"] = customer
        if category is not UNSET:
            field_dict["category"] = category
        if project is not UNSET:
            field_dict["project"] = project
        if import_components is not UNSET:
            field_dict["import_components"] = import_components
        if import_plans is not UNSET:
            field_dict["import_plans"] = import_plans
        if import_screenshots is not UNSET:
            field_dict["import_screenshots"] = import_screenshots
        if import_files is not UNSET:
            field_dict["import_files"] = import_files
        if import_endpoints is not UNSET:
            field_dict["import_endpoints"] = import_endpoints
        if import_organization_groups is not UNSET:
            field_dict["import_organization_groups"] = import_organization_groups
        if import_terms_of_service is not UNSET:
            field_dict["import_terms_of_service"] = import_terms_of_service
        if import_plugin_options is not UNSET:
            field_dict["import_plugin_options"] = import_plugin_options
        if import_secret_options is not UNSET:
            field_dict["import_secret_options"] = import_secret_options
        if overwrite_existing is not UNSET:
            field_dict["overwrite_existing"] = overwrite_existing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_export_data_request import OfferingExportDataRequest

        d = dict(src_dict)
        offering_data = OfferingExportDataRequest.from_dict(d.pop("offering_data"))

        def _parse_customer(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_type_0 = UUID(data)

                return customer_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        def _parse_category(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        category = _parse_category(d.pop("category", UNSET))

        def _parse_project(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_type_0 = UUID(data)

                return project_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project = _parse_project(d.pop("project", UNSET))

        import_components = d.pop("import_components", UNSET)

        import_plans = d.pop("import_plans", UNSET)

        import_screenshots = d.pop("import_screenshots", UNSET)

        import_files = d.pop("import_files", UNSET)

        import_endpoints = d.pop("import_endpoints", UNSET)

        import_organization_groups = d.pop("import_organization_groups", UNSET)

        import_terms_of_service = d.pop("import_terms_of_service", UNSET)

        import_plugin_options = d.pop("import_plugin_options", UNSET)

        import_secret_options = d.pop("import_secret_options", UNSET)

        overwrite_existing = d.pop("overwrite_existing", UNSET)

        offering_import_parameters_request = cls(
            offering_data=offering_data,
            customer=customer,
            category=category,
            project=project,
            import_components=import_components,
            import_plans=import_plans,
            import_screenshots=import_screenshots,
            import_files=import_files,
            import_endpoints=import_endpoints,
            import_organization_groups=import_organization_groups,
            import_terms_of_service=import_terms_of_service,
            import_plugin_options=import_plugin_options,
            import_secret_options=import_secret_options,
            overwrite_existing=overwrite_existing,
        )

        offering_import_parameters_request.additional_properties = d
        return offering_import_parameters_request

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
