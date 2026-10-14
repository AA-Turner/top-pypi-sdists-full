from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.matrix_crypto_conflict_state_enum import MatrixCryptoConflictStateEnum

T = TypeVar("T", bound="MatrixCryptoConflict")


@_attrs_define
class MatrixCryptoConflict:
    """
    Attributes:
        state (MatrixCryptoConflictStateEnum):
        detail (str):
    """

    state: MatrixCryptoConflictStateEnum
    detail: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = MatrixCryptoConflictStateEnum(d.pop("state"))

        detail = d.pop("detail")

        matrix_crypto_conflict = cls(
            state=state,
            detail=detail,
        )

        matrix_crypto_conflict.additional_properties = d
        return matrix_crypto_conflict

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
