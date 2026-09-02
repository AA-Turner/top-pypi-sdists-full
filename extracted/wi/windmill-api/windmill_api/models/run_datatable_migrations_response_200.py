from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.run_datatable_migrations_response_200_applied_item import RunDatatableMigrationsResponse200AppliedItem


T = TypeVar("T", bound="RunDatatableMigrationsResponse200")


@_attrs_define
class RunDatatableMigrationsResponse200:
    """
    Attributes:
        applied (List['RunDatatableMigrationsResponse200AppliedItem']):
    """

    applied: List["RunDatatableMigrationsResponse200AppliedItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        applied = []
        for applied_item_data in self.applied:
            applied_item = applied_item_data.to_dict()

            applied.append(applied_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "applied": applied,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_datatable_migrations_response_200_applied_item import (
            RunDatatableMigrationsResponse200AppliedItem,
        )

        d = src_dict.copy()
        applied = []
        _applied = d.pop("applied")
        for applied_item_data in _applied:
            applied_item = RunDatatableMigrationsResponse200AppliedItem.from_dict(applied_item_data)

            applied.append(applied_item)

        run_datatable_migrations_response_200 = cls(
            applied=applied,
        )

        run_datatable_migrations_response_200.additional_properties = d
        return run_datatable_migrations_response_200

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
