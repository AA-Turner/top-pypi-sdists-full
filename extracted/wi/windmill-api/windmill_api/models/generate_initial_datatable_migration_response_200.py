from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateInitialDatatableMigrationResponse200")


@_attrs_define
class GenerateInitialDatatableMigrationResponse200:
    """
    Attributes:
        datatable (str):
        timestamp (int):
        name (str):
        code_up (str):
        code_down (Union[Unset, str]):
    """

    datatable: str
    timestamp: int
    name: str
    code_up: str
    code_down: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datatable = self.datatable
        timestamp = self.timestamp
        name = self.name
        code_up = self.code_up
        code_down = self.code_down

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datatable": datatable,
                "timestamp": timestamp,
                "name": name,
                "code_up": code_up,
            }
        )
        if code_down is not UNSET:
            field_dict["code_down"] = code_down

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datatable = d.pop("datatable")

        timestamp = d.pop("timestamp")

        name = d.pop("name")

        code_up = d.pop("code_up")

        code_down = d.pop("code_down", UNSET)

        generate_initial_datatable_migration_response_200 = cls(
            datatable=datatable,
            timestamp=timestamp,
            name=name,
            code_up=code_up,
            code_down=code_down,
        )

        generate_initial_datatable_migration_response_200.additional_properties = d
        return generate_initial_datatable_migration_response_200

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
