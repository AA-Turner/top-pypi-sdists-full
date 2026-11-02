import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_latest_workspace_dependencies_response_200_language import (
    GetLatestWorkspaceDependenciesResponse200Language,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetLatestWorkspaceDependenciesResponse200")


@_attrs_define
class GetLatestWorkspaceDependenciesResponse200:
    """
    Attributes:
        id (int):
        archived (bool):
        content (str):
        language (GetLatestWorkspaceDependenciesResponse200Language):
        workspace_id (str):
        created_at (datetime.datetime):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
    """

    id: int
    archived: bool
    content: str
    language: GetLatestWorkspaceDependenciesResponse200Language
    workspace_id: str
    created_at: datetime.datetime
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        archived = self.archived
        content = self.content
        language = self.language.value

        workspace_id = self.workspace_id
        created_at = self.created_at.isoformat()

        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "archived": archived,
                "content": content,
                "language": language,
                "workspace_id": workspace_id,
                "created_at": created_at,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        archived = d.pop("archived")

        content = d.pop("content")

        language = GetLatestWorkspaceDependenciesResponse200Language(d.pop("language"))

        workspace_id = d.pop("workspace_id")

        created_at = isoparse(d.pop("created_at"))

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        get_latest_workspace_dependencies_response_200 = cls(
            id=id,
            archived=archived,
            content=content,
            language=language,
            workspace_id=workspace_id,
            created_at=created_at,
            name=name,
            description=description,
        )

        get_latest_workspace_dependencies_response_200.additional_properties = d
        return get_latest_workspace_dependencies_response_200

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
