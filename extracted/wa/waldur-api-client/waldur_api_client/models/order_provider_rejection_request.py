from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderProviderRejectionRequest")


@_attrs_define
class OrderProviderRejectionRequest:
    """
    Attributes:
        provider_rejection_comment (Union[Unset, str]):
    """

    provider_rejection_comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider_rejection_comment = self.provider_rejection_comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider_rejection_comment is not UNSET:
            field_dict["provider_rejection_comment"] = provider_rejection_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_rejection_comment = d.pop("provider_rejection_comment", UNSET)

        order_provider_rejection_request = cls(
            provider_rejection_comment=provider_rejection_comment,
        )

        order_provider_rejection_request.additional_properties = d
        return order_provider_rejection_request

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
