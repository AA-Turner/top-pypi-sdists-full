from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.option_transform_case import OptionTransformCase
from ..types import UNSET, Unset

T = TypeVar("T", bound="OptionTransformRequest")


@_attrs_define
class OptionTransformRequest:
    """
    Attributes:
        prefix (Union[Unset, str]): Text added before the value.
        suffix (Union[Unset, str]): Text added after the value.
        case (Union[BlankEnum, OptionTransformCase, Unset]): Convert the part the user typed to lower or upper case. The
            prefix and suffix are kept as written.
    """

    prefix: Union[Unset, str] = UNSET
    suffix: Union[Unset, str] = UNSET
    case: Union[BlankEnum, OptionTransformCase, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prefix = self.prefix

        suffix = self.suffix

        case: Union[Unset, str]
        if isinstance(self.case, Unset):
            case = UNSET
        elif isinstance(self.case, OptionTransformCase):
            case = self.case.value
        else:
            case = self.case.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if case is not UNSET:
            field_dict["case"] = case

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        prefix = d.pop("prefix", UNSET)

        suffix = d.pop("suffix", UNSET)

        def _parse_case(data: object) -> Union[BlankEnum, OptionTransformCase, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                case_type_0 = OptionTransformCase(data)

                return case_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            case_type_1 = BlankEnum(data)

            return case_type_1

        case = _parse_case(d.pop("case", UNSET))

        option_transform_request = cls(
            prefix=prefix,
            suffix=suffix,
            case=case,
        )

        option_transform_request.additional_properties = d
        return option_transform_request

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
