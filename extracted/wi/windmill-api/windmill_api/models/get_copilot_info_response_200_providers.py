from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_copilot_info_response_200_providers_additional_property import (
        GetCopilotInfoResponse200ProvidersAdditionalProperty,
    )


T = TypeVar("T", bound="GetCopilotInfoResponse200Providers")


@_attrs_define
class GetCopilotInfoResponse200Providers:
    """ """

    additional_properties: Dict[str, "GetCopilotInfoResponse200ProvidersAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_copilot_info_response_200_providers_additional_property import (
            GetCopilotInfoResponse200ProvidersAdditionalProperty,
        )

        d = src_dict.copy()
        get_copilot_info_response_200_providers = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetCopilotInfoResponse200ProvidersAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_copilot_info_response_200_providers.additional_properties = additional_properties
        return get_copilot_info_response_200_providers

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetCopilotInfoResponse200ProvidersAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GetCopilotInfoResponse200ProvidersAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
