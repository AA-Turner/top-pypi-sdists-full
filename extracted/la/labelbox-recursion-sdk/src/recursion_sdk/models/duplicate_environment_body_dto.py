from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="DuplicateEnvironmentBodyDto")



@_attrs_define
class DuplicateEnvironmentBodyDto:
    """ Target identifier and display name for a new environment duplicated from an existing one within the same
    organization.

        Attributes:
            target_external_id (str): External identifier for the duplicated environment, supplied by the caller (e.g. the
                cloned upstream project id).
            target_name (str): Human-readable display name for the duplicated environment.
     """

    target_external_id: str
    target_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        target_external_id = self.target_external_id

        target_name = self.target_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "targetExternalId": target_external_id,
            "targetName": target_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_external_id = d.pop("targetExternalId")

        target_name = d.pop("targetName")

        duplicate_environment_body_dto = cls(
            target_external_id=target_external_id,
            target_name=target_name,
        )


        duplicate_environment_body_dto.additional_properties = d
        return duplicate_environment_body_dto

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
