from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_settings_response_200_deploy_ui_include_type_item import GetSettingsResponse200DeployUiIncludeTypeItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetSettingsResponse200DeployUi")


@_attrs_define
class GetSettingsResponse200DeployUi:
    """
    Attributes:
        include_path (Union[Unset, List[str]]):
        include_type (Union[Unset, List[GetSettingsResponse200DeployUiIncludeTypeItem]]):
    """

    include_path: Union[Unset, List[str]] = UNSET
    include_type: Union[Unset, List[GetSettingsResponse200DeployUiIncludeTypeItem]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        include_path: Union[Unset, List[str]] = UNSET
        if not isinstance(self.include_path, Unset):
            include_path = self.include_path

        include_type: Union[Unset, List[str]] = UNSET
        if not isinstance(self.include_type, Unset):
            include_type = []
            for include_type_item_data in self.include_type:
                include_type_item = include_type_item_data.value

                include_type.append(include_type_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_path is not UNSET:
            field_dict["include_path"] = include_path
        if include_type is not UNSET:
            field_dict["include_type"] = include_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        include_path = cast(List[str], d.pop("include_path", UNSET))

        include_type = []
        _include_type = d.pop("include_type", UNSET)
        for include_type_item_data in _include_type or []:
            include_type_item = GetSettingsResponse200DeployUiIncludeTypeItem(include_type_item_data)

            include_type.append(include_type_item)

        get_settings_response_200_deploy_ui = cls(
            include_path=include_path,
            include_type=include_type,
        )

        get_settings_response_200_deploy_ui.additional_properties = d
        return get_settings_response_200_deploy_ui

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
