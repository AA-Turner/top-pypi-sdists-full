from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CreateProblemSecretDto")



@_attrs_define
class CreateProblemSecretDto:
    """ Request body for creating a new secret binding.

        Attributes:
            name (str): Environment-variable name the secret will be exposed under.
            upstream_host (str): Upstream host the credential is allowed to be sent to.
            header_name (str): HTTP header the secret value is written into.
            value (str): Ready-to-send header value, including any auth scheme prefix. Leading and trailing whitespace is
                trimmed; the result is written verbatim into the outbound request header.
     """

    name: str
    upstream_host: str
    header_name: str
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        upstream_host = self.upstream_host

        header_name = self.header_name

        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "upstreamHost": upstream_host,
            "headerName": header_name,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        upstream_host = d.pop("upstreamHost")

        header_name = d.pop("headerName")

        value = d.pop("value")

        create_problem_secret_dto = cls(
            name=name,
            upstream_host=upstream_host,
            header_name=header_name,
            value=value,
        )


        create_problem_secret_dto.additional_properties = d
        return create_problem_secret_dto

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
