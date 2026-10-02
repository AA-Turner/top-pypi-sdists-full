from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.environment_with_counts_page_dto_items_item_guided_tour_type_0_steps_item_actions_item_kind import EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItemActionsItemKind






T = TypeVar("T", bound="EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItemActionsItem")



@_attrs_define
class EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItemActionsItem:
    """ Action fired when a guided-tour step becomes active.

        Attributes:
            kind (EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItemActionsItemKind): Verb to perform on the
                target element when the step becomes active.
            target (str): Identifier of the element the action runs against.
     """

    kind: EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItemActionsItemKind
    target: str





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        target = self.target


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "target": target,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = EnvironmentWithCountsPageDtoItemsItemGuidedTourType0StepsItemActionsItemKind(d.pop("kind"))




        target = d.pop("target")

        environment_with_counts_page_dto_items_item_guided_tour_type_0_steps_item_actions_item = cls(
            kind=kind,
            target=target,
        )

        return environment_with_counts_page_dto_items_item_guided_tour_type_0_steps_item_actions_item

