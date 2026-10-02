from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.environment_with_counts_page_dto_items_item_guided_tour_type_0_steps_item import EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItem





T = TypeVar("T", bound="EnvironmentWithCountsPageDtoItemsItemGuidedTourType0")



@_attrs_define
class EnvironmentWithCountsPageDtoItemsItemGuidedTourType0:
    """ Persisted guided-tour definition stored on an environment.

        Attributes:
            steps (list[EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItem]): Ordered list of tour steps; each
                step id must be unique within the tour.
     """

    steps: list[EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_with_counts_page_dto_items_item_guided_tour_type_0_steps_item import EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItem # noqa: PLC0415
        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "steps": steps,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_with_counts_page_dto_items_item_guided_tour_type_0_steps_item import EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItem # noqa: PLC0415
        d = dict(src_dict)
        steps = []
        _steps = d.pop("steps")
        for steps_item_data in (_steps):
            steps_item = EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItem.from_dict(steps_item_data)



            steps.append(steps_item)


        environment_with_counts_page_dto_items_item_guided_tour_type_0 = cls(
            steps=steps,
        )

        return environment_with_counts_page_dto_items_item_guided_tour_type_0

