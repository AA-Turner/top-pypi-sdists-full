from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TTimeoutSpec")


@_attrs_define
class TTimeoutSpec:
    """
    Attributes:
        grace_period (Union[Unset, float, int]):
        timeout (Union[Unset, float, int]):
    """

    grace_period: Union[Unset, float, int] = UNSET
    timeout: Union[Unset, float, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grace_period: Union[Unset, float, int]
        if isinstance(self.grace_period, Unset):
            grace_period = UNSET
        else:
            grace_period = self.grace_period

        timeout: Union[Unset, float, int]
        if isinstance(self.timeout, Unset):
            timeout = UNSET
        else:
            timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if grace_period is not UNSET:
            field_dict["grace_period"] = grace_period
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_grace_period(data: object) -> Union[Unset, float, int]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, float, int], data)

        grace_period = _parse_grace_period(d.pop("grace_period", UNSET))

        def _parse_timeout(data: object) -> Union[Unset, float, int]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, float, int], data)

        timeout = _parse_timeout(d.pop("timeout", UNSET))

        t_timeout_spec = cls(
            grace_period=grace_period,
            timeout=timeout,
        )

        t_timeout_spec.additional_properties = d
        return t_timeout_spec

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
