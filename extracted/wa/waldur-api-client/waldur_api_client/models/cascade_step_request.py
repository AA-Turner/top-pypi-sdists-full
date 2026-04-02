from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.cascade_step_type_enum import CascadeStepTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CascadeStepRequest")


@_attrs_define
class CascadeStepRequest:
    """
    Attributes:
        name (str):
        label (str):
        type_ (CascadeStepTypeEnum):
        depends_on (Union[Unset, str]):
        choices (Union[Unset, Any]):
        choices_map (Union[Unset, Any]):
    """

    name: str
    label: str
    type_: CascadeStepTypeEnum
    depends_on: Union[Unset, str] = UNSET
    choices: Union[Unset, Any] = UNSET
    choices_map: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        label = self.label

        type_ = self.type_.value

        depends_on = self.depends_on

        choices = self.choices

        choices_map = self.choices_map

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "label": label,
                "type": type_,
            }
        )
        if depends_on is not UNSET:
            field_dict["depends_on"] = depends_on
        if choices is not UNSET:
            field_dict["choices"] = choices
        if choices_map is not UNSET:
            field_dict["choices_map"] = choices_map

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        label = d.pop("label")

        type_ = CascadeStepTypeEnum(d.pop("type"))

        depends_on = d.pop("depends_on", UNSET)

        choices = d.pop("choices", UNSET)

        choices_map = d.pop("choices_map", UNSET)

        cascade_step_request = cls(
            name=name,
            label=label,
            type_=type_,
            depends_on=depends_on,
            choices=choices,
            choices_map=choices_map,
        )

        cascade_step_request.additional_properties = d
        return cascade_step_request

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
