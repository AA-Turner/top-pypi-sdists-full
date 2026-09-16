from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListHubIntegrationsResponse200Item")


@_attrs_define
class ListHubIntegrationsResponse200Item:
    """
    Attributes:
        name (str):
        picks (Union[Unset, int]): how often the integration has been picked, absent on a hub that does not count picks
        display_name (Union[Unset, None, str]): the label the hub curates for the integration, null or absent where it
            names none
    """

    name: str
    picks: Union[Unset, int] = UNSET
    display_name: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        picks = self.picks
        display_name = self.display_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if picks is not UNSET:
            field_dict["picks"] = picks
        if display_name is not UNSET:
            field_dict["display_name"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        picks = d.pop("picks", UNSET)

        display_name = d.pop("display_name", UNSET)

        list_hub_integrations_response_200_item = cls(
            name=name,
            picks=picks,
            display_name=display_name,
        )

        list_hub_integrations_response_200_item.additional_properties = d
        return list_hub_integrations_response_200_item

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
