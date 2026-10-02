from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixReprovisionResponse")


@_attrs_define
class MatrixReprovisionResponse:
    """
    Attributes:
        rooms_reprovisioned (int):
        users_reset (int):
    """

    rooms_reprovisioned: int
    users_reset: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rooms_reprovisioned = self.rooms_reprovisioned

        users_reset = self.users_reset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rooms_reprovisioned": rooms_reprovisioned,
                "users_reset": users_reset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rooms_reprovisioned = d.pop("rooms_reprovisioned")

        users_reset = d.pop("users_reset")

        matrix_reprovision_response = cls(
            rooms_reprovisioned=rooms_reprovisioned,
            users_reset=users_reset,
        )

        matrix_reprovision_response.additional_properties = d
        return matrix_reprovision_response

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
