from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmitRequestRequest")


@_attrs_define
class SubmitRequestRequest:
    """
    Attributes:
        project_name (Union[Unset, str]): Custom project name to use instead of auto-generated one
        project_description (Union[Unset, str]): Custom project description
    """

    project_name: Union[Unset, str] = UNSET
    project_description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_name = self.project_name

        project_description = self.project_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_description is not UNSET:
            field_dict["project_description"] = project_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_name = d.pop("project_name", UNSET)

        project_description = d.pop("project_description", UNSET)

        submit_request_request = cls(
            project_name=project_name,
            project_description=project_description,
        )

        submit_request_request.additional_properties = d
        return submit_request_request

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
