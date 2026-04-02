from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.option_validator_type_enum import OptionValidatorTypeEnum

T = TypeVar("T", bound="OptionValidator")


@_attrs_define
class OptionValidator:
    """
    Attributes:
        type_ (OptionValidatorTypeEnum):
        target_field (str):
    """

    type_: OptionValidatorTypeEnum
    target_field: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        target_field = self.target_field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "target_field": target_field,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = OptionValidatorTypeEnum(d.pop("type"))

        target_field = d.pop("target_field")

        option_validator = cls(
            type_=type_,
            target_field=target_field,
        )

        option_validator.additional_properties = d
        return option_validator

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
