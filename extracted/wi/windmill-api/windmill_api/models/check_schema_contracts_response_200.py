from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.check_schema_contracts_response_200_warnings_item import CheckSchemaContractsResponse200WarningsItem


T = TypeVar("T", bound="CheckSchemaContractsResponse200")


@_attrs_define
class CheckSchemaContractsResponse200:
    """
    Attributes:
        warnings (List['CheckSchemaContractsResponse200WarningsItem']):
    """

    warnings: List["CheckSchemaContractsResponse200WarningsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        warnings = []
        for warnings_item_data in self.warnings:
            warnings_item = warnings_item_data.to_dict()

            warnings.append(warnings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.check_schema_contracts_response_200_warnings_item import (
            CheckSchemaContractsResponse200WarningsItem,
        )

        d = src_dict.copy()
        warnings = []
        _warnings = d.pop("warnings")
        for warnings_item_data in _warnings:
            warnings_item = CheckSchemaContractsResponse200WarningsItem.from_dict(warnings_item_data)

            warnings.append(warnings_item)

        check_schema_contracts_response_200 = cls(
            warnings=warnings,
        )

        check_schema_contracts_response_200.additional_properties = d
        return check_schema_contracts_response_200

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
