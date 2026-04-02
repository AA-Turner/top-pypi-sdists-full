from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Fingerprint")


@_attrs_define
class Fingerprint:
    """
    Attributes:
        md5 (Union[Unset, str]): MD5 fingerprint of SSH key
        sha256 (Union[Unset, str]): SHA256 fingerprint of SSH key
        sha512 (Union[Unset, str]): SHA512 fingerprint of SSH key
    """

    md5: Union[Unset, str] = UNSET
    sha256: Union[Unset, str] = UNSET
    sha512: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        md5 = self.md5

        sha256 = self.sha256

        sha512 = self.sha512

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if md5 is not UNSET:
            field_dict["md5"] = md5
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if sha512 is not UNSET:
            field_dict["sha512"] = sha512

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        md5 = d.pop("md5", UNSET)

        sha256 = d.pop("sha256", UNSET)

        sha512 = d.pop("sha512", UNSET)

        fingerprint = cls(
            md5=md5,
            sha256=sha256,
            sha512=sha512,
        )

        fingerprint.additional_properties = d
        return fingerprint

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
