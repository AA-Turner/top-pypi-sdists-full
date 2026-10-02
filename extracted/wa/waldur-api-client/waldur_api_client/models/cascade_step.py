from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.cascade_step_type_enum import CascadeStepTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cascade_step_choices import CascadeStepChoices
    from ..models.cascade_step_choices_map import CascadeStepChoicesMap


T = TypeVar("T", bound="CascadeStep")


@_attrs_define
class CascadeStep:
    """
    Attributes:
        name (str):
        label (str):
        type_ (CascadeStepTypeEnum):
        depends_on (Union[Unset, str]):
        choices (Union[Unset, CascadeStepChoices]):
        choices_map (Union[Unset, CascadeStepChoicesMap]):
    """

    name: str
    label: str
    type_: CascadeStepTypeEnum
    depends_on: Union[Unset, str] = UNSET
    choices: Union[Unset, "CascadeStepChoices"] = UNSET
    choices_map: Union[Unset, "CascadeStepChoicesMap"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        label = self.label

        type_ = self.type_.value

        depends_on = self.depends_on

        choices: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.choices, Unset):
            choices = self.choices.to_dict()

        choices_map: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.choices_map, Unset):
            choices_map = self.choices_map.to_dict()

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
        from ..models.cascade_step_choices import CascadeStepChoices
        from ..models.cascade_step_choices_map import CascadeStepChoicesMap

        d = dict(src_dict)
        name = d.pop("name")

        label = d.pop("label")

        type_ = CascadeStepTypeEnum(d.pop("type"))

        depends_on = d.pop("depends_on", UNSET)

        _choices = d.pop("choices", UNSET)
        choices: Union[Unset, CascadeStepChoices]
        if isinstance(_choices, Unset):
            choices = UNSET
        else:
            choices = CascadeStepChoices.from_dict(_choices)

        _choices_map = d.pop("choices_map", UNSET)
        choices_map: Union[Unset, CascadeStepChoicesMap]
        if isinstance(_choices_map, Unset):
            choices_map = UNSET
        else:
            choices_map = CascadeStepChoicesMap.from_dict(_choices_map)

        cascade_step = cls(
            name=name,
            label=label,
            type_=type_,
            depends_on=depends_on,
            choices=choices,
            choices_map=choices_map,
        )

        cascade_step.additional_properties = d
        return cascade_step

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
