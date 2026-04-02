from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceProviderSignatureRequest")


@_attrs_define
class ServiceProviderSignatureRequest:
    """
    Attributes:
        customer (UUID): Service provider customer UUID
        data (str): JWT-encoded data signed with the service provider's API secret code
        dry_run (Union[Unset, bool]): If true, validates the signature without executing the operation Default: False.
    """

    customer: UUID
    data: str
    dry_run: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer = str(self.customer)

        data = self.data

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer": customer,
                "data": data,
            }
        )
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        customer = UUID(d.pop("customer"))

        data = d.pop("data")

        dry_run = d.pop("dry_run", UNSET)

        service_provider_signature_request = cls(
            customer=customer,
            data=data,
            dry_run=dry_run,
        )

        service_provider_signature_request.additional_properties = d
        return service_provider_signature_request

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
