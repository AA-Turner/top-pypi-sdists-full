from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_run_response_list_envelope_dto_items_item import ProblemRunResponseListEnvelopeDtoItemsItem





T = TypeVar("T", bound="ProblemRunResponseListEnvelopeDto")



@_attrs_define
class ProblemRunResponseListEnvelopeDto:
    """ Problem-run list response. Truncated flag signals an over-cap drawer view.

        Example:
            {'items': [{'id': '8e6d1c7f-3b4a-4d12-9a5e-2c0b1a3d4e5f', 'jobId': None, 'runName': 'claude-sonnet-baseline on
                detect-surface-defects', 'batchId': '6b9f0e51-8a2d-4c73-b0f4-7e1d5a9c3b28', 'jobV2Id':
                '5c4b3a29-1d8e-4f60-9a7b-3c2d1e0f9a8b', 'topJobId': '7f6e5d4c-3b2a-4190-8d6e-9c0b1a2d3e4f', 'topJobType':
                'problem_run_batch', 'topJobEnvironmentId': 'e3f1b6c2-5a7d-4c98-b1e0-9d8c7b6a5f43', 'problemId':
                '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'status':
                'completed', 'attemptNumber': 2, 'queuePosition': None, 'prompt': None, 'executionTimeMs': 51000, 'finalScore':
                0.83, 'errorMessage': None, 'apiModelName': 'claude-sonnet-4-6', 'gradingModelName': 'claude-opus-4-6',
                'turnsCount': 12, 'createdAt': '2026-01-15T09:31:00.000Z', 'startedAt': '2026-01-15T09:31:12.000Z',
                'completedAt': '2026-01-15T09:32:03.000Z', 'transcript': None, 'source': 'job', 'provenance': 'v2',
                'hasRetainedSolverRun': True, 'gradedAt': '2026-01-15T09:32:18.000Z', 'gradingError': None,
                'gradingJustification': 'All four visible scratches were correctly localized; one faint dent was missed, costing
                partial credit.', 'regradeCount': 0, 'gradingConfig': {'type': 'agentic', 'agenticGradingPrompt': 'Score how
                completely the reported defects match the gold-standard annotations, from 0 to 1.'}, 'solverRunConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad', 'solverRunConfigName': 'claude-sonnet-baseline',
                'solverRunConfigVersionNumber': 2, 'graderRunConfigVersionId': '49088cb6-ca62-4544-a074-fc66e10807ae',
                'graderRunConfigName': 'claude-opus-grader', 'graderRunConfigVersionNumber': 3, 'outputFilesTruncated': False,
                'outputFilesListedCount': 2}, {'id': '22d435e7-9e41-4554-b0bd-dab57a202b71', 'jobId':
                '818b2f68-236c-4ba8-9257-e032f4fd5efb', 'runName': 'claude-sonnet-baseline on detect-surface-defects',
                'batchId': '6b9f0e51-8a2d-4c73-b0f4-7e1d5a9c3b28', 'jobV2Id': None, 'topJobId': None, 'topJobType': None,
                'topJobEnvironmentId': None, 'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
                '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'status': 'completed', 'attemptNumber': 1, 'queuePosition': None,
                'prompt': 'Inspect the part image and report every surface defect with its bounding box.', 'executionTimeMs':
                42000, 'finalScore': 0.83, 'errorMessage': None, 'apiModelName': 'claude-sonnet-4-6', 'gradingModelName':
                'claude-opus-4-6', 'turnsCount': 12, 'createdAt': '2026-01-15T09:30:00.000Z', 'startedAt':
                '2026-01-15T09:30:08.000Z', 'completedAt': '2026-01-15T09:30:50.000Z', 'transcript': None, 'source': 'job',
                'provenance': None, 'hasRetainedSolverRun': True, 'gradedAt': '2026-01-15T09:31:05.000Z', 'gradingError': None,
                'gradingJustification': 'All four visible scratches were correctly localized; one faint dent was missed, costing
                partial credit.', 'regradeCount': 0, 'gradingConfig': {'type': 'agentic', 'agenticGradingPrompt': 'Score how
                completely the reported defects match the gold-standard annotations, from 0 to 1.'}, 'solverRunConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad', 'solverRunConfigName': 'claude-sonnet-baseline',
                'solverRunConfigVersionNumber': 2, 'graderRunConfigVersionId': '49088cb6-ca62-4544-a074-fc66e10807ae',
                'graderRunConfigName': 'claude-opus-grader', 'graderRunConfigVersionNumber': 3, 'outputFilesTruncated': False,
                'outputFilesListedCount': 2}], 'truncated': False}

        Attributes:
            items (list[ProblemRunResponseListEnvelopeDtoItemsItem]): Newest-first problem runs for the requested problem.
            truncated (bool): True when the requested problem has more runs than the hard cap returns.
     """

    items: list[ProblemRunResponseListEnvelopeDtoItemsItem]
    truncated: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_run_response_list_envelope_dto_items_item import ProblemRunResponseListEnvelopeDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        truncated = self.truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "truncated": truncated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_run_response_list_envelope_dto_items_item import ProblemRunResponseListEnvelopeDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ProblemRunResponseListEnvelopeDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        truncated = d.pop("truncated")

        problem_run_response_list_envelope_dto = cls(
            items=items,
            truncated=truncated,
        )

        return problem_run_response_list_envelope_dto

