from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckUniqueBackendIDResponse")


@_attrs_define
class CheckUniqueBackendIDResponse:
    """
    Attributes:
        is_unique (bool): Whether the backend ID is unique
        is_valid_format (Union[None, Unset, bool]): Whether the backend ID matches the offering's format regex (null if
            no rules configured)
        errors (Union[Unset, list[str]]): List of validation error messages
    """

    is_unique: bool
    is_valid_format: Union[None, Unset, bool] = UNSET
    errors: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_unique = self.is_unique

        is_valid_format: Union[None, Unset, bool]
        if isinstance(self.is_valid_format, Unset):
            is_valid_format = UNSET
        else:
            is_valid_format = self.is_valid_format

        errors: Union[Unset, list[str]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_unique": is_unique,
            }
        )
        if is_valid_format is not UNSET:
            field_dict["is_valid_format"] = is_valid_format
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_unique = d.pop("is_unique")

        def _parse_is_valid_format(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_valid_format = _parse_is_valid_format(d.pop("is_valid_format", UNSET))

        errors = cast(list[str], d.pop("errors", UNSET))

        check_unique_backend_id_response = cls(
            is_unique=is_unique,
            is_valid_format=is_valid_format,
            errors=errors,
        )

        check_unique_backend_id_response.additional_properties = d
        return check_unique_backend_id_response

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
