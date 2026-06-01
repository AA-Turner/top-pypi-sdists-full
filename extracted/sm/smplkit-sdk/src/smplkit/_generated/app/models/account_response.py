from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.account_resource import AccountResource


T = TypeVar("T", bound="AccountResponse")


@_attrs_define
class AccountResponse:
    """JSON:API single-resource response envelope for an account.

    Attributes:
        data (AccountResource): JSON:API resource envelope for an account.

            `id` must not be specified for create requests (the server assigns it). Example: {'attributes': {'created_at':
            '2026-03-20T11:02:16.616Z', 'has_stripe_customer': False, 'key': 'acme_corp', 'name': 'Acme Corp'}, 'id':
            'd290f1ee-6c54-4b01-90e6-d701748f0851', 'type': 'account'}.
    """

    data: AccountResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_resource import AccountResource

        d = dict(src_dict)
        data = AccountResource.from_dict(d.pop("data"))

        account_response = cls(
            data=data,
        )

        account_response.additional_properties = d
        return account_response

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
