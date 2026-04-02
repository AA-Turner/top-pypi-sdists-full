from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LockStats")


@_attrs_define
class LockStats:
    """
    Attributes:
        total_locks (int): Total number of locks currently held
        waiting_locks (int): Number of locks being waited for
        access_exclusive_locks (int): Number of AccessExclusive locks (blocks all access)
    """

    total_locks: int
    waiting_locks: int
    access_exclusive_locks: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_locks = self.total_locks

        waiting_locks = self.waiting_locks

        access_exclusive_locks = self.access_exclusive_locks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_locks": total_locks,
                "waiting_locks": waiting_locks,
                "access_exclusive_locks": access_exclusive_locks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_locks = d.pop("total_locks")

        waiting_locks = d.pop("waiting_locks")

        access_exclusive_locks = d.pop("access_exclusive_locks")

        lock_stats = cls(
            total_locks=total_locks,
            waiting_locks=waiting_locks,
            access_exclusive_locks=access_exclusive_locks,
        )

        lock_stats.additional_properties = d
        return lock_stats

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
