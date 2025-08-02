from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SyncTeamsResponse200ItemChannelsItem")


@_attrs_define
class SyncTeamsResponse200ItemChannelsItem:
    """
    Attributes:
        channel_id (str): The unique identifier of the channel Example: 19:channel123@thread.tacv2.
        channel_name (str): The display name of the channel Example: General.
        tenant_id (str): The Microsoft Teams tenant identifier Example: 12345678-1234-1234-1234-123456789012.
        service_url (str): The service URL for the channel Example:
            https://smba.trafficmanager.net/amer/12345678-1234-1234-1234-123456789012/.
    """

    channel_id: str
    channel_name: str
    tenant_id: str
    service_url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel_id = self.channel_id
        channel_name = self.channel_name
        tenant_id = self.tenant_id
        service_url = self.service_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_id": channel_id,
                "channel_name": channel_name,
                "tenant_id": tenant_id,
                "service_url": service_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel_id = d.pop("channel_id")

        channel_name = d.pop("channel_name")

        tenant_id = d.pop("tenant_id")

        service_url = d.pop("service_url")

        sync_teams_response_200_item_channels_item = cls(
            channel_id=channel_id,
            channel_name=channel_name,
            tenant_id=tenant_id,
            service_url=service_url,
        )

        sync_teams_response_200_item_channels_item.additional_properties = d
        return sync_teams_response_200_item_channels_item

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
