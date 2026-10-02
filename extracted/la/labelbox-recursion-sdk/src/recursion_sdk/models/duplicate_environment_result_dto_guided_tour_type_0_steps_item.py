from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.duplicate_environment_result_dto_guided_tour_type_0_steps_item_actions_item import DuplicateEnvironmentResultDtoGuidedTourType0StepsItemActionsItem





T = TypeVar("T", bound="DuplicateEnvironmentResultDtoGuidedTourType0StepsItem")



@_attrs_define
class DuplicateEnvironmentResultDtoGuidedTourType0StepsItem:
    """ A single ordered step in a guided tour.

        Attributes:
            id (str): Stable identifier of the step (must be unique within a tour).
            title (str): Short title rendered as the step heading.
            body (str): Markdown-capable body text explaining what the user should do for this step.
            optional (bool | Unset): When true, the step can be skipped without blocking tour completion.
            actions (list[DuplicateEnvironmentResultDtoGuidedTourType0StepsItemActionsItem] | Unset): Actions to fire when
                the step becomes active.
     """

    id: str
    title: str
    body: str
    optional: bool | Unset = UNSET
    actions: list[DuplicateEnvironmentResultDtoGuidedTourType0StepsItemActionsItem] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.duplicate_environment_result_dto_guided_tour_type_0_steps_item_actions_item import DuplicateEnvironmentResultDtoGuidedTourType0StepsItemActionsItem # noqa: PLC0415
        id = self.id

        title = self.title

        body = self.body

        optional = self.optional

        actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "title": title,
            "body": body,
        })
        if optional is not UNSET:
            field_dict["optional"] = optional
        if actions is not UNSET:
            field_dict["actions"] = actions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.duplicate_environment_result_dto_guided_tour_type_0_steps_item_actions_item import DuplicateEnvironmentResultDtoGuidedTourType0StepsItemActionsItem # noqa: PLC0415
        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        body = d.pop("body")

        optional = d.pop("optional", UNSET)

        _actions = d.pop("actions", UNSET)
        actions: list[DuplicateEnvironmentResultDtoGuidedTourType0StepsItemActionsItem] | Unset = UNSET
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:
                actions_item = DuplicateEnvironmentResultDtoGuidedTourType0StepsItemActionsItem.from_dict(actions_item_data)



                actions.append(actions_item)


        duplicate_environment_result_dto_guided_tour_type_0_steps_item = cls(
            id=id,
            title=title,
            body=body,
            optional=optional,
            actions=actions,
        )

        return duplicate_environment_result_dto_guided_tour_type_0_steps_item

