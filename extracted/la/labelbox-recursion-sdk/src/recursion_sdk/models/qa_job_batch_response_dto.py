from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="QaJobBatchResponseDto")



@_attrs_define
class QaJobBatchResponseDto:
    """ Response returned when triggering a QA-job batch, identifying the batch and its constituent jobs.

        Example:
            {'batchId': 'dea4f9aa-f37e-4c87-a06f-0e918e637973', 'jobIds': ['dff37696-37ff-4504-bb59-22d728409c7b']}

        Attributes:
            batch_id (UUID): Stable QA-batch identifier (UUID). Groups QA jobs that should be evaluated together.
            job_ids (list[UUID]): Identifiers of every QA job created as part of this batch (individual and aggregate).
     """

    batch_id: UUID
    job_ids: list[UUID]





    def to_dict(self) -> dict[str, Any]:
        batch_id = str(self.batch_id)

        job_ids = []
        for job_ids_item_data in self.job_ids:
            job_ids_item = str(job_ids_item_data)
            job_ids.append(job_ids_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "batchId": batch_id,
            "jobIds": job_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        batch_id = UUID(d.pop("batchId"))




        job_ids = []
        _job_ids = d.pop("jobIds")
        for job_ids_item_data in (_job_ids):
            job_ids_item = UUID(job_ids_item_data)



            job_ids.append(job_ids_item)


        qa_job_batch_response_dto = cls(
            batch_id=batch_id,
            job_ids=job_ids,
        )

        return qa_job_batch_response_dto

