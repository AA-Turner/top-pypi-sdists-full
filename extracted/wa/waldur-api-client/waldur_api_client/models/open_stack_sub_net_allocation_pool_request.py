from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OpenStackSubNetAllocationPoolRequest")


@_attrs_define
class OpenStackSubNetAllocationPoolRequest:
    """
    Attributes:
        start (str): An IPv4 or IPv6 address.
        end (str): An IPv4 or IPv6 address.
    """

    start: str
    end: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start: str
        start = self.start

        end: str
        end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start": start,
                "end": end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_start(data: object) -> str:
            return cast(str, data)

        start = _parse_start(d.pop("start"))

        def _parse_end(data: object) -> str:
            return cast(str, data)

        end = _parse_end(d.pop("end"))

        open_stack_sub_net_allocation_pool_request = cls(
            start=start,
            end=end,
        )

        open_stack_sub_net_allocation_pool_request.additional_properties = d
        return open_stack_sub_net_allocation_pool_request

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
