from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_available_slack_channels_response_200_channels_item import (
        ListAvailableSlackChannelsResponse200ChannelsItem,
    )


T = TypeVar("T", bound="ListAvailableSlackChannelsResponse200")


@_attrs_define
class ListAvailableSlackChannelsResponse200:
    """
    Attributes:
        channels (List['ListAvailableSlackChannelsResponse200ChannelsItem']):
        next_cursor (Union[Unset, str]):
    """

    channels: List["ListAvailableSlackChannelsResponse200ChannelsItem"]
    next_cursor: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.to_dict()

            channels.append(channels_item)

        next_cursor = self.next_cursor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channels": channels,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_available_slack_channels_response_200_channels_item import (
            ListAvailableSlackChannelsResponse200ChannelsItem,
        )

        d = src_dict.copy()
        channels = []
        _channels = d.pop("channels")
        for channels_item_data in _channels:
            channels_item = ListAvailableSlackChannelsResponse200ChannelsItem.from_dict(channels_item_data)

            channels.append(channels_item)

        next_cursor = d.pop("next_cursor", UNSET)

        list_available_slack_channels_response_200 = cls(
            channels=channels,
            next_cursor=next_cursor,
        )

        list_available_slack_channels_response_200.additional_properties = d
        return list_available_slack_channels_response_200

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
