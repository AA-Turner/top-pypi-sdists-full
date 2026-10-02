from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AttachEnvironmentExternalIdDto")



@_attrs_define
class AttachEnvironmentExternalIdDto:
    """ Request body for attaching an external ID to an environment that doesn't already have one. Fails with 409 if the
    environment already has any external ID set (detach it first), or if the supplied external ID is in use by another
    active environment.

        Example:
            {'externalId': 'vision-agent-eval'}

        Attributes:
            external_id (str): External identifier to bind to the environment. Must not already be in use by another
                environment.
     """

    external_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        external_id = self.external_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "externalId": external_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        external_id = d.pop("externalId")

        attach_environment_external_id_dto = cls(
            external_id=external_id,
        )


        attach_environment_external_id_dto.additional_properties = d
        return attach_environment_external_id_dto

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
