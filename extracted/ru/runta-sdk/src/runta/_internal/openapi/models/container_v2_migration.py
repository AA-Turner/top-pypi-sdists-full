from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerV2Migration")


@_attrs_define
class ContainerV2Migration:
    """
    Attributes:
        migration_id (str):
        phase (str):
        outcome_unknown (bool):
        reason (str | Unset):
    """

    migration_id: str
    phase: str
    outcome_unknown: bool
    reason: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        migration_id = self.migration_id

        phase = self.phase

        outcome_unknown = self.outcome_unknown

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "migration_id": migration_id,
                "phase": phase,
                "outcome_unknown": outcome_unknown,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        migration_id = d.pop("migration_id")

        phase = d.pop("phase")

        outcome_unknown = d.pop("outcome_unknown")

        reason = d.pop("reason", UNSET)

        container_v2_migration = cls(
            migration_id=migration_id,
            phase=phase,
            outcome_unknown=outcome_unknown,
            reason=reason,
        )

        container_v2_migration.additional_properties = d
        return container_v2_migration

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
