from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCustomerServiceAccountRequest")


@_attrs_define
class PatchedCustomerServiceAccountRequest:
    """
    Attributes:
        username (Union[Unset, str]):
        description (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        email (Union[Unset, str]):
        preferred_identifier (Union[Unset, str]):
        customer (Union[None, UUID, Unset]):
    """

    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    preferred_identifier: Union[Unset, str] = UNSET
    customer: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        description = self.description

        error_traceback = self.error_traceback

        email = self.email

        preferred_identifier = self.preferred_identifier

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        elif isinstance(self.customer, UUID):
            customer = str(self.customer)
        else:
            customer = self.customer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if description is not UNSET:
            field_dict["description"] = description
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if email is not UNSET:
            field_dict["email"] = email
        if preferred_identifier is not UNSET:
            field_dict["preferred_identifier"] = preferred_identifier
        if customer is not UNSET:
            field_dict["customer"] = customer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username", UNSET)

        description = d.pop("description", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        email = d.pop("email", UNSET)

        preferred_identifier = d.pop("preferred_identifier", UNSET)

        def _parse_customer(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_type_0 = UUID(data)

                return customer_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        patched_customer_service_account_request = cls(
            username=username,
            description=description,
            error_traceback=error_traceback,
            email=email,
            preferred_identifier=preferred_identifier,
            customer=customer,
        )

        patched_customer_service_account_request.additional_properties = d
        return patched_customer_service_account_request

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
