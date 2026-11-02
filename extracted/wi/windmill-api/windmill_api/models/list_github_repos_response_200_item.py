from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListGithubReposResponse200Item")


@_attrs_define
class ListGithubReposResponse200Item:
    """
    Attributes:
        full_name (str):
        name (str):
        owner (str):
        private (bool):
    """

    full_name: str
    name: str
    owner: str
    private: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        full_name = self.full_name
        name = self.name
        owner = self.owner
        private = self.private

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "name": name,
                "owner": owner,
                "private": private,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        full_name = d.pop("full_name")

        name = d.pop("name")

        owner = d.pop("owner")

        private = d.pop("private")

        list_github_repos_response_200_item = cls(
            full_name=full_name,
            name=name,
            owner=owner,
            private=private,
        )

        list_github_repos_response_200_item.additional_properties = d
        return list_github_repos_response_200_item

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
