from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingBackendIdRulesUpdateRequest")


@_attrs_define
class OfferingBackendIdRulesUpdateRequest:
    """
    Attributes:
        backend_id_rules (Union[Unset, Any]): Validation rules for resource backend_id: format regex and uniqueness
            scope.
    """

    backend_id_rules: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backend_id_rules = self.backend_id_rules

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if backend_id_rules is not UNSET:
            field_dict["backend_id_rules"] = backend_id_rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backend_id_rules = d.pop("backend_id_rules", UNSET)

        offering_backend_id_rules_update_request = cls(
            backend_id_rules=backend_id_rules,
        )

        offering_backend_id_rules_update_request.additional_properties = d
        return offering_backend_id_rules_update_request

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
