from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateCustomerSecretDto")



@_attrs_define
class UpdateCustomerSecretDto:
    """ Request body for updating a customer secret. Supports metadata edits and optional credential rotation.

        Example:
            {'upstreamHost': 'api.anthropic.com', 'headerName': 'x-api-key'}

        Attributes:
            upstream_host (str | Unset): New upstream hostname; omit to leave unchanged.
            header_name (str | Unset): New HTTP header the egress proxy injects the credential into; omit to leave
                unchanged.
            value (str | Unset): Optional credential rotation; when provided, replaces the stored secret with this value and
                bumps the version.
     """

    upstream_host: str | Unset = UNSET
    header_name: str | Unset = UNSET
    value: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        upstream_host = self.upstream_host

        header_name = self.header_name

        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if upstream_host is not UNSET:
            field_dict["upstreamHost"] = upstream_host
        if header_name is not UNSET:
            field_dict["headerName"] = header_name
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        upstream_host = d.pop("upstreamHost", UNSET)

        header_name = d.pop("headerName", UNSET)

        value = d.pop("value", UNSET)

        update_customer_secret_dto = cls(
            upstream_host=upstream_host,
            header_name=header_name,
            value=value,
        )


        update_customer_secret_dto.additional_properties = d
        return update_customer_secret_dto

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
