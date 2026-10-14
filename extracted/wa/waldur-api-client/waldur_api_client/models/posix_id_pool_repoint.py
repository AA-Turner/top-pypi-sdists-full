from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.posix_id_pool_left_behind_consumer import PosixIdPoolLeftBehindConsumer
    from ..models.posix_id_pool_repoint_change import PosixIdPoolRepointChange


T = TypeVar("T", bound="PosixIdPoolRepoint")


@_attrs_define
class PosixIdPoolRepoint:
    """
    Attributes:
        changes (list['PosixIdPoolRepointChange']):
        released (int): Identities freed in the previously resolved pool. Their values are withheld from recycling until
            an operator returns them.
        retained (int): Users whose previous identity stays active because this pool does not manage every namespace
            they hold a value in.
        other_consumers (list['PosixIdPoolLeftBehindConsumer']): Robot accounts and groups of the offering that keep
            their values from the previously resolved pool; re-pointing moves offering accounts only.
    """

    changes: list["PosixIdPoolRepointChange"]
    released: int
    retained: int
    other_consumers: list["PosixIdPoolLeftBehindConsumer"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        changes = []
        for changes_item_data in self.changes:
            changes_item = changes_item_data.to_dict()
            changes.append(changes_item)

        released = self.released

        retained = self.retained

        other_consumers = []
        for other_consumers_item_data in self.other_consumers:
            other_consumers_item = other_consumers_item_data.to_dict()
            other_consumers.append(other_consumers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "changes": changes,
                "released": released,
                "retained": retained,
                "other_consumers": other_consumers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.posix_id_pool_left_behind_consumer import PosixIdPoolLeftBehindConsumer
        from ..models.posix_id_pool_repoint_change import PosixIdPoolRepointChange

        d = dict(src_dict)
        changes = []
        _changes = d.pop("changes")
        for changes_item_data in _changes:
            changes_item = PosixIdPoolRepointChange.from_dict(changes_item_data)

            changes.append(changes_item)

        released = d.pop("released")

        retained = d.pop("retained")

        other_consumers = []
        _other_consumers = d.pop("other_consumers")
        for other_consumers_item_data in _other_consumers:
            other_consumers_item = PosixIdPoolLeftBehindConsumer.from_dict(other_consumers_item_data)

            other_consumers.append(other_consumers_item)

        posix_id_pool_repoint = cls(
            changes=changes,
            released=released,
            retained=retained,
            other_consumers=other_consumers,
        )

        posix_id_pool_repoint.additional_properties = d
        return posix_id_pool_repoint

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
