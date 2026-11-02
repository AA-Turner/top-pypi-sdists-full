from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_native_trigger_services_response_200_item_service_name import (
    ListNativeTriggerServicesResponse200ItemServiceName,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_native_trigger_services_response_200_item_oauth_data import (
        ListNativeTriggerServicesResponse200ItemOauthData,
    )


T = TypeVar("T", bound="ListNativeTriggerServicesResponse200Item")


@_attrs_define
class ListNativeTriggerServicesResponse200Item:
    """
    Attributes:
        service_name (ListNativeTriggerServicesResponse200ItemServiceName):
        oauth_data (Union[Unset, None, ListNativeTriggerServicesResponse200ItemOauthData]):
    """

    service_name: ListNativeTriggerServicesResponse200ItemServiceName
    oauth_data: Union[Unset, None, "ListNativeTriggerServicesResponse200ItemOauthData"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        service_name = self.service_name.value

        oauth_data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.oauth_data, Unset):
            oauth_data = self.oauth_data.to_dict() if self.oauth_data else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_name": service_name,
            }
        )
        if oauth_data is not UNSET:
            field_dict["oauth_data"] = oauth_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_native_trigger_services_response_200_item_oauth_data import (
            ListNativeTriggerServicesResponse200ItemOauthData,
        )

        d = src_dict.copy()
        service_name = ListNativeTriggerServicesResponse200ItemServiceName(d.pop("service_name"))

        _oauth_data = d.pop("oauth_data", UNSET)
        oauth_data: Union[Unset, None, ListNativeTriggerServicesResponse200ItemOauthData]
        if _oauth_data is None:
            oauth_data = None
        elif isinstance(_oauth_data, Unset):
            oauth_data = UNSET
        else:
            oauth_data = ListNativeTriggerServicesResponse200ItemOauthData.from_dict(_oauth_data)

        list_native_trigger_services_response_200_item = cls(
            service_name=service_name,
            oauth_data=oauth_data,
        )

        list_native_trigger_services_response_200_item.additional_properties = d
        return list_native_trigger_services_response_200_item

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
