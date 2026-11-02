from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_available_teams_channels_response_200_channels_item import (
        ListAvailableTeamsChannelsResponse200ChannelsItem,
    )


T = TypeVar("T", bound="ListAvailableTeamsChannelsResponse200")


@_attrs_define
class ListAvailableTeamsChannelsResponse200:
    """
    Attributes:
        channels (Union[Unset, List['ListAvailableTeamsChannelsResponse200ChannelsItem']]):
        total_count (Union[Unset, int]):
    """

    channels: Union[Unset, List["ListAvailableTeamsChannelsResponse200ChannelsItem"]] = UNSET
    total_count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.channels, Unset):
            channels = []
            for channels_item_data in self.channels:
                channels_item = channels_item_data.to_dict()

                channels.append(channels_item)

        total_count = self.total_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channels is not UNSET:
            field_dict["channels"] = channels
        if total_count is not UNSET:
            field_dict["total_count"] = total_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_available_teams_channels_response_200_channels_item import (
            ListAvailableTeamsChannelsResponse200ChannelsItem,
        )

        d = src_dict.copy()
        channels = []
        _channels = d.pop("channels", UNSET)
        for channels_item_data in _channels or []:
            channels_item = ListAvailableTeamsChannelsResponse200ChannelsItem.from_dict(channels_item_data)

            channels.append(channels_item)

        total_count = d.pop("total_count", UNSET)

        list_available_teams_channels_response_200 = cls(
            channels=channels,
            total_count=total_count,
        )

        list_available_teams_channels_response_200.additional_properties = d
        return list_available_teams_channels_response_200

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
