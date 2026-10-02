from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AtlassianCustomFieldResponse")


@_attrs_define
class AtlassianCustomFieldResponse:
    """
    Attributes:
        id (str):
        name (str):
        clause_names (Union[Unset, list[str]]):
        field_type (Union[Unset, str]):
        required (Union[Unset, bool]):  Default: False.
    """

    id: str
    name: str
    clause_names: Union[Unset, list[str]] = UNSET
    field_type: Union[Unset, str] = UNSET
    required: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        clause_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.clause_names, Unset):
            clause_names = self.clause_names

        field_type = self.field_type

        required = self.required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if clause_names is not UNSET:
            field_dict["clause_names"] = clause_names
        if field_type is not UNSET:
            field_dict["field_type"] = field_type
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        clause_names = cast(list[str], d.pop("clause_names", UNSET))

        field_type = d.pop("field_type", UNSET)

        required = d.pop("required", UNSET)

        atlassian_custom_field_response = cls(
            id=id,
            name=name,
            clause_names=clause_names,
            field_type=field_type,
            required=required,
        )

        atlassian_custom_field_response.additional_properties = d
        return atlassian_custom_field_response

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
