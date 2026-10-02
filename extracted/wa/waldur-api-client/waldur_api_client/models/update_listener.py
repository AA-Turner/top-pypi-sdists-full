from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateListener")


@_attrs_define
class UpdateListener:
    """
    Attributes:
        name (Union[Unset, str]):
        default_pool (Union[None, Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    default_pool: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        default_pool: Union[None, Unset, str]
        if isinstance(self.default_pool, Unset):
            default_pool = UNSET
        else:
            default_pool = self.default_pool

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if default_pool is not UNSET:
            field_dict["default_pool"] = default_pool

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        def _parse_default_pool(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_pool = _parse_default_pool(d.pop("default_pool", UNSET))

        update_listener = cls(
            name=name,
            default_pool=default_pool,
        )

        update_listener.additional_properties = d
        return update_listener

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
