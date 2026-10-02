from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_file import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File
  from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_text import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text





T = TypeVar("T", bound="TriggerQaJobBodyDto")



@_attrs_define
class TriggerQaJobBodyDto:
    """ Payload for triggering a single QA job against one problem (optionally pinned to a specific version).

        Example:
            {'qaConfigId': 'd6bcc57c-7b71-4369-98da-ab69d9571bb9', 'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb',
                'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'timeoutSeconds': 600}

        Attributes:
            qa_config_id (UUID): Stable QA-config identifier (UUID).
            problem_id (UUID): Stable problem identifier (UUID).
            problem_version_id (UUID | Unset): Stable problem-version identifier (UUID). Each problem can have many
                versions; this points at one specific version.
            gold_reference_transcript (None | TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File |
                TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text | Unset): Optional gold reference transcript for
                gt-grading-oracle QA jobs; when omitted the backend synthesizes one from the gold outputs + problem prompt.
                Ignored by non-oracle QA jobs.
            timeout_seconds (int | Unset): Per-job timeout override in seconds. Example: 600.
            cpu_milli (int | Unset): Per-job CPU allocation override in milli-CPUs. Example: 1000.
            memory_mib (int | Unset): Per-job memory allocation override in MiB. Example: 2048.
            max_retries (int | Unset): Per-job retry budget override. Applies to single-container QA kinds (standard,
                grading-oracle, metrics-validator), where a failed or unusable attempt is re-dispatched until the budget is
                spent. Ignored by the composite kinds (gtGradingOracle, standard-composite), which always run a single attempt.
                Example: 1.
            callback_url (str | Unset): Optional HTTPS webhook URL invoked when the QA job finishes.
            callback_token (str | Unset): Bearer token sent in the bearer authorization header of the callback request.
     """

    qa_config_id: UUID
    problem_id: UUID
    problem_version_id: UUID | Unset = UNSET
    gold_reference_transcript: None | TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File | TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    cpu_milli: int | Unset = UNSET
    memory_mib: int | Unset = UNSET
    max_retries: int | Unset = UNSET
    callback_url: str | Unset = UNSET
    callback_token: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_file import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File # noqa: PLC0415
        from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_text import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text # noqa: PLC0415
        qa_config_id = str(self.qa_config_id)

        problem_id = str(self.problem_id)

        problem_version_id: str | Unset = UNSET
        if not isinstance(self.problem_version_id, Unset):
            problem_version_id = str(self.problem_version_id)

        gold_reference_transcript: dict[str, Any] | None | Unset
        if isinstance(self.gold_reference_transcript, Unset):
            gold_reference_transcript = UNSET
        elif isinstance(self.gold_reference_transcript, TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text):
            gold_reference_transcript = self.gold_reference_transcript.to_dict()
        elif isinstance(self.gold_reference_transcript, TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File):
            gold_reference_transcript = self.gold_reference_transcript.to_dict()
        else:
            gold_reference_transcript = self.gold_reference_transcript

        timeout_seconds = self.timeout_seconds

        cpu_milli = self.cpu_milli

        memory_mib = self.memory_mib

        max_retries = self.max_retries

        callback_url = self.callback_url

        callback_token = self.callback_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "qaConfigId": qa_config_id,
            "problemId": problem_id,
        })
        if problem_version_id is not UNSET:
            field_dict["problemVersionId"] = problem_version_id
        if gold_reference_transcript is not UNSET:
            field_dict["goldReferenceTranscript"] = gold_reference_transcript
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
        from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_file import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File # noqa: PLC0415
        from ..models.trigger_qa_job_body_dto_properties_gold_reference_transcript_any_of_0_text import TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text # noqa: PLC0415
        d = dict(src_dict)
        qa_config_id = UUID(d.pop("qaConfigId"))




        problem_id = UUID(d.pop("problemId"))




        _problem_version_id = d.pop("problemVersionId", UNSET)
        problem_version_id: UUID | Unset
        if isinstance(_problem_version_id,  Unset):
            problem_version_id = UNSET
        else:
            problem_version_id = UUID(_problem_version_id)




        def _parse_gold_reference_transcript(data: object) -> None | TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File | TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gold_reference_transcript_type_0_type_0 = TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text.from_dict(data)



                return gold_reference_transcript_type_0_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gold_reference_transcript_type_0_type_1 = TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File.from_dict(data)



                return gold_reference_transcript_type_0_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0File | TriggerQaJobBodyDtoPropertiesGoldReferenceTranscriptAnyOf0Text | Unset, data)

        gold_reference_transcript = _parse_gold_reference_transcript(d.pop("goldReferenceTranscript", UNSET))


        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        cpu_milli = d.pop("cpuMilli", UNSET)

        memory_mib = d.pop("memoryMib", UNSET)

        max_retries = d.pop("maxRetries", UNSET)

        callback_url = d.pop("callbackUrl", UNSET)

        callback_token = d.pop("callbackToken", UNSET)

        trigger_qa_job_body_dto = cls(
            qa_config_id=qa_config_id,
            problem_id=problem_id,
            problem_version_id=problem_version_id,
            gold_reference_transcript=gold_reference_transcript,
            timeout_seconds=timeout_seconds,
            cpu_milli=cpu_milli,
            memory_mib=memory_mib,
            max_retries=max_retries,
            callback_url=callback_url,
            callback_token=callback_token,
        )

        return trigger_qa_job_body_dto

