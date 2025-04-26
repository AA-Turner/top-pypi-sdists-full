from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.team_info_channels_item import TeamInfoChannelsItem


T = TypeVar("T", bound="TeamInfo")


@_attrs_define
class TeamInfo:
    """
    Attributes:
        team_id (str): The unique identifier of the Microsoft Teams team Example: 19:abc123def456@thread.tacv2.
        team_name (str): The display name of the Microsoft Teams team Example: Engineering Team.
        channels (List['TeamInfoChannelsItem']): List of channels within the team
    """

    team_id: str
    team_name: str
    channels: List["TeamInfoChannelsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        team_id = self.team_id
        team_name = self.team_name
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.to_dict()

            channels.append(channels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "team_id": team_id,
                "team_name": team_name,
                "channels": channels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.team_info_channels_item import TeamInfoChannelsItem

        d = src_dict.copy()
        team_id = d.pop("team_id")

        team_name = d.pop("team_name")

        channels = []
        _channels = d.pop("channels")
        for channels_item_data in _channels:
            channels_item = TeamInfoChannelsItem.from_dict(channels_item_data)

            channels.append(channels_item)

        team_info = cls(
            team_id=team_id,
            team_name=team_name,
            channels=channels,
        )

        team_info.additional_properties = d
        return team_info

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
