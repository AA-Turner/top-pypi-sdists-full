from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.issue_type_enum import IssueTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedTemplateRequest")


@_attrs_define
class PatchedTemplateRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        issue_type (Union[Unset, IssueTypeEnum]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    issue_type: Union[Unset, IssueTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        issue_type: Union[Unset, str] = UNSET
        if not isinstance(self.issue_type, Unset):
            issue_type = self.issue_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if issue_type is not UNSET:
            field_dict["issue_type"] = issue_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _issue_type = d.pop("issue_type", UNSET)
        issue_type: Union[Unset, IssueTypeEnum]
        if isinstance(_issue_type, Unset):
            issue_type = UNSET
        else:
            issue_type = IssueTypeEnum(_issue_type)

        patched_template_request = cls(
            name=name,
            description=description,
            issue_type=issue_type,
        )

        patched_template_request.additional_properties = d
        return patched_template_request

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
