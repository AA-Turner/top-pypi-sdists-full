from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PlanDatatableAclResponse200")


@_attrs_define
class PlanDatatableAclResponse200:
    """
    Attributes:
        statements (List[str]):
        warnings (List[str]):
    """

    statements: List[str]
    warnings: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        statements = self.statements

        warnings = self.warnings

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "statements": statements,
                "warnings": warnings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        statements = cast(List[str], d.pop("statements"))

        warnings = cast(List[str], d.pop("warnings"))

        plan_datatable_acl_response_200 = cls(
            statements=statements,
            warnings=warnings,
        )

        plan_datatable_acl_response_200.additional_properties = d
        return plan_datatable_acl_response_200

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
