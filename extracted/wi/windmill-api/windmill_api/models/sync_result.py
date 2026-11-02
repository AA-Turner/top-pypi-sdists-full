from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SyncResult")


@_attrs_define
class SyncResult:
    """
    Attributes:
        already_in_sync (bool):
        added_count (int):
        added_triggers (List[str]):
        total_external (int):
        total_windmill (int):
    """

    already_in_sync: bool
    added_count: int
    added_triggers: List[str]
    total_external: int
    total_windmill: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        already_in_sync = self.already_in_sync
        added_count = self.added_count
        added_triggers = self.added_triggers

        total_external = self.total_external
        total_windmill = self.total_windmill

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "already_in_sync": already_in_sync,
                "added_count": added_count,
                "added_triggers": added_triggers,
                "total_external": total_external,
                "total_windmill": total_windmill,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        already_in_sync = d.pop("already_in_sync")

        added_count = d.pop("added_count")

        added_triggers = cast(List[str], d.pop("added_triggers"))

        total_external = d.pop("total_external")

        total_windmill = d.pop("total_windmill")

        sync_result = cls(
            already_in_sync=already_in_sync,
            added_count=added_count,
            added_triggers=added_triggers,
            total_external=total_external,
            total_windmill=total_windmill,
        )

        sync_result.additional_properties = d
        return sync_result

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
