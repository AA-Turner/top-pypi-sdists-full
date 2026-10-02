from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_rollout_batch_dto_properties_dataset_file_ref_kind import CreateRolloutBatchDtoPropertiesDatasetFileRefKind
from uuid import UUID






T = TypeVar("T", bound="CreateRolloutBatchDtoPropertiesDatasetFileRef")



@_attrs_define
class CreateRolloutBatchDtoPropertiesDatasetFileRef:
    """ 
        Attributes:
            kind (CreateRolloutBatchDtoPropertiesDatasetFileRefKind): Dataset items sourced from an uploaded file.
            file_id (UUID): Uploaded file whose content is a JSON array of item records.
     """

    kind: CreateRolloutBatchDtoPropertiesDatasetFileRefKind
    file_id: UUID





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        file_id = str(self.file_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "fileId": file_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = CreateRolloutBatchDtoPropertiesDatasetFileRefKind(d.pop("kind"))




        file_id = UUID(d.pop("fileId"))




        create_rollout_batch_dto_properties_dataset_file_ref = cls(
            kind=kind,
            file_id=file_id,
        )

        return create_rollout_batch_dto_properties_dataset_file_ref

