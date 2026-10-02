from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_environment_settings_dto_guided_tour_type_0_steps_item_actions_item_kind import UpdateEnvironmentSettingsDtoGuidedTourType0StepsItemActionsItemKind






T = TypeVar("T", bound="UpdateEnvironmentSettingsDtoGuidedTourType0StepsItemActionsItem")



@_attrs_define
class UpdateEnvironmentSettingsDtoGuidedTourType0StepsItemActionsItem:
    """ Action fired when a guided-tour step becomes active.

        Attributes:
            kind (UpdateEnvironmentSettingsDtoGuidedTourType0StepsItemActionsItemKind): Verb to perform on the target
                element when the step becomes active.
            target (str): Identifier of the element the action runs against.
     """

    kind: UpdateEnvironmentSettingsDtoGuidedTourType0StepsItemActionsItemKind
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
        kind = UpdateEnvironmentSettingsDtoGuidedTourType0StepsItemActionsItemKind(d.pop("kind"))




        target = d.pop("target")

        update_environment_settings_dto_guided_tour_type_0_steps_item_actions_item = cls(
            kind=kind,
            target=target,
        )

        return update_environment_settings_dto_guided_tour_type_0_steps_item_actions_item

