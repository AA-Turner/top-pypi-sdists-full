from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GitlabProject")


@_attrs_define
class GitlabProject:
    """a GitLab project a token can sync, as the resource form needs it

    Attributes:
        path_with_namespace (str): nested group path plus project name, which is also GitLab's project id
        http_url_to_repo (str):
        default_branch (Union[Unset, str]):
    """

    path_with_namespace: str
    http_url_to_repo: str
    default_branch: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path_with_namespace = self.path_with_namespace
        http_url_to_repo = self.http_url_to_repo
        default_branch = self.default_branch

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path_with_namespace": path_with_namespace,
                "http_url_to_repo": http_url_to_repo,
            }
        )
        if default_branch is not UNSET:
            field_dict["default_branch"] = default_branch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path_with_namespace = d.pop("path_with_namespace")

        http_url_to_repo = d.pop("http_url_to_repo")

        default_branch = d.pop("default_branch", UNSET)

        gitlab_project = cls(
            path_with_namespace=path_with_namespace,
            http_url_to_repo=http_url_to_repo,
            default_branch=default_branch,
        )

        gitlab_project.additional_properties = d
        return gitlab_project

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
