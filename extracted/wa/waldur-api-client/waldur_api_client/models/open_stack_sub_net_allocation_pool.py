from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackSubNetAllocationPool")


@_attrs_define
class OpenStackSubNetAllocationPool:
    """
    Attributes:
        start (Union[Unset, str]): An IPv4 or IPv6 address.
        end (Union[Unset, str]): An IPv4 or IPv6 address.
    """

    start: Union[Unset, str] = UNSET
    end: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start: Union[Unset, str]
        if isinstance(self.start, Unset):
            start = UNSET
        else:
            start = self.start

        end: Union[Unset, str]
        if isinstance(self.end, Unset):
            end = UNSET
        else:
            end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_start(data: object) -> Union[Unset, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, str], data)

        start = _parse_start(d.pop("start", UNSET))

        def _parse_end(data: object) -> Union[Unset, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, str], data)

        end = _parse_end(d.pop("end", UNSET))

        open_stack_sub_net_allocation_pool = cls(
            start=start,
            end=end,
        )

        open_stack_sub_net_allocation_pool.additional_properties = d
        return open_stack_sub_net_allocation_pool

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
