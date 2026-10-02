from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedScienceSubDomainRequest")


@_attrs_define
class PatchedScienceSubDomainRequest:
    """
    Attributes:
        code (Union[Unset, str]): Sub-domain code (e.g. '1.1'). Auto-derived from domain code if left blank.
        name (Union[Unset, str]):
        domain (Union[Unset, str]):
    """

    code: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    domain: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        name = self.name

        domain = self.domain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if name is not UNSET:
            field_dict["name"] = name
        if domain is not UNSET:
            field_dict["domain"] = domain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code", UNSET)

        name = d.pop("name", UNSET)

        domain = d.pop("domain", UNSET)

        patched_science_sub_domain_request = cls(
            code=code,
            name=name,
            domain=domain,
        )

        patched_science_sub_domain_request.additional_properties = d
        return patched_science_sub_domain_request

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
