from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_available_teams_ids_response_200_teams_item import ListAvailableTeamsIdsResponse200TeamsItem


T = TypeVar("T", bound="ListAvailableTeamsIdsResponse200")


@_attrs_define
class ListAvailableTeamsIdsResponse200:
    """
    Attributes:
        teams (Union[Unset, List['ListAvailableTeamsIdsResponse200TeamsItem']]):
        total_count (Union[Unset, int]): Total number of teams across all pages
        per_page (Union[Unset, int]): Number of teams per page (configurable via TEAMS_PER_PAGE env var)
        next_link (Union[Unset, None, str]): URL to fetch next page of results. Null if no more pages.
    """

    teams: Union[Unset, List["ListAvailableTeamsIdsResponse200TeamsItem"]] = UNSET
    total_count: Union[Unset, int] = UNSET
    per_page: Union[Unset, int] = UNSET
    next_link: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        teams: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.teams, Unset):
            teams = []
            for teams_item_data in self.teams:
                teams_item = teams_item_data.to_dict()

                teams.append(teams_item)

        total_count = self.total_count
        per_page = self.per_page
        next_link = self.next_link

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if teams is not UNSET:
            field_dict["teams"] = teams
        if total_count is not UNSET:
            field_dict["total_count"] = total_count
        if per_page is not UNSET:
            field_dict["per_page"] = per_page
        if next_link is not UNSET:
            field_dict["next_link"] = next_link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_available_teams_ids_response_200_teams_item import ListAvailableTeamsIdsResponse200TeamsItem

        d = src_dict.copy()
        teams = []
        _teams = d.pop("teams", UNSET)
        for teams_item_data in _teams or []:
            teams_item = ListAvailableTeamsIdsResponse200TeamsItem.from_dict(teams_item_data)

            teams.append(teams_item)

        total_count = d.pop("total_count", UNSET)

        per_page = d.pop("per_page", UNSET)

        next_link = d.pop("next_link", UNSET)

        list_available_teams_ids_response_200 = cls(
            teams=teams,
            total_count=total_count,
            per_page=per_page,
            next_link=next_link,
        )

        list_available_teams_ids_response_200.additional_properties = d
        return list_available_teams_ids_response_200

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
