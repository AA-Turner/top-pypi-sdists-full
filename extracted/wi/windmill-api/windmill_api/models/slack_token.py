from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.slack_token_team import SlackTokenTeam


T = TypeVar("T", bound="SlackToken")


@_attrs_define
class SlackToken:
    """
    Attributes:
        access_token (str):
        team (Union[Unset, SlackTokenTeam]):
    """

    access_token: str
    team: Union[Unset, "SlackTokenTeam"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token
        team: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.team, Unset):
            team = self.team.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_token": access_token,
            }
        )
        if team is not UNSET:
            field_dict["team"] = team

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.slack_token_team import SlackTokenTeam

        d = src_dict.copy()
        access_token = d.pop("access_token")

        _team = d.pop("team", UNSET)
        team: Union[Unset, SlackTokenTeam]
        if isinstance(_team, Unset):
            team = UNSET
        else:
            team = SlackTokenTeam.from_dict(_team)

        slack_token = cls(
            access_token=access_token,
            team=team,
        )

        slack_token.additional_properties = d
        return slack_token

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
