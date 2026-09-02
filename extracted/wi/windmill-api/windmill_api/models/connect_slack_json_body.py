from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ConnectSlackJsonBody")


@_attrs_define
class ConnectSlackJsonBody:
    """
    Attributes:
        bot_token (str): xoxb-... bot token obtained at api.slack.com/apps
        team_id (str):
        team_name (str):
    """

    bot_token: str
    team_id: str
    team_name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bot_token = self.bot_token
        team_id = self.team_id
        team_name = self.team_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bot_token": bot_token,
                "team_id": team_id,
                "team_name": team_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bot_token = d.pop("bot_token")

        team_id = d.pop("team_id")

        team_name = d.pop("team_name")

        connect_slack_json_body = cls(
            bot_token=bot_token,
            team_id=team_id,
            team_name=team_name,
        )

        connect_slack_json_body.additional_properties = d
        return connect_slack_json_body

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
