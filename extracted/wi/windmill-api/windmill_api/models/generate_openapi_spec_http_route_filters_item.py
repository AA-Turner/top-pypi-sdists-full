from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GenerateOpenapiSpecHttpRouteFiltersItem")


@_attrs_define
class GenerateOpenapiSpecHttpRouteFiltersItem:
    """
    Attributes:
        folder_regex (str):
        path_regex (str):
        route_path_regex (str):
    """

    folder_regex: str
    path_regex: str
    route_path_regex: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        folder_regex = self.folder_regex
        path_regex = self.path_regex
        route_path_regex = self.route_path_regex

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "folder_regex": folder_regex,
                "path_regex": path_regex,
                "route_path_regex": route_path_regex,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        folder_regex = d.pop("folder_regex")

        path_regex = d.pop("path_regex")

        route_path_regex = d.pop("route_path_regex")

        generate_openapi_spec_http_route_filters_item = cls(
            folder_regex=folder_regex,
            path_regex=path_regex,
            route_path_regex=route_path_regex,
        )

        generate_openapi_spec_http_route_filters_item.additional_properties = d
        return generate_openapi_spec_http_route_filters_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
