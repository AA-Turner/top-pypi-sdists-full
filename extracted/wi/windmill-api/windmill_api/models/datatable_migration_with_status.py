from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.datatable_migration_with_status_status import DatatableMigrationWithStatusStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatatableMigrationWithStatus")


@_attrs_define
class DatatableMigrationWithStatus:
    """
    Attributes:
        timestamp (int):
        name (str):
        code_up (str):
        status (DatatableMigrationWithStatusStatus):
        code_down (Union[Unset, str]):
    """

    timestamp: int
    name: str
    code_up: str
    status: DatatableMigrationWithStatusStatus
    code_down: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp = self.timestamp
        name = self.name
        code_up = self.code_up
        status = self.status.value

        code_down = self.code_down

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "name": name,
                "code_up": code_up,
                "status": status,
            }
        )
        if code_down is not UNSET:
            field_dict["code_down"] = code_down

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        timestamp = d.pop("timestamp")

        name = d.pop("name")

        code_up = d.pop("code_up")

        status = DatatableMigrationWithStatusStatus(d.pop("status"))

        code_down = d.pop("code_down", UNSET)

        datatable_migration_with_status = cls(
            timestamp=timestamp,
            name=name,
            code_up=code_up,
            status=status,
            code_down=code_down,
        )

        datatable_migration_with_status.additional_properties = d
        return datatable_migration_with_status

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
