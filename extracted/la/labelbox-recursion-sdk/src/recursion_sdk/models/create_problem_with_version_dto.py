from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CreateProblemWithVersionDto")



@_attrs_define
class CreateProblemWithVersionDto:
    """ Request body for creating a problem together with its initial version in a single call, keyed by external ID.

        Example:
            {'externalId': 'detect-surface-defects'}

        Attributes:
            external_id (str): Caller-supplied external identifier for the new problem; the operation is idempotent on this
                value.
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

        create_problem_with_version_dto = cls(
            external_id=external_id,
        )


        create_problem_with_version_dto.additional_properties = d
        return create_problem_with_version_dto

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
