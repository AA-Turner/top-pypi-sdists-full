from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixRecoveryKey")


@_attrs_define
class MatrixRecoveryKey:
    """
    Attributes:
        recovery_key (Union[None, str]): The user's secret-storage recovery key, for unlocking chat history in another
            Matrix client. Null while Waldur holds no key that opens the user's secret storage.
    """

    recovery_key: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recovery_key: Union[None, str]
        recovery_key = self.recovery_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recovery_key": recovery_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_recovery_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        recovery_key = _parse_recovery_key(d.pop("recovery_key"))

        matrix_recovery_key = cls(
            recovery_key=recovery_key,
        )

        matrix_recovery_key.additional_properties = d
        return matrix_recovery_key

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
