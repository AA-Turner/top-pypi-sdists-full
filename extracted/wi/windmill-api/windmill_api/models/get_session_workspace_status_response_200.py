from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_session_workspace_status_response_200_additional_property import (
    GetSessionWorkspaceStatusResponse200AdditionalProperty,
)

T = TypeVar("T", bound="GetSessionWorkspaceStatusResponse200")


@_attrs_define
class GetSessionWorkspaceStatusResponse200:
    """ """

    additional_properties: Dict[str, GetSessionWorkspaceStatusResponse200AdditionalProperty] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.value

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        get_session_workspace_status_response_200 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetSessionWorkspaceStatusResponse200AdditionalProperty(prop_dict)

            additional_properties[prop_name] = additional_property

        get_session_workspace_status_response_200.additional_properties = additional_properties
        return get_session_workspace_status_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> GetSessionWorkspaceStatusResponse200AdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: GetSessionWorkspaceStatusResponse200AdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
