from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="TriggerQaJobBatchBodyDto")



@_attrs_define
class TriggerQaJobBatchBodyDto:
    """ Payload for triggering a QA-job batch across multiple problems with optional aggregate roll-up.

        Example:
            {'qaConfigId': 'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'problemIds': ['2d3fe029-a7d1-4747-9d09-81b976087bbb'],
                'includeAggregate': True, 'timeoutSeconds': 600}

        Attributes:
            qa_config_id (UUID): Stable QA-config identifier (UUID).
            problem_ids (list[UUID]): Problems to evaluate; each receives an individual QA job in the batch.
            include_aggregate (bool | Unset): When true, an additional aggregate-kind QA job is queued to roll up the batch
                results.
            timeout_seconds (int | Unset): Per-job timeout override in seconds applied to every job. Example: 600.
            cpu_milli (int | Unset): Per-job CPU allocation in milli-CPUs. Example: 1000.
            memory_mib (int | Unset): Per-job memory allocation in MiB. Example: 2048.
            max_retries (int | Unset): Per-job retry budget applied to every job. Applies to single-container QA kinds
                (standard, grading-oracle, metrics-validator), where a failed or unusable attempt is re-dispatched until the
                budget is spent. Ignored by the composite kinds (gtGradingOracle, standard-composite), which always run a single
                attempt. Example: 1.
            callback_url (str | Unset): Optional HTTPS webhook URL invoked when each job in the batch finishes.
            callback_token (str | Unset): Bearer token sent in the bearer authorization header of each callback request.
     """

    qa_config_id: UUID
    problem_ids: list[UUID]
    include_aggregate: bool | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    cpu_milli: int | Unset = UNSET
    memory_mib: int | Unset = UNSET
    max_retries: int | Unset = UNSET
    callback_url: str | Unset = UNSET
    callback_token: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        qa_config_id = str(self.qa_config_id)

        problem_ids = []
        for problem_ids_item_data in self.problem_ids:
            problem_ids_item = str(problem_ids_item_data)
            problem_ids.append(problem_ids_item)



        include_aggregate = self.include_aggregate

        timeout_seconds = self.timeout_seconds

        cpu_milli = self.cpu_milli

        memory_mib = self.memory_mib

        max_retries = self.max_retries

        callback_url = self.callback_url

        callback_token = self.callback_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "qaConfigId": qa_config_id,
            "problemIds": problem_ids,
        })
        if include_aggregate is not UNSET:
            field_dict["includeAggregate"] = include_aggregate
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if cpu_milli is not UNSET:
            field_dict["cpuMilli"] = cpu_milli
        if memory_mib is not UNSET:
            field_dict["memoryMib"] = memory_mib
        if max_retries is not UNSET:
            field_dict["maxRetries"] = max_retries
        if callback_url is not UNSET:
            field_dict["callbackUrl"] = callback_url
        if callback_token is not UNSET:
            field_dict["callbackToken"] = callback_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        qa_config_id = UUID(d.pop("qaConfigId"))




        problem_ids = []
        _problem_ids = d.pop("problemIds")
        for problem_ids_item_data in (_problem_ids):
            problem_ids_item = UUID(problem_ids_item_data)



            problem_ids.append(problem_ids_item)


        include_aggregate = d.pop("includeAggregate", UNSET)

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        cpu_milli = d.pop("cpuMilli", UNSET)

        memory_mib = d.pop("memoryMib", UNSET)

        max_retries = d.pop("maxRetries", UNSET)

        callback_url = d.pop("callbackUrl", UNSET)

        callback_token = d.pop("callbackToken", UNSET)

        trigger_qa_job_batch_body_dto = cls(
            qa_config_id=qa_config_id,
            problem_ids=problem_ids,
            include_aggregate=include_aggregate,
            timeout_seconds=timeout_seconds,
            cpu_milli=cpu_milli,
            memory_mib=memory_mib,
            max_retries=max_retries,
            callback_url=callback_url,
            callback_token=callback_token,
        )

        return trigger_qa_job_batch_body_dto

