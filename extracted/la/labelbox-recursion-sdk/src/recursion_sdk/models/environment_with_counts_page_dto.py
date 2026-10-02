from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.environment_with_counts_page_dto_items_item import EnvironmentWithCountsPageDtoItemsItem





T = TypeVar("T", bound="EnvironmentWithCountsPageDto")



@_attrs_define
class EnvironmentWithCountsPageDto:
    """ Cursor-paginated page of environments with their problem and run counts.

        Example:
            {'items': [{'id': '784e2386-e297-4f9d-a886-838422383b65', 'externalId': 'vision-agent-eval', 'organizationId':
                '60b52abd-bbea-4c69-987a-103cfd752060', 'name': 'vision-agent-eval', 'templateProblemId':
                '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'maxImportFileSizeBytes': 10485760, 'maxUploadFileSizeBytes': 10485760,
                'maxVersionAggregateFileSizeBytes': 104857600, 'runFieldConfig': {'attemptCount': {'default': 3}},
                'requireLockBeforeNewVersion': True, 'problemEditorInstructions': 'Describe the visual defect to detect and
                attach a representative reference image.', 'rubricIssueTemplate': None, 'globalIssueTemplate': None,
                'qaGateOverrideAllowedStages': ['locking', 'running'], 'disabledBuiltInSynthesizerKeys': ['generate-tools'],
                'guidedTour': None, 'previewFilename': None, 'solverRunConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad',
                'graderRunConfigVersionId': None, 'programmaticGraderRunConfigVersionId': None, 'qaRunConfigVersionId': None,
                'synthesizerRunConfigVersionId': None, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z', 'problemCount': 42, 'problemRunCount': 128}], 'nextCursor': None, 'total': 1}

        Attributes:
            items (list[EnvironmentWithCountsPageDtoItemsItem]): Items in this page, ordered per the requested sort.
            next_cursor (None | str): Cursor for fetching the next page, or null when this is the last page.
            total (int): Total number of items matching the filter across all pages.
     """

    items: list[EnvironmentWithCountsPageDtoItemsItem]
    next_cursor: None | str
    total: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_with_counts_page_dto_items_item import EnvironmentWithCountsPageDtoItemsItem # noqa: PLC0415
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
        from ..models.environment_with_counts_page_dto_items_item import EnvironmentWithCountsPageDtoItemsItem # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = EnvironmentWithCountsPageDtoItemsItem.from_dict(items_item_data)



            items.append(items_item)


        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("nextCursor"))


        total = d.pop("total")

        environment_with_counts_page_dto = cls(
            items=items,
            next_cursor=next_cursor,
            total=total,
        )

        return environment_with_counts_page_dto

