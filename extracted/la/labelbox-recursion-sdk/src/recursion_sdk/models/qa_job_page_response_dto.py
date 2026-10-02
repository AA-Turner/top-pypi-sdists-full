from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.qa_job_page_response_dto_items_item import QaJobPageResponseDtoItemsItem





T = TypeVar("T", bound="QaJobPageResponseDto")



@_attrs_define
class QaJobPageResponseDto:
    """ Cursor-paginated page of QA jobs.

        Example:
            {'items': [{'id': 'dff37696-37ff-4504-bb59-22d728409c7b', 'qaConfigId': 'd6bcc57c-7b71-4369-98da-ab69d9571bb9',
                'qaConfigName': 'semantic-critic-review', 'batchId': None, 'environmentId':
                '784e2386-e297-4f9d-a886-838422383b65', 'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
                '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'kind': 'individual', 'status': 'completed', 'containerImage': 'us-
                docker.pkg.dev/example-project/recursion-qa/semantic-critic:1.2.0', 'externalRunId': 'modal-run-7f3a2c7b1d4e',
                'errorMessage': None, 'executionTimeMs': 12500, 'totalCostUsd': '0.12', 'attemptCount': 1, 'maxRetries': 1,
                'startedAt': '2026-01-16T14:20:05.000Z', 'completedAt': '2026-01-16T14:20:17.000Z', 'createdAt':
                '2026-01-16T14:20:00.000Z', 'updatedAt': '2026-01-16T14:20:17.000Z', 'score': 0.92, 'grade': 'pass',
                'problemTitle': 'Detect surface defects on machined parts', 'result': {'summary': 'Instruction is clear and the
                rubric covers all stated requirements.', 'issues': [{'type': 'rubric_gap', 'severity': 'info', 'description':
                'Edge-case handling for empty inputs could add a dedicated criterion.'}], 'details': {'instructionQuality':
                {'score': 0.95}, 'rubricCoverage': {'score': 0.9}}, 'artifacts': [{'filename': 'critic-report.json', 'url':
                'https://storage.example.com/qa/dff37696/critic-report.json'}]}, 'qaRunConfigVersionId':
                '39088cb6-ca62-4544-a074-fc66e10807ad', 'qaRunConfigName': 'claude-sonnet-baseline', 'qaRunConfigVersionNumber':
                3}], 'nextCursor': None, 'total': 1}

        Attributes:
            items (list[QaJobPageResponseDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[QaJobPageResponseDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.qa_job_page_response_dto_items_item import QaJobPageResponseDtoItemsItem # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        next_cursor: None | str
        next_cursor = self.next_cursor

        total = self.total


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "nextCursor": next_cursor,
            "total": total,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qa_job_page_response_dto_items_item import QaJobPageResponseDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = QaJobPageResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        qa_job_page_response_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return qa_job_page_response_dto

