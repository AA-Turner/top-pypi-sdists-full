from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListGitlabProjectsJsonBody")


@_attrs_define
class ListGitlabProjectsJsonBody:
    """
    Attributes:
        base_url (str): The GitLab instance, e.g. https://gitlab.com
        token (str): A project access token with the api scope, or a group token that reaches the project
        search (Union[Unset, str]): Narrow the list to projects matching this text
    """

    base_url: str
    token: str
    search: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base_url = self.base_url
        token = self.token
        search = self.search

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_url": base_url,
                "token": token,
            }
        )
        if search is not UNSET:
            field_dict["search"] = search

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        base_url = d.pop("base_url")

        token = d.pop("token")

        search = d.pop("search", UNSET)

        list_gitlab_projects_json_body = cls(
            base_url=base_url,
            token=token,
            search=search,
        )

        list_gitlab_projects_json_body.additional_properties = d
        return list_gitlab_projects_json_body

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
