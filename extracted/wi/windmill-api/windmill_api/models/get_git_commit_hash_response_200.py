from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetGitCommitHashResponse200")


@_attrs_define
class GetGitCommitHashResponse200:
    """
    Attributes:
        commit_hash (str): Latest commit hash from git ls-remote
    """

    commit_hash: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        commit_hash = self.commit_hash

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commit_hash": commit_hash,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        commit_hash = d.pop("commit_hash")

        get_git_commit_hash_response_200 = cls(
            commit_hash=commit_hash,
        )

        get_git_commit_hash_response_200.additional_properties = d
        return get_git_commit_hash_response_200

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
