from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PosixIdPoolRepointRequestRequest")


@_attrs_define
class PosixIdPoolRepointRequestRequest:
    """
    Attributes:
        confirm (bool): Must be true. Re-pointing rewrites identifiers that the provider's directory and filesystem
            already carry, so it is never applied implicitly - preview it first with repoint_preview.
    """

    confirm: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        confirm = self.confirm

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "confirm": confirm,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        confirm = d.pop("confirm")

        posix_id_pool_repoint_request_request = cls(
            confirm=confirm,
        )

        posix_id_pool_repoint_request_request.additional_properties = d
        return posix_id_pool_repoint_request_request

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
