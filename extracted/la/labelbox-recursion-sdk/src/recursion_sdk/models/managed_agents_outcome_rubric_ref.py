from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_outcome_rubric_ref_type import ManagedAgentsOutcomeRubricRefType
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsOutcomeRubricRef")



@_attrs_define
class ManagedAgentsOutcomeRubricRef:
    """ A file whose text is an outcome's rubric.

        Example:
            {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}

        Attributes:
            file_id (UUID): A file in the caller's organization holding the rubric: text or YAML, at most 256 KiB, uploaded
                through POST /v1/files. Its text is echoed back as the outcome's rubric. An unknown, expired, or out-of-scope
                file answers 404; a file that is not text, is oversized, is not UTF-8, or holds no criterion answers 400.
            type_ (ManagedAgentsOutcomeRubricRefType): Always file.
     """

    file_id: UUID
    type_: ManagedAgentsOutcomeRubricRefType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        type_ = self.type_.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_id": file_id,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = UUID(d.pop("file_id"))




        type_ = ManagedAgentsOutcomeRubricRefType(d.pop("type"))




        managed_agents_outcome_rubric_ref = cls(
            file_id=file_id,
            type_=type_,
        )


        managed_agents_outcome_rubric_ref.additional_properties = d
        return managed_agents_outcome_rubric_ref

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
