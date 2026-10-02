from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AtlassianRequestTypeResponse")


@_attrs_define
class AtlassianRequestTypeResponse:
    """
    Attributes:
        id (str):
        name (str):
        description (Union[Unset, str]):
        issue_type_id (Union[Unset, str]):
    """

    id: str
    name: str
    description: Union[Unset, str] = UNSET
    issue_type_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        issue_type_id = self.issue_type_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if issue_type_id is not UNSET:
            field_dict["issue_type_id"] = issue_type_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        issue_type_id = d.pop("issue_type_id", UNSET)

        atlassian_request_type_response = cls(
            id=id,
            name=name,
            description=description,
            issue_type_id=issue_type_id,
        )

        atlassian_request_type_response.additional_properties = d
        return atlassian_request_type_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
