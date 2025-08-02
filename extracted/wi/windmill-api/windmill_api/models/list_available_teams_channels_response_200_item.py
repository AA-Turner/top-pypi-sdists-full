from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAvailableTeamsChannelsResponse200Item")


@_attrs_define
class ListAvailableTeamsChannelsResponse200Item:
    """
    Attributes:
        channel_name (Union[Unset, str]):
        channel_id (Union[Unset, str]):
        service_url (Union[Unset, str]):
        tenant_id (Union[Unset, str]):
    """

    channel_name: Union[Unset, str] = UNSET
    channel_id: Union[Unset, str] = UNSET
    service_url: Union[Unset, str] = UNSET
    tenant_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_name = self.channel_name
        channel_id = self.channel_id
        service_url = self.service_url
        tenant_id = self.tenant_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channel_name is not UNSET:
            field_dict["channel_name"] = channel_name
        if channel_id is not UNSET:
            field_dict["channel_id"] = channel_id
        if service_url is not UNSET:
            field_dict["service_url"] = service_url
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel_name = d.pop("channel_name", UNSET)

        channel_id = d.pop("channel_id", UNSET)

        service_url = d.pop("service_url", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        list_available_teams_channels_response_200_item = cls(
            channel_name=channel_name,
            channel_id=channel_id,
            service_url=service_url,
            tenant_id=tenant_id,
        )

        list_available_teams_channels_response_200_item.additional_properties = d
        return list_available_teams_channels_response_200_item

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
