from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.problem_list_items_response_dto_items_item import ProblemListItemsResponseDtoItemsItem
  from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_applied import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied
  from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_degraded import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegraded
  from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_not_requested import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested





T = TypeVar("T", bound="ProblemListItemsResponseDto")



@_attrs_define
class ProblemListItemsResponseDto:
    """ Paged response for the environment-overview problem list, with enrichment-filter status metadata.

        Example:
            {'items': [{'id': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'environmentId':
                '784e2386-e297-4f9d-a886-838422383b65', 'externalId': 'detect-surface-defects', 'title': 'Detect surface defects
                on machined parts', 'isTemplate': False, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z', 'latestVersionCreatedAt': '2026-01-16T14:20:00.000Z', 'hasLockedVersion': True,
                'isDraft': False, 'totalCostUsd': 12.47, 'runsCount': 42, 'models': ['claude-sonnet-4-5-20250929'], 'avgScore':
                {'avg': 0.72, 'min': 0.31, 'max': 0.95}, 'bestScore': 0.95, 'latestRun': {'status': 'completed', 'finalScore':
                0.88, 'apiModelName': 'claude-sonnet-4-5-20250929', 'promptExcerpt': 'Inspect the supplied micrograph and report
                any surface defects you can identify.'}, 'recentRuns': [{'id': '22d435e7-9e41-4554-b0bd-dab57a202b71',
                'attemptNumber': 3, 'runName': 'claude-sonnet-baseline on detect-surface-defects', 'status': 'completed',
                'score': 0.88}], 'previewFileUrl': 'https://storage.googleapis.com/recursion-example-
                previews/2d3fe029-a7d1-4747-9d09-81b976087bbb/latest.png'}], 'nextCursor': None, 'total': 1,
                'enrichmentFilterStatus': {'state': 'not_requested'}}

        Attributes:
            items (list[ProblemListItemsResponseDtoItemsItem]): Page of problem list items in sort order.
            next_cursor (None | str): Opaque cursor for the next page, or null when no further pages exist.
            total (int): Total number of problems that match the current filter set across all pages.
            enrichment_filter_status (ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied |
                ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegraded |
                ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested): Status of enrichment filtering on the
                server (applied, degraded, or not requested) for this response.
     """

    items: list[ProblemListItemsResponseDtoItemsItem]
    next_cursor: None | str
    total: int
    enrichment_filter_status: ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied | ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegraded | ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_list_items_response_dto_items_item import ProblemListItemsResponseDtoItemsItem # noqa: PLC0415
        from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_applied import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied # noqa: PLC0415
        from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_degraded import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegraded # noqa: PLC0415
        from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_not_requested import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)



        next_cursor: None | str
        next_cursor = self.next_cursor

        total = self.total

        enrichment_filter_status: dict[str, Any]
        if isinstance(self.enrichment_filter_status, ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested):
            enrichment_filter_status = self.enrichment_filter_status.to_dict()
        elif isinstance(self.enrichment_filter_status, ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied):
            enrichment_filter_status = self.enrichment_filter_status.to_dict()
        else:
            enrichment_filter_status = self.enrichment_filter_status.to_dict()



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "nextCursor": next_cursor,
            "total": total,
            "enrichmentFilterStatus": enrichment_filter_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_list_items_response_dto_items_item import ProblemListItemsResponseDtoItemsItem # noqa: PLC0415
        from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_applied import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied # noqa: PLC0415
        from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_degraded import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegraded # noqa: PLC0415
        from ..models.problem_list_items_response_dto_properties_enrichment_filter_status_not_requested import ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ProblemListItemsResponseDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        def _parse_enrichment_filter_status(data: object) -> ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied | ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegraded | ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                enrichment_filter_status_type_0 = ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusNotRequested.from_dict(data)



                return enrichment_filter_status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                enrichment_filter_status_type_1 = ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusApplied.from_dict(data)



                return enrichment_filter_status_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            enrichment_filter_status_type_2 = ProblemListItemsResponseDtoPropertiesEnrichmentFilterStatusDegraded.from_dict(data)



            return enrichment_filter_status_type_2

        enrichment_filter_status = _parse_enrichment_filter_status(d.pop("enrichmentFilterStatus"))


        problem_list_items_response_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
            enrichment_filter_status=enrichment_filter_status,
        )

        return problem_list_items_response_dto

