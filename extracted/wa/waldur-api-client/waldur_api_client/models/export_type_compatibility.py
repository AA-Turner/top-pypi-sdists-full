from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExportTypeCompatibility")


@_attrs_define
class ExportTypeCompatibility:
    """
    Attributes:
        reference (str):
        name (str):
        required_fields_total (int):
        required_fields_found (int):
        important_fields_total (int):
        important_fields_found (int):
        missing_required_fields (list[str]):
        missing_important_fields (list[str]):
        compatible (bool):
        recommended (bool):
    """

    reference: str
    name: str
    required_fields_total: int
    required_fields_found: int
    important_fields_total: int
    important_fields_found: int
    missing_required_fields: list[str]
    missing_important_fields: list[str]
    compatible: bool
    recommended: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reference = self.reference

        name = self.name

        required_fields_total = self.required_fields_total

        required_fields_found = self.required_fields_found

        important_fields_total = self.important_fields_total

        important_fields_found = self.important_fields_found

        missing_required_fields = self.missing_required_fields

        missing_important_fields = self.missing_important_fields

        compatible = self.compatible

        recommended = self.recommended

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reference": reference,
                "name": name,
                "required_fields_total": required_fields_total,
                "required_fields_found": required_fields_found,
                "important_fields_total": important_fields_total,
                "important_fields_found": important_fields_found,
                "missing_required_fields": missing_required_fields,
                "missing_important_fields": missing_important_fields,
                "compatible": compatible,
                "recommended": recommended,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reference = d.pop("reference")

        name = d.pop("name")

        required_fields_total = d.pop("required_fields_total")

        required_fields_found = d.pop("required_fields_found")

        important_fields_total = d.pop("important_fields_total")

        important_fields_found = d.pop("important_fields_found")

        missing_required_fields = cast(list[str], d.pop("missing_required_fields"))

        missing_important_fields = cast(list[str], d.pop("missing_important_fields"))

        compatible = d.pop("compatible")

        recommended = d.pop("recommended")

        export_type_compatibility = cls(
            reference=reference,
            name=name,
            required_fields_total=required_fields_total,
            required_fields_found=required_fields_found,
            important_fields_total=important_fields_total,
            important_fields_found=important_fields_found,
            missing_required_fields=missing_required_fields,
            missing_important_fields=missing_important_fields,
            compatible=compatible,
            recommended=recommended,
        )

        export_type_compatibility.additional_properties = d
        return export_type_compatibility

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
