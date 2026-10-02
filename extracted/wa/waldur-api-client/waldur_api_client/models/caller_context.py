from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CallerContext")


@_attrs_define
class CallerContext:
    """
    Attributes:
        full_name (str):
        email (str):
        organization (str):
    """

    full_name: str
    email: str
    organization: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        email = self.email

        organization = self.organization

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "email": email,
                "organization": organization,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("full_name")

        email = d.pop("email")

        organization = d.pop("organization")

        caller_context = cls(
            full_name=full_name,
            email=email,
            organization=organization,
        )

        caller_context.additional_properties = d
        return caller_context

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
