from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rollback_datatable_migrations_response_200_rolled_back_item import (
        RollbackDatatableMigrationsResponse200RolledBackItem,
    )


T = TypeVar("T", bound="RollbackDatatableMigrationsResponse200")


@_attrs_define
class RollbackDatatableMigrationsResponse200:
    """
    Attributes:
        rolled_back (List['RollbackDatatableMigrationsResponse200RolledBackItem']):
    """

    rolled_back: List["RollbackDatatableMigrationsResponse200RolledBackItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rolled_back = []
        for rolled_back_item_data in self.rolled_back:
            rolled_back_item = rolled_back_item_data.to_dict()

            rolled_back.append(rolled_back_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rolled_back": rolled_back,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.rollback_datatable_migrations_response_200_rolled_back_item import (
            RollbackDatatableMigrationsResponse200RolledBackItem,
        )

        d = src_dict.copy()
        rolled_back = []
        _rolled_back = d.pop("rolled_back")
        for rolled_back_item_data in _rolled_back:
            rolled_back_item = RollbackDatatableMigrationsResponse200RolledBackItem.from_dict(rolled_back_item_data)

            rolled_back.append(rolled_back_item)

        rollback_datatable_migrations_response_200 = cls(
            rolled_back=rolled_back,
        )

        rollback_datatable_migrations_response_200.additional_properties = d
        return rollback_datatable_migrations_response_200

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
