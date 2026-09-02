from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConnectTeamsJsonBody")


@_attrs_define
class ConnectTeamsJsonBody:
    """
    Attributes:
        team_id (Union[Unset, str]):
        team_name (Union[Unset, str]):
    """

    team_id: Union[Unset, str] = UNSET
    team_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        team_id = self.team_id
        team_name = self.team_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if team_id is not UNSET:
            field_dict["team_id"] = team_id
        if team_name is not UNSET:
            field_dict["team_name"] = team_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        team_id = d.pop("team_id", UNSET)

        team_name = d.pop("team_name", UNSET)

        connect_teams_json_body = cls(
            team_id=team_id,
            team_name=team_name,
        )

        connect_teams_json_body.additional_properties = d
        return connect_teams_json_body

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
