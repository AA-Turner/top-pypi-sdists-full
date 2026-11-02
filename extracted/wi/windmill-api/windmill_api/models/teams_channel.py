from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TeamsChannel")


@_attrs_define
class TeamsChannel:
    """
    Attributes:
        team_id (str): Microsoft Teams team ID
        team_name (str): Microsoft Teams team name
        channel_id (str): Microsoft Teams channel ID
        channel_name (str): Microsoft Teams channel name
    """

    team_id: str
    team_name: str
    channel_id: str
    channel_name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        team_id = self.team_id
        team_name = self.team_name
        channel_id = self.channel_id
        channel_name = self.channel_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "team_id": team_id,
                "team_name": team_name,
                "channel_id": channel_id,
                "channel_name": channel_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        team_id = d.pop("team_id")

        team_name = d.pop("team_name")

        channel_id = d.pop("channel_id")

        channel_name = d.pop("channel_name")

        teams_channel = cls(
            team_id=team_id,
            team_name=team_name,
            channel_id=channel_id,
            channel_name=channel_name,
        )

        teams_channel.additional_properties = d
        return teams_channel

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
